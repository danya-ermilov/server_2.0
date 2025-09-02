import os
from types import SimpleNamespace

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

DB_CONFIG = SimpleNamespace(
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "postgres"),
    database=os.getenv("POSTGRES_DB", "server_2"),
    host=os.getenv("POSTGRES_HOST", "db"),   # не localhost, а сервис из docker-compose
    port=int(os.getenv("POSTGRES_PORT", 5432)),
    database_test=os.getenv("POSTGRES_DB_TEST", "server_2_test"),
)

REDIS_CONFIG = SimpleNamespace(
    redis_host=os.getenv("REDIS_HOST", "redis"),  # имя сервиса из docker-compose
    redis_port=int(os.getenv("REDIS_PORT", 6379)),
    redis_db=int(os.getenv("REDIS_DB", 0)),
)
