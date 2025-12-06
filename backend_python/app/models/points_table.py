"""
Points table model for group standings.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class PointsTable(Base):
    """Points table for tournament groups"""
    __tablename__ = "points_table"
    
    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"), nullable=False, index=True)
    group = Column(String, nullable=False, index=True)  # "A" or "B"
    
    # Entries stored as JSON array of team standings
    # [{"teamId": 1, "teamName": "Team A", "played": 3, "won": 2, "lost": 1, ...}, ...]
    entries = Column(JSON, nullable=False, default=list)
    
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    tournament = relationship("Tournament", backref="points_tables")

