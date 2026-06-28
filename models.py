from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
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