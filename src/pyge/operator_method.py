from dataclasses import dataclass
from typing import Callable
from .registeritem import RegisterItem


@dataclass(frozen=True, kw_only=True)
class OperatorMethod(RegisterItem):
    """For description and representation of the fwd/inv functionality of an operator method"""

    id: str
    description: str = ""
    fwd: Callable
    inv: Callable | None = None

    @property
    def invertible(self) -> bool:
        return self.inv is not None
