# task-queue-checker

Tool designed to simplify the management and monitoring of task queues in Python environments

[![Downloads](https://static.pepy.tech/badge/task-queue-checker)](https://pepy.tech/project/task-queue-checker)
[![PyPI version](https://badge.fury.io/py/task-queue-checker.svg)](https://badge.fury.io/py/task-queue-checker)
![Repo Size](https://img.shields.io/github/repo-size/raulodev/task-queue-checker)
![PyPI - License](https://img.shields.io/pypi/l/task-queue-checker)

## Installing

```console
pip install task-queue-checker
```

## Tutorial

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

storage.add("Task # 4")


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


# this code simulates the execution of your main program
while True:
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        break

```
