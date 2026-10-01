from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.sql import func
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True)
    username   = Column(String, unique=True)
    email      = Column(String, unique=True)
    password   = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    is_active  = Column(Boolean, default=True)

class ReportedNumber(Base):
    __tablename__ = "reported_numbers"

    id          = Column(Integer, primary_key=True)
    phone       = Column(String, unique=True)
    reason      = Column(String)
    reported_at = Column(DateTime, default=datetime.now)
    reported_by = Column(Integer, ForeignKey("users.id"), nullable=True)

class ScamReport(Base):
    __tablename__ = "scam_reports"

    id          = Column(Integer, primary_key=True)
    phone       = Column(String)
    message     = Column(String)
    risk_score  = Column(String)
    reported_at = Column(DateTime, default=datetime.now)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=True)

# --- NEW: Audit Log Model for Non-Repudiation ---
class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True) # Who did it
    action = Column(String, index=True)   # What they did (e.g., LOGIN, CHECK_SCAM)
    details = Column(Text)                # Extra info (e.g., "Checked number +256...")
    ip_address = Column(String)           # Where they did it from
    timestamp = Column(DateTime(timezone=True), server_default=func.now()) # Exact time
