from tests.stores import storage_sqlite, storage_redis, storage_postgres, storage_mysql

values = [
    1,
    "Hola Mundo",
    {"name": "Raúl", "last_name": "Cobiellas"},
    ["Task # 3"],
    None,
    True,
]


# Redis
def test_add_redis():
    add(storage_redis)


def test_get_redis():
    get(storage_redis)


def test_count_redis():
    count(storage_redis)


def test_task_modify_redis():
    task_modify(storage_redis)


def test_update_to_latest_redis():
    update_to_latest(storage_redis)


# SQLite
def test_add_sqlite():
    add(storage_sqlite)


def test_get_sqlite():
    get(storage_sqlite)


def test_count_sqlite():
    count(storage_sqlite)


def test_task_modify_sqlite():
    task_modify(storage_sqlite)


def test_update_to_latest_sqlite():
    update_to_latest(storage_sqlite)


# Postgres
def test_add_postgres():
    add(storage_postgres)


def test_get_postgres():
    get(storage_postgres)


def test_count_postgres():
    count(storage_postgres)


def test_task_modify_postgres():
    task_modify(storage_postgres)


def test_update_to_latest_postgres():
    update_to_latest(storage_postgres)


# Mysql
def test_add_mysql():
    add(storage_mysql)


def test_get_mysql():
    get(storage_mysql)


def test_count_mysql():
    count(storage_mysql)


def test_task_modify_mysql():
    task_modify(storage_mysql)


def test_update_to_latest_mysql():
    update_to_latest(storage_mysql)


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
