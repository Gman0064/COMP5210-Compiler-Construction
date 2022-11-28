#!/usr/bin/env python3
### Shebang for script execution

### Project Imports
from lexer import Lexer
from Parser import Parser
from abstractTree import AST
from ir_gen import IR
from error import ErrorHandler

### Python Imports
import argparse
import os


def main():
    """
    Main Method

    Parse the incoming flags provided, and if all arguments are valid
    pass over to the lexer
    """

    # Define our program arguments and parse them
    arg_parser = argparse.ArgumentParser(
        description='COMP5210 Compiler Construction project.\
                     Produces tokens for a subset of the C language \
                     using a lexer and parser.'
    )

    arg_parser.add_argument('filename', metavar="filename", help="input script filename", type=str)

    arg_parser.add_argument("-l", 
                            help="Generate output token file", 
                            action="store_true")
    arg_parser.add_argument("-g", 
                            help="Generate grammar file used during parsing", 
                            action="store_true")
    arg_parser.add_argument("-p", 
                            help="Generate output parse tree", 
                            action="store_true")
    arg_parser.add_argument("-a", 
                            help="Generate output abstract syntax tree", 
                            action="store_true")
    arg_parser.add_argument("-i", 
                            help="Generate output intermediate representation / 3 address code", 
                            action="store_true")
    arg_parser.add_argument("-v", 
                            help="Increase verbosity level and allow for printing debug statments",
                            action="store_true")

    args = arg_parser.parse_args()

    # Check to see if the incoming file exists, otherwise exit
    if os.path.exists(args.filename):
        file = open(args.filename, 'r')
        script = file.read()

        # Lexer step
        lexer = Lexer(
                token_outfile_flag=args.l,
                verbose_flag=args.v
            )
        tokens = lexer.tokenize_file(script)

        # Parser step
        parser = Parser(
                token_list=tokens,
                grammar_outfile_flag=args.g,
                parse_tree_outfile_flag=args.p,
                ast_outfile_flag=args.a,
                verbose_flag=args.v
            )
        parser.parse_tokens()
        parse_tree = parser.ParseTree

        #AST Step
        ast = AST(parse_tree)
        ast_tree = ast.ast_tree

        # 3 Address Code / IR Step
        ir = IR(
                ast_tree=ast_tree,
                ir_outfile_flag=args.i,
                verbose_flag=args.v
            )
        tac_tree = ir.tac_tree


    else:
        print('[Error] Given filename "{0}" does not exist!'.format(args.filename))
        exit(-1)


if __name__ == "__main__":
    """
    Main Method

    Parse the incoming flags provided, and if all arguments are valid
    pass over to the lexer
    """
    main()