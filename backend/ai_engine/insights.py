from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func


def generate_spending_patterns(db: Session, user_id: str) -> dict:
    from backend.core.models import Expense

    cutoff = datetime.utcnow().date() - timedelta(days=180)

    expenses = (
        db.query(Expense)
        .filter(Expense.user_id == user_id, Expense.date >= cutoff)
        .all()
    )

    if not expenses:
        return {
            "avg_spend": 0.0,
            "total_spend": 0.0,
            "monthly_trend": [],
            "by_category": {},
            "top_category": None,
            "risk_trend": [],
        }

    monthly: dict[str, float] = {}
    monthly_risk: dict[str, list] = {}
    by_category: dict[str, float] = {}

    for exp in expenses:
        month_key = exp.date.strftime("%Y-%m")
        amount = exp.converted_amount or exp.amount or 0
        risk = exp.risk_score or 0.0
        cat = exp.category or "Uncategorised"

        monthly[month_key] = monthly.get(month_key, 0.0) + amount
        monthly_risk.setdefault(month_key, []).append(risk)
        by_category[cat] = by_category.get(cat, 0.0) + amount

    sorted_months = sorted(monthly.keys())
    monthly_trend = [{"month": m, "total": round(monthly[m], 2)} for m in sorted_months]
    risk_trend = [
        round(sum(monthly_risk[m]) / len(monthly_risk[m]), 4)
        for m in sorted_months
    ]

    total_spend = sum(monthly.values())
    avg_spend = total_spend / max(len(monthly), 1)
    top_category = max(by_category, key=by_category.get) if by_category else None

    return {
        "avg_spend": round(avg_spend, 2),
        "total_spend": round(total_spend, 2),
        "monthly_trend": monthly_trend,
        "by_category": {k: round(v, 2) for k, v in by_category.items()},
        "top_category": top_category,
        "risk_trend": risk_trend,
    }


def detect_high_spenders(db: Session, company_id: str = None, top_n: int = 10) -> list:
    import math
    from backend.core.models import Expense, User

    cutoff = datetime.utcnow().date() - timedelta(days=90)

    query = (
        db.query(
            Expense.user_id,
            func.sum(Expense.converted_amount).label("total")
        )
        .filter(Expense.date >= cutoff)
    )

    if company_id:
        query = (
            query.join(User, User.id == Expense.user_id)
            .filter(User.company_id == company_id)
        )

    rows = query.group_by(Expense.user_id).all()

    if not rows:
        return []

    totals = [float(r.total or 0) for r in rows]
    mean = sum(totals) / len(totals)
    variance = sum((x - mean) ** 2 for x in totals) / len(totals)
    std = math.sqrt(variance) if variance > 0 else 1.0

    results = []
    for r in rows:
        total = float(r.total or 0)
        z = (total - mean) / std

        if z >= 1.5:
            results.append({
                "user_id": str(r.user_id),
                "total_spend": round(total, 2),
                "z_score": round(z, 3),
                "flag": "VERY_HIGH" if z >= 2.5 else "HIGH",
            })

    results.sort(key=lambda x: x["total_spend"], reverse=True)
    return results[:top_n]


def approval_delay_analysis(db: Session, company_id: str = None) -> dict:
    from backend.core.models import Expense, Approval, User
    from backend.core.models import StatusEnum

    query = db.query(Expense).filter(Expense.status != StatusEnum.PENDING)

    if company_id:
        query = (
            query.join(User, User.id == Expense.user_id)
            .filter(User.company_id == company_id)
        )

    expenses = query.all()

    if not expenses:
        return {
            "avg_delay_days": 0.0,
            "median_delay_days": 0.0,
            "max_delay_days": 0.0,
            "bottleneck_approvers": [],
            "delay_by_category": {},
        }

    delays = []
    category_delays: dict[str, list] = {}
    approver_delays: dict[str, list] = {}

    today = datetime.utcnow().date()

    for exp in expenses:
        approval = (
            db.query(Approval)
            .filter(Approval.expense_id == exp.id)
            .order_by(Approval.step_order)
            .first()
        )

        if approval and exp.date:
            delay = (today - exp.date).days
            delays.append(delay)

            cat = exp.category or "Uncategorised"
            category_delays.setdefault(cat, []).append(delay)

            approver_id = str(approval.approver_id)
            approver_delays.setdefault(approver_id, []).append(delay)

    if not delays:
        return {
            "avg_delay_days": 0.0,
            "median_delay_days": 0.0,
            "max_delay_days": 0.0,
            "bottleneck_approvers": [],
            "delay_by_category": {},
        }

    delays.sort()
    n = len(delays)
    avg_delay = sum(delays) / n
    median_delay = delays[n // 2] if n % 2 != 0 else (delays[n // 2 - 1] + delays[n // 2]) / 2
    max_delay = max(delays)

    bottleneck_approvers = sorted(
        [
            {
                "approver_id": aid,
                "avg_delay_days": round(sum(d) / len(d), 2),
                "expense_count": len(d),
            }
            for aid, d in approver_delays.items()
        ],
        key=lambda x: x["avg_delay_days"],
        reverse=True,
    )[:5]

    delay_by_category = {
        cat: round(sum(d) / len(d), 2)
        for cat, d in category_delays.items()
    }

    return {
        "avg_delay_days": round(avg_delay, 2),
        "median_delay_days": round(median_delay, 2),
        "max_delay_days": float(max_delay),
        "bottleneck_approvers": bottleneck_approvers,
        "delay_by_category": delay_by_category,
    }


def generate_company_summary(db: Session, company_id: str) -> dict:
    from backend.core.models import Expense, User
    from backend.core.models import StatusEnum

    cutoff = datetime.utcnow().date() - timedelta(days=90)

    company_expenses = (
        db.query(Expense)
        .join(User, User.id == Expense.user_id)
        .filter(User.company_id == company_id, Expense.date >= cutoff)
        .all()
    )

    total_spend = sum(e.converted_amount or 0 for e in company_expenses)
    flagged = [e for e in company_expenses if (e.risk_score or 0) >= 0.7]
    avg_risk = (
        sum(e.risk_score for e in company_expenses if e.risk_score is not None)
        / max(len(company_expenses), 1)
    )

    cat_totals: dict[str, float] = {}
    for exp in company_expenses:
        cat = exp.category or "Uncategorised"
        cat_totals[cat] = cat_totals.get(cat, 0) + (exp.converted_amount or 0)

    top_categories = sorted(
        [{"category": k, "total": round(v, 2)} for k, v in cat_totals.items()],
        key=lambda x: x["total"],
        reverse=True,
    )[:5]

    return {
        "total_spend_90d": round(total_spend, 2),
        "flagged_expense_count": len(flagged),
        "avg_risk_score": round(avg_risk, 4),
        "high_spenders": detect_high_spenders(db, company_id=company_id, top_n=5),
        "approval_delay": approval_delay_analysis(db, company_id=company_id),
        "top_categories": top_categories,
    }