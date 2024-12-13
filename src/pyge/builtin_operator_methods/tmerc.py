"""
Transverse Mercator, following Bowring (1989)
"""

from ..context import Context
from ..coordinateset import CoordinateSet
from ..operator_method import OperatorMethod
from ..operator import Operator
from ..ellipsoid import Ellipsoid
from typing import Any
from math import sin, sinh, cos, radians, atan2, atan, atanh


# Forward transverse mercator, following Bowring (1989)
def tmerc_forward(op: Operator, _ctx: Context, operands: CoordinateSet) -> int:
    if operands.dim() < 2:
        raise ValueError("tmerc: Cannot project 1D data")

    ellps = Ellipsoid.named(op.parameters.get("ellps", "GRS80"))
    eps = ellps.second_eccentricity_squared()

    x_0, y_0, lon_0, lat_0 = op.prepared["offsets"]
    k_0 = op.prepared["k_0"]

    successes = 0
    for i, operand in enumerate(operands):
        lat = operand[1] + lat_0
        s = sin(lat)
        c = cos(lat)
        cc = c * c
        ss = s * s

        dlon = operand[0] - lon_0
        oo = dlon * dlon

        N = ellps.prime_vertical_radius_of_curvature(lat)
        z = eps * dlon**3 * c**5 / 6.0
        sd2 = sin(dlon / 2.0)
        theta_2 = atan2(2.0 * s * c * sd2 * sd2, ss + cc * cos(dlon))

        # Easting
        sd = sin(dlon)
        easting = x_0 + k_0 * N * (
            atanh(c * sd) + z * (1.0 + oo * (36.0 * cc - 29.0) / 10.0)
        )

        # Northing
        # latitude to meridional distance
        m = ellps.meridian_latitude_to_distance(lat)

        znos4 = z * N * dlon * s / 4.0
        ecc = 4.0 * eps * cc
        northing = y_0 + k_0 * (
            m + N * theta_2 + znos4 * (9.0 + ecc + oo * (20.0 * cc - 11.0))
        )
        operands[i] = (easting, northing)
        successes += 1

    return successes


# Inverse transverse mercator, following Bowring (1989)
def tmerc_inverse(op: Operator, _ctx: Context, operands: CoordinateSet) -> int:
    if operands.dim() < 2:
        raise ValueError("tmerc: Cannot project 1D data")

    ellps = Ellipsoid.named(op.parameters.get("ellps", "GRS80"))
    eps = ellps.second_eccentricity_squared()

    x_0, y_0, lon_0, lat_0 = op.prepared["offsets"]
    k_0 = op.prepared["k_0"]

    successes = 0
    for i, operand in enumerate(operands):
        # Footpoint latitude, i.e. the latitude of a point on the central meridian
        # having the same northing as the point of interest
        lat = ellps.meridian_distance_to_latitude((operand[1] - y_0) / k_0)
        N = ellps.prime_vertical_radius_of_curvature(lat)
        s = sin(lat)
        c = cos(lat)
        t = s / c
        cc = c * c

        x = (operand[0] - x_0) / (k_0 * N)
        xx = x * x
        theta_4 = atan2(sinh(x), c)
        theta_5 = atan(t * cos(theta_4))

        # Latitude
        xet = xx * xx * eps * t / 24.0
        lat = (
            lat_0
            + (1.0 + cc * eps) * (theta_5 - xet * (9.0 - 10.0 * cc))
            - eps * cc * lat
        )

        # Longitude
        approx = lon_0 + theta_4
        coef = eps / 60.0 * xx * x * c
        lon = approx - coef * (10.0 - 4.0 * xx / cc + xx * cc)

        operands[i] = (lon, lat)
        successes += 1

    return successes


def tmerc_prepare(parameters: dict[str, str]) -> dict[str, (float)]:
    prepared = {}
    ellps = Ellipsoid.named(parameters.get("ellps", "GRS80"))
    prepared["ellps"] = (ellps.a, ellps.f)
    prepared["offsets"] = (
        OperatorMethod.parameter_as_floats(parameters, "x_0", (0,))[0],
        OperatorMethod.parameter_as_floats(parameters, "y_0", (0,))[0],
        radians(OperatorMethod.parameter_as_floats(parameters, "lon_0", (0,))[0]),
        radians(OperatorMethod.parameter_as_floats(parameters, "lat_0", (0,))[0]),
    )
    prepared["k_0"] = OperatorMethod.parameter_as_floats(parameters, "k_0", (1,))[0]

    return prepared


tmerc = OperatorMethod(
    id="tmerc",
    fwd=tmerc_forward,
    inv=tmerc_inverse,
    prep=tmerc_prepare,
)


def utm_prepare(parameters: dict[str, str]) -> dict[str, Any]:
    prepared = {}
    prepared["ellps"] = Ellipsoid.named(parameters.get("ellps", "GRS80"))

    # The scaling factor is 0.9996 by definition of UTM
    prepared["k_0"] = 0.9996

    # The center meridian is determined by the zone
    zone = OperatorMethod.parameter_as_floats(parameters, "zone")[0]
    prepared["lon_0"] = -183.0 + 6.0 * zone

    # The base parallel is by definition the equator
    prepared["lat_0"] = 0.0

    # The false easting is 500000 m by definition of UTM
    prepared["x_0"] = 500_000

    # The false northing is 0 m by definition of UTM or 10_000_000 m
    # if using the southern aspect
    if "south" in parameters:
        prepared["y_0"] = 10_000_000.0
    else:
        prepared["y_0"] = 0.0

    return prepared


utm = OperatorMethod(
    id="utm",
    fwd=tmerc_forward,
    inv=tmerc_inverse,
    prep=utm_prepare,
)
