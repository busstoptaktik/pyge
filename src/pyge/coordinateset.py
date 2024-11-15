from abc import ABC, abstractmethod
from math import sqrt, hypot, atan2, sin, cos, radians, degrees, copysign, pi, nan
from .coordinatetuple import CoordinateTuple


class CoordinateSet(ABC):
    """Blueprint for the bare minimum functionality of an implementation of the ISO19111 CoordinateSet"""

    def len(self) -> int:
        """Number of coordinate tuples in the set"""
        ...

    def dim(self) -> int:
        """Native dimension of the underlying coordinates"""
        ...

    def get(self, index: int) -> CoordinateTuple:
        """Access the `index`th coordinate tuple"""
        ...

    def set(self, idx: int, value: CoordinateTuple):
        """Overwrite the `index`th coordinate tuple"""
        ...

    # Support direct indexing. Syntactic sugar for the `set` and `get` methods
    # https://stackoverflow.com/questions/6486387/implement-list-like-index-access-in-python
    def __getitem__(self, key: int) -> float:
        return self.get(key)

    def __setitem__(self, key, value: float):
        self.set(key, value)
        return


class Datum(ABC):
    def __init__(self, name: str, units: tuple[str], attrs: dict[str, str] = {}):
        ...

    def dim(self) -> int:
        ...


class DatumEnsemble(ABC):
    def __init__(self, name: str, units: tuple[str], attrs: dict[str, str] = {}):
        ...

    def dim(self) -> int:
        ...


class ReferenceFrame(Datum):
    name: str = None
    units: tuple[str] = ()
    attrs: dict[str, str] = {}

    def __init__(self, name: str, units: tuple[str], attrs: dict[str, str] = {}):
        self.name = name
        self.units = units
        self.attrs = attrs

    def dim(self) -> int:
        return len(self.units)


etrs89_xyz_to_geo = {
    "from": "etrs89_xyz",
    "to": "etrs89_geo",
    "op": "inv cart ellps=GRS80",
    "invertible": True,
}

etrs89 = ReferenceFrame("etrs89", ("m", "m", "m", "y"))

print(etrs89_xyz_to_geo)
print(etrs89.units, etrs89.name, etrs89.attrs, etrs89.dim())

etrs89 = ReferenceFrame("etrs89", ("m", "m", "m", "y"), {"bonk": "duns", "foo": "bar"})

print(etrs89_xyz_to_geo)
print(etrs89.units, etrs89.name, etrs89.attrs, etrs89.dim())

mytuple = ("apple", "banana", "cherry")

for x in mytuple:
    print(x)


def funcy(town):
    return 42


mylist = ["apple", "banana", "cherry"]

mytuple = tuple(funcy(town) for town in mytuple)
print(mylist, mytuple)
