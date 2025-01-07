import datetime
import pickle
from typing import List, Union
from urllib.parse import urlparse

from ..base import Base, QueueBase
from ..types import Task
from ..utils import get_tasks


class MySqlBase(Base):
    def __init__(self) -> None:
        super().__init__()
        # NOTE : this import is here for skip ImportError
        # when import the storage module

        try:
            import pymysql
        except ImportError as exc:
            raise ImportError("First install pymysql: pip install pymysql") from exc

        self._driver = pymysql

    def create_connection(self):
        return self._driver.connect(
            host=self._HOST,
            user=self._USER,
            password=self._PASSWORD,
            database=self._DATABASE,
            port=self._PORT,
        )

    def create_table(self):
        connection = self.create_connection()
        cursor = connection.cursor()

        sql = (
            "CREATE TABLE IF NOT EXISTS {} ("
            "id INT AUTO_INCREMENT PRIMARY KEY,"
            "data BLOB,"
            "timestamp DATETIME(3) DEFAULT CURRENT_TIMESTAMP(3))"
        ).format(self._TABLE_NAME)

        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()

    def insert(self, args):
        connection = self.create_connection()
        cursor = connection.cursor()

        data = pickle.dumps(args)

        sql = ("INSERT INTO {} (data) VALUES (%s)").format(self._TABLE_NAME)

        cursor.execute(sql, (data,))

        connection.commit()
        cursor.close()
        connection.close()

    def select(self, _all=False):
        connection = self.create_connection()
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
        connection = self.create_connection()
        cursor = connection.cursor()

        sql = "DELETE FROM {} WHERE id = %s".format(self._TABLE_NAME)

        cursor.execute(sql, (task_id,))
        connection.commit()
        cursor.close()
        connection.close()

    def count(self) -> int:
        connection = self.create_connection()
        cursor = connection.cursor()

        sql = "SELECT COUNT(*) FROM {}".format(self._TABLE_NAME)

        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        return result[0]

    def update_to_latest(self, task_id: int):
        connection = self.create_connection()
        cursor = connection.cursor()

        sql = "UPDATE {} SET timestamp = %s WHERE id = %s".format(self._TABLE_NAME)

        cursor.execute(sql, (datetime.datetime.now(datetime.timezone.utc), task_id))
        connection.commit()
        cursor.close()
        connection.close()

    def __str__(self) -> str:
        return "<MySqlBase>"


class PersistQueueMySql(MySqlBase, QueueBase):
    def __init__(
        self,
        host: str = None,
        user: str = None,
        password: str = None,
        database: str = None,
        port=3306,
        database_url: str = None,
        tablename: str = "_persistqueue",
    ):
        super().__init__()

        self._TABLE_NAME = tablename

        if database_url is None:
            self._HOST = host
            self._USER = user
            self._PASSWORD = password
            self._DATABASE = database
            self._PORT = port

        else:
            self._parse_database_url(database_url)

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

    def _parse_database_url(self, database_url: str):
        parsed_url = urlparse(database_url)

        self._HOST = parsed_url.hostname
        self._USER = parsed_url.username
        self._PASSWORD = parsed_url.password
        self._PORT = parsed_url.port
        self._DATABASE = parsed_url.path.lstrip("/")

    def __str__(self) -> str:
        return "<PersistQueueMySql>"
