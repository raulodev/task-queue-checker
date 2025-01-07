# import time
# import random

# from src.task_queue_checker import TaskQueueChecker
# from src.task_queue_checker.storage import PersistQueueRedis
# from src.task_queue_checker.types import Task

# storage = PersistQueueRedis()


# storage.add([1, 2, 3, "Hola Mundo"])

# storage.add({"name": "Raùl", "last_name": "Cobiellas"})

# storage.add("Task # 3")

# storage.add("Task # 4")


# def consumer(task: Task):
#     print(task.data)  # task content

#     number = random.randint(1, 3)

#     if number == 1:
#         print(f"task {task.id} done")
#         task.done()

#     elif number == 2:
#         print(f"task {task.id} canceled")
#         task.cancel()

#     elif number == 3:
#         print(f"task {task.id} put last")
#         task.put_last()


# monitor = TaskQueueChecker(consumer=consumer, task_storage=storage)
# monitor.start()


# while len(storage) > 0:
#     try:
#         time.sleep(10)
#     except KeyboardInterrupt:
#         break
