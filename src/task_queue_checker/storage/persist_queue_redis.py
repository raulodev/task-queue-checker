import time
import pickle
from typing import List, Union

from ..base import Base, QueueBase
from ..types import Task
from ..utils import get_tasks


class RedisBase(Base):

    def __init__(self) -> None:
        super().__init__()
        # NOTE : this import is here for skip ImportError
        # when import the storage module

        try:
            import redis
        except ImportError as exc:
            raise ImportError(
                "First install redis: pip install redis[hiredis]"
            ) from exc

        self._driver = redis

    def create_connection(self):
        creds_provider = None

        if self._USER and self._PASSWORD:
            creds_provider = self._driver.UsernamePasswordCredentialProvider(
                self._USER,
                self._PASSWORD,
            )

        return self._driver.Redis(
            host=self._HOST,
            port=self._PORT,
            decode_responses=False,
            credential_provider=creds_provider,
        )

    def create_table(self): ...

    def insert(self, args):
        redis = self.create_connection()

        data = pickle.dumps([args, time.time()])

        redis.lpush(self._TABLE_NAME, data)

    def select(self, _all):
        redis = self.create_connection()

        if _all:
            result = redis.lrange(self._TABLE_NAME, 0, -1)
        else:

            result = redis.lindex(self._TABLE_NAME, -1)

        tasks = get_tasks(self, result, _all)

        if _all:
            tasks.reverse()

        return tasks

    def count(self) -> int:
        redis = self.create_connection()

        return redis.llen(self._TABLE_NAME)

    def delete(self, task_id):
        redis = self.create_connection()

        value = redis.lindex(self._TABLE_NAME, task_id)

        redis.lrem(self._TABLE_NAME, -1, value)

    def update_to_latest(self, task_id):
        redis = self.create_connection()

        value = redis.lindex(self._TABLE_NAME, task_id)

        redis.lrem(self._TABLE_NAME, -1, value)

        redis.lpush(self._TABLE_NAME, value)


class PersistQueueRedis(RedisBase, QueueBase):
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        user: str = None,
        password: str = None,
        tablename: str = "_persistqueue",
    ):
        super().__init__()

        self._HOST = host
        self._PORT = port
        self._USER = user
        self._PASSWORD = password
        self._TABLE_NAME = tablename

    def add(self, args):
        """Add task to queue

        Args:
        - args : Can be any information to run the consumer

        Example
        ```python
        storage.add([1, 2, 3, "Hola Mundo"])

        storage.add({"name": "Raùl", "last_name": "Cobiellas"})

        storage.add("Task # 3")

        storage.add("Task # 4")
        ```
        """
        super().insert(args)

    def get(self, _all=False) -> Union[Task, List[Task], None]:
        """
        if _all = False (default) return 1 task
        else  all task are returned
        """
        return super().select(_all)

    def task_done(self, task_id: int):
        """Delete the task from the table"""
        super().delete(task_id)

    def task_cancel(self, task_id):
        """Delete the task from the table"""
        super().delete(task_id)

    def len(self):
        return super().count()

    def __len__(self):
        return super().count()

    def __str__(self) -> str:
        # Return a string representation of the class
        return "<PersistQueueRedis>"
