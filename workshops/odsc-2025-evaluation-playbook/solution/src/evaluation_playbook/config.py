from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration settings for the evaluation playbook application.

    This class uses Pydantic's BaseSettings to manage configuration through environment
    variables and .env files. It includes settings for OpenAI, Qdrant vector store,
    Opik monitoring, RAG system, and file paths.
    """

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

    # --- RAG Configuration ---
    RAG_TEXT_EMBEDDING_MODEL_ID: str = "text-embedding-3-small"
    RAG_TEXT_EMBEDDING_MODEL_DIM: int = 1536
    RAG_CHUNK_SIZE: int = 128
    RAG_TOP_K: int = 3
    RAG_DEVICE: str = "cpu"

    # --- Paths Configuration ---
    EVALUATION_DATASET_FILE_PATH: Path = Path("data/evaluation_dataset.json")
    EXTRACTION_METADATA_FILE_PATH: Path = Path("data/extraction_metadata_slim.json")


settings = Settings()
