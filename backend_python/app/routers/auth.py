"""
Auth router - mirrors AuthController.cs
"""
from fastapi import APIRouter, Depends, status
from app.schemas.auth import ValidateTokenRequest
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])


def get_auth_service() -> AuthService:
    """Dependency injection for AuthService"""
    return AuthService()


@router.post("/validateToken", status_code=status.HTTP_200_OK)
async def validate_token(
    request: ValidateTokenRequest,
    service: AuthService = Depends(get_auth_service)
):
    """
    Validate Firebase JWT token.
    Mirrors POST /api/auth/validateToken
    """
    is_valid = await service.validate_token(request.token)
    return {"valid": is_valid}

