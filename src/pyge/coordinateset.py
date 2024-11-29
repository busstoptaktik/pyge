from abc import ABC, abstractmethod
from math import nan, isnan


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
        for index, value in enumerate(mask):
            if isnan(result[index]):
                result[index] = float(value)

        return result

    # Support direct indexing. Syntactic sugar for the `set` and `get` methods
    # https://stackoverflow.com/questions/6486387/implement-list-like-index-access-in-python

    def __getitem__(self, idx: int) -> list[float]:
        return self.get(idx)

    def __setitem__(self, idx: int, value: list[float]):
        self.set(idx, value)
        return

    def __len__(self) -> int:
        return self.len()


#
# Demo implementations
#


class CoordinateSetColumnWise(CoordinateSet):
    """A column-store (struct-of-arrays) based CoordinateSet,
    where each coordinate dimension (i.e. x,y,z,t) resides in a separate list"""

    def __init__(self, args: list[list[float]], crs_id: str = "unknown"):
        self.coords = args
        self.crs_id = crs_id

    def len(self) -> int:
        return len(self.coords[0])

    def dim(self) -> int:
        return len(self.coords)

    def get(self, idx: int) -> list[float]:
        return [float(self.coords[i][idx]) for i in range(self.dim())]

    def set(self, idx: int, value: list[float]):
        for i in range(min(self.dim(), len(value))):
            self.coords[i][idx] = float(value[i])


class CoordinateSetRowWise(CoordinateSet):
    """A row-store (array-of-structs) based CoordinateSet, where the data is
    accessed as a list of coordinate tuples (encoded as lists)
    """

    def __init__(self, args: list[list[float]], crs_id: str = "unknown"):
        self.coords = args
        self.crs_id = crs_id

    def len(self) -> int:
        return len(self.coords)

    def dim(self) -> int:
        return len(self.coords[0])

    def get(self, idx: int) -> list[float]:
        return [float(self.coords[idx][i]) for i in range(self.dim())]

    def set(self, idx: int, value: list[float]):
        for i in range(min(self.dim(), len(value))):
            self.coords[idx][i] = float(value[i])
