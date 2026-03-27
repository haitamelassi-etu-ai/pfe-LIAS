from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "LIAS Platform API"
    env: str = "development"
    secret_key: str = "change_me"
    access_token_expire_minutes: int = 1440
    database_url: str = "sqlite:///./lias.db"
    orcid_api_base: str = "https://pub.orcid.org/v3.0"
    storage_backend: str = "local"
    local_storage_path: str = "./storage"
    s3_bucket_name: str | None = None
    s3_region: str | None = None
    s3_endpoint_url: str | None = None
    s3_access_key_id: str | None = None
    s3_secret_access_key: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
