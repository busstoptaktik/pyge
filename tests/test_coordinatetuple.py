from math import nan, isnan
from pyge import Coor4D, Coor3D, Coor2D, Coor1D


def test_coor4d():
    cc = Coor4D(1.0, 2.0, 3.0, 4.0)
    assert cc.dim() == 4

    # Indexing via __getitem__/__setitem__
    assert cc[1] == 2
    cc[1] = 55
    assert cc[1] == 55

    # Reading out-of-range returns NaN
    assert isnan(cc[1000])
    assert isnan(cc[-1])

    # Writing out-of-range is a no-op
    cc[1000] = 5
    cc[-1] = 5

    # as_list is explicitly implemented by Coor4D
    assert cc.as_list() == [1.0, 55.0, 3.0, 4.0]

    # as_tuple() defers to the blanket implementation from the
    # abstract base class `CoordinateTuple`
    assert cc.as_tuple() == (1.0, 55.0, 3.0, 4.0)

    # Missing initializers default to NaN
    cc = Coor4D(1)
    # List does the sensible (but formally wrong) thing when comparing NaNs!
    assert cc.as_list() == [1.0, nan, nan, nan]

    # Superfluous initializers are ignored
    cc = Coor4D(1, 2, 3, 4, 5, 6, 7, 8, 9)
    assert cc.as_list() == [1.0, 2.0, 3.0, 4.0]

    # Inherited documentation elements
    assert cc.authority == None
    assert len(cc.crossref) == 0
    print(f"item_name {cc.item_name} aha!")
    print(f"item_name {cc.brief} aha!")

    # Overwritten element
    assert cc.brief == "Generic 4D coordinate tuple"


def test_coor3d():
    cc = Coor3D(1.0, 2.0, 3.0)
    assert cc.dim() == 3

    assert cc[1] == 2
    cc[1] = 55
    assert cc[1] == 55

    assert isnan(cc[1000])
    assert isnan(cc[-1])

    cc[1000] = 5
    cc[-1] = 5

    assert cc.as_list() == [1.0, 55.0, 3.0]
    assert cc.as_tuple() == (1.0, 55.0, 3.0)


def test_coor2d():
    cc = Coor2D(1.0, 2.0)
    assert cc.dim() == 2

    assert cc[1] == 2
    cc[1] = 55
    assert cc[1] == 55

    cc[1000] = 5
    cc[-1] = 5

    assert isnan(cc[1000])
    assert isnan(cc[-1])

    assert cc.as_list() == [1.0, 55.0]
    assert cc.as_tuple() == (1.0, 55.0)

    # Promote a 2D coordinate tuple to 4D
    mask = nan, nan, 0.0, 2020.0
    assert cc.as_promoted_list(mask) == [1.0, 55.0, 0.0, 2020.0]

    # Nothing happens for shorter masks
    mask = [0, 2020]
    assert cc.as_promoted_list(mask) == [1.0, 55.0]
    mask = []
    assert cc.as_promoted_list(mask) == [1.0, 55.0]

    # Fill in also works
    mask = 1, 2, nan, nan, 456
    cc = Coor2D(nan, nan)
    assert cc.as_promoted_list(mask) == [1.0, 2.0, nan, nan, 456.0]

    # The default value for mask is [nan, nan, 0, nan]
    cc = Coor2D(1, 2)
    assert cc.as_promoted_list() == [1.0, 2.0, 0.0, nan]


def test_coor1d():
    cc = Coor1D(1.0)
    assert cc.dim() == 1

    assert cc[0] == 1
    cc[0] = 55
    assert cc[0] == 55

    cc[1000] = 5
    cc[-1] = 5

    assert isnan(cc[1])
    assert isnan(cc[-1])

    assert cc.as_list() == [55.0]
    assert cc.as_tuple() == (55.0,)
