### Project Imports
from tokenize import Token
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

        self.config = json.loads(f_data)

        self.gen_token_outfile = token_outfile_flag
        
        self.newline_re = r"\n|\r"

        self.preprocessor_re = r"(#.*>)"

        # https://stackoverflow.com/a/49187259
        self.comment_re = r"(\/\/)(.+?)(?=[\n\r]|\*\))"
        
        # Matches any number literal with no decimal amount
        # or with decimal amount
        # Won't match anything if there's a second decimal (which is expected?)
        self.num_re = r"([0-9]*\.[0-9]+|[0-9]+)"

        # Matches any character between quotations, including
        # newlines and whitespace
        # Note: Does not recognize escaped characters yet
        self.string_re = r"(\"{1}[\S\s]*?\")"

        self.escape_re = self.__keyword_regex(self.config["ESCAPE_SEQ"])
        
        self.identifier_re = r"[_a-zA-Z][_a-zA-Z0-9]*"

        self.terminator_re = r";"

        
    def tokenize(self, input_str: str) -> list:
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

        # Mukarram: I changed how the list in lexemes.json is inserted because of some
        # incorrect matches. For example, keywords were incorrectly being identified as identifiers
        index = 0
        offset = 3
        for key in self.config.keys():
            # token_specs.append((key, self.__keyword_regex(self.config[key])))
            # Mukarram: Working on adding escape seq implementation, doesn't work just yet
            # That is why I skip adding it in token_spec for now
            if(key == "ESCAPE_SEQ"):
                index += 1
                continue
            token_specs.insert(index + offset, (key, self.__keyword_regex(self.config[key])))
            index += 1

        # Used regex documentation by Python as reference for the code below
        # https://docs.python.org/3/library/re.html#writing-a-tokenizer

        self.grammar_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specs)

        # Mukarram: Line counting has been fixed
        line_num = 1
        line_start = 0
        for match in re.finditer(self.grammar_regex, input_str):
            kind = match.lastgroup
            value = match.group()
            column = match.start() - line_start
            if kind == 'NEWLINE':
                value = "\\n"
                line_start = match.end()
                # yield TokenType(kind, value, line_num, column)
                line_num += 1
                continue
            if kind == 'COMMENT':
                continue
            yield TokenType(kind, value, line_num, column)
        
        # Garrett: Add EOF token for program grammar
        yield TokenType("EOF", '', line_num, column + 1)

    """
    tokenize_file

    Tokenize the incoming script using all of the preset flags
    from the class instantiation
    """
    def tokenize_file(self, input_str: str) -> list:
        tokens = []
        token_yielded = self.tokenize(input_str)
        for token_attr in token_yielded:
            print_token = ("{0},  '{1}',  Line: {2},  Column: {3}".format(
                token_attr.tokenType,
                token_attr.tokenValue,
                token_attr.tokenLine,
                token_attr.tokenColumn
            ))
            # TODO: Garrett: Make verbosity check for print statements
            # print(print_token)
            tokens.append(token_attr)

        if (self.gen_token_outfile):
            self.write_token_file(tokens)

        return tokens


    """
    write_token_file

    Write a text file of all the tokens found previously
    in the lexer
    """
    def write_token_file(self, tokens: list):
        with open("tokens.txt", "w") as token_file_out:

            # Mukarram: Writing tokens to a file has been fixed
            for token in tokens:
                print_token = ("{0},  '{1}',  Line: {2},  Column: {3}".format(
                    token.tokenType,
                    token.tokenValue,
                    token.tokenLine,
                    token.tokenColumn
                ))
                token_file_out.write("{0}\n".format(print_token))
