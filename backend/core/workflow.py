from sqlalchemy.orm import Session
from .models import Expense, Approval, StatusEnum, User, RoleEnum

def create_approval_flow(db: Session, expense_id: str) -> list:
    """
    - Generate approval chain (manager -> finance -> director)
    Returns:
    [
    {"approver_id": str, "step": int}
    ]
    """
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise ValueError("Expense not found")
        
    user = db.query(User).filter(User.id == expense.user_id).first()
    
    steps = []
    current_step_order = 1
    
    # 1. Manager Approval
    if user and user.manager_id:
        steps.append({
            "approver_id": str(user.manager_id),
            "step": current_step_order
        })
        current_step_order += 1
        
    # 2. Finance / Admin Approval (Dynamic lookup for an ADMIN in the company)
    # Just an example logic: grab an admin user from the same company
    finance_admin = db.query(User).filter(
        User.role == RoleEnum.ADMIN,
        User.company_id == user.company_id
    ).first()
    
    if finance_admin and (not steps or steps[-1]["approver_id"] != str(finance_admin.id)):
        steps.append({
            "approver_id": str(finance_admin.id),
            "step": current_step_order
        })
        current_step_order += 1
        
    # Save the approvals
    for step_info in steps:
        approval = Approval(
            expense_id=expense.id,
            approver_id=step_info["approver_id"],
            step_order=step_info["step"],
            status=StatusEnum.PENDING
        )
        db.add(approval)
        
    db.commit()
    return steps

def process_approval_step(db: Session, approval_id: str, decision: str) -> dict:
    """
    - Approve/reject current step
    - Move to next step if needed
    Returns:
    {
    "next_step": bool,
    "final_status": str
    }
    """
    approval = db.query(Approval).filter(Approval.id == approval_id).first()
    if not approval:
        raise ValueError("Approval step not found")
        
    try:
        new_status = StatusEnum(decision)
    except ValueError:
        raise ValueError("Invalid decision")
        
    approval.status = new_status
    db.commit()
    
    expense = db.query(Expense).filter(Expense.id == approval.expense_id).first()
    
    if new_status == StatusEnum.REJECTED:
        expense.status = StatusEnum.REJECTED
        db.commit()
        return {"next_step": False, "final_status": "REJECTED"}
        
    if new_status == StatusEnum.APPROVED:
        # Check if there are more pending approvals for this expense
        next_approval = db.query(Approval).filter(
            Approval.expense_id == approval.expense_id,
            Approval.status == StatusEnum.PENDING,
            Approval.step_order > approval.step_order
        ).order_by(Approval.step_order.asc()).first()
        
        if next_approval:
            return {"next_step": True, "final_status": "PENDING"}
        else:
            # All steps approved
            expense.status = StatusEnum.APPROVED
            db.commit()
            return {"next_step": False, "final_status": "APPROVED"}
            
    return {"next_step": False, "final_status": "PENDING"}

def move_to_next_approver(db: Session, expense_id: str) -> bool:
    """
    Returns:
    True
    """
    # In a real system, this might send an email or push notification to the next approver.
    # The actual state progression is handled by process_approval_step.
    
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        return False
        
    next_approval = db.query(Approval).filter(
        Approval.expense_id == expense_id,
        Approval.status == StatusEnum.PENDING
    ).order_by(Approval.step_order.asc()).first()
    
    if next_approval:
        # Notify next_approval.approver_id here
        pass
        
    return True
