from .registeritem import RegisterItem
from .coordinateset import CoordinateSet
from .context import Context


class Operator(RegisterItem):
    """Attempt at a potentially simplified operator/operation class

    The term *operation* in the *Coordinate Operations* package of the current
    ISO-19111 and OGC Topic 2 standards, entangles two related concepts:

    - **Operator**, i.e. an entity able to operate on an operand
    - **Operation**, i.e. the act of applying an operator to an operand

    Here, we attempt to untangle the two, by explicitly introducing the
    class `Operator` for objects able to *operate* on an *operand*.
    The actual operation is carried out using the `Context`-method `apply()`,
    which applies the operator to an operand (of base class CoordinateSet).

    Hence, we have this collection of disentangled concepts:

    - **OperatorMethod**: The mathematical expression(s) behind an operator
    - **Operator**: An instantiation of an **OperatorMethod** and its associated
      defining constants
    - Operand: The **CoordinateSet** operated on by an **Operator**
    - Operation: The act of applying the **Operator** to the operand

    Note that the term 'operator' is heavily overloaded in computer science,
    so in some programming languages 'operator' may be a reserved word. Hence,
    it may not be possible to define an element with that name.

    In Python, however, this is not the case, so for conceptual clarity, we
    represent operators as instantiations of the class **Operator**.
    """

    def __init__(self, id: str, definition: str, ctx: Context):
        self.id = id
        self.definition = definition
        self.steps: tuple[Operator] = ()
        self.args: dict[str, str] = {}
        self.forward_function = None
        self.inverse_function = None
        self.ctx = ctx

        # We use the Rust Geodesy syntax, where steps are separated by the
        # vertical bar ("pipe") character
        definitions = definition.split("|")

        # For a pipeline of operators, fill the steps-list and be done with it:
        # The hard work is carried out by the stepwise recursive calls
        if len(definitions) > 1:
            method = ctx.operator_method("pipeline")
            if method is None:
                raise NameError(f"Unknown OperatorMethod 'pipeline' in '{definition}'")
            self.args["_name"] = "pipeline"
            self.forward_function = method.fwd
            self.inverse_function = method.inv
            self.steps = tuple(
                Operator("step", definition.strip(), ctx)
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

        method = ctx.operator_method(id)
        if method is None:
            raise NameError(f"Unknown OperatorMethod '{id}'  in '{definition}'")
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
            return self.inverse_function(self, ctx, operands)
        return self.forward_function(self, ctx, operands)

    def inv(self, ctx: Context, operands: CoordinateSet):
        if self.omit_inverse:
            return None
        if self.inverted:
            return self.forward_function(self, ctx, operands)
        return self.inverse_function(self, ctx, operands)
