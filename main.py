from core.lexer import lex
from core.parser import Parser
from core.ast import print_ast
import sys
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_script>")
        sys.exit(1)

    filepath = sys.argv[1]

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        sys.exit(1)

    tokens = lex(code)
    parser = Parser(tokens)
    ast = parser.parse()


    # compliting AST
    class EvalContext:
        def __init__(self):
            self.env = {}
        def eval(self, node):
            return node._eval(self, node)

    class AssignNode:
        def __init__(self, name, value):
            self.name = name
            self.value = value
    
        def _eval(self, ctx, node):
            ctx.env[self.name] = self.value._eval(ctx, self.value)
            return ctx.env[self.name]

    ctx = EvalContext()
    ctx.eval(ast)