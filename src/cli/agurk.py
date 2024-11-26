from pyge import CoordinateSetColumnWise
from uuid import uuid4

def agurk():
    print("AGURK!")
    x = [11, 12, 13, 14, 15]
    y = [21, 22, 23, 24, 25]
    z = [31, 32, 33, 34, 35]
    t = [41, 42, 43, 44, 45]
    lol = CoordinateSetColumnWise([x, y, z, t])

    assert lol.len() == 5
    assert lol.dim() == 4

    assert lol.get(0) == [11, 21, 31, 41]
    lol.set(0, [1, 2])
    assert lol.get(0) == [1, 2, 31, 41]  # automatic passthru
    print(f"{lol.crs_id}\n{lol.coords}")
