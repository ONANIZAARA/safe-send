from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import AuditLog
from routes import messages, numbers, reports, ussd, users

# Create all tables in the database (This is safe and won't delete existing data)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SafeSend API",
    description="Offline + Scam-Aware Payment Protection System for Africa",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(messages.router)
app.include_router(numbers.router)
app.include_router(reports.router)
app.include_router(ussd.router)
app.include_router(users.router)

@app.get("/")
def home():
    return FileResponse("index.html")

@app.get("/admin")
def admin():
    return FileResponse("admin.html")

# Route to view Audit Logs for Non-Repudiation
@app.get("/admin/audit-logs")
def get_audit_logs(db: Session = Depends(get_db)):
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(50).all()
    return [
        {
            "time": str(log.timestamp),
            "user": log.username,
            "action": log.action,
            "details": log.details,
            "ip": log.ip_address
        } 
        for log in logs
    ]
