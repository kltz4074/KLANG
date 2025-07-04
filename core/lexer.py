import os
"""Lexical analyzer for KLANG programming language."""
import re
from collections import namedtuple

Token = namedtuple('Token', ['type', 'value'])

KEYWORDS = {
    'echo',
    'klang'
}

TOKE_SPECIFICATION= [
    ('NUMBER', r'\d+(\.\d*)?'),  # Integer or decimal number
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),  # opeations ( assigment and etc..)
    ("OP", r'[+\-*/=<>!]+'),  # operators
    ('SKIP', r'[ \t]+'),  # skip whitespace and tabs
    ('NEWLINE', r'\n'),  # line endings
    ('STRING', r'"[^"]*"'),  # string literals
    ('COMMENT', r'//.*'),  # single line comments
    ('LBRACE', r'\{'),  # left brace
    ('RBRACE', r'\}'),  # right brace
    ('LPAREN', r'\('),  # left parenthesis
    ('RPAREN', r'\)'),  # right parenthesis
    ('SEMICOLON', r';'),  # semicolon
]

def lex(code, filename=None):
    """
    Tokenize the input code into a list of tokens.
    If filename is provided, only accept files with .kl extension.
    """
    def get_file_extension(filename):
        return os.path.splitext(filename)[1][1:]

    if filename is not None:
        ext = get_file_extension(filename)
        if ext != 'kl':
            raise ValueError(f"Unsupported file extension: .{ext}. Only .kl files are allowed.")

    tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKE_SPECIFICATION)

    for match in re.finditer(tok_regex, code):
        kind = match.lastgroup
        value = match.group(kind)

        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
            yield Token(kind, value)
        elif kind == 'ID':
            if value in KEYWORDS:
                yield Token(value.upper(), value)
            else:
                yield Token('ID', value)
        elif kind == 'STRING':
            yield Token('STRING', value[1:-1])
        elif kind == 'OP':
            yield Token('OP', value)
        elif kind == 'LBRACE':
            yield Token('LBRACE', value)
        elif kind == 'RBRACE':
            yield Token('RBRACE', value)
        elif kind == 'LPAREN':
            yield Token('LPAREN', value)
        elif kind == 'RPAREN':
            yield Token('RPAREN', value)
        elif kind == 'SEMICOLON':
            yield Token('SEMICOLON', value)
        elif kind == 'NEWLINE':
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'COMMENT':
            continue
        else:
            raise RuntimeError(f'Unexpected token: {value}')
        
