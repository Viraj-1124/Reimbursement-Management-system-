import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.core.database import SessionLocal, engine, Base
from backend.core.models import User, RoleEnum, Company
from backend.core.auth import get_password_hash

def seed_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if already seeded
    if db.query(Company).first():
        print("Database already seeded.")
        return

    company = Company(name="Acme Corp", default_currency="USD")
    db.add(company)
    db.commit()
    db.refresh(company)

    # Create Admin
    admin = User(
        name="Admin Sys",
        email="admin@test.com",
        password_hash=get_password_hash("password"),
        role=RoleEnum.ADMIN,
        company_id=company.id
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)

    # Create Manager
    manager = User(
        name="Sam Manager",
        email="manager@test.com",
        password_hash=get_password_hash("password"),
        role=RoleEnum.MANAGER,
        company_id=company.id,
        manager_id=admin.id
    )
    db.add(manager)
    db.commit()
    db.refresh(manager)

    # Create Employee
    employee = User(
        name="Alex Employee",
        email="employee@test.com",
        password_hash=get_password_hash("password"),
        role=RoleEnum.EMPLOYEE,
        company_id=company.id,
        manager_id=manager.id
    )
    db.add(employee)
    db.commit()

    print("Database successfully seeded with demo accounts!")

if __name__ == "__main__":
    seed_db()
