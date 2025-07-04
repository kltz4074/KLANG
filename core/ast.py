"""Abstract Syntax Tree classes for klang Script programming language"""

class KlBase:
    def __init__(self, _eval: callable):
        self._eval = _eval


class KlNumber(KlBase):
    __match_args__ = ("value",)

    def __init__(self, value):
        super().__init__(
            _eval=lambda x, node: node.value
        )
        self.value = value


class KlVariable(KlBase):
    __match_args__ = ("name",)

    def __init__(self, name):
        def _eval(x, node):
            if node.name in x.env:
                return x.env[node.name]
            raise NameError(f"Variable '{node.name}' is not defined")

        super().__init__(
            _eval=_eval
        )
        self.name = name


class KlBinOp(KlBase):
    __match_args__ = ("left", "op", "right")

    def __init__(self, left, op, right):
        def _eval(x, node):
            _left = x.eval(node.left)
            _right = x.eval(node.right)

            operators = {
                '+': lambda a, b: a + b,
                '-': lambda a, b: a - b,
                '*': lambda a, b: a * b,
                '/': lambda a, b: a / b,
            }

            if node.op in operators:
                return operators[node.op](_left, _right)
            else:
                raise ValueError(f"Unknown operator: {node.op}")

        super().__init__(_eval)
        self.left = left
        self.op = op
        self.right = right


class KlAssign(KlBase):
    __match_args__ = ("name", "expr")

    def __init__(self, name, expr):
        super().__init__(
            _eval=lambda x, node: x.env.update({node.name: x.eval(node.expr)}) or None
        )
        self.name = name
        self.expr = expr


class KlEcho(KlBase):
    __match_args__ = ("expr",)

    def __init__(self, expr):
        super().__init__(
            _eval=lambda x, node: print(x.eval(node.expr))
        )
        self.expr = expr


class KlProgram(KlBase):
    __match_args__ = ("statements",)

    def __init__(self, statements):
        super().__init__(
            _eval=lambda x, node: [x.eval(stmt) for stmt in node.statements]
        )
        self.statements = statements

class print_ast:
    def __init__(self, ast):
        self.ast = ast

    def print_node(self, node, indent=0):
        print(' ' * indent + str(node.__class__.__name__))
        for attr in node.__dict__:
            value = getattr(node, attr)
            if isinstance(value, list):
                for item in value:
                    self.print_node(item, indent + 2)
            elif isinstance(value, KlBase):
                self.print_node(value, indent + 2)
            else:
                print(' ' * (indent + 2) + str(value))

    def run(self):
        self.print_node(self.ast)