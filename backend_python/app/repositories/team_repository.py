"""
Team repository - mirrors ITeamRepository
"""
from google.cloud import firestore
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class TeamRepository:
    """
    Repository for team operations.
    Mirrors the .NET TeamRepository.
    """
    
    COLLECTION = "teams"
    
    def __init__(self, db: firestore.Client):
        self.db = db
    
    def _convert_to_dict(self, team: dict) -> dict:
        """Convert team entity to Firestore dictionary"""
        data = {
            "tournamentId": team["tournamentId"],
            "name": team["name"],
            "group": team["group"],
            "captainName": team["captainName"],
            "captainUid": team["captainUid"],
            "logoUrl": team.get("logoUrl", ""),
            "players": [
                {"name": p["name"], "role": p["role"]} 
                for p in team.get("players", [])
            ]
        }
        
        if team.get("substitute"):
            data["substitute"] = {
                "name": team["substitute"]["name"],
                "role": team["substitute"]["role"]
            }
        
        return data
    
    def _convert_from_dict(self, doc_id: str, data: dict) -> dict:
        """Convert Firestore document to team entity"""
        players = []
        if "players" in data and data["players"]:
            players = [
                {"name": p.get("name", ""), "role": p.get("role", "")}
                for p in data["players"]
            ]
        
        substitute = None
        if "substitute" in data and data["substitute"]:
            sub_data = data["substitute"]
            substitute = {
                "name": sub_data.get("name", ""),
                "role": sub_data.get("role", "")
            }
        
        return {
            "id": doc_id,
            "tournamentId": data.get("tournamentId", ""),
            "name": data.get("name", ""),
            "group": data.get("group", ""),
            "captainName": data.get("captainName", ""),
            "captainUid": data.get("captainUid", ""),
            "logoUrl": data.get("logoUrl", ""),
            "players": players,
            "substitute": substitute
        }
    
    async def create(self, team: dict) -> str:
        """Create a team - mirrors CreateAsync"""
        doc_data = self._convert_to_dict(team)
        doc_ref = self.db.collection(self.COLLECTION).document()
        doc_ref.set(doc_data)
        return doc_ref.id
    
    async def get_by_id(self, team_id: str) -> Optional[dict]:
        """Get team by ID - mirrors GetByIdAsync"""
        doc_ref = self.db.collection(self.COLLECTION).document(team_id)
        doc_snapshot = doc_ref.get()
        
        if not doc_snapshot.exists:
            return None
        
        return self._convert_from_dict(doc_snapshot.id, doc_snapshot.to_dict())
    
    async def get_by_tournament_id(self, tournament_id: str) -> list[dict]:
        """Get teams by tournament ID - mirrors GetByTournamentIdAsync"""
        docs = self.db.collection(self.COLLECTION).where("tournamentId", "==", tournament_id).stream()
        results = []
        for doc in docs:
            results.append(self._convert_from_dict(doc.id, doc.to_dict()))
        return results
    
    async def update(self, team: dict) -> None:
        """Update team - mirrors UpdateAsync"""
        team_id = team["id"]
        doc_data = self._convert_to_dict(team)
        doc_ref = self.db.collection(self.COLLECTION).document(team_id)
        doc_ref.set(doc_data, merge=True)
    
    async def delete(self, team_id: str) -> None:
        """Delete team - mirrors DeleteAsync"""
        doc_ref = self.db.collection(self.COLLECTION).document(team_id)
        doc_ref.delete()

