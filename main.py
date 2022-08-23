### Project Imports
import lexer
import error

### Python Imports
import argparse


def main():
    """
    Main Method

    Parse the incoming flags provided, and if all arguments are valid
    pass over to the lexer
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("[filename]", help="input script file", type=str)
    arg_parser.add_argument("-l", help="generate file of tokens produced from the lexer", type=str)
    if arg_parser.l:
        print("verbosity turned on")

    print(arg_parser.file)



if __name__ == "__main__":
    """
    Main Method

    Parse the incoming flags provided, and if all arguments are valid
    pass over to the lexer
    """
    main()