#!/usr/bin/env python3
### Shebang for script execution

### Python Imports
import argparse
import os
import pprint

### Project Imports
from parsenode import ParseNode


"""
AST Class

Class containing all code responsible for parsing a given
parse tree to generate an AST file.
"""
class AST():

    """
    __init__

    Process the incoming parse tree and generate an AST structure
    """
    def __init__(self, parse_tree: dict) -> list:
        # pp = pprint.PrettyPrinter(indent=1)
        # f = open("ast.txt", "w")
        # f.write(pp.pformat(parse_tree))
        # f.close()
        self.__recursive_descent(parse_tree)

        
    def __recursive_descent(self, tree: dict):
        if type(tree) == dict:
            for key in tree.keys():
                if key == "varDecl":
                    print("varDecl found")
                self.__recursive_descent(tree[key])
        else:
            print("\tval: {0}".format(tree))

"""
main

Main method executed when ran as a standalone script. Used to generate
a grammar based on a provided filename and prints the output.
Useful for debugging grammar iterations.
"""
def main():
    pass


"""
Script entry point
"""
if __name__ == "__main__":
    main()