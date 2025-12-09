"""
Configuration management for AI Customer Support Bot
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Google Gemini API
    gemini_api_key: str
    
    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/support_bot"
    redis_url: str = "redis://localhost:6379/0"
    
    # Application
    app_env: str = "development"
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:3000,http://localhost:5173"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    # LLM Settings
    llm_model: str = "gemini-2.5-flash"
    llm_temperature: float = 0.2
    llm_max_tokens: int = 1024
    confidence_threshold: float = 0.4
    
    # Vector DB
    vector_db_type: str = "faiss"
    faiss_index_path: str = "./data/faiss_index"
    embedding_model: str = "all-MiniLM-L6-v2"
    
    # Session Settings
    session_memory_window: int = 6
    session_ttl_hours: int = 1
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
