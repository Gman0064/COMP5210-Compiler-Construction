### Python Imports
import json

### Project Imports
from grammar import Grammar
from tokentype import TokenType


REMOVABLE_TOKENS = ["NEWLINE"]


"""
Parser Class

Class containing all code responsible for parsing a given
list of tokens based on a gmr grammar file.
"""
class Parser:

    """
    __gen_grammar_file

    Generate a text file listing the grammar tree that is read from the
    grammar configured for the parser
    """
    def __gen_grammar_file(self):
        print("Generating grammar file")
        f = open("grammar.txt", "w")
        for key in self.grammar_tree.keys():
            f.write("{0} : {1}\n".format(key, self.grammar_tree[key][0]))
            for x in range(1, len(self.grammar_tree[key])):
                f.write("\t\t  {0}\n".format(self.grammar_tree[key][x]))
        f.close()


    """
    __gen_parse_tree_file

    Generate a text file listing the generated parse tree from the script
    """
    def __gen_parse_tree_file(self):
        #TODO Implement this
        pass


    """
    __gen_ast_file

    Generate a text file listing the abstract syntax tree for the parser's parse
    tree
    """
    def __gen_ast_file(self):
        #TODO Implement this
        pass


    """
    __init__

    Parse the incoming flags provided and set the internal
    instance variables appropriately.
    """
    def __init__(
            self,
            token_list: list,
            grammar_outfile_flag: bool=False,
            parse_tree_outfile_flag: bool=False,
            ast_outfile_flag: bool=False):
        
        self.tokens = token_list
        self.grammar_outfile_flag = grammar_outfile_flag
        self.parse_tree_outfile_flag = parse_tree_outfile_flag
        self.ast_outfile_flag = ast_outfile_flag

        # Remove any unnecessary tokens that are not explicility needed in the
        # grammar
        for token in self.tokens:
            if token.tokenType in REMOVABLE_TOKENS:
                self.tokens.remove(token)

        # Open the grammar configuration and create a grammar tree.
        f = open("config/grammar-mini.gmr", 'r')
        self.grammar_file = f.readlines()
        self.grammar_tree = Grammar(self.grammar_file).tree

        # Define the lookahead of the parser as the first token in the list of tokens
        self.lookahead_index = 0
        self.lookahead = self.tokens[self.lookahead_index]
        

    """
    parse_tokens

    Parse the tokens specified at instantiation, and generate any extra files based
    on provided flags.
    """
    def parse_tokens(self):
        
        while (self.lookahead.tokenType != "EOF"):
            self.descend_grammar("varDecl")


        if (self.grammar_outfile_flag):
            self.__gen_grammar_file()

        if (self.parse_tree_outfile_flag):
            self.__gen_parse_tree_file()

        if (self.ast_outfile_flag):
            self.__gen_ast_file()


    def match(self, token: str) -> bool:
        if self.lookahead.tokenType == token:
            return True
        else:
            return False

    
    def descend_grammar(self, rule_str: str):
        if (rule_str in self.grammar_tree.keys()):
            rule_branches = self.grammar_tree[rule_str]
            for branch in rule_branches:
                for token in branch:
                    if self.match(token):
                        print("Lookahead token {0} matched rule {1}!".format(self.lookahead.tokenType, token))
                        self.lookahead_index += 1
                        self.lookahead = self.tokens[self.lookahead_index]
                        break
                    else:
                        #print("Descending rule {0}".format(token))
                        self.descend_grammar(token)
        else:
            #print("Reached leaf")
            return