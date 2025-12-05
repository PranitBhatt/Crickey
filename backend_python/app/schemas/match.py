"""
Match DTOs - mirrors CricketTournament.Application.DTOs.MatchDTO
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MatchScoreDTO(BaseModel):
    """Match score data transfer object"""
    runs: int = Field(..., ge=0)
    wickets: int = Field(..., ge=0, le=10)
    overs: float = Field(..., ge=0)


class MatchDTO(BaseModel):
    """Match data transfer object"""
    id: Optional[str] = None
    tournamentId: str = Field(..., min_length=1)
    group: str = Field(..., min_length=1)
    matchNumber: int = Field(..., gt=0)
    team1Id: str = Field(..., min_length=1)
    team2Id: str = Field(..., min_length=1)
    dateTime: datetime
    venue: str = Field(..., min_length=1)
    overs: int = Field(..., gt=0)
    status: str = Field(default="scheduled", pattern="^(scheduled|live|completed)$")
    winnerTeamId: Optional[str] = None
    scores: Optional[dict[str, MatchScoreDTO]] = None


class ScoreUpdateDTO(BaseModel):
    """Score update data transfer object"""
    teamId: str = Field(..., min_length=1)
    runs: int = Field(..., ge=0)
    wickets: int = Field(..., ge=0, le=10)
    overs: float = Field(..., ge=0)


class BallByBallDTO(BaseModel):
    """Ball-by-ball data transfer object"""
    ballNumber: int = Field(..., gt=0, le=6)
    overNumber: int = Field(..., gt=0)
    batsman: str = Field(..., min_length=1)
    bowler: str = Field(..., min_length=1)
    runs: int = Field(..., ge=0)
    isWicket: bool = False
    extras: int = Field(default=0, ge=0)

