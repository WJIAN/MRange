import ply.yacc as yacc
import ply.lex as lex

from Lexi import *
from Yacci import *
from Rope import travel_tree, build_tree

class MRange():
    def __init__(self, nodes):
       self.nodes = None
       self.string = None

       if isinstance(nodes, str):
           self.string = nodes

       elif isinstance(nodes, list):
           self.nodes = nodes

       else:
           #TODO except
           pass

    def extend(self):
        if self.nodes is None:
            self.nodes = self.parse()

        return self.nodes

    def serial(self):
        if self.string is None:
            self.string = travel_tree(build_tree(self.nodes))

        return self.string

    def parse(self):
        lexer = lex.lex(debug=False)
        parser = yacc.yacc(debug=False)
        result = parser.parse(self.string, lexer=lexer)
        return sorted(result)

if __name__ == '__main__':
    import sys
    mr = MRange(sys.argv[1])
    print mr.extend()
    print mr.serial()

    print "------------------"
    mr = MRange(['api01','api02','api03','api10'])
    print mr.extend()
    print mr.serial()

