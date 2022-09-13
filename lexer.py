### Project Imports
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
        self.config = json.loads(f_data)

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

        self.newline_re = "\\n"


    def tokenize(self, input_str: str) -> list:
        # Mukarram: We need to double check which lexemes should be checked for first
        # This might require abandoning appending lexemes.json to token_specs
        # and instead just add lexemes from lexemes.json to token_specs one based on priority
        token_specs = [
            ('NEWLINE', self.newline_re),
            ('PREPROCESSOR', self.preprocessor_re),
            ('COMMENT', self.comment_re),
            # The list from lexemes.json is inserted from this position
            ('NUMBER', self.num_re),
            ('STRING', self.string_re),
            ('IDENTIFIER', self.identifier_re),
            ('TERMINATOR', self.terminator_re)
        ]

        for key in self.config.keys():
            # token_specs.append((key, self.__keyword_regex(self.config[key])))
            # Mukarram: I changed it because keywords were incorrectly being identified as identifiers
            token_specs.insert(3, (key, self.__keyword_regex(self.config[key])))

        # Based on following resources below
        # https://stackoverflow.com/questions/70680363/structural-pattern-matching-using-regex
        # https://docs.python.org/3/library/re.html#writing-a-tokenizer

        self.grammar_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specs)

        # Mukarram: Line counting isn't working right, regex expression for NEWLINE does not work
        line_num = 1
        line_start = 0
        for match in re.finditer(self.grammar_regex, input_str):
            kind = match.lastgroup
            value = match.group()
            column = match.start() - line_start
            if kind == 'NEWLINE':
                 line_start = match.end()
                 line_num += 1
                 continue
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
