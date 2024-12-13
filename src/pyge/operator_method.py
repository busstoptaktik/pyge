from dataclasses import dataclass
from typing import Callable, Any
from .registeritem import RegisterItem
from math import isnan


@dataclass(frozen=True, kw_only=True)
class OperatorMethod(RegisterItem):
    """For description and representation of the fwd/inv functionality of an operator method"""

    id: str
    description: str = ""
    fwd: Callable
    inv: Callable | None = None
    prep: Callable | None = None

    @property
    def invertible(self) -> bool:
        return self.inv is not None

    def forward(self) -> Callable:
        return self.fwd

    def inverse(self) -> Callable | None:
        return self.inv

    def prepare(self, parameters: dict[str, str]) -> dict[str, Any]:
        if self.prep is not None:
            return self.prep(parameters)
        return {}

    def parameter_as_floats(
        parameters: dict[str, str], param: str, mask: list[float] | tuple[float] = ()
    ) -> tuple[float]:
        """
        Convert the value of parameter `param` to a list of floats

        The mask provides defaults and extension values to pad the value to the expected dimension.
        """

        if param in parameters:
            values = [float(v) for v in parameters[param].split(",")]
        else:
            values = []

        # If too short, extend the values using the tail of the mask
        n = len(values)
        if n < len(mask):
            values.extend([float(v) for v in mask[n:]])

        # Then update NaNs in the original coordinate tuple, with mask content
        for index, mask_value in enumerate(mask):
            if isnan(values[index]):
                values[index] = float(mask_value)

        return tuple(values)

    def parameter_as_strs(
        parameters: dict[str, str], param: str, mask: list[str] | tuple[str] = ()
    ) -> tuple[str]:
        """
        Convert the value of parameter `param` to a list of strings

        The mask provides defaults and extension values to pad the value to the expected dimension.
        """

        if param in parameters:
            values = [v for v in parameters[param].split(",")]
        else:
            values = []

        # If too short, extend the values using the tail of the mask
        n = len(values)
        if n < len(mask):
            values.extend(mask[n:])

        # Then update empty strings in the original coordinate tuple, with mask content
        for index, mask_value in enumerate(mask):
            if values[index] == "":
                values[index] = mask_value

        return tuple(values)
