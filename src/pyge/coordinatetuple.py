"""
Generic abstract class for coordinate tuples.

Also concrete implementations for 1-4 dimensions:
Coor1D, Coor2D, Coor3D, Coor4D.

Note that this class is largely useless: It is here because coordinate tuples are
part of the ISO 19111 standard, and are conceptually useful. They are, however,
not particularly practical.

The main interface between application coordinate data and Python Geodesy is via the
CoordinateSet ABC (or interface in UML lingo), which consists of just 4 methods.

These 4 methods can be implemented for a concrete data storage architecture in
typically as little as 20 lines of code (cf. `CoordinateSetColumnWise` and
`CoordinateSetRowWise`, the concrete demo implementations in coordinateset.py)
"""

from abc import ABC, abstractmethod
from math import nan, isnan


class CoordinateTuple(ABC):
    """Bare minimum blueprint for a coordinate tuple class"""

    def dim(self) -> int:
        return len(self.as_list())

    @abstractmethod
    def as_list(self) -> list[float]: ...

    def as_promoted_list(
        self, mask: list[float] | tuple[float] = [nan, nan, 0, nan]
    ) -> list[float]:
        """
        Promote the n-dimensional base coordinate tuple to the m-dimensions of the mask.

        The default value represents the common case of promoting 2D coordinates to 4D
        by providing values interpretable as a zero ellipsoidal height and an undefined
        time coordinate
        """

        # First, extend the tuple using the tail of the mask
        result = [*self.as_list(), *(mask[self.dim() :])]

        # Then update NaNs in the original coordinate tuple, with mask content
        for index, value in enumerate(mask):
            if isnan(result[index]):
                result[index] = float(value)

        return result

    def as_tuple(self) -> tuple[float]:
        return tuple(self.as_list())

    @abstractmethod
    def set(self, idx: int, value: float):
        """Return the `idx`th element of the CoordinateTuple, or `nan` if out-of-range"""
        ...

    @abstractmethod
    def get(self, idx: int) -> float:
        """Modify the `idx`th element of the CoordinateTuple. Do nothing if out-of-range"""
        ...

    # Support direct indexing. Syntactic sugar for the `set` and `get` methods
    # https://stackoverflow.com/questions/6486387/implement-list-like-index-access-in-python

    def __getitem__(self, idx: int) -> float:
        return self.get(idx)

    def __setitem__(self, idx: int, value: float):
        self.set(idx, value)
        return

    # The __init__ method asserts that the actual coordinate values are stored
    # in the field `self.c`, which is the case for the provided Coor4D, Coord3D,
    # Coord2D, and Coor1D classes. In other cases, the concrete class must
    # provide a concrete implementation of this abstract __init__

    def __init__(self, *args):
        """Fill coordinate tuple from args. Ignore superfluous args, provide NaN for missing"""
        args = [*args, *[nan] * self.dim()]
        self.c = args[0 : self.dim()]


class Coor4D(CoordinateTuple):
    """4D coordinate tuple"""

    @property
    def brief(self) -> str | None:
        return "Generic 4D coordinate tuple"

    def dim(self) -> int:
        return 4

    def get(self, key: int) -> float:
        if key < 0 or key > 3:
            return nan
        return self.c[key]

    def set(self, key: int, value: float):
        if key < 0 or key > 3:
            return
        self.c[key] = float(value)
        return

    def as_list(self):
        return self.c


class Coor3D(CoordinateTuple):
    """3D coordinate tuple"""

    @property
    def brief(self) -> str | None:
        return "Generic 3D coordinate tuple"

    def dim(self) -> int:
        return 3

    def get(self, key: int) -> float:
        if key < 0 or key > 2:
            return nan
        return self.c[key]

    def set(self, key: int, value: float):
        if key < 0 or key > 2:
            return
        self.c[key] = float(value)
        return

    def as_list(self):
        return self.c


class Coor2D(CoordinateTuple):
    """4D coordinate tuple"""

    @property
    def brief(self) -> str | None:
        return "Generic 2D coordinate tuple"

    def dim(self) -> int:
        return 2

    def get(self, key: int) -> float:
        if key < 0 or key > 1:
            return nan
        return self.c[key]

    def set(self, key: int, value: float):
        if key < 0 or key > 1:
            return
        self.c[key] = float(value)
        return

    def as_list(self):
        return self.c


class Coor1D(CoordinateTuple):
    """1D coordinate tuple"""

    @property
    def brief(self) -> str | None:
        return "Generic 1D coordinate tuple"

    def __init__(self, z: float):
        self.c = [float(z)]

    def dim(self) -> int:
        return 1

    def get(self, key: int) -> float:
        if key != 0:
            return nan
        return self.c[key]

    def set(self, key: int, value: float):
        if key != 0:
            return
        self.c[key] = float(value)
        return

    def as_list(self):
        return self.c
