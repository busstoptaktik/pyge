import pytest

from pyge.ellipsoid import Ellipsoid
from math import hypot, degrees, radians


def test_ellipsoid():
    # Trying to instantiate an ellipsoid with an undefined name
    # should raise an exception
    with pytest.raises(Exception):
        Ellipsoid.named("Undefined ellipsoid name")

    # Some basic properties on a named ellipsoid
    e = Ellipsoid.named("GRS80")
    assert abs(e.eccentricity() - 0.08181919104283186) < 1e-15
    assert abs(e.eccentricity_squared() - 0.006694380022903417) < 1e-15
    assert e.a == 6378137

    # Init by (a, rf) pair should give identical results as by name
    n = Ellipsoid(6378137, 298.2572221008827)
    assert n.f == e.f
    assert n.a == e.a

    # Geographic to cartesian
    (x, y, z) = e.cartesian(radians(12), radians(55), 100)
    (xx, yy, zz) = (3586525.7611, 762339.5841, 5201465.4383)
    assert hypot(x - xx, hypot(y - yy, z - zz)) < 1e-3

    # Cartesian to geographic
    (lon, lat, h) = e.geographic(x, y, z)
    lon = degrees(lon)
    lat = degrees(lat)
    assert hypot(lon - 12, lat - 55) < 1e-12
    assert abs(h - 100) < 1e-5
