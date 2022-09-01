### Project Imports
from lib2to3.pgen2.tokenize import tokenize
from tokentype import TokenType
from error import Error, ErrorTypes

### Python Imports
from typing import Any
import json
import re

"""
Lexer Class

Class containing all code responsible for lexing
and incoming script.
"""


class Lexer:
    """
    __keyword_regex

    Private method that generates a regular expression from
    a set of keywords

    Ex. (int|bool|char|float|long)
    """

    def __keyword_regex(self, lexeme_set: set) -> str:
        lexeme_re: str = "("

        for lexeme in lexeme_set:
            lexeme_re += (lexeme + "|")
        lexeme_re = (lexeme_re[:-1] + ')')

        return lexeme_re

    def __keyword_regex_set(self, lexeme_set: set) -> str:
        lexeme_re: set = "["

        for lexeme in lexeme_set:
            lexeme_re += lexeme
        lexeme_re = (lexeme_re[:-1] + ']')

        return lexeme_re

    """
    __init__

    Parse the incoming flags provided and set the internal
    instance variables appropriately
    """

    def __init__(self, token_outfile_flag: bool):

        # Load our keywords and lexemes from the
        # keyword config file
        self.grammar_regex = None
        f = open("config/keywords.json", 'r')
        f_data = f.read()
        f.close()

        config = json.loads(f_data)

        self.gen_token_outfile = token_outfile_flag

        # Matches any character between quotations, including
        # newlines and whitespace
        # Note: Does not recognize escaped characters
        self.string_re = r"[\S\s]*?(?=\")"

        # Matches any number literal with digits between
        # single decimal point
        # Won't match anything if there's a second decimal    
        self.num_re = r"([0-9]*\.[0-9]*)\w"

        self.newline_re = r"\n"

        self.type_re = self.__keyword_regex(config["types"])
        self.keyword_re = self.__keyword_regex(config["keywords"])
        self.single_operands_re = self.__keyword_regex_set(config["single_operands"])
        self.double_operands_re = self.__keyword_regex_set(config["double_operands"])
        self.unary_operands_re = self.__keyword_regex(config["unary_operands"])
        self.binary_operands_re = self.__keyword_regex(config["binary_operands"])

    def tokenize(self, input_str: str) -> list:
        token_specifications = [
            ('NUMBER', self.num_re),  # Integer or decimal number
            ('STRING', self.string_re),  # String literal Debug: The detection of String is not working properly
            ('TYPES', self.type_re),  # Variable Type declaration
            ('KEYWORDS', self.keyword_re),  # Generic keywords
            ('SINGLE_OP', self.single_operands_re),  # Single char operators Debug: There's some problem with this one
            ('DOUBLE_OP', self.double_operands_re),  # Double char operators
            # ('UNARY_OP', self.unary_operands_re),  # Unary operators
            ('BINARY_OP', self.binary_operands_re),  # Binary statement operators
            ('NEWLINE', self.newline_re),  # Newline operator
            ('UNKNOWN', self.binary_operands_re),  # Any other character
        ]

        # https://stackoverflow.com/questions/70680363/structural-pattern-matching-using-regex
        # https://docs.python.org/3/library/re.html#writing-a-tokenizer

        # Untested, don't think it works, but the basic idea is to make a big
        # regular expression to match and iterate through
        # Note 8/31: the loop for match in re.finditer() didn't work

        self.grammar_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specifications)
        line_num = 1
        line_start = 0
        for match in re.finditer(self.grammar_regex, input_str):
            kind = match.lastgroup
            value = match.group()
            column = match.start() - line_start
            if kind == 'NUMBER':
                value = float(value) if '.' in value else int(value)
            elif kind == 'NEWLINE':
                line_start = match.end()
                line_num += 1
                continue
            elif kind == 'UNKNOWN':
                Error.throw_error("Unidentified token", ErrorTypes.TOKEN, line_num, column)
            yield TokenType(kind, value, line_num, column)

    """
    tokenize_script

    Tokenize the incoming script using all of the preset flags
    from the class instantiation
    """

    def tokenize_script(self, input_str: str) -> list:
        # Error.throw_error("This is a test error", ErrorTypes.RUNTIME, 0, 0)
        tokens = self.tokenize(input_str)
        for token in tokens:
            print(token)

        if (self.gen_token_outfile):
            self.write_token_file(tokens)

        return tokens

    def write_token_file(self, tokens: list):
        pass


statements = "if quantity do\n total := total + price * quantity;\n tax := price * 0.05;\n ENDIF;\n This is a String ++ ||"

statement = "this is a statement"

lexer = Lexer(False)

lexer.tokenize_script(statements)
