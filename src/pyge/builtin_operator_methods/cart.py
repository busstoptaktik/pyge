"""Cartesian to  geographic, and v.v."""

from ..context import Context
from ..coordinateset import CoordinateSet
from ..operator_method import OperatorMethod
from ..operator import Operator
from ..ellipsoid import Ellipsoid
from math import nan, hypot, atan2, sqrt


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
    f = ellps.flattening()

    for i in range(len(operands)):
        x, y, z = operands.promoted(i, (nan, nan, 0))
        if two_dimensional:
            longitude = atan2(y, x)
            p = hypot(x, y)

            # What we do below is essentially this:
            #     reduced_latitude = acos(p / a)
            #     latitude = atan(a / b * tan(reduced_latitude))
            # But since the acos in the first line serves only to provide the angle
            # for the tangent in the second, we might as well compute the tangent
            # directly from the cos, i.e. the argument to acos, and the sin computed
            # from the pythagorean identity:
            cos_reduced_latitude = p / a
            sin_reduced_latitude = sqrt(1.0 - cos_reduced_latitude**2.0)
            # But by keeping cos as p / a, when inserting tan = sin/cos into atan's
            # argument, and by using b = (1 - f) * a, we can simplify a bit more:
            #     a / b * sin_reduced_latitude/(p/a) =
            #     a / (1-f) * sin_reduced_latitude/p
            # Finally, we avoid division by zero at the poles, where p==0,
            # by switching atan(y/x) to atan2(y, x):
            latitude = atan2(a * sin_reduced_latitude, (1 - f) * p)
            # Hence reducing 3 trig calls to one trig call and a square root,
            # all while solving a stability issue for free.

            if south:
                latitude = -latitude
            operands[i] = (longitude, latitude)
        else:
            operands[i] = ellps.geographic(x, y, z)

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
