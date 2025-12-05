"""
Team service - mirrors ITeamService
"""
from app.repositories.team_repository import TeamRepository
from app.schemas.team import TeamDTO
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class TeamService:
    """
    Service for team operations.
    Mirrors the .NET TeamService.
    """
    
    def __init__(self, team_repo: TeamRepository):
        self.team_repo = team_repo
    
    async def create_team(self, team: TeamDTO) -> str:
        """Create team - mirrors CreateTeamAsync"""
        team_dict = team.model_dump(exclude={"id"})
        return await self.team_repo.create(team_dict)
    
    async def get_team(self, team_id: str) -> Optional[TeamDTO]:
        """Get team by ID - mirrors GetTeamAsync"""
        entity = await self.team_repo.get_by_id(team_id)
        if not entity:
            return None
        return TeamDTO(**entity)
    
    async def get_teams_by_tournament(self, tournament_id: str) -> list[TeamDTO]:
        """Get teams by tournament - mirrors GetTeamsByTournamentAsync"""
        entities = await self.team_repo.get_by_tournament_id(tournament_id)
        return [TeamDTO(**entity) for entity in entities]
    
    async def update_team(self, team_id: str, team: TeamDTO) -> None:
        """Update team - mirrors UpdateTeamAsync"""
        team_dict = team.model_dump(exclude={"id"})
        team_dict["id"] = team_id
        await self.team_repo.update(team_dict)
    
    async def delete_team(self, team_id: str) -> None:
        """Delete team - mirrors DeleteTeamAsync"""
        await self.team_repo.delete(team_id)

