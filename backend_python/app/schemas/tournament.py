"""
Tournament schemas.
"""
from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from app.models.tournament import TournamentStatus


class TournamentCreate(BaseModel):
    """Tournament creation request"""
    name: str
    start_date: date
    end_date: date
    location: str
    overs_group: int = 6
    overs_knockout: int = 7
    groups: List[str] = ["A", "B"]


class TournamentUpdate(BaseModel):
    """Tournament update request"""
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    location: Optional[str] = None
    overs_group: Optional[int] = None
    overs_knockout: Optional[int] = None
    status: Optional[TournamentStatus] = None


class TournamentResponse(BaseModel):
    """Tournament response model"""
    id: int
    name: str
    start_date: date
    end_date: date
    location: str
    overs_group: int
    overs_knockout: int
    groups: List[str]
    status: TournamentStatus
    created_by: int
    
    class Config:
        from_attributes = True

