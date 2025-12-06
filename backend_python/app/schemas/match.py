"""
Match and Ball schemas.
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict
from app.models.match import MatchStatus


class ScoreUpdate(BaseModel):
    """Score update request"""
    team_id: int
    runs: int
    wickets: int
    overs: float


class BallCreate(BaseModel):
    """Ball-by-ball entry creation"""
    over_number: int
    ball_number: int
    batsman: str
    bowler: str
    runs: int = 0
    is_wicket: bool = False
    extras: int = 0


class BallResponse(BaseModel):
    """Ball response model"""
    id: int
    match_id: int
    over_number: int
    ball_number: int
    batsman: str
    bowler: str
    runs: int
    is_wicket: bool
    extras: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


class MatchCreate(BaseModel):
    """Match creation request"""
    tournament_id: int
    group: Optional[str] = None
    match_number: int
    team1_id: int
    team2_id: int
    date_time: datetime
    venue: str
    overs: int
    status: MatchStatus = MatchStatus.SCHEDULED


class MatchUpdate(BaseModel):
    """Match update request"""
    group: Optional[str] = None
    match_number: Optional[int] = None
    team1_id: Optional[int] = None
    team2_id: Optional[int] = None
    date_time: Optional[datetime] = None
    venue: Optional[str] = None
    overs: Optional[int] = None
    status: Optional[MatchStatus] = None
    winner_team_id: Optional[int] = None


class MatchResponse(BaseModel):
    """Match response model"""
    id: int
    tournament_id: int
    group: Optional[str]
    match_number: int
    team1_id: int
    team2_id: int
    date_time: datetime
    venue: str
    overs: int
    status: MatchStatus
    winner_team_id: Optional[int]
    scores: Optional[Dict] = {}
    
    class Config:
        from_attributes = True

