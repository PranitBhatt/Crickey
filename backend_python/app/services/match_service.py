"""
Match service - mirrors IMatchService
"""
from app.repositories.match_repository import MatchRepository
from app.schemas.match import MatchDTO, ScoreUpdateDTO, BallByBallDTO
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class MatchService:
    """
    Service for match operations.
    Mirrors the .NET MatchService.
    """
    
    def __init__(self, match_repo: MatchRepository):
        self.match_repo = match_repo
    
    async def create_match(self, match: MatchDTO) -> str:
        """Create match - mirrors CreateMatchAsync"""
        match_dict = match.model_dump(exclude={"id"})
        return await self.match_repo.create(match_dict)
    
    async def get_match(self, match_id: str) -> Optional[MatchDTO]:
        """Get match by ID - mirrors GetMatchAsync"""
        entity = await self.match_repo.get_by_id(match_id)
        if not entity:
            return None
        return MatchDTO(**entity)
    
    async def get_matches_by_tournament(self, tournament_id: str) -> list[MatchDTO]:
        """Get matches by tournament - mirrors GetMatchesByTournamentAsync"""
        entities = await self.match_repo.get_by_tournament_id(tournament_id)
        return [MatchDTO(**entity) for entity in entities]
    
    async def update_match(self, match_id: str, match: MatchDTO) -> None:
        """Update match - mirrors UpdateMatchAsync"""
        match_dict = match.model_dump(exclude={"id"})
        match_dict["id"] = match_id
        await self.match_repo.update(match_dict)
    
    async def delete_match(self, match_id: str) -> None:
        """Delete match - mirrors DeleteMatchAsync"""
        await self.match_repo.delete(match_id)
    
    async def update_match_score(self, match_id: str, score: ScoreUpdateDTO) -> None:
        """Update match score - mirrors UpdateMatchScoreAsync"""
        await self.match_repo.update_score(
            match_id,
            score.teamId,
            score.runs,
            score.wickets,
            score.overs
        )
    
    async def add_ball_by_ball(self, match_id: str, ball: BallByBallDTO) -> None:
        """Add ball-by-ball entry - mirrors AddBallByBallAsync"""
        ball_dict = ball.model_dump()
        await self.match_repo.add_ball_by_ball(match_id, ball_dict)

