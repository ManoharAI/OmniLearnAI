"""
Application settings using Pydantic
"""
from pydantic_settings import BaseSettings
from typing import List
from pydantic import field_validator

class Settings(BaseSettings):
    # Google AI API
    google_api_key: str

    # Qdrant Configuration
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_api_key: str = ""
    qdrant_collection_documents: str = "documents"
    qdrant_collection_web: str = "web_pages"
    qdrant_collection_videos: str = "videos"

    # FastAPI Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    log_level: str = "INFO"

    # CORS
    cors_origins: List[str] = ["http://localhost", "http://localhost:8501"]
    
    @field_validator('cors_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v

    # Embedding Configuration
    embedding_model: str = "models/text-embedding-004"
    embedding_dimension: int = 768

    # LLM Configuration
    llm_model: str = "gemini/gemini-2.0-flash"
    llm_temperature: float = 0.2

    # Chunking Configuration
    chunk_size: int = 1500
    chunk_overlap: int = 200

    # Retrieval Configuration
    retrieval_top_k: int = 10

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
