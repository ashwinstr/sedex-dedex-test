
from typing import Callable, List, Any

from ..ext import RawClient


_PYROFUNC = Callable[['types.bound.Message'], Any]


class RawDecorator(RawClient):
    """ userge raw decoretor """
    _PYRORETTYPE = Callable[[_PYROFUNC], _PYROFUNC]

    def __init__(self, **kwargs) -> None:
        self.manager = types.new.Manager(self)
        self._tasks: List[Callable[[], Any]] = []
        super().__init__(**kwargs)