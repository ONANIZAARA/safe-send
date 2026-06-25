from fastapi import APIRouter
from models import ScamReport
from database import SessionLocal

router = APIRouter()

@router.get("/all-scam-reports")
def all_scam_reports():
    db = SessionLocal()
    reports = db.query(ScamReport).all()
    db.close()
    return [
        {
            "phone":       r.phone,
            "message":     r.message,
            "risk_score":  r.risk_score,
            "reported_at": str(r.reported_at)
        }
        for r in reports
    ]

@router.get("/scam-stats")
def scam_stats():
    db = SessionLocal()
    all_reports = db.query(ScamReport).all()
    db.close()

    total      = len(all_reports)
    high_risk  = 0
    suspicious = 0
    safe       = 0

    for r in all_reports:
        try:
            score = float(r.risk_score)
        except (ValueError, TypeError):
            score = 0.0

        if score >= 0.6:
            high_risk += 1
        elif score >= 0.3:
            suspicious += 1
        else:
            safe += 1

    return {
        "total_checks": total,
        "high_risk":    high_risk,
        "suspicious":   suspicious,
        "safe":         safe
    }
