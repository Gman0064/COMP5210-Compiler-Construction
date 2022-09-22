### Project Imports
from lexer import Lexer
from error import Error

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
    arg_parser.add_argument("-l", help="increase output verbosity", action="store_true")
    args = arg_parser.parse_args()


    # Check to see if the incoming file exists, otherwise exit
    if os.path.exists(args.filename):
        file = open(args.filename, 'r')
        script = file.read()
        lexer = Lexer(True)
        lexer.tokenize_file(script)
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