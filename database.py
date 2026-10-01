from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///safesend.db")

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- FAIL-SAFE audit log function ---
def create_audit_log(db, username: str, action: str, details: str, ip_address: str = "Unknown"):
    """Records an action for Non-Repudiation (fails silently if table doesn't exist)"""
    try:
        from models import AuditLog
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
    except Exception as e:
        # If audit log fails, don't crash the app - just print error
        print(f"Audit log error (non-critical): {e}")
        return None
