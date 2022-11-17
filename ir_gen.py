#!/usr/bin/env python3
### Shebang for script execution

### Python Imports
import argparse
import os
import pprint

### Project Imports
from parsenode import ParseNode
from error import ErrorHandler, ErrorTypes


"""
IR Class

Class containing all code responsible for parsing a given
AST tree to generate an intermediate representation.
"""
class IR():
    """
    __v_print

    Verbose print. Only print these statements if the verbose flag is set
    """

    def __v_print(self, input):
        if self.verbose_flag:
            print(input)


    """
    __init__

    Process the incoming AST tree and generate an IR structure
    """
    def __init__(self, 
                ast_tree: dict = None,
                verbose_flag: bool = False) -> list:
        self.verbose_flag = verbose_flag
        self.ast_tree = ast_tree

        error_handler = ErrorHandler()

        code_blocks = {}

        if "main" in self.ast_tree.keys():
            for code_block in self.ast_tree.keys():
                
                
                pass
            pass
        

        else:
            error_handler.throw_error(
                "Main function entry point not found!",
                ErrorTypes.PARSER,
                0,
                0,
            )
            exit()