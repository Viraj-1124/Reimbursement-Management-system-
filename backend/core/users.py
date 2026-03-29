from sqlalchemy.orm import Session
from .models import User, RoleEnum
from .auth import get_password_hash

def create_employee(db: Session, admin_id: str, data: dict) -> dict:
    """
    - Only admin can create
    Returns:
    {"user_id": str}
    """
    admin_user = db.query(User).filter(User.id == admin_id).first()
    if not admin_user or admin_user.role != RoleEnum.ADMIN:
        raise PermissionError("Only admins can create employees")
        
    hashed_pwd = get_password_hash(data.get("password"))
    new_employee = User(
        name=data.get("name"),
        email=data.get("email"),
        password_hash=hashed_pwd,
        role=RoleEnum.EMPLOYEE,
        company_id=data.get("company_id")
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    
    return {"user_id": str(new_employee.id)}

def assign_manager(db: Session, employee_id: str, manager_id: str) -> bool:
    """
    Returns:
    True
    """
    employee = db.query(User).filter(User.id == employee_id).first()
    manager = db.query(User).filter(User.id == manager_id).first()
    
    if not employee or not manager:
        raise ValueError("Employee or Manager not found")
        
    if manager.role not in [RoleEnum.MANAGER, RoleEnum.ADMIN]:
        raise ValueError("Assigned user is not a manager")
        
    employee.manager_id = manager.id
    db.commit()
    
    return True

def update_role(db: Session, user_id: str, role: str) -> bool:
    """
    Returns:
    True
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
        
    # Validation of enum string is handled implicitly here, but explicitly:
    try:
        new_role = RoleEnum(role)
    except ValueError:
        raise ValueError("Invalid role specified")
        
    user.role = new_role
    db.commit()
    
    return True
