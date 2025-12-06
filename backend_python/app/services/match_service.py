"""
Match service for business logic.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.match import Match, Ball
from app.schemas.match import MatchCreate, MatchUpdate, BallCreate, ScoreUpdate
from typing import List, Optional, Dict


class MatchService:
    """Service for match operations"""
    
    @staticmethod
    async def create_match(db: AsyncSession, match_data: MatchCreate) -> Match:
        """Create a new match"""
        match = Match(
            tournament_id=match_data.tournament_id,
            group=match_data.group,
            match_number=match_data.match_number,
            team1_id=match_data.team1_id,
            team2_id=match_data.team2_id,
            date_time=match_data.date_time,
            venue=match_data.venue,
            overs=match_data.overs,
            status=match_data.status
        )
        db.add(match)
        await db.commit()
        await db.refresh(match)
        return match
    
    @staticmethod
    async def get_match(db: AsyncSession, match_id: int) -> Optional[Match]:
        """Get match by ID"""
        result = await db.execute(select(Match).where(Match.id == match_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_matches_by_tournament(db: AsyncSession, tournament_id: int) -> List[Match]:
        """Get all matches for a tournament"""
        result = await db.execute(
            select(Match)
            .where(Match.tournament_id == tournament_id)
            .order_by(Match.match_number)
        )
        return list(result.scalars().all())
    
    @staticmethod
    async def update_match(db: AsyncSession, match_id: int, match_data: MatchUpdate) -> Optional[Match]:
        """Update match"""
        match = await MatchService.get_match(db, match_id)
        if not match:
            return None
        
        update_data = match_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(match, field, value)
        
        await db.commit()
        await db.refresh(match)
        return match
    
    @staticmethod
    async def update_score(db: AsyncSession, match_id: int, score_data: ScoreUpdate) -> Optional[Match]:
        """Update match score"""
        match = await MatchService.get_match(db, match_id)
        if not match:
            return None
        
        if not match.scores:
            match.scores = {}
        
        match.scores[str(score_data.team_id)] = {
            "runs": score_data.runs,
            "wickets": score_data.wickets,
            "overs": score_data.overs
        }
        
        await db.commit()
        await db.refresh(match)
        return match
    
    @staticmethod
    async def add_ball(db: AsyncSession, match_id: int, ball_data: BallCreate) -> Ball:
        """Add ball-by-ball entry"""
        ball = Ball(
            match_id=match_id,
            over_number=ball_data.over_number,
            ball_number=ball_data.ball_number,
            batsman=ball_data.batsman,
            bowler=ball_data.bowler,
            runs=ball_data.runs,
            is_wicket=ball_data.is_wicket,
            extras=ball_data.extras
        )
        db.add(ball)
        await db.commit()
        await db.refresh(ball)
        return ball
    
    @staticmethod
    async def get_balls_by_match(db: AsyncSession, match_id: int) -> List[Ball]:
        """Get all balls for a match"""
        result = await db.execute(
            select(Ball)
            .where(Ball.match_id == match_id)
            .order_by(Ball.over_number, Ball.ball_number)
        )
        return list(result.scalars().all())
    
    @staticmethod
    async def delete_match(db: AsyncSession, match_id: int) -> bool:
        """Delete match"""
        match = await MatchService.get_match(db, match_id)
        if not match:
            return False
        
        await db.delete(match)
        await db.commit()
        return True

