#!/usr/bin/env python3
### Shebang for script execution

### Python Imports
import argparse
import os

### Token constants, used for parsing .gmr file
RULE_ASSIGNMENT = "==>"
RULE_BRANCH = "|"
COMMENT_TOKEN = "//"
COMMENT_BLOCK_START = "/*"
COMMENT_BLOCK_END = "*/"
ZERO_OR_MORE_CLOSURE_TOKEN = ")*"
ZERO_OR_ONE_CLOSURE_TOKEN = ")?"


"""
Grammar Class

Class containing all code responsible for parsing a given
gmr grammar file and generating a grammar tree.
"""
class Grammar():

    """
    __init__

    Parse the incoming grammar string and generate a tree structure based on rules,
    their tokens, and any branches for that rule.
    """
    def __init__(self, grammer_str: str) -> list:
        
        """
        Grammar tree variable, holds the following data structure:

        dictionary
            key -> rule name 
            value -> list of lists
                Each sub list represents a branch containing all of that branches tokens

        Example:
        {
            varDecl : ['TYPE', 'IDENTIFIER', 'EQUALS', 'term', 'SEMICOLON'],
                    ['TYPE', 'IDENTIFIER', 'SEMICOLON']
            EQUALS : ['"="']
            SEMICOLON : ['";"']
            term : ['NUMBER'],
                    ['STRING'],
                    ['IDENTIFIER']
        }
        """
        self.tree = {}

        lines = grammer_str
        rule = ""
        comment_block = False

        # Iterate through every line of the grammar file
        for line in lines:
            # Get the tokens based on spaces, strip of whitespace
            tokens = line.strip().split(" ")

            # Handle rule branches on new lines
            if tokens[0] != RULE_BRANCH:
                token_branch = 0
            
            # Iterate through tokens on line
            for x in range(0, len(tokens)):

                # Handle single commented lines
                if tokens[x].strip() == COMMENT_TOKEN:
                    break

                # Handle start of block comment
                if tokens[x].strip() == COMMENT_BLOCK_START:
                    comment_block = True

                # Handle end of block comment
                if tokens[x].strip() == COMMENT_BLOCK_END:
                    comment_block = False

                # Handle rule declaration
                if (x+1 < len(tokens)) and tokens[x+1].strip() == RULE_ASSIGNMENT:
                    if (not comment_block):
                        rule = tokens[x]
                        self.tree[rule] = [[]]
                        token_branch = 0
                        x += 1

                # Handle same-line rule branches
                if tokens[x].strip() == RULE_BRANCH:
                    if (not comment_block):
                        self.tree[rule].append([])
                        token_branch += 1
                        x += 1

                # Collect any other tokens provided that are not assignments or empty tokens
                elif tokens[x].strip() != RULE_ASSIGNMENT and tokens[x].strip() != "":
                    if (not comment_block):
                        self.tree[rule][token_branch].append(tokens[x])


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
    arg_parser.add_argument("-v", 
                            help="Increase verbosity level and allow for printing debug statments",
                            action="store_true")

    args = arg_parser.parse_args()

    # Check to see if the incoming file exists, otherwise exit
    if os.path.exists(args.filename):
        file = open(args.filename, 'r')
        grammar_file = file.readlines()
        grammar_tree = Grammar(grammar_file, args.v).tree

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