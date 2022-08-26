### Project Imports
from error import Error, ErrorTypes

### Python Imports




"""
Lexer Class

Class containing all code responsible for lexing
and incoming script.
"""
class Lexer:
    
    """
    __init__

    Parse the incoming flags provided and set the internal
    instance variables appropriately
    """
    def __init__(self, token_outfile_flag: bool):
        self.gen_token_outfile = token_outfile_flag

    """
    process_script

    Parse the incoming script using all of the preset flags
    from the class instantiation
    """
    def process_script(self, input_str: str):
        print(input_str)
        Error.throw_error("This is a test error", ErrorTypes.RUNTIME, 0, 0)