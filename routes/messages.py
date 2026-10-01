from fastapi import APIRouter, Request
from detector import analyze_message, is_number_reported, calculate_risk_level
from models import ScamReport
from database import SessionLocal, create_audit_log

router = APIRouter()

@router.post("/check-message")
def check_message(request: Request, data: dict):
    message = data.get("message", "")
    phone   = data.get("phone", "")

    found_keywords, risk_score = analyze_message(message)

    number_flagged = is_number_reported(phone)

    if number_flagged:
        risk_score = min(risk_score + 0.5, 1.0)

    level, advice = calculate_risk_level(risk_score)

    db = SessionLocal()
    report = ScamReport(
        phone=phone,
        message=message,
        risk_score=str(risk_score)
    )
    db.add(report)
    db.commit()

    # --- NEW: Record the scam check for Non-Repudiation ---
    # We truncate the message to 50 characters so the log stays clean
    msg_snippet = message[:50] + "..." if len(message) > 50 else message
    create_audit_log(
        db, 
        "Anonymous", 
        "SCAM_CHECK", 
        f"Checked message: '{msg_snippet}' (Phone: {phone})", 
        request.client.host
    )
    # ------------------------------------------------------

    db.close()

    return {
        "risk_score":     risk_score,
        "level":          level,
        "keywords_found": found_keywords,
        "number_flagged": number_flagged,
        "advice":         advice
    }
