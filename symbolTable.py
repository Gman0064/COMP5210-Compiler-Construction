### Python Imports
import json

### Project Imports
from parsenode import ParseNode

PROGRAM_SCOPE = "program"
TYPE = "0"
DATATYPE = "1"
VARS_DECLARED = "2"
NO_OF_PARAMETERS = "3"

#tokenValue
SCOPE_BEGIN = (
    "funcDecl",
)

#tokenValue
IN_SCOPE_DECL = (
    "parameterDef",
    "parameterDefList",
    "varDecl",
)

IN_SCOPE_ACCESS = (
    "funcCall",
    "assignment",
    "primary",
)

#tokenType
SCOPE_END = (
    "SCOPE_CLOSE",    # SCOPE_CLOSE
    "EOF"      # EOF
)

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
        self.symbol_table = {PROGRAM_SCOPE:{}}
        self.previous_scope = PROGRAM_SCOPE
        self.current_scope = PROGRAM_SCOPE


    """
    __check_for_children

    Execute this function to check if relevant children of a node exist and then return those child nodes
    """

    def __determine_children(self, node):
        child0 = ""
        child1 = ""
        child2 = ""
        child0OfChild0 = ""
        child0OfChild1 = ""
        children = []
        
        numberOfChildren = len(node.get_child())
        if numberOfChildren >= 1:
            child0 = node.get_child()[0]
            noOfChildrenOfChild0 = len(child0.get_child())
            if noOfChildrenOfChild0 >= 1:
                child0OfChild0 = child0.get_child()[0]
        if numberOfChildren >= 2:
            child1 = node.get_child()[1]
            noOfChildrenOfChild1 = len(child1.get_child())
            if noOfChildrenOfChild1 >= 1:
                child0OfChild1 = child1.get_child()[0]
        if numberOfChildren >= 3:
            child2 = node.get_child()[2]

        children = [child0, child0OfChild0, child1, child0OfChild1, child2]
        return children


    """
    __scope_begin

    Execute this function to indicate beginning of scope
    """

    def __scope_begin(self, node, tokenValue):
        children = self.__determine_children(node)
        child0 = children[0]
        child0OfChild0 = children[1]
        child1 = children[2]

        #Extract type information
        if child0 != "":
            type = child0.nodeVal.tokenValue
        else:
            self.__v_print("[ST] Node: '{0}': '{1}' does not have children to check for DATATYPE information!".format(
                node.nodeVal.tokenType, node.nodeVal.tokenValue))

        if type == "varType":
            if child0OfChild0 != "":
                type = child0OfChild0.nodeVal.tokenValue
            else:
                self.__v_print("[ST] Node: '{0}': '{1}' does not have children to check for DATATYPE information!".format(
                    child0.nodeVal.tokenType, child0.nodeVal.tokenValue))

        #Extract identifier information
        if child1 != "":
            identifier = child1.nodeVal.tokenValue
        else:
            self.__v_print("[ST] Node: '{0}': '{1}' does not have children to check for IDENTIFIER information!".format(
                    node.nodeVal.tokenType, node.nodeVal.tokenValue))

        #Add information to symbol table under current scope
        self.symbol_table[self.current_scope][identifier] = {
            TYPE: tokenValue,
            DATATYPE: type
        }

        #Current scope is now the identifier i.e. function
        self.previous_scope = self.current_scope
        self.current_scope = identifier
        #self.__v_print("[ST] Start of scope: '{0}', the previous scope was: '{1}'".format(self.current_scope, self.previous_scope))


    """
    __in_scope_decl

    Execute this function to handle in-scope declarations
    """

    def __in_scope_decl(self, node, tokenValue):
        children = self.__determine_children(node)
        child0 = children[0]
        child0OfChild0 = children[1]
        child1 = children[2]
        child0OfChild1 = children[3]
        child2 = children[4]

        if child0.nodeVal.tokenType != "RIGHT_PAREN":
            if child0.nodeVal.tokenType != "COMMA":
                identifier = child1.nodeVal.tokenValue
                type = child0OfChild0.nodeVal.tokenValue
            else:
                identifier = child2.nodeVal.tokenValue
                type = child0OfChild1.nodeVal.tokenValue

            if self.current_scope == PROGRAM_SCOPE:
                self.symbol_table[self.current_scope][identifier] = {
                    TYPE: 'varDecl', DATATYPE: type}
            else:
                if VARS_DECLARED not in self.symbol_table[self.previous_scope][self.current_scope]:
                    self.symbol_table[self.previous_scope][self.current_scope][VARS_DECLARED] = {}

                if tokenValue == "varDecl":
                    self.symbol_table[self.previous_scope][self.current_scope][VARS_DECLARED][identifier] = {
                        TYPE: 'varDecl', DATATYPE: type}
                else:
                    self.symbol_table[self.previous_scope][self.current_scope][VARS_DECLARED][identifier] = {
                        TYPE: 'parameterDecl', DATATYPE: type}

            #self.__v_print("[ST] Adding variable: '{0}' of type: '{1}' to scope: '{2}'".format(identifier, type, self.current_scope))


    """
    __params_passed

    Called by __in_scope_access to list parameters passed by function call
    """
    def __param_passed(self, node):
        tokenType = node.nodeVal.tokenType
        tokenValue = node.nodeVal.tokenValue

        if tokenValue == "expressionList":
            return


    """
    __in_scope_access

    Execute this function to handle scope checking
    """

    def __in_scope_access(self, node, tokenValue):
        children = self.__determine_children(node)
        child0 = children[0]

        if child0.nodeVal.tokenType == "IDENTIFIER":
            identifier = child0.nodeVal.tokenValue

            if tokenValue == "funcCall":
                type = "functionCall"

                self.__v_print("[ST] {0}: '{1}' found in local scope: '{2}'".format(
                    type, identifier, self.current_scope))
                
                # check function declaration in global scope
                self.__v_print("[ST] Searching for '{0}' declaration in global scope '{1}'".format(
                    identifier, self.previous_scope))

                if identifier in self.symbol_table[self.previous_scope]:
                    self.__v_print("[ST] '{0}' declaration found in global scope: '{1}'".format(
                        identifier, self.previous_scope))
                else:
                    self.__v_print("[ST] [Error] '{0}' declaration NOT found in global scope: '{1}'!".format(
                        identifier, self.previous_scope))

            else:
                type = "variableAccess"

                self.__v_print("[ST] {0}: '{1}' found in local scope: '{2}'".format(
                    type, identifier, self.current_scope))
                # check variable declaration in local scope
                self.__v_print("[ST] Searching for '{0}' declaration in local scope '{1}'".format(
                    identifier, self.current_scope))
                if VARS_DECLARED in self.symbol_table[self.previous_scope][self.current_scope]:
                    if identifier in self.symbol_table[self.previous_scope][self.current_scope][VARS_DECLARED]:
                        self.__v_print("[ST] '{0}' declaration found in local scope: '{1}'".format(
                            identifier, self.current_scope))
                    else:
                        self.__v_print("[ST] [Error] '{0}' declaration NOT found in local scope: '{1}'!".format(
                            identifier, self.current_scope))
                        self.__v_print("[ST] Searching for "'{0}'" declaration in global scope '{1}'".format(
                            identifier, self.previous_scope))
                        # check for variable declaration in global scope
                        if identifier in self.symbol_table[self.previous_scope]:
                            self.__v_print("[ST] '{0}' declaration found in global scope: '{1}'".format(
                                identifier, self.previous_scope))
                        else:
                            self.__v_print("[ST] [Error] '{0}' declaration NOT found in global scope: '{1}'!".format(
                                identifier, self.previous_scope))

            """
            if "ACCESS" not in self.symbol_table[self.previous_scope][self.current_scope]:
                    self.symbol_table[self.previous_scope][self.current_scope]['ACCESS'] = {}
            self.symbol_table[self.previous_scope][self.current_scope]['ACCESS'][identifier] = {'TYPE': 'funcCall|varAccess'}
            """

    """
    __scope_end

    Execute this function to handle end of scope
    """

    def __scope_end(self, tokenType):
        if self.current_scope != PROGRAM_SCOPE:
            if VARS_DECLARED in self.symbol_table[self.previous_scope][self.current_scope]:
                noOfParameterDecls = 0
                for variable in self.symbol_table[self.previous_scope][self.current_scope][VARS_DECLARED]:
                    if self.symbol_table[self.previous_scope][self.current_scope][VARS_DECLARED][variable][TYPE] == "parameterDecl":
                        noOfParameterDecls += 1
            else:
                noOfParameterDecls = 0
            if NO_OF_PARAMETERS not in self.symbol_table[self.previous_scope][self.current_scope]:
                self.symbol_table[self.previous_scope][self.current_scope][NO_OF_PARAMETERS] = noOfParameterDecls

        if tokenType == "SCOPE_CLOSE":
            #self.__v_print("[ST] End of scope: '{0}', scope changed to: '{1}'".format(self.current_scope, self.previous_scope))
            self.previous_scope = self.current_scope
            self.current_scope = PROGRAM_SCOPE
        #elif tokenType == "EOF":
            #self.__v_print("[ST] End of scope: '{0}'".format(self.current_scope))


    """
    __traverse_parse_tree

    Traverse the parse to build symbol table
    """

    def __traverse_parse_tree(self, node: ParseNode):
        tokenType = node.nodeVal.tokenType
        tokenValue = node.nodeVal.tokenValue

        if tokenValue in SCOPE_BEGIN:
            self.__scope_begin(node, tokenValue)

        if tokenValue in IN_SCOPE_DECL:
            self.__in_scope_decl(node, tokenValue)

        if tokenValue in IN_SCOPE_ACCESS:
            self.__in_scope_access(node, tokenValue)

        if tokenType in SCOPE_END:
            self.__scope_end(tokenType)

        for child in node.child:
            self.__traverse_parse_tree(child)


    """
    build_symbol_table()

    Build the symbol table
    """

    def build_symbol_table(self):
        #self.__v_print("[ST] Start of scope: '{0}', the previous scope was: '{1}'".format(self.current_scope, self.previous_scope))
        self.__traverse_parse_tree(self.parse_tree)
        self.__v_print("[ST] Generated symbol table:")
        self.__v_print(json.dumps(self.symbol_table, indent = 4))