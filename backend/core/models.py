from sqlalchemy import Column, String, Float, Integer, ForeignKey, Enum, Date, Text
from sqlalchemy.orm import relationship
import uuid
import enum
from .database import Base

# ENUMS
class RoleEnum(enum.Enum):
    EMPLOYEE = "EMPLOYEE"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"

class StatusEnum(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


# COMPANY
class Company(Base):
    __tablename__ = "companies"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    default_currency = Column(String)


# USER
class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    email = Column(String, unique=True)
    password_hash = Column(String)

    role = Column(Enum(RoleEnum))
    manager_id = Column(String(36), ForeignKey("users.id"))
    company_id = Column(String(36), ForeignKey("companies.id"))

    manager = relationship("User", remote_side=[id])


# EXPENSE
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"))

    amount = Column(Float)
    currency = Column(String)
    converted_amount = Column(Float)

    category = Column(String)
    vendor = Column(String)
    description = Column(String)
    date = Column(Date)

    status = Column(Enum(StatusEnum), default=StatusEnum.PENDING)
    risk_score = Column(Float)

    user = relationship("User")


# APPROVAL
class Approval(Base):
    __tablename__ = "approvals"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    expense_id = Column(String(36), ForeignKey("expenses.id"))
    approver_id = Column(String(36), ForeignKey("users.id"))

    step_order = Column(Integer)
    status = Column(Enum(StatusEnum), default=StatusEnum.PENDING)
    comments = Column(String)


# APPROVAL RULE
class ApprovalRule(Base):
    __tablename__ = "approval_rules"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36))

    min_approval_percentage = Column(Float)
    special_approver_id = Column(String(36))


# RECEIPT
class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    expense_id = Column(String(36), ForeignKey("expenses.id"))

    image_url = Column(String)
    extracted_text = Column(Text)
