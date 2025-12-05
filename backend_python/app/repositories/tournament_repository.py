"""
Tournament repository - mirrors ITournamentRepository
"""
from google.cloud import firestore
from typing import Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class TournamentRepository:
    """
    Repository for tournament operations.
    Mirrors the .NET TournamentRepository.
    """
    
    COLLECTION = "tournaments"
    
    def __init__(self, db: firestore.Client):
        self.db = db
        self.firestore_repo = None  # Will be injected
    
    def _convert_to_dict(self, tournament: dict) -> dict:
        """Convert tournament entity to Firestore dictionary"""
        return {
            "name": tournament["name"],
            "startDate": tournament.get("startDate"),
            "endDate": tournament.get("endDate"),
            "location": tournament["location"],
            "oversGroup": tournament["oversGroup"],
            "oversKnockout": tournament["oversKnockout"],
            "groups": tournament["groups"],
            "status": tournament["status"],
            "createdBy": tournament["createdBy"]
        }
    
    def _convert_from_dict(self, doc_id: str, data: dict) -> dict:
        """Convert Firestore document to tournament entity"""
        # Handle Firestore timestamps
        start_date = data.get("startDate")
        end_date = data.get("endDate")
        
        if hasattr(start_date, 'timestamp'):
            start_date = datetime.fromtimestamp(start_date.timestamp())
        elif isinstance(start_date, datetime):
            pass  # Already datetime
        else:
            start_date = datetime.now()
        
        if hasattr(end_date, 'timestamp'):
            end_date = datetime.fromtimestamp(end_date.timestamp())
        elif isinstance(end_date, datetime):
            pass  # Already datetime
        else:
            end_date = datetime.now()
        
        return {
            "id": doc_id,
            "name": data.get("name", ""),
            "startDate": start_date,
            "endDate": end_date,
            "location": data.get("location", ""),
            "oversGroup": data.get("oversGroup", 0),
            "oversKnockout": data.get("oversKnockout", 0),
            "groups": data.get("groups", []),
            "status": data.get("status", "upcoming"),
            "createdBy": data.get("createdBy", "")
        }
    
    async def create(self, tournament: dict) -> str:
        """Create a tournament - mirrors CreateAsync"""
        doc_data = {
            "name": tournament["name"],
            "startDate": tournament["startDate"],
            "endDate": tournament["endDate"],
            "location": tournament["location"],
            "oversGroup": tournament["oversGroup"],
            "oversKnockout": tournament["oversKnockout"],
            "groups": tournament["groups"],
            "status": tournament["status"],
            "createdBy": tournament["createdBy"]
        }
        
        doc_ref = self.db.collection(self.COLLECTION).document()
        doc_ref.set(doc_data)
        return doc_ref.id
    
    async def get_by_id(self, tournament_id: str) -> Optional[dict]:
        """Get tournament by ID - mirrors GetByIdAsync"""
        doc_ref = self.db.collection(self.COLLECTION).document(tournament_id)
        doc_snapshot = doc_ref.get()
        
        if not doc_snapshot.exists:
            return None
        
        return self._convert_from_dict(doc_snapshot.id, doc_snapshot.to_dict())
    
    async def get_all(self) -> list[dict]:
        """Get all tournaments - mirrors GetAllAsync"""
        docs = self.db.collection(self.COLLECTION).stream()
        results = []
        for doc in docs:
            results.append(self._convert_from_dict(doc.id, doc.to_dict()))
        return results
    
    async def update(self, tournament: dict) -> None:
        """Update tournament - mirrors UpdateAsync"""
        tournament_id = tournament["id"]
        doc_data = self._convert_to_dict(tournament)
        doc_ref = self.db.collection(self.COLLECTION).document(tournament_id)
        doc_ref.set(doc_data, merge=True)
    
    async def delete(self, tournament_id: str) -> None:
        """Delete tournament - mirrors DeleteAsync"""
        doc_ref = self.db.collection(self.COLLECTION).document(tournament_id)
        doc_ref.delete()

