"""handle different input/output axis order and unit conventions"""

from ..context import Context
from ..coordinateset import CoordinateSet
from ..operator_method import OperatorMethod
from ..operator import Operator
from math import radians, degrees


# Geo: (Latitude, Longitude) in degrees to (Longitude, Latitude) in radians
def geo_forward(op: Operator, _ctx: Context, operands: CoordinateSet) -> int:
    if operands.dim() < 2:
        raise ValueError("geo: Cannot handle 1D data")

    for i, operand in enumerate(operands):
        operands[i] = (radians(operand[1]), radians(operand[0]))
    return len(operands)


def geo_inverse(op: Operator, _ctx: Context, operands: CoordinateSet) -> int:
    if operands.dim() < 2:
        raise ValueError("geo: Cannot handle 1D data")

    for i, operand in enumerate(operands):
        operands[i] = (degrees(operand[1]), degrees(operand[0]))
    return len(operands)


# GIS: (Longitude, Latitude) in degrees to (Longitude, Latitude) in radians
def gis_forward(op: Operator, _ctx: Context, operands: CoordinateSet) -> int:
    if operands.dim() < 2:
        raise ValueError("gis: Cannot handle 1D data")

    for i, operand in enumerate(operands):
        operands[i] = (radians(operand[0]), radians(operand[1]))
    return len(operands)


def gis_inverse(op: Operator, _ctx: Context, operands: CoordinateSet) -> int:
    if operands.dim() < 2:
        raise ValueError("gis: Cannot handle 1D data")

    for i, operand in enumerate(operands):
        operands[i] = (degrees(operand[0]), degrees(operand[1]))
    return len(operands)


geo = OperatorMethod(
    id="geo",
    fwd=geo_forward,
    inv=geo_inverse,
)

gis = OperatorMethod(
    id="gis",
    fwd=gis_forward,
    inv=gis_inverse,
)


# ne: (northing, easting) in meter to (easting, northing) in meter
def ne_both(op: Operator, _ctx: Context, operands: CoordinateSet) -> int:
    if operands.dim() < 2:
        raise ValueError("ne: Cannot handle 1D data")

    for i, operand in enumerate(operands):
        operands[i] = (operand[1], operand[0])
    return len(operands)


# Note: ne is an involution - its inverse is identical to itself
ne = OperatorMethod(
    id="ne",
    fwd=ne_both,
    inv=ne_both,
)
