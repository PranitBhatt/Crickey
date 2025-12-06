"""
Firebase authentication dependencies for FastAPI.
Provides reusable token verification for protected endpoints.
"""
from fastapi import Depends, HTTPException, status, Request
from firebase_admin import auth as admin_auth
import logging

logger = logging.getLogger(__name__)


async def verify_token(request: Request) -> dict:
    """
    Verify Firebase ID token from Authorization header.
    Returns decoded token claims if valid, raises HTTPException if invalid.
    
    Usage:
        @router.post("/protected")
        async def protected_endpoint(decoded_token: dict = Depends(verify_token)):
            user_id = decoded_token["uid"]
            ...
    """
    auth_header = request.headers.get("Authorization")
    
    if not auth_header:
        logger.warning("Missing Authorization header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization token"
        )
    
    try:
        # Extract token from "Bearer <token>" format
        parts = auth_header.split(" ")
        if len(parts) != 2 or parts[0].lower() != "bearer":
            logger.warning(f"Invalid Authorization header format: {auth_header[:20]}...")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header format. Expected: Bearer <token>"
            )
        
        token = parts[1]
        
        # Verify token with Firebase Admin SDK
        decoded_token = admin_auth.verify_id_token(token)
        
        logger.debug(f"Token verified for user: {decoded_token.get('uid')}")
        return decoded_token
        
    except ValueError as e:
        logger.warning(f"Token verification error (ValueError): {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    except Exception as e:
        logger.error(f"Token verification error: {type(e).__name__}: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token verification failed"
        )


def get_current_user_id(decoded_token: dict = Depends(verify_token)) -> str:
    """
    Extract user ID from verified token.
    Convenience dependency for endpoints that only need the user ID.
    
    Usage:
        @router.post("/protected")
        async def protected_endpoint(user_id: str = Depends(get_current_user_id)):
            ...
    """
    return decoded_token.get("uid")

