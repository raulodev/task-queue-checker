from typing import Callable, Union
import threading
from .storage.persist_queue_sqlite import PersistQueueSQLite
from .storage.persist_queue_postgres import PersistQueuePostgres


class TaskQueueChecker(threading.Thread):
    def __init__(
        self,
        consumer: Callable,
        task_storage: Union[PersistQueueSQLite, PersistQueuePostgres],
        sleep_interval=5,
        daemon=True,
    ):
        """

        Args:
            consumer (Callable): function to which the task argument will be passed
            task_storage (Union[PersistQueueSQLite, PersistQueuePostgres]): storage
            sleep_interval (int, optional): time between task execution. Defaults to 5.

        Example
        ```python
        import time
        import random

        from task_queue_checker.storage import PersistQueueSQLite
        from task_queue_checker.types import Task
        from task_queue_checker import TaskQueueChecker

        storage = PersistQueueSQLite()

        # add tasks to queue
        storage.add([1, 2, 3, "Hola Mundo"])

        storage.add({"name": "Raùl", "last_name": "Cobiellas"})

        storage.add("Task # 3")

        storage.add("Task # 3")


        def consumer(task: Task):
            print(task.data)  # task content

            number = random.randint(1, 3)

            if number == 1:
                print(f"task {task.id} done")
                task.done()

            elif number == 2:
                print(f"task {task.id} canceled")
                task.cancel()

            elif number == 3:
                print(f"task {task.id} put last")
                task.put_last()


        monitor = TaskQueueChecker(consumer=consumer, task_storage=storage)
        # run monitor in background
        monitor.start()
        ```
        """
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
        """Set the stop event to stop the thread"""
        self._stop.set()
