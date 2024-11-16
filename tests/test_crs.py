from pyge import CoordinateSetLoL, Crs
from math import nan


def test_crs():
    etrs89dnk = Crs(id="etrs89dnk", family="etrs89", units=("m", "m", "m", "y"))

    assert etrs89dnk.attrs == {}
    assert etrs89dnk.base_id == None
    assert etrs89dnk.family == "etrs89"
    assert etrs89dnk.crs_id == "etrs89dnk"
    assert etrs89dnk.units == ("m", "m", "m", "y")

    # Optional documentation
    assert etrs89dnk.brief == None


# etrs89_xyz_to_geo = {
#     "from": "etrs89_xyz",
#     "to": "etrs89_geo",
#     "op": "inv cart ellps=GRS80",
#     "invertible": True,
# }
