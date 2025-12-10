"""Application configuration using Pydantic Settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # LLM Configuration
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    default_model: str = "claude-sonnet-4-20250514"

    # Gemini Configuration
    google_api_key: str = ""
    gemini_model: str = "gemini-1.5-pro"
    gemini_temperature: float = 0.3
    gemini_max_output_tokens: int = 8192

    # Azure Storage Configuration
    azure_storage_connection_string: str = ""
    azure_storage_account_url: str = ""
    azure_storage_sas_token: str = ""

    # Redis Configuration
    redis_url: str = "redis://localhost:6379/0"

    # ChromaDB Configuration
    chroma_persist_directory: str = "./data/chroma"

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_debug: bool = False

    # Patent Pipeline Configuration
    patent_pipeline_timeout: int = 600  # seconds
    patent_pipeline_max_retries: int = 3

    # Logging
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
