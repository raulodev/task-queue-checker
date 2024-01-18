from .base import TaskBase, SQLBase


class Task(TaskBase):
    def __init__(self, id: int, data, timestamp: int, storage: SQLBase) -> None:
        self.id = id
        self.data = data
        self.timestamp = timestamp
        self._storage = storage

    def done(self):
        self._storage.delete(self.id)

    def cancel(self):
        self._storage.delete(self.id)

    def put_last(self):
        self._storage.update_to_latest(self.id)
