"""
Teams router - mirrors TeamsController.cs
"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.team import TeamDTO
from app.services.team_service import TeamService
from app.database import get_db
from app.auth.dependencies import verify_token
from google.cloud import firestore

router = APIRouter(prefix="/api/teams", tags=["teams"])


def get_team_service(db: firestore.Client = Depends(get_db)) -> TeamService:
    """Dependency injection for TeamService"""
    from app.repositories.team_repository import TeamRepository
    repo = TeamRepository(db)
    return TeamService(repo)


@router.post("", status_code=status.HTTP_200_OK)
async def create_team(
    team: TeamDTO,
    decoded_token: dict = Depends(verify_token),
    service: TeamService = Depends(get_team_service)
):
    """
    Create team.
    Mirrors POST /api/teams
    """
    team_id = await service.create_team(team)
    return {"id": team_id}


@router.get("/{team_id}")
async def get_team(
    team_id: str,
    service: TeamService = Depends(get_team_service)
):
    """
    Get team by ID.
    Mirrors GET /api/teams/{id}
    """
    team = await service.get_team(team_id)
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return team


@router.get("/tournament/{tournament_id}")
async def get_teams_by_tournament(
    tournament_id: str,
    service: TeamService = Depends(get_team_service)
):
    """
    Get teams by tournament.
    Mirrors GET /api/teams/tournament/{tournamentId}
    """
    teams = await service.get_teams_by_tournament(tournament_id)
    return teams


@router.put("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_team(
    team_id: str,
    team: TeamDTO,
    decoded_token: dict = Depends(verify_token),
    service: TeamService = Depends(get_team_service)
):
    """
    Update team.
    Mirrors PUT /api/teams/{id}
    """
    await service.update_team(team_id, team)
    return None


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(
    team_id: str,
    decoded_token: dict = Depends(verify_token),
    service: TeamService = Depends(get_team_service)
):
    """
    Delete team.
    Mirrors DELETE /api/teams/{id}
    """
    await service.delete_team(team_id)
    return None

