"""
ai_engine/ — SmartReimburse AI Engine
Person 2 module

Exports:
    ocr               — Receipt scanning & text extraction
    fraud_detection   — Duplicate detection & anomaly scoring
    approval_ai       — AI approval path suggestion & auto-approval
    insights          — Spending analytics & company dashboard
"""

from . import ocr
from . import fraud_detection
from . import approval_ai
from . import insights

__all__ = ["ocr", "fraud_detection", "approval_ai", "insights"]
