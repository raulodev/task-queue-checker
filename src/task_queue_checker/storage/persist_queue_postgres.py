from typing import List, Union
import pickle
import datetime
from ..base import SQLBase, QueueBase
from ..types import Task
from ..utils import get_tasks


class PostgresBase(SQLBase):
    # Create a table in the database if it does not already exist

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
        # Connect to the database
        connection = self._driver.connect(self._DATABASE_URL)
        cursor = connection.cursor()

        # Create the table
        sql = (
            "CREATE TABLE IF NOT EXISTS {} ("
            "id SERIAL PRIMARY KEY,"
            "data BYTEA,"
            "timestamp TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP(3))"
        ).format(self._TABLE_NAME)

        # Execute the query
        cursor.execute(sql)
        # Commit the changes
        connection.commit()
        # Close the connection
        cursor.close()
        connection.close()

    # Insert a record into the table
    def insert(self, args):
        # Connect to the database
        connection = self._driver.connect(self._DATABASE_URL)
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
        connection = self._driver.connect(self._DATABASE_URL)
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
        connection = self._driver.connect(self._DATABASE_URL)
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
        connection = self._driver.connect(self._DATABASE_URL)
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
        connection = self._driver.connect(self._DATABASE_URL)
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
        return "<PostgresBase>"


class PersistQueuePostgres(PostgresBase, QueueBase):
    def __init__(
        self,
        database_url: str,
        tablename: str = "_persistqueue",
    ):
        super().__init__()
        # Set the database URL and table name
        self._DATABASE_URL = database_url
        self._TABLE_NAME = tablename

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

    def __str__(self) -> str:
        # Return a string representation of the class
        return "<PersistQueuePostgres>"
