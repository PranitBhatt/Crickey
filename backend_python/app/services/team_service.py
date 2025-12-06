"""
Team service for business logic.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.team import Team, Player
from app.models.tournament import Tournament
from app.schemas.team import TeamCreate, TeamUpdate
from typing import List, Optional


class TeamService:
    """Service for team operations"""
    
    @staticmethod
    async def create_team(db: AsyncSession, team_data: TeamCreate) -> Team:
        """Create a new team with players"""
        team = Team(
            tournament_id=team_data.tournament_id,
            name=team_data.name,
            group=team_data.group,
            captain_name=team_data.captain_name,
            captain_uid=team_data.captain_uid,
            logo_url=team_data.logo_url
        )
        db.add(team)
        await db.flush()  # Get team.id
        
        # Add players
        for player_data in team_data.players:
            player = Player(
                team_id=team.id,
                name=player_data.name,
                role=player_data.role,
                is_substitute=player_data.is_substitute
            )
            db.add(player)
        
        await db.commit()
        await db.refresh(team)
        return team
    
    @staticmethod
    async def get_team(db: AsyncSession, team_id: int) -> Optional[Team]:
        """Get team by ID"""
        result = await db.execute(select(Team).where(Team.id == team_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_teams_by_tournament(db: AsyncSession, tournament_id: int) -> List[Team]:
        """Get all teams for a tournament"""
        result = await db.execute(
            select(Team)
            .where(Team.tournament_id == tournament_id)
            .order_by(Team.group, Team.name)
        )
        return list(result.scalars().all())
    
    @staticmethod
    async def update_team(db: AsyncSession, team_id: int, team_data: TeamUpdate) -> Optional[Team]:
        """Update team"""
        team = await TeamService.get_team(db, team_id)
        if not team:
            return None
        
        update_data = team_data.model_dump(exclude_unset=True, exclude={"players"})
        for field, value in update_data.items():
            setattr(team, field, value)
        
        # Update players if provided
        if team_data.players is not None:
            # Delete existing players
            await db.execute(select(Player).where(Player.team_id == team_id))
            result = await db.execute(select(Player).where(Player.team_id == team_id))
            existing_players = result.scalars().all()
            for player in existing_players:
                await db.delete(player)
            
            # Add new players
            for player_data in team_data.players:
                player = Player(
                    team_id=team.id,
                    name=player_data.name,
                    role=player_data.role,
                    is_substitute=player_data.is_substitute
                )
                db.add(player)
        
        await db.commit()
        await db.refresh(team)
        return team
    
    @staticmethod
    async def delete_team(db: AsyncSession, team_id: int) -> bool:
        """Delete team"""
        team = await TeamService.get_team(db, team_id)
        if not team:
            return False
        
        await db.delete(team)
        await db.commit()
        return True

