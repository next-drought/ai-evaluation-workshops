from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )

    # --- OpenAI Configuration ---
    OPENAI_API_KEY: SecretStr | None
    OPENAI_MODEL: str = "gpt-4o-mini"

    # --- Qdrant Configuration ---
    QDRANT_URL: str = Field(
        default="http://localhost:6333",
        description="Connection URI for the local Qdrant instance.",
    )
    QDRANT_COLLECTION_NAME: str = "philosopher_long_term_memory"

    # --- Opik Configuration ---
    OPIK_API_KEY: SecretStr | None = Field(
        default=None, description="API key for Opik services."
    )
    OPIK_PROJECT: str = Field(
        default="odsc-2025-evaluation-playbook-webinar",
        description="Project name for Opik tracking.",
    )

    # --- Agents Configuration ---
    TOTAL_MESSAGES_SUMMARY_TRIGGER: int = 30
    TOTAL_MESSAGES_AFTER_SUMMARY: int = 5

    # --- RAG Configuration ---
    RAG_TEXT_EMBEDDING_MODEL_ID: str = "text-embedding-3-small"
    RAG_TEXT_EMBEDDING_MODEL_DIM: int = 1536
    RAG_CHUNK_SIZE: int = 256
    RAG_TOP_K: int = 3
    RAG_DEVICE: str = "cpu"

    # --- Paths Configuration ---
    EVALUATION_DATASET_FILE_PATH: Path = Path("data/evaluation_dataset.json")
    EXTRACTION_METADATA_FILE_PATH: Path = Path("data/extraction_metadata_slim.json")


settings = Settings()
