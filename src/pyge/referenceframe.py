from abc import ABC


class Datum(ABC):
    def __init__(self, name: str, units: tuple[str], attrs: dict[str, str] = {}): ...

    def dim(self) -> int: ...


class DatumEnsemble(ABC):
    def __init__(self, name: str, units: tuple[str], attrs: dict[str, str] = {}): ...

    def dim(self) -> int: ...


class ReferenceFrame(Datum):
    name: str = None
    units: tuple[str] = ()
    attrs: dict[str, str] = {}

    def __init__(self, name: str, units: tuple[str], attrs: dict[str, str] = {}):
        self.name = name
        self.units = units
        self.attrs = attrs

    def dim(self) -> int:
        return len(self.units)


class Mapping:
    src: str = None
    dst: str = None
    ops: list[str] = []
    invertible: bool = True


etrs89_xyz_to_geo = {
    "from": "etrs89_xyz",
    "to": "etrs89_geo",
    "op": "inv cart ellps=GRS80",
    "invertible": True,
}

etrs89 = ReferenceFrame("etrs89", ("m", "m", "m", "y"))

print(etrs89_xyz_to_geo)
print(etrs89.units, etrs89.name, etrs89.attrs, etrs89.dim())

etrs89 = ReferenceFrame("etrs89", ("m", "m", "m", "y"), {"bonk": "duns", "foo": "bar"})
