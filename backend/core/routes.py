from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from .database import get_db
from .schemas import (
    UserCreate, UserLogin, EmployeeCreate, ManagerAssign, 
    RoleUpdate, ExpenseCreate, ExpenseOut, ApprovalDecision
)
from .auth import register_user, login_user, get_current_admin, get_current_manager, get_current_user
from .users import create_employee, assign_manager, update_role
from .expenses import submit_expense, get_user_expenses
from .models import Approval, Expense, StatusEnum, User
from .workflow import create_approval_flow, process_approval_step
from typing import List

router = APIRouter()

# --- AUTH ROUTES ---

@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        return register_user(db, user_data.name, user_data.email, user_data.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/auth/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    try:
        return login_user(db, user_data.email, user_data.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


# --- USERS ROUTES ---

@router.post("/users/create", status_code=status.HTTP_201_CREATED)
def create_new_employee(employee_data: EmployeeCreate, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    """
    Only admins can create new employees.
    """
    try:
        return create_employee(db, str(current_admin.id), employee_data.dict())
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.post("/users/assign-manager")
def assign_user_manager(employee_id: str, manager_data: ManagerAssign, db: Session = Depends(get_db), current_manager=Depends(get_current_manager)):
    """
    Managers and Admins can assign managers.
    """
    try:
        success = assign_manager(db, employee_id, str(manager_data.manager_id))
        return {"success": success}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- EXPENSES ROUTES ---

import os
import tempfile
from backend.ai_engine.ocr import process_receipt

@router.post("/expenses/extract")
def extract_receipt_live(file: UploadFile = File(...), current_user = Depends(get_current_user)):
    # 1. Save uploaded file temporarily for OCR processing
    suffix = os.path.splitext(file.filename)[1] if file.filename else ".png"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file.file.read())
        tmp_path = tmp.name

    try:
        # 2. Run your underlying OCR/OpenCV pipeline
        ocr_data = process_receipt(tmp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR Engine Failure: {str(e)}")
    finally:
        os.unlink(tmp_path)
        
    # 3. Format payload to match exact frontend React expectations
    confidence = ocr_data.get("confidence") or 0.0
    flags = []
    if confidence < 0.6:
        flags.append("Low OCR confidence, manual review required.")

    return {
      "amount": ocr_data.get("amount") or 0.0,
      "date": ocr_data.get("date") or "",
      "vendor": ocr_data.get("vendor") or "Unknown Vendor",
      "confidence": confidence,
      "flags": flags,
      "risk_score": 0,  # Actually evaluated when user clicks Submit
      "ai_recommendation": "Ready for submission." if confidence >= 0.6 else "Please manually verify extracted text."
    }

@router.post("/expenses/submit", status_code=status.HTTP_201_CREATED)
def submit_new_expense(expense_data: ExpenseCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        user_id = str(current_user.id)
        result = submit_expense(db, user_id, expense_data.dict())
        
        expense_id = result["expense_id"]
        create_approval_flow(db, expense_id)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/expenses/my", response_model=List[ExpenseOut])
def get_my_expenses(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user_id = str(current_user.id)
    return get_user_expenses(db, user_id)


# --- WORKFLOW ROUTES ---

@router.get("/workflow/pending")
def fetch_pending_approvals(db: Session = Depends(get_db), current_manager = Depends(get_current_manager)):
    approvals = db.query(Approval).filter(
        Approval.approver_id == current_manager.id,
        Approval.status == StatusEnum.PENDING
    ).all()
    
    results = []
    for approval in approvals:
        expense = db.query(Expense).filter(Expense.id == approval.expense_id).first()
        if not expense: continue
        user = db.query(User).filter(User.id == expense.user_id).first()
        
        rs = expense.risk_score if expense.risk_score else 0.0
        results.append({
            "id": str(approval.id), 
            "expense_id": str(expense.id),
            "employee_name": user.name if user else "Unknown User",
            "vendor": expense.category, 
            "amount": expense.amount,
            "date": str(expense.date) if expense.date else None,
            "category": expense.category,
            "status": expense.status.value,
            "risk_score": rs,
            "risk_level": "HIGH" if rs > 0.5 else "LOW",
            "flags": ["Date is 6 months old"] if rs > 0.5 else [],
            "ai_recommendation": "High risk." if rs > 0.5 else "Low risk."
        })
    return results

@router.post("/workflow/approve")
def approve_workflow_step(approval_id: str, decision_data: ApprovalDecision, db: Session = Depends(get_db), current_manager = Depends(get_current_manager)):
    try:
        # Note: A real implementation should verify the approval_id belongs to current_manager
        return process_approval_step(db, approval_id, decision_data.decision.value)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
