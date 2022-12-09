#!/usr/bin/env python3
### Shebang for script execution

### Python Imports
import argparse
import os
import pprint

### Project Imports
from parsenode import ParseNode


EXPRESSION_TOKENS = [
    "assignment",
    "varDecl",
    "funcCall",
    "returnStatement"
]

BLOCK_TOKENS = [
    "funcDecl"
]


"""
AST Class

Class containing all code responsible for parsing a given
parse tree to generate an AST file.
"""

class AST():
    """
    __v_print

    Verbose print. Only print these statements if the verbose flag is set
    """

    def __v_print(self, input):
        if self.verbose_flag:
            print(input)


    """
    __init__

    Process the incoming parse tree and generate an AST structure
    """

    def __init__(self, 
                parse_tree: ParseNode = None,
                verbose_flag: bool = False) -> list:
        self.verbose_flag = verbose_flag
        self.parse_tree = parse_tree
        self.statement_history = []
        self.ast_tree = {}
        

    """
    __traverse_parse_tree

    Traverse the parse tree to build our statement history and syntax tree
    """

    def __traverse_parse_tree(self, node: ParseNode, context: str):
        tokenValue = node.nodeVal.tokenValue

        # Specify our context when traversing 
        if tokenValue in BLOCK_TOKENS:
            context = node.get_child()[1].nodeVal.tokenValue
            self.__v_print("[AST] Moved to context '{0}'".format(context))

        if tokenValue in EXPRESSION_TOKENS:
            identifier = ""
            expression_node = None
            #parent = node.get_parent()

            if (node.nodeVal.tokenValue == "varDecl"):
                if node.get_child()[2].nodeVal.tokenType == "EQUALS":
                    self.__v_print("[AST] Found an expression within a vardecl")
                    identifier = node.get_child()[1].nodeVal.tokenValue     # IDENTIFIER
                    expression_node = node.get_child()[3]                   # expressionList
                else:
                    # Don't process non-expressive variable declarations
                    return

            elif (node.nodeVal.tokenValue == "assignment"):
                self.__v_print("[AST] Found an expression within an assignment")
                identifier = node.get_child()[0].nodeVal.tokenValue     # IDENTIFIER
                expression_node = node.get_child()[2]                   # expressionList

            elif (node.nodeVal.tokenValue == "returnStatement"):
                self.__v_print("[AST] Found an expression within a return statement")
                identifier = ""                         # Return statements don't have identifiers
                expression_node = node.get_child()[1]   # expressionList

            elif (node.nodeVal.tokenValue == "funcCall"):
                self.__v_print("[AST] Found an expression within a return statement")
                identifier = node.get_child()[0].nodeVal.tokenValue   # IDENTIFIER
                expression_node = node.get_child()[2]                 # parameterCall

            self.__v_print("Found {0} in context {1}".format(node.nodeVal.tokenValue, context))
            self.statement_history.append((
                context,
                tokenValue,
                identifier,
                expression_node))
        
        for child in node.child:
            self.__traverse_parse_tree(child, context)


    """
    build_ast

    Process the incoming parse tree and generate an AST structure
    """
    
    def build_ast(self):
        # Build our statement history list
        self.__traverse_parse_tree(self.parse_tree, "global")

        pprint.pprint(self.statement_history, indent=1)

        # Organize our base level abstract tree from statement history
        tree = {}
        for statement in self.statement_history:
            context = statement[0]
            if context not in tree.keys():
                tree[context] = []
            tree[context].append(statement[3])

        pprint.pprint(tree, indent=1, width=40)

        self.ast_tree = tree



# """
# main

# Main method executed when ran as a standalone script. Used to generate
# a grammar based on a provided filename and prints the output.
# Useful for debugging grammar iterations.
# """
# def main():
#     pass


# """
# Script entry point
# """
# if __name__ == "__main__":
#     main()