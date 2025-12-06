"""
Match and Ball models for scoring.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Enum as SQLEnum, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class MatchStatus(str, enum.Enum):
    """Match status"""
    SCHEDULED = "scheduled"
    LIVE = "live"
    COMPLETED = "completed"


class Match(Base):
    """Match model"""
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"), nullable=False, index=True)
    group = Column(String, nullable=True)  # Group name (A/B) or "semi" or "final"
    match_number = Column(Integer, nullable=False)
    team1_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    team2_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    date_time = Column(DateTime(timezone=True), nullable=False)
    venue = Column(String, nullable=False)
    overs = Column(Integer, nullable=False)  # Number of overs for this match
    status = Column(SQLEnum(MatchStatus), nullable=False, default=MatchStatus.SCHEDULED)
    winner_team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    
    # Scores stored as JSON: {"team1_id": {"runs": 120, "wickets": 5, "overs": 6.0}, ...}
    scores = Column(JSON, nullable=True, default=dict)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    tournament = relationship("Tournament", backref="matches")
    team1 = relationship("Team", foreign_keys=[team1_id], backref="matches_as_team1")
    team2 = relationship("Team", foreign_keys=[team2_id], backref="matches_as_team2")
    balls = relationship("Ball", back_populates="match", cascade="all, delete-orphan", order_by="Ball.over_number, Ball.ball_number")


class Ball(Base):
    """Ball-by-ball scoring entry"""
    __tablename__ = "balls"
    
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False, index=True)
    over_number = Column(Integer, nullable=False)
    ball_number = Column(Integer, nullable=False)  # 1-6 within the over
    batsman = Column(String, nullable=False)
    bowler = Column(String, nullable=False)
    runs = Column(Integer, nullable=False, default=0)
    is_wicket = Column(String, default=False)
    extras = Column(Integer, nullable=False, default=0)  # Wide, no-ball, etc.
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    match = relationship("Match", back_populates="balls")

