from medquery.config.settings import settings


def test_default_settings() -> None:
    assert settings.app_name == "MedQuery"
    assert settings.environment == "development"
    assert settings.embedding_model
    assert settings.qdrant_url
    assert settings.qdrant_collection