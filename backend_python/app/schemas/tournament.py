"""
Tournament DTOs - mirrors CricketTournament.Application.DTOs.TournamentDTO
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TournamentDTO(BaseModel):
    """Tournament data transfer object"""
    id: Optional[str] = None
    name: str = Field(..., min_length=1)
    startDate: datetime
    endDate: datetime
    location: str = Field(..., min_length=1)
    oversGroup: int = Field(..., gt=0)
    oversKnockout: int = Field(..., gt=0)
    groups: list[str] = Field(default_factory=list)
    status: str = Field(default="upcoming", pattern="^(upcoming|ongoing|completed)$")
    createdBy: str = Field(..., min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Cricket Premier League 2024",
                "startDate": "2024-06-01T00:00:00Z",
                "endDate": "2024-07-31T00:00:00Z",
                "location": "Mumbai, India",
                "oversGroup": 20,
                "oversKnockout": 20,
                "groups": ["A", "B"],
                "status": "upcoming",
                "createdBy": "organizer-uid"
            }
        }

