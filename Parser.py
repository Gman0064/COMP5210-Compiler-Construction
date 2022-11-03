### Python Imports
import json

### Project Imports
from grammar import Grammar
from tokentype import TokenType
from parsenode import ParseNode
from error import ErrorHandler, ErrorTypes

REMOVABLE_TOKENS = ["NEWLINE", "COMMENT"]

"""
Parser Class

Class containing all code responsible for parsing a given
list of tokens based on a gmr grammar file.
"""
class Parser:

    """
    __parse_tree_recursion

    Generate a string representing the generated parse tree in a recursive manner.
    The method is initially called by the method __gen_parse_tree_file.
    """
    def __parse_tree_recursion(self, tree: ParseNode, parent_node: dict):
        tree_node = {}  # Declare an empty dict to pass to the method recursively
        for child in tree.child:
            # If the next declList's only child is EOF, it will generate a single pair
            # as declList: EOF
            if child.nodeVal.tokenType == "EOF":
                parent_node.update({tree.nodeVal.tokenValue: child.nodeVal.tokenType})
            # Generate a branch in the parse tree output
            elif tree.nodeVal.tokenType == "RULE":
                parent_node.update({tree.nodeVal.tokenValue: self.__parse_tree_recursion(child, tree_node)})
        # When at the bottom leaf of the parse tree, create a dict with pair tokenType: tokenValue
        if tree.nodeVal.tokenType != "RULE":
            parent_node.update({tree.nodeVal.tokenType: tree.nodeVal.tokenValue})
        return parent_node

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
        # Initial empty dict which contains the parse tree file
        tree = {}
        tree = self.__parse_tree_recursion(self.ParseTree, tree)
        print(tree)

    """
    __gen_ast_file

    Generate a text file listing the abstract syntax tree for the parser's parse
    tree
    """
    def __gen_ast_file(self):
        # TODO Implement this
        pass

    """
    __init__

    Parse the incoming flags provided and set the internal
    instance variables appropriately.
    """
    def __init__(
            self,
            token_list: list,
            grammar_outfile_flag: bool = False,
            parse_tree_outfile_flag: bool = False,
            ast_outfile_flag: bool = False):

        self.tokens = token_list
        self.grammar_outfile_flag = grammar_outfile_flag
        self.parse_tree_outfile_flag = parse_tree_outfile_flag
        self.ast_outfile_flag = ast_outfile_flag

        self.error_handler = ErrorHandler()

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

        # Define the starting point of descending grammar, set to program by default
        self.rule = "program"
        # Define the root node of the parse tree
        self.ParseTree = ParseNode(TokenType("RULE", self.rule, self.lookahead.tokenLine, self.lookahead.tokenColumn))

    """
    parse_tokens

    Parse the tokens specified at instantiation, and generate any extra files based
    on provided flags.
    """
    def parse_tokens(self):

        self.descend_grammar(self.rule, self.ParseTree)

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

    """
    descend_grammar
    
    The actual function that parse through the code with the given grammar
    TODO: The code structure still has some issues, it would encounter recursion error when initial input is not 
    "varDecl", need to fix this to make parse tree generation achievable
    """
    def descend_grammar(self, rule_str: str, parent_node: ParseNode = None):
        match = False
        token_count = 0
        print("Descending rule `{0}`".format(rule_str))
        if (rule_str in self.grammar_tree.keys()):
            rule_branches = self.grammar_tree[rule_str]
            for branch in rule_branches:
                for branch_node in branch:
                    # When the lookahead token matches the token in grammar, consume the lookahead
                    if self.match(branch_node):
                        print("Lookahead token {0} at line {1} column {2} matched rule {3}"
                              .format(self.lookahead.tokenValue, self.lookahead.tokenLine, self.lookahead.tokenColumn,
                                      branch_node))
                        node = ParseNode(self.lookahead, parent_node)
                        parent_node.assign_child(node)
                        self.lookahead_index += 1
                        token_count += 1
                        if self.lookahead_index < len(self.tokens):
                            self.lookahead = self.tokens[self.lookahead_index]
                        if branch.index(branch_node) == len(branch) - 1:
                            match = True
                    # Start the recursion when lookahead does not match, pass the current grammar token to the method
                    else:
                        rule_node = TokenType("RULE", branch_node, self.lookahead.tokenLine, None)
                        node = self.descend_grammar(branch_node, ParseNode(rule_node, parent_node))
                        if node:
                            parent_node.assign_child(node.parent)
                            node = node.parent
                            match = True
                        else:
                            break
                if match:
                    break
                else:
                    index = len(parent_node.child)
                    for i in range(0, index):
                        print("Removed token {0} at line {1} unmatched rule {2}"
                              .format(parent_node.child[0].nodeVal.tokenValue,
                                      parent_node.child[0].nodeVal.tokenLine,
                                      rule_str))
                        parent_node.remove_child(parent_node.child[0])
                        self.lookahead_index -= 1
                    self.lookahead = self.tokens[self.lookahead_index]
            
            # After iterating through all branches, return the node found for the rule
            if match:
                return node
            else:
                # If no match was made, a Parse error was found. Report to user and exit
                # self.error_handler.throw_error(
                #     "Unexpected token `{0}` for rule `{1}`".format(self.lookahead.tokenValue, rule_str),
                #     ErrorTypes.PARSER,
                #     self.lookahead.tokenLine,
                #     self.lookahead.tokenColumn
                # )
                print("Unexpected token `{0}` for rule `{1}`".format(self.lookahead.tokenValue, rule_str))
                pass
        else:
            # Return None when rule does not match in Grammar
            print("No match for rule `{0}`".format(rule_str))
            return None