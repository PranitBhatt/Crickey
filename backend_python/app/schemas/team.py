"""
Team DTOs - mirrors CricketTournament.Application.DTOs.TeamDTO
"""
from pydantic import BaseModel, Field
from typing import Optional


class PlayerDTO(BaseModel):
    """Player data transfer object"""
    name: str = Field(..., min_length=1)
    role: str = Field(..., min_length=1)


class TeamDTO(BaseModel):
    """Team data transfer object"""
    id: Optional[str] = None
    tournamentId: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    group: str = Field(..., pattern="^[A-Z]$")
    captainName: str = Field(..., min_length=1)
    captainUid: str = Field(..., min_length=1)
    logoUrl: str = Field(default="")
    players: list[PlayerDTO] = Field(default_factory=list)
    substitute: Optional[PlayerDTO] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "tournamentId": "tournament-id",
                "name": "Mumbai Indians",
                "group": "A",
                "captainName": "Captain Name",
                "captainUid": "captain-uid",
                "logoUrl": "",
                "players": [
                    {"name": "Player 1", "role": "Batsman"},
                    {"name": "Player 2", "role": "Bowler"}
                ],
                "substitute": {"name": "Substitute Player", "role": "All-rounder"}
            }
        }

