from pydantic_settings import BaseSettings, SettingsConfigDict

class AppConfig(BaseSettings):
    """
    Base configuration for SpotiGram services.
    Services should inherit from this and add their own specific configuration.
    """
    app_name: str = "spotigram-service"
    environment: str = "development"
    log_level: str = "INFO"
    
    # Common integrations
    kafka_broker_url: str = "localhost:9092"
    redis_host: str = "localhost"
    redis_port: int = 6379

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

def get_base_config() -> AppConfig:
    """Returns the base configuration instance."""
    return AppConfig()
