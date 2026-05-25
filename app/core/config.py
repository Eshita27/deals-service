from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Polyglot Commerce - Deals API"
    PORT: int = 8082
    MONGO_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "deals_db"

    # Allows loading from a local .env file seamlessly
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()