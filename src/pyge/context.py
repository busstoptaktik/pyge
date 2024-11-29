from abc import ABC

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


class Context(ABC):
    """Modes of communication between the *Rust Geodesy* internals and the external
    world (i.e. resources like grids, transformation definitions, or ellipsoid parameters)."""

    def __init__(self): ...

    def register_method(self, user_defined_method: OperatorMethod):
        """Add a user defined method to the gamut of the context"""
        ...

    def method(self, id: str) -> OperatorMethod | None:
        """The OperatorMethod representation of the operator method named `id`"""
        ...

    def builtins(self) -> tuple[str]:
        """The names of all built in operator methods"""
        ...

    def op(self, definition: str) -> OpHandle | None:
        """Instantiate the operation given by `definition`"""
        ...

    def apply(
        self, op: OpHandle, direction: OpDirection, operands: CoordinateSet
    ) -> int:
        """Apply operation `op` to `operands` in direction `FWD` or `INV`"""
        ...
