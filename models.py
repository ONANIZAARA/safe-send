from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from database import Base

class ReportedNumber(Base):
    __tablename__ = "reported_numbers"

    id          = Column(Integer, primary_key=True)
    phone       = Column(String, unique=True)
    reason      = Column(String)
    reported_at = Column(DateTime, default=datetime.now)

class ScamReport(Base):
    __tablename__ = "scam_reports"

    id          = Column(Integer, primary_key=True)
    phone       = Column(String)
    message     = Column(String)
    risk_score  = Column(String)
    reported_at = Column(DateTime, default=datetime.now)
