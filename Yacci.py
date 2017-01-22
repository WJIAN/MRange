from Rope import do_expr,do_multi,do_range,do_operator,do_term

def p_expr(p):
    '''expr : multi
            | expr multi
            | expr operator expr '''
    p[0] = do_expr(p)

def p_multi(p):
    '''multi : term
             | range
             | LBRACE expr RBRACE'''
    p[0] = do_multi(p)

def p_range(p):
    '''range : term RANGE term
             | term LPAREN term COLON term RPAREN'''
    p[0] = do_range(p)

def p_operator(p):
    '''operator : UNION
                | DIFF
                | INTER'''
    p[0] = do_operator(p)

def p_term(p):
    '''term : WORD'''
    p[0] = do_term(p)

def p_error(p):
    print(p)
    print("Syntax error in input!")
