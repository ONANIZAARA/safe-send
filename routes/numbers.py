from fastapi import APIRouter
from models import ReportedNumber
from database import SessionLocal
from detector import is_number_reported

router = APIRouter()

@router.post("/report-number")
def report_number(data: dict):
    phone  = data.get("phone", "")
    reason = data.get("reason", "No reason given")

    if not phone:
        return {"error": "Phone number is required"}

    db = SessionLocal()
    existing = db.query(ReportedNumber).filter(
        ReportedNumber.phone == phone
    ).first()

    if existing:
        db.close()
        return {"message": f"Number {phone} was already reported."}

    new_number = ReportedNumber(phone=phone, reason=reason)
    db.add(new_number)
    db.commit()
    db.close()

    return {"message": f"Number {phone} reported successfully. Thank you."}

@router.get("/number-status/{phone}")
def number_status(phone: str):
    flagged = is_number_reported(phone)
    return {
        "phone":   phone,
        "flagged": flagged,
        "status":  "REPORTED AS SCAM" if flagged else "CLEAN"
    }

@router.get("/all-reported-numbers")
def all_reported_numbers():
    db = SessionLocal()
    numbers = db.query(ReportedNumber).all()
    db.close()
    return [
        {
            "phone":       n.phone,
            "reason":      n.reason,
            "reported_at": str(n.reported_at)
        }
        for n in numbers
    ]
