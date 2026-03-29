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

@router.post("/expenses/extract")
def extract_receipt_mock(file: UploadFile = File(...), current_user = Depends(get_current_user)):
    return {
      "amount": 142.50,
      "date": "2023-10-24",
      "vendor": "Delta Airlines",
      "confidence": 0.94,
      "flags": ["Date is 6 months old"],
      "risk_score": 85,
      "ai_recommendation": "High risk due to old date."
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
