from sqlalchemy.orm import Session
from .models import Expense, StatusEnum, User
from backend.ai_engine.fraud_detection import risk_score_expense

def submit_expense(db: Session, user_id: str, data: dict) -> dict:
    """
    - Save expense
    - Call AI function: risk_score_expense()
    - Store risk_score
    Returns:
    {
    "expense_id": str,
    "risk_score": float
    }
    """
    # Create the expense object
    new_expense = Expense(
        user_id=user_id,
        amount=data.get("amount"),
        currency=data.get("currency"),
        category=data.get("category"),
        vendor=data.get("vendor"),
        description=data.get("description"),
        date=data.get("date"),
        status=StatusEnum.PENDING
    )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user and user.company_id:
        from .models import Company
        company = db.query(Company).filter(Company.id == user.company_id).first()
        if company and company.default_currency and company.default_currency.upper() != new_expense.currency.upper():
            new_expense.converted_amount = convert_currency(new_expense.amount, new_expense.currency, company.default_currency)
        else:
            new_expense.converted_amount = new_expense.amount
    else:
        new_expense.converted_amount = new_expense.amount

    # Get risk score from AI Engine
    # Build complete dict for AI engine (can expand later)
    expense_data = {
        "user_id": user_id,
        "amount": new_expense.amount,
        "converted_amount": new_expense.converted_amount or new_expense.amount,
        "category": new_expense.category,
        "date": new_expense.date.isoformat() if new_expense.date else None
    }
    risk_score = risk_score_expense(db, expense_data)
    new_expense.risk_score = risk_score
    
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    
    
    return {
        "expense_id": str(new_expense.id),
        "risk_score": float(new_expense.risk_score) if new_expense.risk_score is not None else 0.0
    }

def get_user_expenses(db: Session, user_id: str) -> list:
    """
    Returns:
    List[Expense]
    """
    expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
    return expenses

def convert_currency(amount: float, from_curr: str, to_curr: str) -> float:
    """
    - Use external API via backend.core.exchange
    Returns:
    float
    """
    from backend.core.exchange import get_exchange_rates
    
    if from_curr.upper() == to_curr.upper():
        return amount
        
    rates = get_exchange_rates(from_curr.upper())
    target_rate = rates.get(to_curr.upper())
    
    if not target_rate:
        # Fallback if exchange rate is missing
        return amount
        
    converted = amount * target_rate
    return round(converted, 2)
