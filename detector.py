import re
from keywords import HIGH_WEIGHT_KEYWORDS, MEDIUM_WEIGHT_KEYWORDS, LOW_WEIGHT_KEYWORDS
from models import ReportedNumber
from database import SessionLocal

# ─────────────────────────────────────────────
# SafeSend — Detector Engine
# Uses weighted keyword matching with whole-word
# checking to avoid false positives.
# ─────────────────────────────────────────────

WEIGHTS = {
    "high":   0.6,
    "medium": 0.3,
    "low":    0.1,
}


def _contains(text: str, keyword: str) -> bool:
    """
    Check if keyword appears in text.
    - Multi-word keywords matched as phrases.
    - Single-word keywords use whole-word matching
      so 'pin' does NOT match inside 'discipline'.
    """
    if " " in keyword:
        return keyword in text
    else:
        pattern = r'\b' + re.escape(keyword) + r'\b'
        return bool(re.search(pattern, text))


def analyze_message(message: str):
    """
    Analyze a message for scam signals.
    Returns (found_keywords, risk_score).
    risk_score is between 0.0 and 1.0.
    """
    text = message.lower()
    found_keywords = []
    total_score = 0.0

    for kw in HIGH_WEIGHT_KEYWORDS:
        if _contains(text, kw):
            found_keywords.append(kw)
            total_score += WEIGHTS["high"]

    for kw in MEDIUM_WEIGHT_KEYWORDS:
        if _contains(text, kw):
            found_keywords.append(kw)
            total_score += WEIGHTS["medium"]

    for kw in LOW_WEIGHT_KEYWORDS:
        if _contains(text, kw):
            found_keywords.append(kw)
            total_score += WEIGHTS["low"]

    risk_score = min(round(total_score, 2), 1.0)
    return found_keywords, risk_score


def is_number_reported(phone: str) -> bool:
    """Check if a phone number has been reported as a scam."""
    if not phone:
        return False
    db = SessionLocal()
    result = db.query(ReportedNumber).filter(
        ReportedNumber.phone == phone
    ).first()
    db.close()
    return result is not None


def calculate_risk_level(risk_score: float):
    """
    Convert numeric risk score to a human-readable
    level and advice message.
    """
    if risk_score >= 0.6:
        return (
            "HIGH RISK",
            "Do NOT respond, send money, or share any details. "
            "This message has strong signs of being a scam."
        )
    elif risk_score >= 0.3:
        return (
            "SUSPICIOUS",
            "Be careful. Do not share personal details or send money "
            "without verifying the sender through a trusted method."
        )
    else:
        return (
            "SAFE",
            "No scam indicators found. Always stay cautious — "
            "when in doubt, verify before acting."
        )
