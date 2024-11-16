from . import Documentation


class Crs(Documentation):
    crs_id: str = None
    units: tuple[str] = ()
    attrs: dict[str, str] = {}
    norvis: tuple[int] = (0, 1, 2, 3)
    base_id: str = None
    family: str = None

    def __init__(
        self,
        id: str,
        base_id: (str | None) = None,
        family: (str | None) = None,
        units: tuple[str] = (),
        attrs: dict[str, str] = {},
    ):
        self.crs_id = id
        self.units = units
        self.attrs = attrs
        self.base_id = base_id
        self.family = family

    def dim(self) -> int:
        return len(self.units)
