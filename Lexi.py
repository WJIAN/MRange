# -*- coding: utf-8 -*-

# List of token names.   This is always required
tokens = (
    'WORD',
    'UNION',
    'DIFF',
    'INTER',
    'RANGE',
    'LBRACE',
    'RBRACE',
    'LPAREN',
    'RPAREN',
    'COLON',
)

# Regular expression rules for simple tokens
t_WORD   = r'[A-Za-z\d\-\._]+'
t_UNION  = r','
t_DIFF   = r',-'
t_INTER  = r',&'
t_RANGE  = r'~'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON  = r':'

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
