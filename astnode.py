from dataclasses import dataclass
from Parser import ParseNode


#TODO: Not done implementing this yet, will be a data class that keeps track of the nodes
#code blocks and where it is referenced in the symbol table
@dataclass
class AstNode():
    def __init__(self, identifier: str, statement_type: str, statement: ParseNode):
        self.identifier = identifier
        self.statement_type = statement_type
        self.statement = statement

    def __str__(self):
        return "Identifier: {}\n \
                Statement Type: {} \
                Statement: {}".format(self.identifier, self.statement_type, self.statement)
            