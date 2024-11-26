from math import pi
from enum import Enum
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
