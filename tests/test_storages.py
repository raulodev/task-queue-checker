from tests.stores import storage_sqlite, storage_redis

values = [
    1,
    "Hola Mundo",
    {"name": "Raúl", "last_name": "Cobiellas"},
    ["Task # 3"],
    None,
    True,
]


def test_add_redis():
    add(storage_redis)


def test_add_sqlite():
    add(storage_sqlite)


def test_get_redis():
    get(storage_redis)


def test_get_sqlite():
    get(storage_sqlite)


def test_count_redis():
    count(storage_redis)


def test_count_sqlite():
    count(storage_sqlite)


def task_modify_redis():
    task_modify(storage_redis)


def task_modify_sqlite():
    task_modify(storage_sqlite)


def test_update_to_latest_redis():
    update_to_latest(storage_redis)


def test_update_to_latest_sqlite():
    update_to_latest(storage_sqlite)


def add(storage):
    for value in values:
        assert None is storage.add(value)


def get(storage):
    assert values[0] == storage.get().data

    for index, value in enumerate(values):
        assert value == storage.get(True)[index].data


def count(storage):
    assert len(values) == storage.len()
    assert len(values) == len(storage)


def task_modify(storage):
    initial_len = storage.len()

    task = storage.get()
    storage.task_cancel(task.id)

    assert initial_len - 1 == storage.len()


def update_to_latest(storage):

    task = storage.get()

    storage.update_to_latest(task.id)

    all_tasks = storage.get(True)

    assert task.data == all_tasks[-1].data
