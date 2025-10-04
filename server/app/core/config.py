from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    algorithm: str

    access_token_expire_minutes: int = 30

    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_db_test: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    debug: bool = False

    class Config:
        env_file = ".env.dev"


settings = Settings()

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.postgres_user}:"
    f"{settings.postgres_password}@{settings.postgres_host}:"
    f"{settings.postgres_port}/{settings.postgres_db}"
)

REDIS_URL = f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}"
