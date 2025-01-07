from src.task_queue_checker.storage import PersistQueueRedis, PersistQueueSQLite

storage_sqlite = PersistQueueSQLite()

storage_redis = PersistQueueRedis()
