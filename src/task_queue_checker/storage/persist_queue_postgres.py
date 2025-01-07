import datetime
import pickle
from typing import List, Union

from ..base import Base, QueueBase
from ..types import Task
from ..utils import get_tasks


class PostgresBase(Base):

    def __init__(self) -> None:
        super().__init__()
        # NOTE : this import is here for skip ImportError
        # when import the storage module

        try:
            import psycopg2
        except ImportError as exc:
            raise ImportError(
                "First install psycopg2: pip install psycopg2-binary"
            ) from exc

        self._driver = psycopg2

    def create_table(self):
        connection = self._driver.connect(self._DATABASE_URL)
        cursor = connection.cursor()

        sql = (
            "CREATE TABLE IF NOT EXISTS {} ("
            "id SERIAL PRIMARY KEY,"
            "data BYTEA,"
            "timestamp TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP(3))"
        ).format(self._TABLE_NAME)

        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()

    def insert(self, args):
        connection = self._driver.connect(self._DATABASE_URL)
        cursor = connection.cursor()

        data = pickle.dumps(args)

        sql = ("INSERT INTO {} (data) VALUES (%s)").format(self._TABLE_NAME)

        cursor.execute(sql, (data,))
        connection.commit()
        cursor.close()
        connection.close()

    def select(self, _all=False):
        connection = self._driver.connect(self._DATABASE_URL)
        cursor = connection.cursor()

        if _all:
            sql = "SELECT * FROM {} ORDER BY timestamp ASC".format(self._TABLE_NAME)

        else:
            sql = ("SELECT * FROM {} ORDER BY timestamp ASC LIMIT 1").format(
                self._TABLE_NAME
            )

        cursor.execute(sql)

        if _all:
            result = cursor.fetchall()
        else:
            result = cursor.fetchone()

        cursor.close()
        connection.close()

        return get_tasks(self, result, _all)

    def delete(self, task_id: int):
        connection = self._driver.connect(self._DATABASE_URL)
        cursor = connection.cursor()

        sql = "DELETE FROM {} WHERE id = %s".format(self._TABLE_NAME)

        cursor.execute(sql, (task_id,))
        connection.commit()
        cursor.close()
        connection.close()

    def count(self) -> int:
        connection = self._driver.connect(self._DATABASE_URL)
        cursor = connection.cursor()

        sql = "SELECT COUNT(*) FROM {}".format(self._TABLE_NAME)

        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        return result[0]

    def update_to_latest(self, task_id: int):
        connection = self._driver.connect(self._DATABASE_URL)
        cursor = connection.cursor()

        sql = "UPDATE {} SET timestamp = %s WHERE id = %s".format(self._TABLE_NAME)

        cursor.execute(sql, (datetime.datetime.now(datetime.timezone.utc), task_id))
        connection.commit()
        cursor.close()
        connection.close()

    def __str__(self) -> str:
        return "<PostgresBase>"


class PersistQueuePostgres(PostgresBase, QueueBase):
    def __init__(
        self,
        database_url: str,
        tablename: str = "_persistqueue",
    ):
        super().__init__()
        self._DATABASE_URL = database_url
        self._TABLE_NAME = tablename

        super().create_table()

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
        return "<PersistQueuePostgres>"
