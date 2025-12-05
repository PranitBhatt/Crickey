"""
Notification service - mirrors INotificationService
"""
from app.repositories.firestore_repository import FirestoreRepository
from app.config import settings
from firebase_admin import messaging
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Service for FCM notification operations.
    Mirrors the .NET NotificationService.
    Uses Firebase Admin SDK for FCM (more aligned with .NET FCM.Net).
    """
    
    def __init__(self, firestore_repo: FirestoreRepository):
        self.firestore_repo = firestore_repo
    
    async def send_notification(
        self,
        token: str,
        title: str,
        body: str,
        data: Optional[dict[str, str]] = None
    ) -> None:
        """
        Send FCM notification to a token.
        Mirrors SendNotificationAsync.
        """
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=data or {},
                token=token
            )
            
            response = messaging.send(message)
            logger.info(f"Notification sent successfully: {response}")
        except Exception as e:
            # Log error but don't throw (matches .NET behavior)
            logger.error(f"Error sending notification: {e}")
    
    async def send_notification_to_team(
        self,
        team_id: str,
        title: str,
        body: str,
        data: Optional[dict[str, str]] = None
    ) -> None:
        """
        Send FCM notification to team captain.
        Mirrors SendNotificationToTeamAsync.
        """
        try:
            # Get team captain's FCM token from users collection
            team = await self.firestore_repo.get_document("teams", team_id)
            if not team or "captainUid" not in team:
                logger.warning(f"Team {team_id} not found or missing captainUid")
                return
            
            captain_uid = team["captainUid"]
            if not captain_uid:
                logger.warning(f"Team {team_id} has empty captainUid")
                return
            
            user = await self.firestore_repo.get_document("users", captain_uid)
            if not user or "fcmToken" not in user:
                logger.warning(f"User {captain_uid} not found or missing fcmToken")
                return
            
            token = user["fcmToken"]
            if token:
                await self.send_notification(token, title, body, data)
        except Exception as e:
            logger.error(f"Error sending notification to team {team_id}: {e}")

