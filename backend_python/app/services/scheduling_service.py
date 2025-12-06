"""
Scheduling service for auto-generating match schedules.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tournament import Tournament
from app.models.team import Team
from app.models.match import Match, MatchStatus
from app.services.team_service import TeamService
from app.services.match_service import MatchService
from datetime import datetime, timedelta
from typing import List
import itertools


class SchedulingService:
    """Service for match scheduling operations"""
    
    @staticmethod
    async def generate_group_stage_schedule(
        db: AsyncSession,
        tournament_id: int,
        start_datetime: datetime
    ) -> List[Match]:
        """
        Generate group stage matches for a tournament.
        Format: 12 teams, 2 groups (A & B), 6 teams each, each team plays 3 matches.
        """
        # Get tournament
        from app.services.tournament_service import TournamentService
        tournament = await TournamentService.get_tournament(db, tournament_id)
        if not tournament:
            raise ValueError("Tournament not found")
        
        # Get teams grouped by group
        teams = await TeamService.get_teams_by_tournament(db, tournament_id)
        teams_by_group = {"A": [], "B": []}
        
        for team in teams:
            teams_by_group[team.group.value].append(team)
        
        matches = []
        current_datetime = start_datetime
        match_number = 1
        
        # Generate matches for each group
        for group_name, group_teams in teams_by_group.items():
            if len(group_teams) != 6:
                continue
            
            # Generate all possible pairs (round-robin, but each team plays only 3 matches)
            # We'll create a schedule where each team plays 3 matches
            pairs = list(itertools.combinations(group_teams, 2))
            
            # Limit to ensure each team plays exactly 3 matches
            # Simple approach: first 9 matches (3 matches per team)
            team_match_count = {team.id: 0 for team in group_teams}
            selected_pairs = []
            
            for pair in pairs:
                team1, team2 = pair
                if team_match_count[team1.id] < 3 and team_match_count[team2.id] < 3:
                    selected_pairs.append(pair)
                    team_match_count[team1.id] += 1
                    team_match_count[team2.id] += 1
                    if len(selected_pairs) >= 9:  # 6 teams * 3 matches / 2 = 9 matches per group
                        break
            
            # Create matches
            for team1, team2 in selected_pairs:
                match = Match(
                    tournament_id=tournament_id,
                    group=group_name,
                    match_number=match_number,
                    team1_id=team1.id,
                    team2_id=team2.id,
                    date_time=current_datetime,
                    venue=tournament.location,
                    overs=tournament.overs_group,
                    status=MatchStatus.SCHEDULED
                )
                db.add(match)
                matches.append(match)
                match_number += 1
                # Add 30 minutes between matches
                current_datetime += timedelta(minutes=30)
        
        await db.commit()
        return matches
    
    @staticmethod
    async def generate_knockout_matches(
        db: AsyncSession,
        tournament_id: int,
        group_a_top2: List[int],  # Team IDs from group A
        group_b_top2: List[int],  # Team IDs from group B
        start_datetime: datetime
    ) -> List[Match]:
        """
        Generate semi-finals and final matches.
        Format: Semi1 (A1 vs B2), Semi2 (B1 vs A2), Final (Semi1 winner vs Semi2 winner)
        """
        from app.services.tournament_service import TournamentService
        tournament = await TournamentService.get_tournament(db, tournament_id)
        if not tournament:
            raise ValueError("Tournament not found")
        
        matches = []
        current_datetime = start_datetime
        
        # Get current max match number
        existing_matches = await MatchService.get_matches_by_tournament(db, tournament_id)
        match_number = max([m.match_number for m in existing_matches], default=0) + 1
        
        # Semi-final 1: A1 vs B2
        semi1 = Match(
            tournament_id=tournament_id,
            group="semi",
            match_number=match_number,
            team1_id=group_a_top2[0],
            team2_id=group_b_top2[1],
            date_time=current_datetime,
            venue=tournament.location,
            overs=tournament.overs_knockout,
            status=MatchStatus.SCHEDULED
        )
        db.add(semi1)
        matches.append(semi1)
        match_number += 1
        current_datetime += timedelta(hours=1)
        
        # Semi-final 2: B1 vs A2
        semi2 = Match(
            tournament_id=tournament_id,
            group="semi",
            match_number=match_number,
            team1_id=group_b_top2[0],
            team2_id=group_a_top2[1],
            date_time=current_datetime,
            venue=tournament.location,
            overs=tournament.overs_knockout,
            status=MatchStatus.SCHEDULED
        )
        db.add(semi2)
        matches.append(semi2)
        match_number += 1
        current_datetime += timedelta(hours=2)  # Gap before final
        
        # Final: Semi1 winner vs Semi2 winner
        # Note: winner_team_id will be set when semi-finals complete
        final = Match(
            tournament_id=tournament_id,
            group="final",
            match_number=match_number,
            team1_id=0,  # Will be updated after semi-finals
            team2_id=0,  # Will be updated after semi-finals
            date_time=current_datetime,
            venue=tournament.location,
            overs=tournament.overs_knockout,
            status=MatchStatus.SCHEDULED
        )
        db.add(final)
        matches.append(final)
        
        await db.commit()
        return matches

