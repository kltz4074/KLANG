"""Parser for Klang language"""
from core.ast import (
    KlProgram,
    KlAssign,
    KlVariable,
    KlNumber,
    KlBinOp,
    KlEcho
)

class Parser:
    def echo_statement(self):
        self.expect("ECHO")
        self.expect("LPAREN")
        expr = self.expr()
        self.expect("RPAREN")
        return KlEcho(expr)

    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.pos = 0
    
    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def advance(self):
        self.pos += 1
    
    def expect(self, token_type):
        tok = self.peek()
        if tok and tok.type == token_type:
            self.advance()
            return tok
        raise SyntaxError(f"Expected token type {token_type}")
    
    def parse(self):
        if not (self.peek() and self.peek().type == "KLANG"):
            raise SyntaxError("Script must start with 'klang' keyword")
        self.advance()

        statements = [] 
        while self.peek():
            statements.append(self.statement())
        
        return KlProgram(statements)
    
    def statement(self):
        tok = self.peek()
        
        if tok.type == "ID":
            return self.assigment()
        elif tok.type == "ECHO":
            return self.echo_statement()
        else:
            raise SyntaxError(f"Unexpected token: {tok}")
        
    def assigment(self):
        name = self.expect("ID").value
        if (self.peek() and 
            self.peek().type == "OP" and 
            self.peek().value == "="):
            self.advance()
            expr = self.expr()
            return KlAssign(name, expr)
        else:
            raise SyntaxError(f"Expected '=' after variable name '{name}'")
        
    def expr(self):
        return self._term_tail(self.term())
    
    def _term_tail(self, left):
        tok = self.peek()
        if tok and tok.type == 'OP' and tok.value in ('+', '-'):
            self.advance()
            op = tok.value
            right = self.term()
            return self._term_tail(KlBinOp(left, op, right))
        return left
    
    def term(self):
        return self._factor_tail(self.factor())

    def _factor_tail(self, left):
        tok = self.peek()
        if tok and tok.type == 'OP' and tok.value in ('*', '/'):
            self.advance()
            op = tok.value
            right = self.factor()
            return self._factor_tail(KlBinOp(left, op, right))
        return left
    
    def factor(self):
        tok = self.peek()
        if tok.type == 'NUMBER':
            self.advance()
            return KlNumber(tok.value)
        elif tok.type == 'ID':
            self.advance()
            return KlVariable(tok.value)
        elif tok.type == 'STRING':
            self.advance()
            return KlNumber(tok.value)  # Можно создать отдельный класс KlString, если нужно отличать
        elif tok.type == 'LPAREN':
            self.advance()
            expr = self.expr()
            self.expect('RPAREN')
            return expr
        
        raise SyntaxError(f"Unexpected token in factor: {tok}")
        