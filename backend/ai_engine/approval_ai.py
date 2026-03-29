from sqlalchemy.orm import Session

AUTO_APPROVE_RISK_THRESHOLD = 0.25
AUTO_APPROVE_AMOUNT_LIMIT = 5000
HIGH_RISK_THRESHOLD = 0.70


def _get_manager_id(db: Session, user_id: str) -> str | None:
    from backend.core.models import User
    user = db.query(User).filter(User.id == user_id).first()
    return str(user.manager_id) if user and user.manager_id else None


def _get_special_approver(db: Session, company_id: str) -> str | None:
    from backend.core.models import ApprovalRule
    rule = db.query(ApprovalRule).filter(ApprovalRule.company_id == company_id).first()
    return str(rule.special_approver_id) if rule and rule.special_approver_id else None


def suggest_approval_path(db: Session, expense_data: dict) -> list[dict]:
    user_id = expense_data.get("user_id")
    company_id = expense_data.get("company_id")
    amount = expense_data.get("converted_amount", 0)
    risk_score = expense_data.get("risk_score", 0.0)

    approvers = []
    priority = 1

    manager_id = _get_manager_id(db, user_id)
    if manager_id:
        approvers.append({
            "approver_id": manager_id,
            "priority": priority,
            "reason": "Direct manager"
        })
        priority += 1

    if amount > 10000 or risk_score >= 0.40:
        special = _get_special_approver(db, company_id)
        if special and special not in [a["approver_id"] for a in approvers]:
            approvers.append({
                "approver_id": special,
                "priority": priority,
                "reason": "Amount exceeds department threshold" if amount > 10000 else "Elevated risk score"
            })
            priority += 1

    if risk_score >= HIGH_RISK_THRESHOLD or amount > 50000:
        special = _get_special_approver(db, company_id)
        if special and special not in [a["approver_id"] for a in approvers]:
            approvers.append({
                "approver_id": special,
                "priority": priority,
                "reason": "High risk: CFO/Admin approval required"
            })
            priority += 1

    return approvers


def auto_approve_decision(risk_score: float, converted_amount: float = 0) -> bool:
    return (
        risk_score < AUTO_APPROVE_RISK_THRESHOLD
        and converted_amount < AUTO_APPROVE_AMOUNT_LIMIT
    )


def get_approval_recommendation(risk_score: float, converted_amount: float) -> dict:
    if risk_score < AUTO_APPROVE_RISK_THRESHOLD and converted_amount < AUTO_APPROVE_AMOUNT_LIMIT:
        return {
            "action": "AUTO_APPROVE",
            "reason": "Low risk score and amount within policy limits",
            "confidence": round(1.0 - risk_score, 2),
        }
    elif risk_score >= HIGH_RISK_THRESHOLD:
        return {
            "action": "FLAG_FOR_INVESTIGATION",
            "reason": "High anomaly score — possible fraud or policy violation",
            "confidence": round(risk_score, 2),
        }
    else:
        return {
            "action": "MANUAL_REVIEW",
            "reason": "Amount or risk requires human judgment",
            "confidence": 0.75,
        }