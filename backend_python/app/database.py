"""
Firebase Firestore database initialization.
Mirrors the .NET Infrastructure/DependencyInjection.cs Firebase setup.
"""
import firebase_admin
from firebase_admin import credentials, firestore
from app.config import settings
import os
import logging

logger = logging.getLogger(__name__)

# Global Firestore client
_db: firestore.Client | None = None


def initialize_firebase() -> None:
    """
    Initialize Firebase Admin SDK.
    Mirrors the .NET Infrastructure/DependencyInjection.cs Firebase initialization.
    """
    global _db
    
    if firebase_admin._apps:
        # Already initialized
        logger.info("Firebase Admin already initialized")
        _db = firestore.client()
        return
    
    project_id = settings.FIREBASE_PROJECT_ID
    credentials_path = settings.FIREBASE_CREDENTIALS_PATH
    
    try:
        if credentials_path and os.path.exists(credentials_path):
            # Use service account key file (matches .NET behavior)
            cred = credentials.Certificate(credentials_path)
            firebase_admin.initialize_app(cred, {
                'projectId': project_id
            })
            logger.info(f"Firebase initialized with credentials from {credentials_path}")
        elif project_id:
            # Use default credentials (for cloud deployment)
            firebase_admin.initialize_app(options={
                'projectId': project_id
            })
            logger.info(f"Firebase initialized with default credentials for project {project_id}")
        else:
            raise ValueError("Firebase configuration missing: need FIREBASE_PROJECT_ID or FIREBASE_CREDENTIALS_PATH")
        
        _db = firestore.client()
        logger.info("Firestore client initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {e}")
        raise


def get_db() -> firestore.Client:
    """
    Get Firestore client instance.
    Dependency injection for FastAPI routes.
    """
    if _db is None:
        initialize_firebase()
    return _db

