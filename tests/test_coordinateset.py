from pyge import CoordinateSetLoL
from math import nan


def test_coordinatesetlol():
    x = [11, 12, 13, 14, 15]
    y = [21, 22, 23, 24, 25]
    z = [31, 32, 33, 34, 35]
    t = [41, 42, 43, 44, 45]
    lol = CoordinateSetLoL([x, y, z, t])

    assert lol.len() == 5
    assert lol.dim() == 4

    assert lol.get(0) == [11, 21, 31, 41]
    lol.set(0, [1, 2])
    assert lol.get(0) == [1, 2, 31, 41]  # automatic passthru

    # same set & get, but using indexed notation
    assert lol[0] == [1, 2, 31, 41]
    lol[0] = [11, 21]
    assert lol[0] == [11, 21, 31, 41]

    # Promote to 8 dimensions
    mask = [1, 2, 3, 4, 5, 6, 7, 8]
    assert lol.promoted(0, mask) == [11, 21, 31, 41, 5, 6, 7, 8]

    # Default promotion (a no-op in this case)
    assert lol.promoted(1) == [12, 22, 32, 42]

    # Mask overrides existing NaN when default is provided
    lol[1] = [nan]
    assert lol.promoted(1, mask) == [1, 22, 32, 42, 5, 6, 7, 8]

    # Default promotion in the 2D case
    x = [11, 12, 13, 14, 15]
    y = [21, 22, 23, 24, 25]
    lol = CoordinateSetLoL([x, y])
    assert lol.promoted(1) == [12, 22, 0, nan]

    # Mask as Python tuple
    lol[1] = [nan]
    assert lol.promoted(1, (1, 2, 0, 2015)) == [1, 22, 0, 2015]
