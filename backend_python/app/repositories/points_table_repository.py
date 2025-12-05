"""
Points Table repository - mirrors IPointsTableRepository
"""
from google.cloud import firestore
from typing import Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PointsTableRepository:
    """
    Repository for points table operations.
    Mirrors the .NET PointsTableRepository.
    """
    
    COLLECTION = "pointsTable"
    
    def __init__(self, db: firestore.Client):
        self.db = db
    
    def _convert_to_dict(self, points_table: dict) -> dict:
        """Convert points table entity to Firestore dictionary"""
        entries = []
        for entry in points_table.get("entries", []):
            entries.append({
                "teamId": entry["teamId"],
                "teamName": entry["teamName"],
                "group": entry["group"],
                "played": entry["played"],
                "won": entry["won"],
                "lost": entry["lost"],
                "tied": entry["tied"],
                "points": entry["points"],
                "netRunRate": entry["netRunRate"],
                "runsFor": entry["runsFor"],
                "runsAgainst": entry["runsAgainst"],
                "oversFor": entry["oversFor"],
                "oversAgainst": entry["oversAgainst"]
            })
        
        return {
            "tournamentId": points_table["tournamentId"],
            "group": points_table["group"],
            "entries": entries,
            "lastUpdated": points_table.get("lastUpdated", datetime.utcnow())
        }
    
    def _convert_from_dict(self, data: dict) -> dict:
        """Convert Firestore document to points table entity"""
        entries = []
        for entry_data in data.get("entries", []):
            entries.append({
                "teamId": entry_data.get("teamId", ""),
                "teamName": entry_data.get("teamName", ""),
                "group": entry_data.get("group", ""),
                "played": entry_data.get("played", 0),
                "won": entry_data.get("won", 0),
                "lost": entry_data.get("lost", 0),
                "tied": entry_data.get("tied", 0),
                "points": entry_data.get("points", 0),
                "netRunRate": entry_data.get("netRunRate", 0.0),
                "runsFor": entry_data.get("runsFor", 0),
                "runsAgainst": entry_data.get("runsAgainst", 0),
                "oversFor": entry_data.get("oversFor", 0.0),
                "oversAgainst": entry_data.get("oversAgainst", 0.0)
            })
        
        last_updated = data.get("lastUpdated")
        if hasattr(last_updated, 'timestamp'):
            last_updated = datetime.fromtimestamp(last_updated.timestamp())
        elif not isinstance(last_updated, datetime):
            last_updated = datetime.utcnow()
        
        return {
            "tournamentId": data.get("tournamentId", ""),
            "group": data.get("group", ""),
            "entries": entries,
            "lastUpdated": last_updated
        }
    
    async def upsert(self, tournament_id: str, group: str, points_table: dict) -> None:
        """Upsert points table - mirrors UpsertAsync"""
        document_id = f"{tournament_id}_{group}"
        doc_data = self._convert_to_dict(points_table)
        doc_ref = self.db.collection(self.COLLECTION).document(document_id)
        doc_ref.set(doc_data)
    
    async def get(self, tournament_id: str, group: str) -> Optional[dict]:
        """Get points table - mirrors GetAsync"""
        document_id = f"{tournament_id}_{group}"
        doc_ref = self.db.collection(self.COLLECTION).document(document_id)
        doc_snapshot = doc_ref.get()
        
        if not doc_snapshot.exists:
            return None
        
        return self._convert_from_dict(doc_snapshot.to_dict())
    
    async def get_all(self, tournament_id: str) -> list[dict]:
        """Get all points tables for tournament - mirrors GetAllAsync"""
        docs = self.db.collection(self.COLLECTION).where("tournamentId", "==", tournament_id).stream()
        results = []
        for doc in docs:
            results.append(self._convert_from_dict(doc.to_dict()))
        return results

