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
        pp = pprint.PrettyPrinter(indent=1)
        f = open("test.txt", "w")
        f.write(pp.pformat(parse_tree))
        f.close()
        #self.__recursive_tree_print(parse_tree)
        
    def __recursive_tree_print(self, tree: dict):
        if type(tree) == dict:
            for key in tree.keys():
                print("{0}".format(key))
                self.__recursive_tree_print(tree[key])
        else:
            print("\tval: {0}".format(tree))

"""
main

Main method executed when ran as a standalone script. Used to generate
a grammar based on a provided filename and prints the output.
Useful for debugging grammar iterations.
"""
def main():
    arg_parser = argparse.ArgumentParser(
        description='Produces a grammar object based on a provided .gmr grammar file. ' \
                    'Can be ran as a script to preview a generated grammar'
    )

    arg_parser.add_argument('filename',
                            metavar="filename",
                            help="Input grammar file as path",
                            type=str)

    args = arg_parser.parse_args()

    # Check to see if the incoming file exists, otherwise exit
    if os.path.exists(args.filename):
        file = open(args.filename, 'r')
        grammar_file = file.readlines()
        grammar_tree = Grammar(grammar_file).tree

        # Print our new grammar tree with leaves
        for key in grammar_tree.keys():
            print("{0} : {1}".format(key, grammar_tree[key]))

    else:
        print('[Error] Given grammar file "{0}" does not exist!'.format(args.filename))
        exit(-1)


"""
Script entry point
"""
if __name__ == "__main__":
    main()