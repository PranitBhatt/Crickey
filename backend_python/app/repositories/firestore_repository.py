"""
Generic Firestore repository - mirrors IFirestoreRepository
"""
from google.cloud import firestore
from typing import TypeVar, Generic, Optional, Any
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')


class FirestoreRepository:
    """
    Generic Firestore repository for document operations.
    Mirrors the .NET IFirestoreRepository interface.
    """
    
    def __init__(self, db: firestore.Client):
        self.db = db
    
    async def get_document(self, collection: str, document_id: str) -> Optional[dict[str, Any]]:
        """
        Get a single document by ID.
        Mirrors GetDocumentAsync<T>.
        """
        try:
            doc_ref = self.db.collection(collection).document(document_id)
            doc_snapshot = doc_ref.get()
            
            if not doc_snapshot.exists:
                return None
            
            data = doc_snapshot.to_dict()
            if data:
                data['id'] = doc_snapshot.id
            return data
        except Exception as e:
            logger.error(f"Error getting document {document_id} from {collection}: {e}")
            raise
    
    async def create_document(
        self, 
        collection: str, 
        document: dict[str, Any], 
        document_id: Optional[str] = None
    ) -> str:
        """
        Create a document in a collection.
        Mirrors CreateDocumentAsync<T>.
        """
        try:
            collection_ref = self.db.collection(collection)
            
            # Remove 'id' from document if present (Firestore manages IDs)
            doc_data = {k: v for k, v in document.items() if k != 'id'}
            
            if document_id:
                doc_ref = collection_ref.document(document_id)
                doc_ref.set(doc_data)
                return document_id
            else:
                # Auto-generate ID
                doc_ref = collection_ref.document()
                doc_ref.set(doc_data)
                return doc_ref.id
        except Exception as e:
            logger.error(f"Error creating document in {collection}: {e}")
            raise
    
    async def update_document(
        self, 
        collection: str, 
        document_id: str, 
        document: dict[str, Any]
    ) -> None:
        """
        Update a document (merge with existing).
        Mirrors UpdateDocumentAsync<T>.
        """
        try:
            doc_ref = self.db.collection(collection).document(document_id)
            # Remove 'id' from document if present
            doc_data = {k: v for k, v in document.items() if k != 'id'}
            doc_ref.set(doc_data, merge=True)
        except Exception as e:
            logger.error(f"Error updating document {document_id} in {collection}: {e}")
            raise
    
    async def delete_document(self, collection: str, document_id: str) -> None:
        """
        Delete a document.
        Mirrors DeleteDocumentAsync.
        """
        try:
            doc_ref = self.db.collection(collection).document(document_id)
            doc_ref.delete()
        except Exception as e:
            logger.error(f"Error deleting document {document_id} from {collection}: {e}")
            raise
    
    async def get_documents(
        self, 
        collection: str, 
        field: Optional[str] = None, 
        value: Optional[Any] = None
    ) -> list[dict[str, Any]]:
        """
        Get multiple documents, optionally filtered by field.
        Mirrors GetDocumentsAsync<T>.
        """
        try:
            query = self.db.collection(collection)
            
            if field and value is not None:
                query = query.where(field, "==", value)
            
            docs = query.stream()
            results = []
            for doc in docs:
                data = doc.to_dict()
                if data:
                    data['id'] = doc.id
                results.append(data)
            
            return results
        except Exception as e:
            logger.error(f"Error getting documents from {collection}: {e}")
            raise

