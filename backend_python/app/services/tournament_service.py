"""
Tournament service for business logic.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.tournament import Tournament
from app.schemas.tournament import TournamentCreate, TournamentUpdate
from typing import List, Optional


class TournamentService:
    """Service for tournament operations"""
    
    @staticmethod
    async def create_tournament(db: AsyncSession, tournament_data: TournamentCreate, user_id: int) -> Tournament:
        """Create a new tournament"""
        tournament = Tournament(
            name=tournament_data.name,
            start_date=tournament_data.start_date,
            end_date=tournament_data.end_date,
            location=tournament_data.location,
            overs_group=tournament_data.overs_group,
            overs_knockout=tournament_data.overs_knockout,
            groups=tournament_data.groups,
            created_by=user_id
        )
        db.add(tournament)
        await db.commit()
        await db.refresh(tournament)
        return tournament
    
    @staticmethod
    async def get_tournament(db: AsyncSession, tournament_id: int) -> Optional[Tournament]:
        """Get tournament by ID"""
        result = await db.execute(select(Tournament).where(Tournament.id == tournament_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all_tournaments(db: AsyncSession) -> List[Tournament]:
        """Get all tournaments"""
        result = await db.execute(select(Tournament).order_by(Tournament.start_date.desc()))
        return list(result.scalars().all())
    
    @staticmethod
    async def update_tournament(
        db: AsyncSession,
        tournament_id: int,
        tournament_data: TournamentUpdate
    ) -> Optional[Tournament]:
        """Update tournament"""
        tournament = await TournamentService.get_tournament(db, tournament_id)
        if not tournament:
            return None
        
        update_data = tournament_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(tournament, field, value)
        
        await db.commit()
        await db.refresh(tournament)
        return tournament
    
    @staticmethod
    async def delete_tournament(db: AsyncSession, tournament_id: int) -> bool:
        """Delete tournament"""
        tournament = await TournamentService.get_tournament(db, tournament_id)
        if not tournament:
            return False
        
        await db.delete(tournament)
        await db.commit()
        return True

