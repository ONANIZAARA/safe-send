from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
from detector import analyze_message, is_number_reported, calculate_risk_level
from models import ScamReport, ReportedNumber
from database import SessionLocal

# ─────────────────────────────────────────────
# SafeSend — USSD Handler
#
# Works with Africa's Talking USSD API.
# When a user dials your code, Africa's Talking
# sends a POST request to /ussd on your server.
#
# The 'text' field tracks all user inputs joined by *.
# Example: "2*0700000000*20000" means:
#   - User chose option 2 (Send Money)
#   - Entered recipient: 0700000000
#   - Entered amount: 20000
# ─────────────────────────────────────────────

router = APIRouter()


@router.post("/ussd", response_class=PlainTextResponse)
async def ussd_handler(request: Request):
    form = await request.form()

    session_id   = form.get("sessionId", "")
    phone_number = form.get("phoneNumber", "")
    text         = form.get("text", "")

    steps = text.split("*") if text else []

    # ── STEP 0: Welcome menu ─────────────────────
    if text == "":
        response = (
            "CON Welcome to SafeSend\n"
            "1. Check a message for scam\n"
            "2. Send money safely\n"
            "3. Report a scam number"
        )

    # ── OPTION 1: Check a message ────────────────
    elif steps[0] == "1":
        if len(steps) == 1:
            response = "CON Type the message you want to check:"
        elif len(steps) == 2:
            message = steps[1]
            found_keywords, risk_score = analyze_message(message)
            level, advice = calculate_risk_level(risk_score)
            score_pct = int(risk_score * 100)
            response = (
                f"END SafeSend Result\n"
                f"Risk: {level} ({score_pct}%)\n"
                f"{advice}"
            )

    # ── OPTION 2: Send money ─────────────────────
    elif steps[0] == "2":
        if len(steps) == 1:
            response = "CON Enter recipient phone number:"
        elif len(steps) == 2:
            response = "CON Enter amount (UGX):"
        elif len(steps) == 3:
            recipient      = steps[1]
            amount         = steps[2]
            number_flagged = is_number_reported(recipient)

            if number_flagged:
                response = (
                    f"END WARNING: High Risk\n"
                    f"{recipient} has been reported as a scam number.\n"
                    "Transaction cancelled for your safety."
                )
            else:
                db = SessionLocal()
                db.add(ScamReport(
                    phone=recipient,
                    message=f"USSD send: UGX {amount}",
                    risk_score="0.0"
                ))
                db.commit()
                db.close()
                response = (
                    f"END SafeSend Check Passed\n"
                    f"Recipient: {recipient}\n"
                    f"Amount: UGX {amount}\n"
                    "No scam flags found.\n"
                    "Proceed to send via your mobile money."
                )

    # ── OPTION 3: Report a number ────────────────
    elif steps[0] == "3":
        if len(steps) == 1:
            response = "CON Enter the scam number to report:"
        elif len(steps) == 2:
            response = "CON Describe the scam briefly\n(e.g. asked for PIN):"
        elif len(steps) == 3:
            scam_number = steps[1]
            reason      = steps[2]
            db = SessionLocal()
            existing = db.query(ReportedNumber).filter(
                ReportedNumber.phone == scam_number
            ).first()

            if existing:
                db.close()
                response = (
                    f"END {scam_number} was already reported.\n"
                    "Thank you for keeping the community safe."
                )
            else:
                db.add(ReportedNumber(phone=scam_number, reason=reason))
                db.commit()
                db.close()
                response = (
                    f"END {scam_number} reported successfully.\n"
                    "Thank you. You are helping protect others."
                )

    # ── Fallback ──────────────────────────────────
    else:
        response = "END Invalid option. Please dial again."

    return PlainTextResponse(content=response)
