from pyge import Crs


def test_crs():
    etrs89dnk = Crs(id="etrs89dnk", family="etrs89", units=("m", "m", "m", "y"))

    assert etrs89dnk.attrs == {}
    assert etrs89dnk.base_id == None
    assert etrs89dnk.family == "etrs89"
    assert etrs89dnk.crs_id == "etrs89dnk"
    assert etrs89dnk.units == ("m", "m", "m", "y")

    # Optional documentation
    assert etrs89dnk.brief == None
