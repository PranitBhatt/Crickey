"""
Points Table DTOs - mirrors CricketTournament.Application.DTOs.PointsTableDTO
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PointsTableEntryDTO(BaseModel):
    """Points table entry data transfer object"""
    teamId: str
    teamName: str
    group: str
    played: int = Field(..., ge=0)
    won: int = Field(..., ge=0)
    lost: int = Field(..., ge=0)
    tied: int = Field(..., ge=0)
    points: int = Field(..., ge=0)
    netRunRate: float
    runsFor: int = Field(..., ge=0)
    runsAgainst: int = Field(..., ge=0)
    oversFor: float = Field(..., ge=0)
    oversAgainst: float = Field(..., ge=0)


class PointsTableDTO(BaseModel):
    """Points table data transfer object"""
    tournamentId: str
    group: str
    entries: list[PointsTableEntryDTO]
    lastUpdated: datetime


class UpdatePointsTableRequest(BaseModel):
    """Request to update points table"""
    tournamentId: str = Field(..., min_length=1)

