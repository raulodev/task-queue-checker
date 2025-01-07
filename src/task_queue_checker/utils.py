import pickle
from typing import Any, List, Tuple, Union

from .types import Task


def get_tasks(
    self, result: Union[List[Tuple[Any, ...]], Tuple[Any, ...], None], _all: bool
):
    if result is not None:
        if _all:

            tasks = []

            for index, r in enumerate(result):

                tasks.append(get_task(r, self, index))

            return tasks

        return get_task(result, self)

    return None


def get_task(result, self, index=-1):

    is_bytes = isinstance(result, bytes)

    result_load = pickle.loads(result) if is_bytes else result

    _id = index if is_bytes else result_load[0]
    timestamp = result_load[1] if is_bytes else result_load[2]

    if is_bytes:
        data = result_load[0]
    else:
        data = pickle.loads(result_load[1])

    return Task(_id=_id, data=data, timestamp=timestamp, storage=self)
