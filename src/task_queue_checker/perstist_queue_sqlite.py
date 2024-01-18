from typing import List, Union
import sqlite3
import pickle
import datetime
from .base import SQLBase, QueueBase
from .types import Task


class SQLiteBase(SQLBase):
    # Create a table in the database if it does not already exist
    def create_table(self):
        # Connect to the database
        connection = sqlite3.connect(self._DATABASE_URL)
        cursor = connection.cursor()

        # Create the table
        sql = (
            "CREATE TABLE IF NOT EXISTS {} "
            "(id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "data BLOB ,"
            "timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
        ).format(self._TABLE_NAME)

        # Execute the query
        cursor.execute(sql)
        # Commit the changes
        connection.commit()
        # Close the connection
        connection.close()

    # Insert a record into the table
    def insert(self, args):
        # Connect to the database
        connection = sqlite3.connect(self._DATABASE_URL)
        cursor = connection.cursor()

        # Convert the arguments to a pickle object
        data = pickle.dumps(args)

        # Create the query
        sql = ("INSERT INTO {} (data) VALUES (?)").format(self._TABLE_NAME)

        # Execute the query
        cursor.execute(sql, (data,))
        # Commit the changes
        connection.commit()
        # Close the connection
        connection.close()

    # Select a record from the table
    def select(self, all=False):
        # Connect to the database
        connection = sqlite3.connect(self._DATABASE_URL)
        cursor = connection.cursor()

        # Create the query
        if all:
            sql = "SELECT * FROM {} ORDER BY timestamp DESC".format(self._TABLE_NAME)

        else:
            sql = ("SELECT * FROM {} ORDER BY timestamp DESC LIMIT 1").format(
                self._TABLE_NAME
            )

        # Execute the query
        cursor.execute(sql)

        # Fetch the result
        if all:
            result = cursor.fetchall()
        else:
            result = cursor.fetchone()

        # Return the result
        if result is not None:
            if all:
                return [
                    Task(
                        id=r[0],
                        data=pickle.loads(r[1]),
                        timestamp=r[2],
                        storage=self,
                    )
                    for r in result
                ]

            else:
                return Task(
                    id=result[0],
                    data=pickle.loads(result[1]),
                    timestamp=result[2],
                    storage=self,
                )

        else:
            return None

    # Delete a record from the table
    def delete(self, task_id: int):
        # Connect to the database
        connection = sqlite3.connect(self._DATABASE_URL)
        cursor = connection.cursor()

        # Create the query
        sql = "DELETE FROM {} WHERE id = ?".format(self._TABLE_NAME)

        # Execute the query
        cursor.execute(sql, (task_id,))
        # Commit the changes
        connection.commit()
        # Close the connection
        connection.close()

    # Count the number of records in the table
    def count(self) -> int:
        # Connect to the database
        connection = sqlite3.connect(self._DATABASE_URL)
        cursor = connection.cursor()

        # Create the query
        sql = "SELECT COUNT(*) FROM {}".format(self._TABLE_NAME)

        # Execute the query
        cursor.execute(sql)
        # Fetch the result
        result = cursor.fetchone()
        # Close the connection
        connection.close()

        # Return the result
        return result[0]

    # Update the timestamp of a record in the table
    def update_to_latest(self, id: int):
        # Connect to the database
        connection = sqlite3.connect(self._DATABASE_URL)
        cursor = connection.cursor()

        # Create the query
        sql = "UPDATE {} SET timestamp = ? WHERE id = ?".format(self._TABLE_NAME)

        # Execute the query
        cursor.execute(sql, (datetime.datetime.now(), id))
        # Commit the changes
        connection.commit()
        # Close the connection
        connection.close()


class PerstistQueueSQLite(SQLiteBase, QueueBase):
    def __init__(
        self,
        database_url: str = "queue.db",
        tablename: str = "queue",
    ):
        # Set the database URL and table name
        self._DATABASE_URL = database_url
        self._TABLE_NAME = tablename

        # Create the table
        super().create_table()

    def add(self, args):
        super().insert(args)

    def get(self, all=False) -> Union[Task, List[Task], None]:
        return super().select(all)

    def task_done(self, id: int):
        """Delete the task from the table"""
        super().delete(id)

    def task_cancel(self, task_id):
        """Delete the task from the table"""
        super().delete(task_id)

    def len(self):
        return super().count()

    def __str__(self) -> str:
        # Return a string representation of the class
        return "<PerstistQueueSQLite>"
