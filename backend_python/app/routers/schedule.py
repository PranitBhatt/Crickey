"""
Schedule router for auto-generating matches.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.auth.dependencies import get_current_organizer
from app.schemas.match import MatchResponse
from app.services.scheduling_service import SchedulingService
from datetime import datetime
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/api/schedule", tags=["schedule"])


class GenerateScheduleRequest(BaseModel):
    """Request to generate schedule"""
    tournament_id: int
    start_datetime: datetime


class GenerateKnockoutRequest(BaseModel):
    """Request to generate knockout matches"""
    tournament_id: int
    group_a_top2: List[int]  # Team IDs
    group_b_top2: List[int]  # Team IDs
    start_datetime: datetime


@router.post("/generate-group-stage", response_model=List[MatchResponse])
async def generate_group_stage(
    request: GenerateScheduleRequest,
    current_user: User = Depends(get_current_organizer),
    db: AsyncSession = Depends(get_db)
):
    """Generate group stage matches (Organizer only)"""
    try:
        matches = await SchedulingService.generate_group_stage_schedule(
            db, request.tournament_id, request.start_datetime
        )
        return matches
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/generate-knockout", response_model=List[MatchResponse])
async def generate_knockout(
    request: GenerateKnockoutRequest,
    current_user: User = Depends(get_current_organizer),
    db: AsyncSession = Depends(get_db)
):
    """Generate knockout matches (Organizer only)"""
    try:
        matches = await SchedulingService.generate_knockout_matches(
            db,
            request.tournament_id,
            request.group_a_top2,
            request.group_b_top2,
            request.start_datetime
        )
        return matches
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

