from .registeritem import RegisterItem
from .coordinateset import CoordinateSet
from .context import Context


class Operation(RegisterItem):
    """Attempt at a potentially simplified operation class"""

    def __init__(self, id: str, definition: str, ctx: Context):
        self.id = id
        self.definition = definition
        self.steps: tuple[Operation] = ()
        self.args: dict[str, str] = {}
        self.forward_function = None
        self.inverse_function = None
        self.ctx = ctx

        # We use the Rust Geodesy syntax, where steps are separated by the
        # vertical bar ("pipe") character
        definitions = definition.split("|")

        # For a pipeline of operations, fill the steps-list and be done with it:
        # The hard work is carried out by the stepwise recursive calls
        if len(definitions) > 1:
            self.args["_name"] = "pipeline"
            self.steps = tuple(
                Operation("step", definition.strip(), ctx)
                for definition in definitions
                if len(definition.strip()) > 0
            )
            return

        # Otherwise parse the definition into arguments and build the object
        theargs = definitions[0].split()

        # The potentially-prefix modifiers, and the operator method name,
        # need special treatment: All modifiers are moved to the back, to
        # ensure that the operator name is at the front. Once that is done,
        # the operator name foo is handled as if given as "_name=foo", in
        # order to fit with the general style of the argument list

        modifiers = ["inv", "omit_fwd", "omit_inv"]
        for modifier in modifiers:
            if modifier in theargs:
                del theargs[theargs.index(modifier)]
                self.args[modifier] = ""

        id = theargs[0]
        self.args["_name"] = id
        del theargs[0]

        # Build the rest of the argument list
        for arg in theargs:
            argval = arg.split("=")
            # Flags get an empty value
            if len(argval) == 1:
                argval.append("")
            self.args[argval[0]] = argval[1]

        # TODO: Look up operator method fwd and inv by a call to ctx
        method = ctx.method(id)
        if method is None:
            raise NameError(f"Unknown OperatorMethod '{id}' in '{definition}'")
        self.forward_function = method.fwd
        self.inverse_function = method.inv

        return

    @property
    def inverted(self):
        return "inv" in self.args

    @property
    def omit_forward(self):
        return "omit_fwd" in self.args

    @property
    def omit_inverse(self):
        return "omit_inv" in self.args

    def fwd(self, ctx: Context, operands: CoordinateSet) -> int | None:
        if self.omit_forward:
            return None
        if self.inverted:
            return self.inverse_function(self.args, ctx, operands)
        self.forward_function(self.args, ctx, operands)

    def inv(self, ctx: Context, operands: CoordinateSet):
        if self.omit_inverse:
            return None
        if self.inverted:
            return self.forward_function(self.args, ctx, operands)
        self.inverse_function(self.args, ctx, operands)
