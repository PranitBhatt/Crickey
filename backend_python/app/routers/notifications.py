"""
Notifications router - mirrors NotificationsController.cs
"""
from fastapi import APIRouter, Depends, status
from app.schemas.notification import SendNotificationRequest, SendNotificationToTeamRequest
from app.services.notification_service import NotificationService
from app.database import get_db
from google.cloud import firestore

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


def get_notification_service(db: firestore.Client = Depends(get_db)) -> NotificationService:
    """Dependency injection for NotificationService"""
    from app.repositories.firestore_repository import FirestoreRepository
    firestore_repo = FirestoreRepository(db)
    return NotificationService(firestore_repo)


@router.post("/send", status_code=status.HTTP_204_NO_CONTENT)
async def send_notification(
    request: SendNotificationRequest,
    service: NotificationService = Depends(get_notification_service)
):
    """
    Send FCM notification.
    Mirrors POST /api/notifications/send
    """
    await service.send_notification(
        request.token,
        request.title,
        request.body,
        request.data
    )
    return None


@router.post("/send-to-team", status_code=status.HTTP_204_NO_CONTENT)
async def send_notification_to_team(
    request: SendNotificationToTeamRequest,
    service: NotificationService = Depends(get_notification_service)
):
    """
    Send FCM notification to team.
    Mirrors POST /api/notifications/send-to-team
    """
    await service.send_notification_to_team(
        request.teamId,
        request.title,
        request.body,
        request.data
    )
    return None

