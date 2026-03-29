import hashlib
from datetime import datetime, timedelta
from sqlalchemy.orm import Session


def _hash_receipt_text(text: str) -> str:
    import re
    normalized = re.sub(r"[\s\W]+", "", text.lower())
    return hashlib.md5(normalized.encode()).hexdigest()


def detect_duplicate_receipt(db: Session, expense_id: str) -> bool:
    from backend.core.models import Expense, Receipt

    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        return False

    receipt = db.query(Receipt).filter(Receipt.expense_id == expense_id).first()
    if not receipt or not receipt.extracted_text:
        return _detect_amount_date_duplicate(db, expense)

    current_hash = _hash_receipt_text(receipt.extracted_text)

    prior_expenses = (
        db.query(Expense)
        .filter(Expense.user_id == expense.user_id, Expense.id != expense_id)
        .all()
    )

    for prior_exp in prior_expenses:
        prior_receipt = db.query(Receipt).filter(Receipt.expense_id == prior_exp.id).first()
        if prior_receipt and prior_receipt.extracted_text:
            prior_hash = _hash_receipt_text(prior_receipt.extracted_text)
            if prior_hash == current_hash:
                return True

    return _detect_amount_date_duplicate(db, expense)


def _detect_amount_date_duplicate(db: Session, expense) -> bool:
    from backend.core.models import Expense

    window_start = expense.date - timedelta(days=7)
    window_end = expense.date + timedelta(days=7)

    duplicate = (
        db.query(Expense)
        .filter(
            Expense.user_id == expense.user_id,
            Expense.id != expense.id,
            Expense.amount == expense.amount,
            Expense.date >= window_start,
            Expense.date <= window_end,
        )
        .first()
    )
    return duplicate is not None


def _get_user_spending_stats(db: Session, user_id: str, category: str) -> dict:
    from backend.core.models import Expense
    from sqlalchemy import func
    import math

    cutoff = datetime.utcnow().date() - timedelta(days=90)

    rows = (
        db.query(Expense.converted_amount)
        .filter(
            Expense.user_id == user_id,
            Expense.category == category,
            Expense.date >= cutoff,
        )
        .all()
    )

    amounts = [r[0] for r in rows if r[0] is not None]

    if not amounts:
        return {"mean": 0.0, "std": 0.0, "count": 0}

    mean = sum(amounts) / len(amounts)
    variance = sum((x - mean) ** 2 for x in amounts) / len(amounts)
    std = math.sqrt(variance)

    return {"mean": mean, "std": std, "count": len(amounts)}


def detect_anomaly(db: Session, expense_data: dict) -> float:
    import math

    score = 0.0
    converted_amount = expense_data.get("converted_amount", expense_data.get("amount", 0))
    user_id = expense_data.get("user_id")
    category = expense_data.get("category", "general")

    stats = _get_user_spending_stats(db, user_id, category)

    if stats["count"] >= 3:
        if stats["std"] > 0:
            z = abs(converted_amount - stats["mean"]) / stats["std"]
        else:
            z = 3.0 if converted_amount > stats["mean"] * 1.5 else 0.0

        z_score_factor = min(z / 5.0, 1.0) * 0.6
        score += z_score_factor

    try:
        expense_date = datetime.strptime(expense_data["date"], "%Y-%m-%d")
        if expense_date.weekday() >= 5:
            score += 0.15
    except Exception:
        pass

    amount = expense_data.get("amount", 0)
    if amount > 0 and amount % 100 == 0:
        score += 0.1
    elif amount > 0 and amount % 50 == 0:
        score += 0.05

    if converted_amount > 50000:
        score += 0.15
    elif converted_amount > 10000:
        score += 0.05

    return round(min(score, 1.0), 4)


def risk_score_expense(db: Session, expense_data: dict) -> float:
    expense_id = expense_data.get("expense_id")

    duplicate_weight = 0.5
    anomaly_weight = 0.5

    is_duplicate = detect_duplicate_receipt(db, expense_id) if expense_id else False
    duplicate_score = 1.0 if is_duplicate else 0.0

    anomaly_score = detect_anomaly(db, expense_data)

    final_score = (duplicate_score * duplicate_weight) + (anomaly_score * anomaly_weight)

    return round(min(final_score, 1.0), 4)


def explain_risk_score(db: Session, expense_data: dict) -> dict:
    import math

    flags = []
    expense_id = expense_data.get("expense_id")
    converted_amount = expense_data.get("converted_amount", expense_data.get("amount", 0))
    user_id = expense_data.get("user_id")
    category = expense_data.get("category", "general")

    is_duplicate = detect_duplicate_receipt(db, expense_id) if expense_id else False
    if is_duplicate:
        flags.append("Similar receipt detected in a prior submission")

    stats = _get_user_spending_stats(db, user_id, category)
    if stats["count"] >= 3 and stats["mean"] > 0:
        ratio = converted_amount / stats["mean"]
        if ratio > 1.5:
            flags.append(f"Amount is {ratio:.1f}x the user's average for '{category}'")

    try:
        expense_date = datetime.strptime(expense_data["date"], "%Y-%m-%d")
        if expense_date.weekday() >= 5:
            flags.append("Submitted on a weekend")
    except Exception:
        pass

    amount = expense_data.get("amount", 0)
    if amount > 0 and amount % 100 == 0:
        flags.append("Suspiciously round amount")

    if converted_amount > 50000:
        flags.append("Very high absolute amount (>50,000)")

    risk_score = risk_score_expense(db, expense_data)

    if risk_score >= 0.7:
        summary = f"High risk: {len(flags)} anomalies detected"
    elif risk_score >= 0.4:
        summary = f"Medium risk: {len(flags)} concern(s) found"
    else:
        summary = "Low risk: expense appears normal"

    return {
        "risk_score": risk_score,
        "flags": flags,
        "summary": summary,
    }