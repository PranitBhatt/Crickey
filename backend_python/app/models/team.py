"""
Team and Player models.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, JSON, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class Group(str, enum.Enum):
    """Team groups"""
    A = "A"
    B = "B"


class Team(Base):
    """Team model"""
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    group = Column(SQLEnum(Group), nullable=False)
    captain_name = Column(String, nullable=False)
    captain_uid = Column(Integer, ForeignKey("users.id"), nullable=False)  # User ID of captain
    logo_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    players = relationship("Player", back_populates="team", cascade="all, delete-orphan")
    tournament = relationship("Tournament", backref="teams")


class Player(Base):
    """Player model"""
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)  # e.g., "Batsman", "Bowler", "All-rounder"
    is_substitute = Column(String, default=False)  # True for substitute player
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    team = relationship("Team", back_populates="players")

