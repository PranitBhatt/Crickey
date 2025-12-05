"""
Configuration settings loaded from environment variables.
Mirrors the .NET appsettings.json structure.
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings - maps to .NET appsettings.json"""
    
    # Firebase Configuration (maps to Firebase:ProjectId, Firebase:CredentialsPath)
    FIREBASE_PROJECT_ID: Optional[str] = os.getenv("FIREBASE_PROJECT_ID", "your-project-id")
    FIREBASE_CREDENTIALS_PATH: Optional[str] = os.getenv("FIREBASE_CREDENTIALS_PATH", "path-to-service-account-key.json")
    
    # FCM Configuration (maps to FCM:ServerKey)
    FCM_SERVER_KEY: Optional[str] = os.getenv("FCM_SERVER_KEY", "your-fcm-server-key")
    
    # API Configuration
    API_PREFIX: str = "/api"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # CORS
    CORS_ORIGINS: list[str] = ["*"]  # Allow all origins (matches .NET "AllowAll" policy)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

