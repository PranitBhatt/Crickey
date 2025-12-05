"""
Auth DTOs - mirrors AuthController request models
"""
from pydantic import BaseModel, Field


class ValidateTokenRequest(BaseModel):
    """Token validation request"""
    token: str = Field(..., min_length=1)

