from typing import Callable
import threading
from .perstist_queue_sqlite import PerstistQueueSQLite


class TaskQueueChecker(threading.Thread):
    def __init__(
        self,
        consumer: Callable,
        task_storage: PerstistQueueSQLite,
        sleep_interval=5,
        daemon=True,
    ):
        threading.Thread.__init__(self, name="TaskQueueChecker", daemon=daemon)

        self._consumers = consumer
        self._task_storage = task_storage
        self._stop = threading.Event()
        self._interval = sleep_interval

    def run(self):
        while True:
            # Get first task from the task storage
            task = self._task_storage.get()

            # If there are task, call the consumer function
            if task:
                self._consumers(task)

            # Wait for the specified interval or until the stop event is set
            is_stoped = self._stop.wait(self._interval)
            if is_stoped:
                break

    def stop(self):
        # Set the stop event to stop the thread
        self._stop.set()
