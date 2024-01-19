from typing import Tuple, Any, List, Union
import pickle
from .types import Task


def get_tasks(
    self, result: Union[List[Tuple[Any, ...]], Tuple[Any, ...], None], _all: bool
):
    if result is not None:
        if _all:
            return [
                Task(
                    _id=r[0],
                    data=pickle.loads(r[1]),
                    timestamp=r[2],
                    storage=self,
                )
                for r in result
            ]

        return Task(
            _id=result[0],
            data=pickle.loads(result[1]),
            timestamp=result[2],
            storage=self,
        )

    return None
