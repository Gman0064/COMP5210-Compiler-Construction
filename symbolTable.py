### Python Imports
import json

### Project Imports
from parsenode import ParseNode

SCOPE_BEGIN = [
    "funcDecl"
]

IN_SCOPE_DECL = [
    "parameterDef",
    "parameterDefList",
    "varDecl"
]

ID_ACCESS = [
    "assignment",
    "funcCall",
    "primary"
]

SCOPE_END = [
    "}",    # SCOPE_CLOSE
    ""      # EOF
]

"""
symbolTable Class

Class containing all code responsible for parsing a given
parse tree to generate a symbol table.
"""

class symbolTable():
    """
    __v_print

    Verbose print. Only print these statements if the verbose flag is set
    """

    def __v_print(self, input):
        if self.verbose_flag:
            print(input)


    """
    __init__

    Process the incoming parse tree and generate symbol table
    """

    def __init__(self, parse_tree, verbose_flag):
        self.verbose_flag = verbose_flag
        self.parse_tree = parse_tree
        self.symbol_table = {"program":{}}
        self.previous_scope = "program"
        self.current_scope = "program"


    """
    __traverse_parse_tree

    Traverse the parse to build symbol table
    """

    def __traverse_parse_tree(self, node: ParseNode):
        #tokenType = node.nodeVal.tokenType
        tokenValue = node.nodeVal.tokenValue
        identifier = ""
        type = ""

        if tokenValue in SCOPE_BEGIN:
            type = node.get_child()[0].nodeVal.tokenValue
            if type == "varType":
                type = (node.get_child()[0]).get_child()[0].nodeVal.tokenValue
            
            identifier = node.get_child()[1].nodeVal.tokenValue
            
            self.symbol_table[self.current_scope][identifier] = {
                'TYPE': tokenValue, 
                'DATATYPE': type
            }
            self.previous_scope = self.current_scope
            self.current_scope = identifier
            self.__v_print("\n[ST] Start of scope: '{0}', the previous scope was: '{1}'".format(self.current_scope, self.previous_scope))
            
        """
        if tokenValue == "IDENTIFIER":
            # Only check for in-scope declarations (this excludes assignment, funcCall, primary etc.)
            if node.get_parent().nodeVal.tokenValue in IN_SCOPE:
                # To get type information, we need to access the node before "IDENTIFIER"
                # To do that, access the parent node (parameterDef, varDecl etc.), then access the first child of the parent node (varType or TYPE)
                type = (node.get_parent()).get_child()[0].nodeVal.tokenValue
                if type == ",":
                    type = (node.get_parent()).get_child()[1].nodeVal.tokenValue
                if type == "varType":
                    # If type information is varType, dig deeper through the children to find type information
                    type = ((node.get_parent()).get_child()[0]).get_child()[0].nodeVal.tokenValue
                print(type)
        """

        if tokenValue in IN_SCOPE_DECL:
            if node.get_child()[0].nodeVal.tokenType != "RIGHT_PAREN":
                if node.get_child()[0].nodeVal.tokenType != "COMMA":
                    identifier = node.get_child()[1].nodeVal.tokenValue
                    type = (node.get_child()[0]).get_child()[0].nodeVal.tokenValue
                else:
                    identifier = node.get_child()[2].nodeVal.tokenValue
                    type = (node.get_child()[1]).get_child()[0].nodeVal.tokenValue
                if self.current_scope == "program":
                    self.symbol_table[self.current_scope][identifier] = {'TYPE': 'varDecl', 'DATATYPE': type}
                else:
                    self.symbol_table[self.previous_scope][self.current_scope][identifier] = {'TYPE': 'varDecl', 'DATATYPE': type}
                self.__v_print("[ST] Adding variable: '{0}' of type: '{1}' to scope: '{2}'".format(identifier, type, self.current_scope))

        if tokenValue in SCOPE_END:
            if tokenValue == "}":
                self.__v_print("[ST] End of scope: '{0}', scope changed to: '{1}'\n".format(self.current_scope, self.previous_scope))
                self.previous_scope = self.current_scope
                self.current_scope = "program"
            elif tokenValue == "":
                self.__v_print("[ST] End of scope: '{0}'\n".format(self.current_scope))

        for child in node.child:
            self.__traverse_parse_tree(child)


    """
    build_symbol_table()

    Build the symbol table
    """

    def build_symbol_table(self):
        self.__v_print("[ST] Start of scope: '{0}', the previous scope was: '{1}'".format(self.current_scope, self.previous_scope))
        self.__traverse_parse_tree(self.parse_tree)
        self.__v_print("[ST] Generated symbol table:")
        self.__v_print(json.dumps(self.symbol_table, indent = 4))