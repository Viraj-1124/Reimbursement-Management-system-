from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date
from uuid import UUID
from .models import RoleEnum, StatusEnum

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    company_id: Optional[UUID] = None

class ManagerAssign(BaseModel):
    manager_id: UUID

class RoleUpdate(BaseModel):
    role: RoleEnum

class ExpenseCreate(BaseModel):
    amount: float
    currency: str
    category: str
    description: str
    date: date

class ExpenseOut(BaseModel):
    id: UUID
    user_id: Optional[UUID]
    amount: float
    currency: str
    converted_amount: Optional[float]
    category: Optional[str]
    description: Optional[str]
    date: Optional[date]
    status: Optional[StatusEnum]
    risk_score: Optional[float]

    class Config:
        from_attributes = True

class ApprovalDecision(BaseModel):
    decision: StatusEnum
    comments: Optional[str] = None
