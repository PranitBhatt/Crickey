"""
Points table service for calculating standings and NRR.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.points_table import PointsTable
from app.models.match import Match, MatchStatus
from app.models.team import Team
from app.schemas.points_table import PointsTableEntry
from typing import List, Dict
import math


class PointsService:
    """Service for points table operations"""
    
    @staticmethod
    async def calculate_points_table(
        db: AsyncSession,
        tournament_id: int,
        group: str
    ) -> PointsTable:
        """
        Calculate and update points table for a group.
        Points: Win=2, Loss=0, Tie=1
        NRR = (Runs For / Overs For) - (Runs Against / Overs Against)
        """
        # Get all teams in the group
        result = await db.execute(
            select(Team)
            .where(Team.tournament_id == tournament_id, Team.group == group)
        )
        teams = list(result.scalars().all())
        
        # Get all completed matches for this group
        result = await db.execute(
            select(Match)
            .where(
                Match.tournament_id == tournament_id,
                Match.group == group,
                Match.status == MatchStatus.COMPLETED
            )
        )
        matches = list(result.scalars().all())
        
        # Initialize team stats
        team_stats: Dict[int, Dict] = {}
        for team in teams:
            team_stats[team.id] = {
                "team_id": team.id,
                "team_name": team.name,
                "group": group,
                "played": 0,
                "won": 0,
                "lost": 0,
                "tied": 0,
                "points": 0,
                "runs_for": 0,
                "runs_against": 0,
                "overs_for": 0.0,
                "overs_against": 0.0,
            }
        
        # Process matches
        for match in matches:
            if not match.scores:
                continue
            
            team1_id = match.team1_id
            team2_id = match.team2_id
            
            score1 = match.scores.get(str(team1_id), {})
            score2 = match.scores.get(str(team2_id), {})
            
            runs1 = score1.get("runs", 0)
            runs2 = score2.get("runs", 0)
            overs1 = score1.get("overs", 0.0)
            overs2 = score2.get("overs", 0.0)
            
            # Update stats
            team_stats[team1_id]["played"] += 1
            team_stats[team2_id]["played"] += 1
            
            team_stats[team1_id]["runs_for"] += runs1
            team_stats[team1_id]["runs_against"] += runs2
            team_stats[team1_id]["overs_for"] += overs1
            team_stats[team1_id]["overs_against"] += overs2
            
            team_stats[team2_id]["runs_for"] += runs2
            team_stats[team2_id]["runs_against"] += runs1
            team_stats[team2_id]["overs_for"] += overs2
            team_stats[team2_id]["overs_against"] += overs1
            
            # Determine winner
            if runs1 > runs2:
                team_stats[team1_id]["won"] += 1
                team_stats[team1_id]["points"] += 2
                team_stats[team2_id]["lost"] += 1
            elif runs2 > runs1:
                team_stats[team2_id]["won"] += 1
                team_stats[team2_id]["points"] += 2
                team_stats[team1_id]["lost"] += 1
            else:
                team_stats[team1_id]["tied"] += 1
                team_stats[team1_id]["points"] += 1
                team_stats[team2_id]["tied"] += 1
                team_stats[team2_id]["points"] += 1
        
        # Calculate NRR
        entries = []
        for team_id, stats in team_stats.items():
            overs_for = stats["overs_for"] if stats["overs_for"] > 0 else 1.0
            overs_against = stats["overs_against"] if stats["overs_against"] > 0 else 1.0
            
            nrr = (stats["runs_for"] / overs_for) - (stats["runs_against"] / overs_against)
            
            entry = PointsTableEntry(
                team_id=stats["team_id"],
                team_name=stats["team_name"],
                group=stats["group"],
                played=stats["played"],
                won=stats["won"],
                lost=stats["lost"],
                tied=stats["tied"],
                points=stats["points"],
                net_run_rate=round(nrr, 3),
                runs_for=stats["runs_for"],
                runs_against=stats["runs_against"],
                overs_for=round(stats["overs_for"], 1),
                overs_against=round(stats["overs_against"], 1),
            )
            entries.append(entry)
        
        # Sort by points (desc), then NRR (desc)
        entries.sort(key=lambda x: (x.points, x.net_run_rate), reverse=True)
        
        # Get or create points table
        result = await db.execute(
            select(PointsTable)
            .where(PointsTable.tournament_id == tournament_id, PointsTable.group == group)
        )
        points_table = result.scalar_one_or_none()
        
        if not points_table:
            points_table = PointsTable(
                tournament_id=tournament_id,
                group=group,
                entries=[e.model_dump() for e in entries]
            )
            db.add(points_table)
        else:
            points_table.entries = [e.model_dump() for e in entries]
        
        await db.commit()
        await db.refresh(points_table)
        return points_table
    
    @staticmethod
    async def get_points_table(db: AsyncSession, tournament_id: int, group: str) -> PointsTable:
        """Get points table for a group"""
        result = await db.execute(
            select(PointsTable)
            .where(PointsTable.tournament_id == tournament_id, PointsTable.group == group)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all_points_tables(db: AsyncSession, tournament_id: int) -> List[PointsTable]:
        """Get all points tables for a tournament"""
        result = await db.execute(
            select(PointsTable)
            .where(PointsTable.tournament_id == tournament_id)
            .order_by(PointsTable.group)
        )
        return list(result.scalars().all())

