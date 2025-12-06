"""
Tournaments router.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.models.user import User
from app.auth.dependencies import get_current_user, get_current_organizer
from app.schemas.tournament import TournamentCreate, TournamentUpdate, TournamentResponse
from app.services.tournament_service import TournamentService

router = APIRouter(prefix="/api/tournaments", tags=["tournaments"])


@router.post("", response_model=TournamentResponse, status_code=status.HTTP_201_CREATED)
async def create_tournament(
    tournament_data: TournamentCreate,
    current_user: User = Depends(get_current_organizer),
    db: AsyncSession = Depends(get_db)
):
    """Create a new tournament (Organizer only)"""
    tournament = await TournamentService.create_tournament(db, tournament_data, current_user.id)
    return tournament


@router.get("", response_model=List[TournamentResponse])
async def get_all_tournaments(
    db: AsyncSession = Depends(get_db)
):
    """Get all tournaments"""
    tournaments = await TournamentService.get_all_tournaments(db)
    return tournaments


@router.get("/{tournament_id}", response_model=TournamentResponse)
async def get_tournament(
    tournament_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get tournament by ID"""
    tournament = await TournamentService.get_tournament(db, tournament_id)
    if not tournament:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tournament not found"
        )
    return tournament


@router.put("/{tournament_id}", response_model=TournamentResponse)
async def update_tournament(
    tournament_id: int,
    tournament_data: TournamentUpdate,
    current_user: User = Depends(get_current_organizer),
    db: AsyncSession = Depends(get_db)
):
    """Update tournament (Organizer only)"""
    tournament = await TournamentService.update_tournament(db, tournament_id, tournament_data)
    if not tournament:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tournament not found"
        )
    return tournament


@router.delete("/{tournament_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tournament(
    tournament_id: int,
    current_user: User = Depends(get_current_organizer),
    db: AsyncSession = Depends(get_db)
):
    """Delete tournament (Organizer only)"""
    success = await TournamentService.delete_tournament(db, tournament_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tournament not found"
        )
