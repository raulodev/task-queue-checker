from src.task_queue_checker.storage import (
    PersistQueueRedis,
    PersistQueueSQLite,
    PersistQueuePostgres,
)

storage_sqlite = PersistQueueSQLite()

storage_redis = PersistQueueRedis()

storage_postgres = PersistQueuePostgres(
    database_url="postgres://raul:1234@127.0.0.1:13784/taskqueue"
)
