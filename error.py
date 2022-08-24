# Error.py
from enum import Enum

"""
ErrorTypes

Error enum for presenting all types of possible errors and their
formatted console output
"""
class ErrorTypes(Enum):
    TOKEN = "Token Error"
    PARSER = "Parser Error"
    RUNTIME = "Runtime Error"


"""
Error Class

Class containing all code responsible for generating and
presenting errors during the compilation process
"""
class Error:
    def __init__():
        pass

    def throw_error(error_msg: str, error_type: ErrorTypes, line: int, column: int):
        print("[line {0}:{1}] {2}; {3}".format(line, column, error_type.value, error_msg))