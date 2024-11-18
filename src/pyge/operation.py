from . import Documentation


class Operation(Documentation):
    """Attempt at a potentially simplified operation class"""

    id: str = None
    definition: str = None
    inverted: bool = False
    args: dict[str, str] = {}
    steps: list = []

    # Still demo time. Not ready for the units etc.
    #
    # left_units: tuple[str] = ()
    # left_norvis: tuple[int] = (1, 2, 3, 4)
    # left_id: str = None
    #
    # right_units: tuple[str] = ()
    # right_norvis: tuple[int] = (1, 2, 3, 4)
    # right_id: str = None

    # Also need function objects here, for init, forward and
    # (if exists) inverse operation method - but I need to
    # look up the proper syntax for this...

    # init
    # fwd
    # inv

    def __init__(
        self,
        id: str,
        definition: str,
    ):
        self.id = id
        self.definition = definition
        self.steps = []
        self.args = {}

        definitions = definition.split("|")

        # For a pipeline of operations, fill the steps-list and be done with it
        if len(definitions) > 1:
            self.args["_name"] = "pipeline"
            self.steps = [
                Operation("step", definition.strip()) for definition in definitions
            ]
            return

        # Otherwise parse the definition into arguments and build the object
        theargs = definitions[0].split()

        # inv and the operator method name needs special treatment
        if "inv" in theargs:
            self.inverted = True
            del theargs[theargs.index("inv")]
            self.args["inv"] = ""
        self.args["_name"] = theargs[0]
        del theargs[0]

        # Build the rest of the argument list
        for arg in theargs:
            argval = arg.split("=")
            # Flags get an empty value
            if len(argval) == 1:
                argval.append("")
            self.args[argval[0]] = argval[1]
        return
