"""
Points Table service - mirrors IPointsTableService
"""
from app.repositories.points_table_repository import PointsTableRepository
from app.repositories.match_repository import MatchRepository
from app.repositories.team_repository import TeamRepository
from app.schemas.points_table import PointsTableDTO, PointsTableEntryDTO
from typing import Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PointsTableService:
    """
    Service for points table operations.
    Mirrors the .NET PointsTableService.
    """
    
    def __init__(
        self,
        points_table_repo: PointsTableRepository,
        match_repo: MatchRepository,
        team_repo: TeamRepository
    ):
        self.points_table_repo = points_table_repo
        self.match_repo = match_repo
        self.team_repo = team_repo
    
    def _calculate_net_run_rate(
        self,
        runs_for: int,
        runs_against: int,
        overs_for: float,
        overs_against: float
    ) -> float:
        """
        Calculate Net Run Rate.
        Mirrors the .NET CalculateNetRunRate method.
        """
        if overs_for == 0 and overs_against == 0:
            return 0.0
        if overs_for == 0:
            return -999.0
        if overs_against == 0:
            return 999.0
        
        run_rate_for = runs_for / overs_for
        run_rate_against = runs_against / overs_against
        return run_rate_for - run_rate_against
    
    async def update_points_table(self, tournament_id: str) -> None:
        """Update points table - mirrors UpdatePointsTableAsync"""
        teams = await self.team_repo.get_by_tournament_id(tournament_id)
        matches = await self.match_repo.get_by_tournament_id(tournament_id)
        completed_matches = [m for m in matches if m.get("status") == "completed"]
        
        groups = list(set(team["group"] for team in teams))
        
        for group in groups:
            group_teams = [t for t in teams if t["group"] == group]
            group_matches = [m for m in completed_matches if m["group"] == group]
            
            entries = []
            
            for team in group_teams:
                team_matches = [
                    m for m in group_matches
                    if m["team1Id"] == team["id"] or m["team2Id"] == team["id"]
                ]
                
                played = len(team_matches)
                won = len([m for m in team_matches if m.get("winnerTeamId") == team["id"]])
                lost = len([
                    m for m in team_matches
                    if m.get("winnerTeamId") and m.get("winnerTeamId") != team["id"]
                ])
                tied = len([m for m in team_matches if not m.get("winnerTeamId")])
                
                runs_for = 0
                runs_against = 0
                overs_for = 0.0
                overs_against = 0.0
                
                for match in team_matches:
                    if not match.get("scores"):
                        continue
                    
                    is_team1 = match["team1Id"] == team["id"]
                    team_score = match["scores"].get(match["team1Id"] if is_team1 else match["team2Id"])
                    opponent_score = match["scores"].get(match["team2Id"] if is_team1 else match["team1Id"])
                    
                    if team_score:
                        runs_for += team_score["runs"]
                        overs_for += team_score["overs"]
                    
                    if opponent_score:
                        runs_against += opponent_score["runs"]
                        overs_against += opponent_score["overs"]
                
                net_run_rate = self._calculate_net_run_rate(
                    runs_for, runs_against, overs_for, overs_against
                )
                points = (won * 2) + tied
                
                entries.append({
                    "teamId": team["id"],
                    "teamName": team["name"],
                    "group": group,
                    "played": played,
                    "won": won,
                    "lost": lost,
                    "tied": tied,
                    "points": points,
                    "netRunRate": net_run_rate,
                    "runsFor": runs_for,
                    "runsAgainst": runs_against,
                    "oversFor": overs_for,
                    "oversAgainst": overs_against
                })
            
            points_table = {
                "tournamentId": tournament_id,
                "group": group,
                "entries": entries,
                "lastUpdated": datetime.utcnow()
            }
            
            await self.points_table_repo.upsert(tournament_id, group, points_table)
    
    async def get_points_table(
        self,
        tournament_id: str,
        group: str
    ) -> Optional[PointsTableDTO]:
        """Get points table - mirrors GetPointsTableAsync"""
        entity = await self.points_table_repo.get(tournament_id, group)
        if not entity:
            return None
        return PointsTableDTO(**entity)
    
    async def get_all_points_tables(self, tournament_id: str) -> list[PointsTableDTO]:
        """Get all points tables - mirrors GetAllPointsTablesAsync"""
        entities = await self.points_table_repo.get_all(tournament_id)
        return [PointsTableDTO(**entity) for entity in entities]

