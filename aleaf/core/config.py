from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict
)
from pydantic import Field

class Setting(BaseSettings):
    # Basic app settings
    APP_NAME: str
    API_VERSION: str

    # MongoDB settings
    MONGO_DB_URL: str = Field(..., description="MongoDB connection URL")
    DB_NAME: str = Field("aleaf", description="Database name")

    # Security settings
    JWT_SECRET_KEY: str = Field(..., description="JWT secret key")
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int  # Token expiration time

    AI_API_KEY: str

    # Other settings (add as needed)
    # Example: Payment, third-party integrations, etc.

    model_config = SettingsConfigDict(
        case_sensitive=True, env_file=".env", env_file_encoding="utf-8"
    )

    @classmethod
    def settings_customise_sources(
        cls, settings_cls: type[BaseSettings], 
        init_settings: PydanticBaseSettingsSource, 
        env_settings: PydanticBaseSettingsSource, 
        dotenv_settings: PydanticBaseSettingsSource, 
        file_secret_settings: PydanticBaseSettingsSource
        ) -> tuple[PydanticBaseSettingsSource, ...]:
        return super().settings_customise_sources(
            settings_cls, init_settings, 
            env_settings, dotenv_settings, 
            file_secret_settings
        )

# Instantiate the settings
settings = Setting() # type: ignore