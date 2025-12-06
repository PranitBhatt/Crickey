"""
Points table schemas.
"""
from pydantic import BaseModel
from typing import List
from datetime import datetime


class PointsTableEntry(BaseModel):
    """Points table entry"""
    team_id: int
    team_name: str
    group: str
    played: int
    won: int
    lost: int
    tied: int
    points: int
    net_run_rate: float
    runs_for: int
    runs_against: int
    overs_for: float
    overs_against: float


class PointsTableResponse(BaseModel):
    """Points table response model"""
    id: int
    tournament_id: int
    group: str
    entries: List[PointsTableEntry]
    last_updated: datetime
    
    class Config:
        from_attributes = True

