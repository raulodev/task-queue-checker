from src.task_queue_checker.storage import PersistQueueRedis

storage = PersistQueueRedis()


values = [
    1,
    "Hola Mundo",
    {"name": "Raúl", "last_name": "Cobiellas"},
    ["Task # 3"],
    None,
    True,
]


def test_add():
    for value in values:
        assert None is storage.add(value)


def test_get():

    assert values[0] == storage.get().data

    for index, value in enumerate(values):
        assert value == storage.get(True)[index].data


def test_count():
    assert len(values) == storage.len()
    assert len(values) == len(storage)


def test_task_canel():
    initial_len = storage.len()

    task = storage.get()
    storage.task_cancel(task.id)

    assert initial_len - 1 == storage.len()


def test_task_done():
    initial_len = storage.len()

    task = storage.get()
    storage.task_done(task.id)

    assert initial_len - 1 == storage.len()


def test_update_to_latest():

    task = storage.get()

    storage.update_to_latest(task.id)

    all_tasks = storage.get(True)

    assert task.data == all_tasks[-1].data
