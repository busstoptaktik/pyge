"""Cartesian to  geographic, and v.v."""

from ..context import Context
from ..coordinateset import CoordinateSet
from ..operator_method import OperatorMethod
from ..operator import Operator
from ..ellipsoid import Ellipsoid
from math import nan, hypot, tan, atan, atan2, acos


def cart_forward(op: Operator, _ctx: Context, operands: CoordinateSet) -> int:
    if operands.dim() < 2:
        raise ValueError("cart: Cannot map 1D data")

    ellps = Ellipsoid.named(op.parameters.get("ellps", "GRS80"))

    for i in range(len(operands)):
        longitude, latitude, height = operands.promoted(i, (nan, nan, 0))
        operands[i] = ellps.cartesian(longitude, latitude, height)
    return len(operands)


def cart_inverse(op: Operator, _ctx: Context, operands: CoordinateSet) -> int:
    if operands.dim() < 2:
        raise ValueError("cart: Cannot map 1D data")

    ellps = Ellipsoid.named(op.parameters.get("ellps", "GRS80"))
    two_dimensional = operands.dim() == 2
    south = op.prepared["south"]
    a = ellps.semimajor_axis()
    b = ellps.semiminor_axis()

    for i in range(len(operands)):
        x, y, z = operands.promoted(i, (nan, nan, 0))
        if two_dimensional:
            longitude = atan2(y, x)
            p = hypot(x, y)
            reduced_latitude = acos(p / a)
            latitude = atan(a / b * tan(reduced_latitude))
            if south:
                latitude = -latitude
            operands[i] = (longitude, latitude)
            print("TWO")
        else:
            operands[i] = ellps.geographic(x, y, z)
            print("THREE")

    return len(operands)


def cart_prepare(parameters: dict[str, str]) -> dict[str, (float)]:
    prepared = {}
    prepared["south"] = "south" in parameters
    return prepared


cart = OperatorMethod(
    id="cart",
    fwd=cart_forward,
    inv=cart_inverse,
    prep=cart_prepare,
)
