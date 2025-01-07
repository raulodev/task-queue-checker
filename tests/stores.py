import os
from dotenv import load_dotenv

from src.task_queue_checker.storage import (
    PersistQueuePostgres,
    PersistQueueRedis,
    PersistQueueSQLite,
)

load_dotenv()

POSTGRES_DATABASE_URL = os.getenv("POSTGRES_DATABASE_URL")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")


storage_sqlite = PersistQueueSQLite()

storage_redis = PersistQueueRedis(host=REDIS_HOST)

storage_postgres = PersistQueuePostgres(database_url=POSTGRES_DATABASE_URL)
