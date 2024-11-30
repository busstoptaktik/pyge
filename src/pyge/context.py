from abc import ABC, abstractmethod

from .coordinateset import CoordinateSet
from .operator_method import OperatorMethod

from uuid import uuid4
from dataclasses import dataclass, field
from enum import Enum


@dataclass(frozen=True)
class OpHandle:
    """A type-wrapped uuid for identifying an Operation instantiated via a Context"""

    handle: uuid4 = field(default_factory=uuid4)


class OpDirection(Enum):
    """Designate whether an operation should be carried out
    in the forward or inverse direction"""

    FWD = True
    INV = False


class Context(ABC):
    """Modes of communication between the PyGe internals and the external
    world (i.e. resources like grids, transformation definitions, or ellipsoid parameters)."""

    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    def register_method(self, user_defined_method: OperatorMethod):
        """Add a user defined method to the gamut of the context"""
        ...

    @abstractmethod
    def method(self, id: str) -> OperatorMethod | None:
        """The OperatorMethod representation of the operator method named `id`"""
        ...

    @abstractmethod
    def builtins(self) -> tuple[str]:
        """The names of all built in operator methods"""
        ...

    @abstractmethod
    def op(self, definition: str) -> OpHandle | None:
        """Instantiate the operation given by `definition`"""
        ...

    @abstractmethod
    def apply(
        self, op: OpHandle, direction: OpDirection, operands: CoordinateSet
    ) -> int:
        """Apply operation `op` to `operands` in direction `FWD` or `INV`"""
        ...
