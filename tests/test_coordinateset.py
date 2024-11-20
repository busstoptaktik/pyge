from pyge import CoordinateSetColumnWise, CoordinateSetRowWise
from math import nan


def test_coordinatesetsoa():
    x = [11, 12, 13, 14, 15]
    y = [21, 22, 23, 24, 25]
    z = [31, 32, 33, 34, 35]
    t = [41, 42, 43, 44, 45]
    soa = CoordinateSetColumnWise([x, y, z, t])

    assert len(soa) == soa.len()
    assert soa.len() == 5
    assert soa.dim() == 4

    for i in range(len(soa)):
        assert soa[i][0] in x

    assert soa.get(0) == [11, 21, 31, 41]
    soa.set(0, [1, 2])
    assert soa.get(0) == [1, 2, 31, 41]  # automatic passthru

    # same set & get, but using indexed notation
    assert soa[0] == [1, 2, 31, 41]
    soa[0] = [11, 21]
    assert soa[0] == [11, 21, 31, 41]

    # Promote to 8 dimensions
    mask = [1, 2, 3, 4, 5, 6, 7, 8]
    assert soa.promoted(0, mask) == [11, 21, 31, 41, 5, 6, 7, 8]

    # Default promotion (a no-op in this case)
    assert soa.promoted(1) == [12, 22, 32, 42]

    # Mask overrides existing nan when default is provided and
    # automatic passthru preserves untouched existing dimensions
    # when overwriting with lower dimensional arg
    soa[1] = [nan]
    assert soa.promoted(1, mask) == [1, 22, 32, 42, 5, 6, 7, 8]

    # Default promotion in the 2D case
    x = [11, 12, 13, 14, 15]
    y = [21, 22, 23, 24, 25]
    soa = CoordinateSetColumnWise([x, y])
    assert soa.promoted(1) == [12, 22, 0, nan]

    # Mask as Python tuple
    soa[1] = [nan]
    assert soa.promoted(1, (1, 2, 0, 2015)) == [1, 22, 0, 2015]

    # Documentation
    assert soa.item_name is None
    assert soa.brief is None


def test_coordinatesetaos():
    x1 = [11, 12, 13, 14]
    x2 = [21, 22, 23, 24]
    x3 = [31, 32, 33, 34]
    x4 = [41, 42, 43, 44]
    x5 = [51, 52, 53, 54]
    aos = CoordinateSetRowWise([x1, x2, x3, x4, x5])

    assert len(aos) == aos.len()
    assert aos.len() == 5
    assert aos.dim() == 4

    for i in range(len(aos)):
        assert aos[i][0] in [11, 21, 31, 41, 51]

    assert aos.get(0) == [11, 12, 13, 14]
    aos.set(0, [1, 2])
    assert aos.get(0) == [1, 2, 13, 14]  # automatic passthru

    # same set & get, but using indexed notation
    assert aos[0] == [1, 2, 13, 14]
    aos[0] = [11, 21]
    assert aos[0] == [11, 21, 13, 14]

    # Promote to 8 dimensions
    mask = [1, 2, 3, 4, 5, 6, 7, 8]
    assert aos.promoted(0, mask) == [11, 21, 13, 14, 5, 6, 7, 8]

    # Default promotion (a no-op in this case)
    assert aos.promoted(1) == [21, 22, 23, 24]

    # Mask overrides existing nan when default is provided
    aos[1] = [nan]
    assert aos.promoted(1, mask) == [1, 22, 23, 24, 5, 6, 7, 8]

    # Default promotion in the 2D case
    x = [11, 12, 13, 14, 15]
    y = [21, 22, 23, 24, 25]
    aos = CoordinateSetColumnWise([x, y])
    assert aos.promoted(1) == [12, 22, 0, nan]

    # Mask as Python tuple
    aos[1] = [nan]
    assert aos.promoted(1, (1, 2, 0, 2015)) == [1, 22, 0, 2015]

    # Documentation
    assert aos.item_name is None
    assert aos.brief is None
