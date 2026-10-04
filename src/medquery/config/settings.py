from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "MedQuery"
    environment: str = "development"

    embedding_model: str = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "medquery"

    groq_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()