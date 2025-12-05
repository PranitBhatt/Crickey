"""
Tournament service - mirrors ITournamentService
"""
from app.repositories.tournament_repository import TournamentRepository
from app.schemas.tournament import TournamentDTO
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class TournamentService:
    """
    Service for tournament operations.
    Mirrors the .NET TournamentService.
    """
    
    def __init__(self, tournament_repo: TournamentRepository):
        self.tournament_repo = tournament_repo
    
    async def create_tournament(self, tournament: TournamentDTO) -> str:
        """Create tournament - mirrors CreateTournamentAsync"""
        tournament_dict = tournament.model_dump(exclude={"id"})
        return await self.tournament_repo.create(tournament_dict)
    
    async def get_tournament(self, tournament_id: str) -> Optional[TournamentDTO]:
        """Get tournament by ID - mirrors GetTournamentAsync"""
        entity = await self.tournament_repo.get_by_id(tournament_id)
        if not entity:
            return None
        return TournamentDTO(**entity)
    
    async def get_all_tournaments(self) -> list[TournamentDTO]:
        """Get all tournaments - mirrors GetAllTournamentsAsync"""
        entities = await self.tournament_repo.get_all()
        return [TournamentDTO(**entity) for entity in entities]
    
    async def update_tournament(self, tournament_id: str, tournament: TournamentDTO) -> None:
        """Update tournament - mirrors UpdateTournamentAsync"""
        tournament_dict = tournament.model_dump(exclude={"id"})
        tournament_dict["id"] = tournament_id
        await self.tournament_repo.update(tournament_dict)
    
    async def delete_tournament(self, tournament_id: str) -> None:
        """Delete tournament - mirrors DeleteTournamentAsync"""
        await self.tournament_repo.delete(tournament_id)

