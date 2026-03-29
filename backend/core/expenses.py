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
        description=data.get("description"),
        date=data.get("date"),
        status=StatusEnum.PENDING
    )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user and user.company_id:
        new_expense.converted_amount = data.get("amount")

    # Get risk score from AI Engine
    # Build complete dict for AI engine (can expand later)
    expense_data = {
        "user_id": user_id,
        "amount": new_expense.amount,
        "category": new_expense.category
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
    - Use external API
    Returns:
    float
    """
    # Mock for external API exchange rate
    if from_curr == to_curr:
        return amount
        
    mock_rates = {
        "USD": 1.0,
        "EUR": 0.85,
        "INR": 83.0
    }
    
    # Convert to USD first, then to target currency
    amount_in_usd = amount / mock_rates.get(from_curr, 1.0)
    converted = amount_in_usd * mock_rates.get(to_curr, 1.0)
    
    return round(converted, 2)
