from abc import ABC, abstractmethod
from typing import Any


class SQLBase(ABC):
    # The name of the table
    _TABLE_NAME: str
    # The URL of the database
    _DATABASE_URL: str

    _HOST: str
    _USER: str
    _PASSWORD: str
    _PORT: int
    _DATABASE: str

    @abstractmethod
    def create_table(self):
        """Create the table"""

    @abstractmethod
    def insert(self, args):
        """Insert data into the table"""

    @abstractmethod
    def select(self):
        """Select data from the table"""

    @abstractmethod
    def delete(self, task_id: int):
        """Delete data from the table"""

    @abstractmethod
    def update_to_latest(self, task_id: int):
        """Update task in the table to the latest position"""

    @abstractmethod
    def count(self):
        """Count the number of tasks in the table"""

    def __str__(self) -> str:
        return "<SQLBase>"


class QueueBase(ABC):
    @abstractmethod
    def add(self, args):
        """Add an item to the queue"""

    @abstractmethod
    def get(self, _all):
        """Get an item from the queue"""

    @abstractmethod
    def len(self):
        """Get the length of the queue"""

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

    @abstractmethod
    def cancel(self):
        """Mark the task as cancelled and delete this from table"""

    @abstractmethod
    def put_last(self):
        """Put the task to the end of the queue"""

    def __str__(self) -> str:
        return "<TaskBase>"
