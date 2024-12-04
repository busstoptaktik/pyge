from pyge.coordinateset import (
    CoordinateSet,
    CoordinateSetColumnWise,
    CoordinateSetRowWise,
)
from math import nan

# Canonical dataset for testing of implementers of abstract base class
# CoordinateSet
coordinate_tuples = [
    [11, 12, 13, 14],
    [21, 22, 23, 24],
    [31, 32, 33, 34],
    [41, 42, 43, 44],
    [51, 52, 53, 54],
]


# Testing any object implementing the abstract base class "CoordinateSet",
# under the assumption that its payload corresponds to the list-of-lists
# coordinate_tuples above
def abstract_test_coordinateset(coords: CoordinateSet):
    assert coordinate_tuples[0] == [11, 12, 13, 14]

    assert len(coords) == coords.len()
    assert coords.len() == 5
    assert coords.dim() == 4

    for i in range(len(coords)):
        assert coords[i][0] == coordinate_tuples[i][0]

    assert coords.get(0) == coordinate_tuples[0]
    coords.set(0, [1, 2])
    assert coords.get(0) == [1, 2, 13, 14]  # automatic passthru

    # same set & get, but using indexed notation
    assert coords[0] == [1, 2, 13, 14]
    coords[0] = [11, 12]
    assert coords[0] == [11, 12, 13, 14]

    # Promote to 8 dimensions
    mask = [1, 2, 3, 4, 5, 6, 7, 8]
    assert coords.promoted(0, mask) == [11, 12, 13, 14, 5, 6, 7, 8]

    # Default promotion (a no-op in this case)
    assert coords.promoted(1) == [21, 22, 23, 24]

    # The mask overrides existing nan where a default is provided and
    # automatic passthru preserves untouched existing dimensions
    # when overwriting with lower dimensional arg
    coords[1] = [nan]
    assert coords.promoted(1, mask) == [1, 22, 23, 24, 5, 6, 7, 8]

    # Mask as Python tuple
    coords[1] = [nan]
    assert coords.promoted(1, (1, 2, 3, 4, 0, 2015)) == [1, 22, 23, 24, 0, 2015]


# This test copies the material from coordinate_tuples, into coordinate_columns,
# so changes does not affect the global values
def test_coordinateset_column_wise():
    coordinate_columns = [
        [coordinate_tuples[r][c] for r in range(len(coordinate_tuples))]
        for c in range(len(coordinate_tuples[0]))
    ]
    assert coordinate_columns[0] == [11, 21, 31, 41, 51]

    coords = CoordinateSetColumnWise(coordinate_columns)
    abstract_test_coordinateset(coords)

    # Default promotion in the 2D case
    x = [11, 12, 13, 14, 15]
    y = [21, 22, 23, 24, 25]
    soa = CoordinateSetColumnWise([x, y])
    assert soa.promoted(1) == [12, 22, 0, nan]


# This test takes ownership of coordinate_tuples, so changes persist
def test_coordinateset_row_wise():
    coords = CoordinateSetRowWise(coordinate_tuples)
    abstract_test_coordinateset(coords)
