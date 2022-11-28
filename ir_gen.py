#!/usr/bin/env python3
### Shebang for script execution

### Python Imports
import pprint

### Project Imports
from parsenode import ParseNode
from astnode import AstNode
from error import ErrorHandler, ErrorTypes
from tacnode import VariableTAC, ReturnTAC


VERBOSE_PREFIX = "[3AC]"


"""
IR Class

Class containing all code responsible for parsing a given
AST tree to generate an intermediate representation.
"""
class IR():

    variableCount = 0
    blockCount = 1
    lastVariable = ""
    tac_history = []

    """
    __v_print

    Verbose print. Only print these statements if the verbose flag is set
    """

    def __v_print(self, input):
        if self.verbose_flag:
            print(VERBOSE_PREFIX + " " + str(input))


    def __gen_ir_file(self):
        f = open("tac.txt", "w")
        for block in self.tac_tree.keys():
            f.write("{}:\n".format(block))
            for tac in self.tac_tree[block]:
                f.write("\t{}\n".format(tac))


    """
    __init__

    Process the incoming AST tree and generate an IR structure
    """
    def __init__(self, 
                ast_tree: dict = None,
                ir_outfile_flag: bool = False,
                verbose_flag: bool = False) -> list:
        self.verbose_flag = verbose_flag
        self.ast_tree = ast_tree

        self.error_handler = ErrorHandler()

        self.tac_tree = {}

        self.build_tac_tree()

        if ir_outfile_flag:
            self.__gen_ir_file()

    

    def build_tac_tree(self):
        if "main" in self.ast_tree.keys():
            for block in self.ast_tree.keys():
                # Pull the list of expressions from the ast 
                expressions = self.ast_tree[block]

                new_block_name = ""
                if block == "main":
                    new_block_name = "b0"
                else: 
                    new_block_name = "b"+str(self.blockCount)
                    self.blockCount += 1

                # Assign an empty list to the block for future use
                self.tac_tree[new_block_name] = []

                # Iterate through all of the compount expressions for a block
                for expression in expressions:
                    # generate the 3AC from our given expression
                    three_address_code = self.__traverse_expression(expression)

                    if three_address_code:
                        # Extend the block's 3AC with our newly generated 3AC
                        self.tac_tree[new_block_name].extend(three_address_code)
        
                # Reset global counters
                self.lastVariable = ""
                self.tac_history = []

            self.__v_print(pprint.pformat(self.tac_tree))

        else:
            # We require a main function as an entry point to compile!
            self.error_handler.throw_error(
                "Main function entry point not found!",
                ErrorTypes.PARSER,
                0,
                0,
            )
        

    """
    __traverse_expression

    Traverses a compound expression and creates a list of 3AC statements
    """
    def __traverse_expression(self, statement: AstNode) -> list:
        self.__v_print("Traversing expression for 3AC")

        tacList = []

        #id = statement.identifier
        type = statement.type
        expression = statement.expression

        # Start our current node at the front of the expression tree
        current_node = expression

        # Traverse all the way down our expression
        while len(current_node.get_child()) > 0:
            # Get the last child in the node's child rule list
            current_node = current_node.get_child()[-1]

        self.__v_print(current_node.nodeVal)
        self.__v_print(str(expression))

        if type == "varDecl":
            tacList = self.__expand_compound_binary_expression(current_node)
            if len(self.tac_history) > 0:
                tacList = self.tac_history
        
        elif type == "returnStatement":
            return_operand = current_node.nodeVal.tokenValue
            tac = ReturnTAC(return_operand, "", "")
            tacList.append(tac)

        self.tac_history = []

        return tacList



    def __expand_compound_binary_expression(self, node: ParseNode) -> list:

        current_node = node

        # Check and see if the 4th parent contains a BINARY_OP rule
        # ...god I hate this
        binary_op_grandparent = current_node.get_parent().get_parent().get_parent().get_parent()

        if (len(binary_op_grandparent.get_child()) > 1):
            binary_op_token = binary_op_grandparent.get_child()[1].nodeVal
            self.__v_print(binary_op_grandparent.get_child())
            self.__v_print(binary_op_token.tokenType)
            if (binary_op_token.tokenType == "BINARY_OP"):
                self.__v_print("We're in a binary op!")
            
                first_operand_grandparent = binary_op_grandparent.get_child()[0]
                first_operand_node = first_operand_grandparent.get_child()[0].get_child()[0]
                first_operand = first_operand_node.nodeVal.tokenValue

                operator = binary_op_token.tokenValue

                second_operand = self.lastVariable
                if second_operand == "":
                    second_operand = current_node.nodeVal.tokenValue

                tac = VariableTAC(self.variableCount, first_operand, operator, second_operand)
                self.variableCount += 1

                self.__v_print(str(tac))

                self.lastVariable = tac.get_id()
                
                self.tac_history.append(tac)

                self.__expand_compound_binary_expression(first_operand_node)

        else:
                # We only have 1 term to apply, therefore a simple TAC
                assignment_operand = current_node.nodeVal.tokenValue
                tac = VariableTAC(self.variableCount, assignment_operand, "", "")
                self.variableCount += 1

                return tac