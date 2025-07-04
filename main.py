from core.lexer import lex
from core.parser import Parser
from core.ast import print_ast

if __name__ == '__main__':
    code = open('test.kl', 'r').read()

    tokens = lex(code)
    parser = Parser(tokens)
    ast = parser.parse()


    # compliting AST
    class EvalContext:
        def __init__(self):
            self.env = {}
        def eval(self, node):
            return node._eval(self, node)

    ctx = EvalContext()
    ctx.eval(ast)