from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import AuditLog # Import the new AuditLog model

engine = create_engine("sqlite:///safesend.db")

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- NEW: Helper function to record actions ---
def create_audit_log(db, username: str, action: str, details: str, ip_address: str = "Unknown"):
    """Records an action for Non-Repudiation"""
    log_entry = AuditLog(
        username=username,
        action=action,
        details=details,
        ip_address=ip_address
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry
