"""
Auth service - mirrors IAuthService
"""
import firebase_admin
from firebase_admin import auth
import logging

logger = logging.getLogger(__name__)


class AuthService:
    """
    Service for authentication operations.
    Mirrors the .NET AuthService.
    """
    
    async def validate_token(self, token: str) -> bool:
        """
        Validate Firebase JWT token.
        Mirrors ValidateTokenAsync.
        """
        try:
            decoded_token = auth.verify_id_token(token)
            return decoded_token is not None
        except Exception as e:
            logger.warning(f"Token validation failed: {e}")
            return False

