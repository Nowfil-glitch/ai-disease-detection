from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:3001"
    
    # Base URL for static files (Heatmaps)
    BASE_URL: str = "http://localhost:8000"
    
    # File Upload
    MAX_FILE_SIZE: int = 10485760  # 10MB
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png"]
    UPLOAD_DIR: str = "uploads"
    
    # AI Models
    MODEL_PATH: str = "./models"
    HEATMAP_OUTPUT_PATH: str = "./static/heatmaps"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    RATE_LIMIT: str = "100/minute"
    
    # Translation
    GOOGLE_TRANSLATE_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    def get_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


settings = Settings()

# Create necessary directories
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.HEATMAP_OUTPUT_PATH, exist_ok=True)
os.makedirs(settings.MODEL_PATH, exist_ok=True)
