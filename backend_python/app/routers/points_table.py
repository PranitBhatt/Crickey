"""
Points Table router - mirrors PointsTableController.cs
"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.points_table import PointsTableDTO, UpdatePointsTableRequest
from app.services.points_table_service import PointsTableService
from app.database import get_db
from google.cloud import firestore

router = APIRouter(prefix="/api/pointsTable", tags=["points-table"])


def get_points_table_service(db: firestore.Client = Depends(get_db)) -> PointsTableService:
    """Dependency injection for PointsTableService"""
    from app.repositories.points_table_repository import PointsTableRepository
    from app.repositories.match_repository import MatchRepository
    from app.repositories.team_repository import TeamRepository
    
    points_table_repo = PointsTableRepository(db)
    match_repo = MatchRepository(db)
    team_repo = TeamRepository(db)
    
    return PointsTableService(points_table_repo, match_repo, team_repo)


@router.post("/update", status_code=status.HTTP_204_NO_CONTENT)
async def update_points_table(
    request: UpdatePointsTableRequest,
    service: PointsTableService = Depends(get_points_table_service)
):
    """
    Update points table.
    Mirrors POST /api/pointsTable/update
    """
    await service.update_points_table(request.tournamentId)
    return None


@router.get("/{tournament_id}/{group}")
async def get_points_table(
    tournament_id: str,
    group: str,
    service: PointsTableService = Depends(get_points_table_service)
):
    """
    Get points table.
    Mirrors GET /api/pointsTable/{tournamentId}/{group}
    """
    points_table = await service.get_points_table(tournament_id, group)
    if not points_table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Points table not found"
        )
    return points_table


@router.get("/{tournament_id}")
async def get_all_points_tables(
    tournament_id: str,
    service: PointsTableService = Depends(get_points_table_service)
):
    """
    Get all points tables for tournament.
    Mirrors GET /api/pointsTable/{tournamentId}
    """
    points_tables = await service.get_all_points_tables(tournament_id)
    return points_tables

