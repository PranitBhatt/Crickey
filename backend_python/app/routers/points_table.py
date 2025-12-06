"""
Points table router.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.models.user import User
from app.auth.dependencies import get_current_user
from app.schemas.points_table import PointsTableResponse
from app.services.points_service import PointsService

router = APIRouter(prefix="/api/points-table", tags=["points-table"])


@router.post("/calculate/{tournament_id}/{group}", response_model=PointsTableResponse)
async def calculate_points_table(
    tournament_id: int,
    group: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Calculate and update points table for a group"""
    points_table = await PointsService.calculate_points_table(db, tournament_id, group)
    return points_table


@router.get("/{tournament_id}/{group}", response_model=PointsTableResponse)
async def get_points_table(
    tournament_id: int,
    group: str,
    db: AsyncSession = Depends(get_db)
):
    """Get points table for a group"""
    points_table = await PointsService.get_points_table(db, tournament_id, group)
    if not points_table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Points table not found"
        )
    return points_table


@router.get("/{tournament_id}", response_model=List[PointsTableResponse])
async def get_all_points_tables(
    tournament_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all points tables for a tournament"""
    points_tables = await PointsService.get_all_points_tables(db, tournament_id)
    return points_tables
