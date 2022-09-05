### Project Imports
from lib2to3.pgen2 import grammar
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


    """
    __set_regex

    Private method that generates a regular expression from
    a set of values

    Ex. [\+\-*/<>]
    """
    def __set_regex(self, lexeme_set: set) -> str:
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
        f = open("config/lexemes.json", 'r')
        f_data = f.read()
        f.close()

        # config = json.loads(f_data)
        self.config2 = json.loads(f_data)

        self.gen_token_outfile = token_outfile_flag

        # Matches any number literal with no decimal amount
        # or with decimal amount
        # Won't match anything if there's a second decimal (which is expected?)
        self.num_re = r"([0-9]*\.[0-9]*|[0-9])"

        # Matches any character between quotations, including
        # newlines and whitespace
        # Note: Does not recognize escaped characters
        self.string_re = r"(\"{1}[\S\s]*?\")"

        self.identifier_re = r"[_a-zA-Z][_a-zA-Z0-9]*"

        self.preprocessor_re = r"(^#.*)"

        self.terminator_re = r";"

        # https://stackoverflow.com/a/49187259
        self.comment_re = r"(\/\/)(.+?)(?=[\n\r]|\*\))"

        # self.type_re = self.__keyword_regex(config["types"])
        # self.keyword_re = self.__keyword_regex(config["keywords"])
        # self.scope_re = self.__keyword_regex(config["scope"])
        # self.function_re = self.__keyword_regex(config["function"])
        # self.access_spec_re = self.__keyword_regex(config["access_specifiers"])
        # self.single_operands_re = self.__set_regex(config["single_operands"])
        # self.double_operands_re = self.__keyword_regex(config["double_operands"])
        # self.unary_operands_re = self.__keyword_regex(config["unary_operands"])
        # self.binary_operands_re = self.__keyword_regex(config["binary_operands"])


    def tokenize(self, input_str: str) -> list:
        # token_specifications = [
        #    ('PREPROCESSOR', self.preprocessor_re),  # String literal Debug: The detection of String is not working properly
        #    ('COMMENT', self.comment_re),               # C style comment strings
        #    ('NUMBER', self.num_re),                    # Integer or decimal number
        #    ('STRING', self.string_re),                 # String literal
        #    ('TYPE', self.type_re),                     # Variable type declaration
        #    ('KEYWORD', self.keyword_re),               # Generic keywords
        #    ('IDENTIFIER', self.identifier_re),         # Match identifier for variables and other keywords not match
        #    ('SCOPE', self.scope_re),                   # Scope tokens like { and }
        #    ('ACCESS_SPEC', self.access_spec_re),       # Access specifiers
        #    ('TERMINATOR', self.terminator_re),         # Statement terminator ;
        #    ('FUNCTION_OP', self.function_re),          # Function tokens
        #    ('SINGLE_OP', self.single_operands_re),     # Single char operators
        #    ('DOUBLE_OP', self.double_operands_re),     # Double char operators
        #    ('UNARY_OP', self.unary_operands_re),       # Unary operators
        #    ('BINARY_OP', self.binary_operands_re),     # Binary statement operators
        # ]


        # This is the new attempt of making the token specification list
        # Needs more testing with this, it currently works the same way as the old one
        token_specifications_new = [
            ('PREPROCESSOR', self.preprocessor_re),
            ('COMMENT', self.comment_re),
            ('NUMBER', self.num_re),
            ('STRING', self.string_re),
        ]
        for key in self.config2.keys():
            token_specifications_new.append((key, self.__keyword_regex(self.config2[key])))
        token_specifications_new.append(('IDENTIFIER', self.identifier_re))
        token_specifications_new.append(('TERMINATOR', self.terminator_re))

        # Based on following resources below
        # https://stackoverflow.com/questions/70680363/structural-pattern-matching-using-regex
        # https://docs.python.org/3/library/re.html#writing-a-tokenizer

        self.grammar_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specifications_new)

        # TODO: Line counting isn't working right, related to NEWLINE regex
        line_num = 1
        line_start = 0
        for match in re.finditer(self.grammar_regex, input_str):
            kind = match.lastgroup
            value = match.group()
            column = match.start() - line_start
            # if kind == 'NEWLINE':
            #     line_start = match.end()
            #     line_num += 1
            #     continue
            yield TokenType(kind, value, line_num, column)


    """
    tokenize_file

    Tokenize the incoming script using all of the preset flags
    from the class instantiation
    """
    def tokenize_file(self, input_str: str) -> list:
        tokens = self.tokenize(input_str)
        for token in tokens:
            print("{0},   '{1}'".format(
                token.tokenType,
                token.tokenValue
            ))

        if (self.gen_token_outfile):
            self.write_token_file(tokens)

        return tokens


    """
    write_token_file

    Write a text file of all the tokens found previously
    in the lexer
    """
    def write_token_file(self, tokens: list):
        token_file_out = open("tokens.txt", "w")

        # Somehow tokens is empty here?
        for token in tokens:
            token_file_out.write("{0},   '{1}'".format(
                token.tokenType,
                token.tokenValue
            ))
        token_file_out.close()
