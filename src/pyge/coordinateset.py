from abc import ABC, abstractmethod
from math import nan, isnan
from .documentation import Documentation


class CoordinateSet(ABC):
    """Blueprint for the bare minimum functionality for a practically useful
    implementation of the ISO19111 CoordinateSet interface
    """

    @abstractmethod
    def len(self) -> int:
        """Number of coordinate tuples in the set"""
        ...

    @abstractmethod
    def dim(self) -> int:
        """Native dimension of the underlying coordinates"""
        ...

    @abstractmethod
    def get(self, idx: int) -> list[float]:
        """Access the `index`th coordinate tuple"""
        ...

    @abstractmethod
    def set(self, idx: int, value: list[float]):
        """Overwrite the `idx`th coordinate tuple"""
        ...

    def promoted(
        self, idx: int, mask: list[float] | tuple[float] = [nan, nan, 0, nan]
    ) -> list[float]:
        """Promote the n-dimensional base coordinate tuple to the m-dimensions of the mask.

        The default value represents the common case of promoting 2D coordinates to 4D
        by providing values interpretable as a zero ellipsoidal height and an undefined
        time coordinate
        """

        # First, extend the tuple using the tail of the mask
        result = [*self.get(idx), *(mask[self.dim() :])]

        # Then update NaNs in the original coordinate tuple, with mask content
        for (index, value) in enumerate(mask):
            if isnan(result[index]):
                result[index] = float(value)

        return result

    # Support direct indexing. Syntactic sugar for the `set` and `get` methods
    # https://stackoverflow.com/questions/6486387/implement-list-like-index-access-in-python

    def __getitem__(self, key: int) -> list[float]:
        return self.get(key)

    def __setitem__(self, key, value: list[float]):
        self.set(key, value)
        return


class CoordinateSetLoL(CoordinateSet, Documentation):
    """A "List of Lists" based CoordinateSet, where each coordinate (i.e. x,y,z,t)
    resides in a separate list"""

    def __init__(self, args: list[list[float]], crs_id: str = "unknown"):
        """Fill coordinate tuple from args. Ignore superfluous args, provide NaN for missing"""
        self.coords = args
        self_crs_id = crs_id

    def dim(self) -> int:
        return len(self.coords)

    def len(self) -> int:
        return len(self.coords[0])

    def get(self, idx: int) -> list[float]:
        return [float(self.coords[i][idx]) for i in range(self.dim())]

    def set(self, idx: int, value: list[float]):
        for i in range(min(self.dim(), len(value))):
            self.coords[i][idx] = float(value[i])

    # Support direct indexing. Syntactic sugar for the `set` and `get` methods
    # https://stackoverflow.com/questions/6486387/implement-list-like-index-access-in-python

    def __getitem__(self, idx: int) -> list[float]:
        return self.get(idx)

    def __setitem__(self, idx: int, value: list[float]):
        self.set(idx, value)
        return


class ReferenceFrame:
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
