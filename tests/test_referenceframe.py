import pytest
import math

from pyge.coordinateset import ReferenceFrame

# from pyge import Coor4D, Aggurg
from math import hypot, degrees, radians


def test_referenceframe():
    etrs89 = ReferenceFrame("etrs89", ("m", "m", "m", "y"))
    assert etrs89.name == "etrs89"
    assert etrs89.units[2] == "m"
    assert etrs89.attrs == {}
