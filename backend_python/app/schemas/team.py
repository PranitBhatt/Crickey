"""
Team and Player schemas.
"""
from pydantic import BaseModel
from typing import List, Optional
from app.models.team import Group


class PlayerCreate(BaseModel):
    """Player creation request"""
    name: str
    role: str
    is_substitute: bool = False


class PlayerResponse(BaseModel):
    """Player response model"""
    id: int
    team_id: int
    name: str
    role: str
    is_substitute: bool
    
    class Config:
        from_attributes = True


class TeamCreate(BaseModel):
    """Team creation request"""
    tournament_id: int
    name: str
    group: Group
    captain_name: str
    captain_uid: int
    logo_url: Optional[str] = None
    players: List[PlayerCreate]


class TeamUpdate(BaseModel):
    """Team update request"""
    name: Optional[str] = None
    group: Optional[Group] = None
    captain_name: Optional[str] = None
    logo_url: Optional[str] = None
    players: Optional[List[PlayerCreate]] = None


class TeamResponse(BaseModel):
    """Team response model"""
    id: int
    tournament_id: int
    name: str
    group: Group
    captain_name: str
    captain_uid: int
    logo_url: Optional[str]
    players: List[PlayerResponse]
    
    class Config:
        from_attributes = True

