"""
Matches router - mirrors MatchesController.cs
"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.match import MatchDTO, ScoreUpdateDTO, BallByBallDTO
from app.services.match_service import MatchService
from app.database import get_db
from google.cloud import firestore

router = APIRouter(prefix="/api/matches", tags=["matches"])


def get_match_service(db: firestore.Client = Depends(get_db)) -> MatchService:
    """Dependency injection for MatchService"""
    from app.repositories.match_repository import MatchRepository
    repo = MatchRepository(db)
    return MatchService(repo)


@router.post("", status_code=status.HTTP_200_OK)
async def create_match(
    match: MatchDTO,
    service: MatchService = Depends(get_match_service)
):
    """
    Create match.
    Mirrors POST /api/matches
    """
    match_id = await service.create_match(match)
    return {"id": match_id}


@router.get("/{match_id}")
async def get_match(
    match_id: str,
    service: MatchService = Depends(get_match_service)
):
    """
    Get match by ID.
    Mirrors GET /api/matches/{id}
    """
    match = await service.get_match(match_id)
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
    return match


@router.get("/tournament/{tournament_id}")
async def get_matches_by_tournament(
    tournament_id: str,
    service: MatchService = Depends(get_match_service)
):
    """
    Get matches by tournament.
    Mirrors GET /api/matches/tournament/{tournamentId}
    """
    matches = await service.get_matches_by_tournament(tournament_id)
    return matches


@router.put("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_match(
    match_id: str,
    match: MatchDTO,
    service: MatchService = Depends(get_match_service)
):
    """
    Update match.
    Mirrors PUT /api/matches/{id}
    """
    await service.update_match(match_id, match)
    return None


@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_match(
    match_id: str,
    service: MatchService = Depends(get_match_service)
):
    """
    Delete match.
    Mirrors DELETE /api/matches/{id}
    """
    await service.delete_match(match_id)
    return None


@router.post("/{match_id}/score", status_code=status.HTTP_204_NO_CONTENT)
async def update_score(
    match_id: str,
    score: ScoreUpdateDTO,
    service: MatchService = Depends(get_match_service)
):
    """
    Update match score.
    Mirrors POST /api/matches/{id}/score
    """
    await service.update_match_score(match_id, score)
    return None


@router.post("/{match_id}/ball", status_code=status.HTTP_204_NO_CONTENT)
async def add_ball_by_ball(
    match_id: str,
    ball: BallByBallDTO,
    service: MatchService = Depends(get_match_service)
):
    """
    Add ball-by-ball entry.
    Mirrors POST /api/matches/{id}/ball
    """
    await service.add_ball_by_ball(match_id, ball)
    return None

