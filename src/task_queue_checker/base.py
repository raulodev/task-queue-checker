from abc import ABC, abstractmethod
from typing import Any
import json


class SQLBase(ABC):
    # The name of the table
    _TABLE_NAME: str
    # The URL of the database
    _DATABASE_URL: str

    @abstractmethod
    def create_table(self):
        """Create the table"""
        pass

    @abstractmethod
    def insert(self):
        """Insert data into the table"""
        pass

    @abstractmethod
    def select(self):
        """Select data from the table"""
        pass

    @abstractmethod
    def delete(self, id: int):
        """Delete data from the table"""
        pass

    @abstractmethod
    def update_to_latest(self, id: int):
        """Update task in the table to the latest position"""
        pass

    @abstractmethod
    def count(self):
        """Count the number of tasks in the table"""
        pass


class QueueBase(ABC):
    @abstractmethod
    def add(self):
        """Add an item to the queue"""
        pass

    @abstractmethod
    def get(self):
        """Get an item from the queue"""
        pass

    @abstractmethod
    def len(self):
        """Get the length of the queue"""
        pass

    def __str__(self) -> str:
        return "<QueueBase>"


class TaskBase(ABC):
    # The ID of the task
    id: int
    # The data of the task
    data: Any
    # The timestamp of the task
    timestamp: int
    # The storage of the task
    storage: SQLBase

    @abstractmethod
    def done(self):
        """Mark the task as done and delete this from table"""
        pass

    @abstractmethod
    def cancel(self):
        """Mark the task as cancelled and delete this from table"""
        pass

    @abstractmethod
    def put_last(self):
        """Put the task to the end of the queue"""
        pass

    def __str__(self) -> str:
        return json.dumps(
            {
                "_": "<TaskBase>",
                "id": self.id,
                "data": self.data,
                "timestamp": self.timestamp,
                "storage": self.storage,
            }
        )
