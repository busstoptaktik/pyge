from abc import ABC

from math import pi
from enum import Enum
from uuid import uuid4

from .coordinateset import CoordinateSet
from .operation  import Operation

class OpHandle():
    def __init__(self):
        self.handle = uuid4()

class Direction(Enum):
    FWD = True
    INV = False

class Dimension(Enum):
    LINEAR = 1
    ANGULAR = 2
    TEMPORAL = 3

class Unit():
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

UNITS: dict[str, Unit] ={
    'm': Unit('meter', Dimension.LINEAR, 1),
    'ft': Unit('foot', Dimension.LINEAR, 0.3048),
    'deg': Unit('degree', Dimension.ANGULAR, pi/180),
    'gon': Unit('grad', Dimension.ANGULAR, pi/200),
    'a': Unit('year', Dimension.TEMPORAL, 1),
}


class Context(ABC):
    """Modes of communication between the *Rust Geodesy* internals and the external
    world (i.e. resources like grids, transformation definitions, or ellipsoid parameters)."""
    def __init__(self):
        self.ops: dict[OpHandle, Operation]

    def op(self, definition: str) -> OpHandle | None:
        """Instantiate the operation given by `definition`"""
        thehandle = OpHandle()
        theop = Operation(str(thehandle), definition)
        if theop is None:
            return None
        self.ops[thehandle] = theop
        return thehandle

    def apply(self, op: OpHandle, direction: Direction, operands: CoordinateSet) -> int:
        """Apply operation `op` to `operands` in direction Fwd or Inv"""
        if op not in self.ops:
            return 0
        if direction==Direction.Fwd:
            return self.ops[op].fwd(self, operands)
        return self.ops[op].inv(self, operands)
