from abc import ABC
from math import sqrt, hypot, atan2, sin, cos, radians, degrees, copysign, pi, nan


class CoordinateTuple(ABC):
    def dim(self) -> int:
        ...

    def as_list(self) -> list[float, float, float, float]:
        ...

    def as_tuple(self) -> tuple[float, float, float, float]:
        return tuple(self.as_list())

    def set(self, idx: int):
        ...

    def get(self, idx: int) -> float:
        ...

    # https://stackoverflow.com/questions/6486387/implement-list-like-index-access-in-python
    def __getitem__(self, key):
        ...

    # return some_value_related_to_key

    def __setitem__(self, key, value):
        ...

    # set value (if needed)


class Coor4D(CoordinateTuple):
    def __init__(self, x, y, z, t):
        self.c = [x, y, z, t]

    c = [nan, nan, nan, nan]

    def dim(self) -> int:
        return 4
