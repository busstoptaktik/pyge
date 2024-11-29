from abc import ABC, abstractmethod
from .registeritem import RegisterItem


class CrsBase(ABC):
    @abstractmethod
    def len(self) -> int:
        """Number of compounded CRSs"""
        ...

    @abstractmethod
    def dim(self) -> int:
        """Native dimension of coordinate tuples referred to this (potentially compound) CRS"""
        ...

    @abstractmethod
    def parts(self) -> tuple:
        """A tuple of the constituent CRSs"""
        ...

    def __len__(self) -> int:
        return self.len()


class Crs(CrsBase, RegisterItem):
    """Attempt at a potentially simplified CRS class"""

    def __init__(
        self,
        id: str,
        parent_id: str | None = None,
        parts: tuple[CrsBase] = (),
        units: tuple[str] = (),
        norvis: tuple[int] = (1, 2, 3, 4),
        attrs: dict[str, str] = {},
    ):
        self.id = id
        self.parent_id = parent_id
        self.parts = parts
        self.units = units
        self.norvis = norvis
        self.attrs = attrs

    def dim(self) -> int:
        return len(self.units)

    def len(self) -> int:
        return len(self.parts)

    def parts(self) -> tuple[CrsBase]:
        return self.parts
