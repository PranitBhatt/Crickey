"""
Tournament model.
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.sql import func
from app.database import Base
import enum


class TournamentStatus(str, enum.Enum):
    """Tournament status"""
    UPCOMING = "upcoming"
    ONGOING = "ongoing"
    COMPLETED = "completed"


class Tournament(Base):
    """Tournament model"""
    __tablename__ = "tournaments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    location = Column(String, nullable=False)
    overs_group = Column(Integer, nullable=False, default=6)  # Overs for group stage
    overs_knockout = Column(Integer, nullable=False, default=7)  # Overs for knockout
    groups = Column(JSON, nullable=False, default=list)  # List of group names ["A", "B"]
    status = Column(SQLEnum(TournamentStatus), nullable=False, default=TournamentStatus.UPCOMING)
    created_by = Column(Integer, nullable=False)  # User ID
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

