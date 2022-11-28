from dataclasses import dataclass
from Parser import ParseNode


#TODO: Not done implementing this yet, will be a data class that keeps track of the nodes
#code blocks and where it is referenced in the symbol table
@dataclass
class AstNode():
    def __init__(self, identifier: str, type: str, expression: ParseNode):
        self.identifier = identifier
        self.type = type
        self.expression = expression

    def __str__(self):
        return "Identifier: {}\n \
                Statement Type: {}\n \
                Expression: {}".format(self.identifier, self.type, self.expression)
            