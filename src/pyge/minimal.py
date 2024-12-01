from .context import Context, OpHandle, OpDirection
from .operation import Operation
from .operator_method import OperatorMethod
from .coordinateset import CoordinateSet
from .builtin_operator_methods import builtin_operator_methods


class MinimalContext(Context):
    """Provide the user facing API, and the OS-facing integration

    Modes of communication between the PyGe internals and the external
    world (i.e. resources like grids, transformation definitions,
    or ellipsoid parameters)."""

    def __init__(self):
        self.ops: dict[OpHandle, Operation] = {}
        self.methods: dict[str, OperatorMethod] = dict(builtin_operator_methods)

    def register_operator_method(self, user_defined_method: OperatorMethod):
        """Add a user defined method to the gamut of built-ins"""
        self.methods[user_defined_method.id] = user_defined_method

    def operator_method(self, id) -> OperatorMethod | None:
        """The OperatorMethod representation of the operator method named `id`"""
        if id in self.methods:
            return self.methods[id]
        return None

    def builtins(self) -> tuple[str]:
        """The names of all built in operator methods"""
        return tuple((val.id for val in self.methods.values() if val.builtin))

    def op(self, definition: str) -> OpHandle | None:
        """Instantiate the operation given by `definition`"""
        thehandle = OpHandle()
        theop = Operation(str(thehandle), definition, self)
        if theop is None:
            return None
        self.ops[thehandle] = theop
        return thehandle

    def apply(
        self, op: OpHandle, direction: OpDirection, operands: CoordinateSet
    ) -> int:
        """Apply operation `op` to `operands` in direction Fwd or Inv"""
        if op not in self.ops:
            return 0
        if direction == OpDirection.FWD:
            return self.ops[op].fwd(self, operands)
        return self.ops[op].inv(self, operands)
