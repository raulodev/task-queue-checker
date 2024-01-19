import json
from typing import Union
from datetime import datetime
from .base import TaskBase, SQLBase


class Task(TaskBase):
    def __init__(
        self, _id: int, data, timestamp: Union[str, datetime], storage: SQLBase
    ) -> None:
        self._id = _id
        self.data = data
        self.timestamp = timestamp
        self.storage = storage

    def done(self):
        self.storage.delete(self._id)

    def cancel(self):
        self.storage.delete(self._id)

    def put_last(self):
        self.storage.update_to_latest(self._id)

    @property
    def id(self):
        return self._id

    def __str__(self) -> str:
        return json.dumps(
            {
                "_": "<Task>",
                "id": self._id,
                "data": str(self.data),
                "timestamp": str(self.timestamp),
                "storage": str(self.storage),
            }
        )
