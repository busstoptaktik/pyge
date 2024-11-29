from abc import ABC

from math import pi
from enum import Enum
from uuid import uuid4

from .coordinateset import CoordinateSet
from .operator_method import OperatorMethod


class OpHandle:
    """A type-wrapped uuid for identifying an Operation instantiated via a Context"""

    def __init__(self):
        self.handle = uuid4()


class OpDirection(Enum):
    """Designate whether an operation should be carried out
    in the forward or inverse direction"""

    FWD = True
    INV = False


class Dimension(Enum):
    LINEAR = 1
    ANGULAR = 2
    TEMPORAL = 3


class Unit:
    id: str
    kind: Dimension
    scale: float
    offset: float

    def __init__(self, id: str, kind: Dimension, scale: float, offset: float = 0):
        self.id = id
        self.kind = kind
        self.scale = scale
        self.offset = offset

    def si(self, value: float):
        return (value - self.offset) * self.scale

    def into(self, value: float):
        return (value / self.scale) + self.offset


UNITS: dict[str, Unit] = {
    "m": Unit("meter", Dimension.LINEAR, 1),
    "ft": Unit("foot", Dimension.LINEAR, 0.3048),
    "deg": Unit("degree", Dimension.ANGULAR, pi / 180),
    "gon": Unit("grad", Dimension.ANGULAR, pi / 200),
    "a": Unit("year", Dimension.TEMPORAL, 1),
}


class Context(ABC):
    """Modes of communication between the *Rust Geodesy* internals and the external
    world (i.e. resources like grids, transformation definitions, or ellipsoid parameters)."""

    def __init__(self): ...

    def method(self, id) -> OperatorMethod | None: ...

    def op(self, definition: str) -> OpHandle | None:
        """Instantiate the operation given by `definition`"""
        ...

    def apply(
        self, op: OpHandle, direction: OpDirection, operands: CoordinateSet
    ) -> int:
        """Apply operation `op` to `operands` in direction Fwd or Inv"""
        ...
