"""
Tournaments router - mirrors TournamentsController.cs
"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.tournament import TournamentDTO
from app.services.tournament_service import TournamentService
from app.database import get_db
from app.auth.dependencies import verify_token
from google.cloud import firestore

router = APIRouter(prefix="/api/tournaments", tags=["tournaments"])


def get_tournament_service(db: firestore.Client = Depends(get_db)) -> TournamentService:
    """Dependency injection for TournamentService"""
    from app.repositories.tournament_repository import TournamentRepository
    repo = TournamentRepository(db)
    return TournamentService(repo)


@router.post("", status_code=status.HTTP_200_OK)
async def create_tournament(
    tournament: TournamentDTO,
    decoded_token: dict = Depends(verify_token),
    service: TournamentService = Depends(get_tournament_service)
):
    """
    Create tournament.
    Mirrors POST /api/tournaments
    """
    tournament_id = await service.create_tournament(tournament)
    return {"id": tournament_id}


@router.get("/{tournament_id}")
async def get_tournament(
    tournament_id: str,
    service: TournamentService = Depends(get_tournament_service)
):
    """
    Get tournament by ID.
    Mirrors GET /api/tournaments/{id}
    """
    tournament = await service.get_tournament(tournament_id)
    if not tournament:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tournament not found")
    return tournament


@router.get("")
async def get_all_tournaments(
    service: TournamentService = Depends(get_tournament_service)
):
    """
    Get all tournaments.
    Mirrors GET /api/tournaments
    """
    tournaments = await service.get_all_tournaments()
    return tournaments


@router.put("/{tournament_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_tournament(
    tournament_id: str,
    tournament: TournamentDTO,
    decoded_token: dict = Depends(verify_token),
    service: TournamentService = Depends(get_tournament_service)
):
    """
    Update tournament.
    Mirrors PUT /api/tournaments/{id}
    """
    await service.update_tournament(tournament_id, tournament)
    return None


@router.delete("/{tournament_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tournament(
    tournament_id: str,
    decoded_token: dict = Depends(verify_token),
    service: TournamentService = Depends(get_tournament_service)
):
    """
    Delete tournament.
    Mirrors DELETE /api/tournaments/{id}
    """
    await service.delete_tournament(tournament_id)
    return None

