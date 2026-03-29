from sqlalchemy import Column, String, Float, Integer, ForeignKey, Enum, Date, Text
from sqlalchemy.dialects.postgresql import UUID
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

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    default_currency = Column(String)


# USER
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(String, unique=True)
    password_hash = Column(String)

    role = Column(Enum(RoleEnum))
    manager_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"))

    manager = relationship("User", remote_side=[id])


# EXPENSE
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    amount = Column(Float)
    currency = Column(String)
    converted_amount = Column(Float)

    category = Column(String)
    description = Column(String)
    date = Column(Date)

    status = Column(Enum(StatusEnum), default=StatusEnum.PENDING)
    risk_score = Column(Float)

    user = relationship("User")


# APPROVAL
class Approval(Base):
    __tablename__ = "approvals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    expense_id = Column(UUID(as_uuid=True), ForeignKey("expenses.id"))
    approver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    step_order = Column(Integer)
    status = Column(Enum(StatusEnum), default=StatusEnum.PENDING)
    comments = Column(String)


# APPROVAL RULE
class ApprovalRule(Base):
    __tablename__ = "approval_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True))

    min_approval_percentage = Column(Float)
    special_approver_id = Column(UUID(as_uuid=True))


# RECEIPT
class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    expense_id = Column(UUID(as_uuid=True), ForeignKey("expenses.id"))

    image_url = Column(String)
    extracted_text = Column(Text)
