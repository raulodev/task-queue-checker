from typing import List, Union
import pickle
import datetime
from urllib.parse import urlparse
from ..base import SQLBase, QueueBase
from ..types import Task
from ..utils import get_tasks


class MySqlBase(SQLBase):
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
        # Connect to the database
        connection = self.create_connection()
        cursor = connection.cursor()

        # Create the table
        sql = (
            "CREATE TABLE IF NOT EXISTS {} ("
            "id INT AUTO_INCREMENT PRIMARY KEY,"
            "data BLOB,"
            "timestamp DATETIME(3) DEFAULT CURRENT_TIMESTAMP(3))"
        ).format(self._TABLE_NAME)

        # Execute the query
        cursor.execute(sql)
        # # Commit the changes
        connection.commit()
        # # Close the connection
        cursor.close()
        connection.close()

    # Insert a record into the table
    def insert(self, args):
        # Connect to the database
        connection = self.create_connection()
        cursor = connection.cursor()

        # Convert the arguments to a pickle object
        data = pickle.dumps(args)

        # Create the query
        sql = ("INSERT INTO {} (data) VALUES (%s)").format(self._TABLE_NAME)

        # Execute the query
        cursor.execute(sql, (data,))
        # Commit the changes
        connection.commit()
        # Close the connection
        cursor.close()
        connection.close()

    # Select a record from the table
    def select(self, _all=False):
        # Connect to the database
        connection = self.create_connection()
        cursor = connection.cursor()

        # Create the query
        if _all:
            sql = "SELECT * FROM {} ORDER BY timestamp ASC".format(self._TABLE_NAME)

        else:
            sql = ("SELECT * FROM {} ORDER BY timestamp ASC LIMIT 1").format(
                self._TABLE_NAME
            )

        # Execute the query
        cursor.execute(sql)

        # Fetch the result
        if _all:
            result = cursor.fetchall()
        else:
            result = cursor.fetchone()

        # Close the connection
        cursor.close()
        connection.close()

        # Return the result
        return get_tasks(self, result, _all)

    # Delete a record from the table
    def delete(self, task_id: int):
        # Connect to the database
        connection = self.create_connection()
        cursor = connection.cursor()

        # Create the query
        sql = "DELETE FROM {} WHERE id = %s".format(self._TABLE_NAME)

        # Execute the query
        cursor.execute(sql, (task_id,))
        # Commit the changes
        connection.commit()
        # Close the connection
        cursor.close()
        connection.close()

    # Count the number of records in the table
    def count(self) -> int:
        # Connect to the database
        connection = self.create_connection()
        cursor = connection.cursor()

        # Create the query
        sql = "SELECT COUNT(*) FROM {}".format(self._TABLE_NAME)

        # Execute the query
        cursor.execute(sql)
        # Fetch the result
        result = cursor.fetchone()
        # Close the connection
        cursor.close()
        connection.close()

        # Return the result
        return result[0]

    # Update the timestamp of a record in the table
    def update_to_latest(self, task_id: int):
        # Connect to the database
        connection = self.create_connection()
        cursor = connection.cursor()

        # Create the query
        sql = "UPDATE {} SET timestamp = %s WHERE id = %s".format(self._TABLE_NAME)

        # Execute the query
        cursor.execute(sql, (datetime.datetime.utcnow(), task_id))
        # Commit the changes
        connection.commit()
        # Close the connection
        cursor.close()
        connection.close()

    def __str__(self) -> str:
        # Return a string representation of the class
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
        # Set the database  and table name

        self._TABLE_NAME = tablename

        if database_url is None:
            self._HOST = host
            self._USER = user
            self._PASSWORD = password
            self._DATABASE = database
            self._PORT = port

        else:
            self._parse_database_url(database_url)

        # Create the table
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

    def _parse_database_url(self, database_url: str):
        parsed_url = urlparse(database_url)

        self._HOST = parsed_url.hostname
        self._USER = parsed_url.username
        self._PASSWORD = parsed_url.password
        self._PORT = parsed_url.port
        self._DATABASE = parsed_url.path.lstrip("/")

    def __str__(self) -> str:
        return "<PersistQueueMySql>"
