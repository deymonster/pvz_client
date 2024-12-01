
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=".env")

    # URLS
    DISCOVERY_URL:  str
    S_POINT_URL: str
    POINT_RATING_URL: str
    POINT_BALANCE_URL: str

settings = Settings()  # type: ignore


__all__ = [
    "settings",
]

    



