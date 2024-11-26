from pyge import Crs


def test_crs():
    etrs89dnk = Crs(id="etrs89dnk", units=("m", "m", "m", "y"))

    assert etrs89dnk.attrs == {}
    assert etrs89dnk.parent_id == None
    assert etrs89dnk.id == "etrs89dnk"
    assert etrs89dnk.units == ("m", "m", "m", "y")

    # Optional documentation
    assert etrs89dnk.brief == None
