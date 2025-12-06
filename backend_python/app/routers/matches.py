"""
Matches router.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.models.user import User
from app.auth.dependencies import get_current_user, get_current_organizer
from app.schemas.match import MatchCreate, MatchUpdate, MatchResponse, BallCreate, BallResponse, ScoreUpdate
from app.services.match_service import MatchService

router = APIRouter(prefix="/api/matches", tags=["matches"])


@router.post("", response_model=MatchResponse, status_code=status.HTTP_201_CREATED)
async def create_match(
    match_data: MatchCreate,
    current_user: User = Depends(get_current_organizer),
    db: AsyncSession = Depends(get_db)
):
    """Create a new match (Organizer only)"""
    match = await MatchService.create_match(db, match_data)
    return match


@router.get("/tournament/{tournament_id}", response_model=List[MatchResponse])
async def get_matches_by_tournament(
    tournament_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all matches for a tournament"""
    matches = await MatchService.get_matches_by_tournament(db, tournament_id)
    return matches


@router.get("/{match_id}", response_model=MatchResponse)
async def get_match(
    match_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get match by ID"""
    match = await MatchService.get_match(db, match_id)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    return match


@router.put("/{match_id}", response_model=MatchResponse)
async def update_match(
    match_id: int,
    match_data: MatchUpdate,
    current_user: User = Depends(get_current_organizer),
    db: AsyncSession = Depends(get_db)
):
    """Update match (Organizer only)"""
    match = await MatchService.update_match(db, match_id, match_data)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    return match


@router.post("/{match_id}/score", response_model=MatchResponse)
async def update_score(
    match_id: int,
    score_data: ScoreUpdate,
    current_user: User = Depends(get_current_organizer),
    db: AsyncSession = Depends(get_db)
):
    """Update match score (Organizer only)"""
    match = await MatchService.update_score(db, match_id, score_data)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    return match


@router.post("/{match_id}/ball", response_model=BallResponse, status_code=status.HTTP_201_CREATED)
async def add_ball(
    match_id: int,
    ball_data: BallCreate,
    current_user: User = Depends(get_current_organizer),
    db: AsyncSession = Depends(get_db)
):
    """Add ball-by-ball entry (Organizer only)"""
    ball = await MatchService.add_ball(db, match_id, ball_data)
    return ball


@router.get("/{match_id}/balls", response_model=List[BallResponse])
async def get_balls(
    match_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all balls for a match"""
    balls = await MatchService.get_balls_by_match(db, match_id)
    return balls


@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_match(
    match_id: int,
    current_user: User = Depends(get_current_organizer),
    db: AsyncSession = Depends(get_db)
):
    """Delete match (Organizer only)"""
    success = await MatchService.delete_match(db, match_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
