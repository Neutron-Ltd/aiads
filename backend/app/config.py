from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    environment: str = "development"  # development | production
    debug: bool = False

    # Database - use DATABASE_URL in production (e.g. PostgreSQL)
    database_url: str = "sqlite:///./ads_copilot.db"

    # CORS - comma-separated in .env (e.g. https://app.example.com,https://admin.example.com)
    cors_origins: list[str] = ["http://localhost:3000"]

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, list):
            return v
        return [o.strip() for o in str(v).split(",") if o.strip()] if v else ["http://localhost:3000"]

    # AI
    gemini_api_key: str = ""

    # Google Ads API - required for production
    google_ads_developer_token: str = ""
    google_ads_client_id: str = ""
    google_ads_client_secret: str = ""
    google_ads_refresh_token: str = ""
    google_ads_login_customer_id: str = ""  # MCC ID for manager accounts

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    @property
    def google_ads_configured(self) -> bool:
        return bool(
            self.google_ads_developer_token
            and self.google_ads_client_id
            and self.google_ads_client_secret
            and self.google_ads_refresh_token
        )


settings = Settings()
