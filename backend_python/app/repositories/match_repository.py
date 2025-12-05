"""
Match repository - mirrors IMatchRepository
"""
from google.cloud import firestore
from typing import Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class MatchRepository:
    """
    Repository for match operations.
    Mirrors the .NET MatchRepository.
    """
    
    COLLECTION = "matches"
    
    def __init__(self, db: firestore.Client):
        self.db = db
    
    def _convert_to_dict(self, match: dict) -> dict:
        """Convert match entity to Firestore dictionary"""
        data = {
            "tournamentId": match["tournamentId"],
            "group": match["group"],
            "matchNumber": match["matchNumber"],
            "team1Id": match["team1Id"],
            "team2Id": match["team2Id"],
            "dateTime": match["dateTime"],
            "venue": match["venue"],
            "overs": match["overs"],
            "status": match["status"]
        }
        
        if match.get("winnerTeamId"):
            data["winnerTeamId"] = match["winnerTeamId"]
        
        if match.get("scores"):
            scores_dict = {}
            for team_id, score in match["scores"].items():
                scores_dict[team_id] = {
                    "runs": score["runs"],
                    "wickets": score["wickets"],
                    "overs": score["overs"]
                }
            data["scores"] = scores_dict
        
        return data
    
    def _convert_from_dict(self, doc_id: str, data: dict) -> dict:
        """Convert Firestore document to match entity"""
        # Handle Firestore timestamp
        date_time = data.get("dateTime")
        if hasattr(date_time, 'timestamp'):
            date_time = datetime.fromtimestamp(date_time.timestamp())
        elif not isinstance(date_time, datetime):
            date_time = datetime.now()
        
        scores = None
        if "scores" in data and data["scores"]:
            scores = {}
            for team_id, score_data in data["scores"].items():
                scores[team_id] = {
                    "runs": score_data.get("runs", 0),
                    "wickets": score_data.get("wickets", 0),
                    "overs": score_data.get("overs", 0.0)
                }
        
        return {
            "id": doc_id,
            "tournamentId": data.get("tournamentId", ""),
            "group": data.get("group", ""),
            "matchNumber": data.get("matchNumber", 0),
            "team1Id": data.get("team1Id", ""),
            "team2Id": data.get("team2Id", ""),
            "dateTime": date_time,
            "venue": data.get("venue", ""),
            "overs": data.get("overs", 0),
            "status": data.get("status", "scheduled"),
            "winnerTeamId": data.get("winnerTeamId"),
            "scores": scores
        }
    
    async def create(self, match: dict) -> str:
        """Create a match - mirrors CreateAsync"""
        doc_data = self._convert_to_dict(match)
        doc_ref = self.db.collection(self.COLLECTION).document()
        doc_ref.set(doc_data)
        return doc_ref.id
    
    async def get_by_id(self, match_id: str) -> Optional[dict]:
        """Get match by ID - mirrors GetByIdAsync"""
        doc_ref = self.db.collection(self.COLLECTION).document(match_id)
        doc_snapshot = doc_ref.get()
        
        if not doc_snapshot.exists:
            return None
        
        return self._convert_from_dict(doc_snapshot.id, doc_snapshot.to_dict())
    
    async def get_by_tournament_id(self, tournament_id: str) -> list[dict]:
        """Get matches by tournament ID - mirrors GetByTournamentIdAsync"""
        docs = self.db.collection(self.COLLECTION).where("tournamentId", "==", tournament_id).stream()
        results = []
        for doc in docs:
            results.append(self._convert_from_dict(doc.id, doc.to_dict()))
        return results
    
    async def update(self, match: dict) -> None:
        """Update match - mirrors UpdateAsync"""
        match_id = match["id"]
        doc_data = self._convert_to_dict(match)
        doc_ref = self.db.collection(self.COLLECTION).document(match_id)
        doc_ref.set(doc_data, merge=True)
    
    async def delete(self, match_id: str) -> None:
        """Delete match - mirrors DeleteAsync"""
        doc_ref = self.db.collection(self.COLLECTION).document(match_id)
        doc_ref.delete()
    
    async def update_score(
        self, 
        match_id: str, 
        team_id: str, 
        runs: int, 
        wickets: int, 
        overs: float
    ) -> None:
        """Update match score - mirrors UpdateScoreAsync"""
        match = await self.get_by_id(match_id)
        if not match:
            raise ValueError(f"Match {match_id} not found")
        
        if not match.get("scores"):
            match["scores"] = {}
        
        match["scores"][team_id] = {
            "runs": runs,
            "wickets": wickets,
            "overs": overs
        }
        
        await self.update(match)
    
    async def add_ball_by_ball(self, match_id: str, ball: dict) -> None:
        """Add ball-by-ball entry - mirrors AddBallByBallAsync"""
        from datetime import datetime
        
        ball_data = {
            "ballNumber": ball["ballNumber"],
            "overNumber": ball["overNumber"],
            "batsman": ball["batsman"],
            "bowler": ball["bowler"],
            "runs": ball["runs"],
            "isWicket": ball["isWicket"],
            "extras": ball["extras"],
            "timestamp": datetime.utcnow()
        }
        
        ball_by_ball_ref = self.db.collection(self.COLLECTION).document(match_id).collection("ballByBall")
        ball_by_ball_ref.add(ball_data)

