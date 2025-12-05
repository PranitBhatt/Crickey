"""
Notification DTOs - mirrors NotificationsController request models
"""
from pydantic import BaseModel, Field
from typing import Optional


class SendNotificationRequest(BaseModel):
    """Send notification request"""
    token: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    body: str = Field(..., min_length=1)
    data: Optional[dict[str, str]] = None


class SendNotificationToTeamRequest(BaseModel):
    """Send notification to team request"""
    teamId: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    body: str = Field(..., min_length=1)
    data: Optional[dict[str, str]] = None

