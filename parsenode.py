from dataclasses import dataclass


@dataclass
class ParseNode:
    def __init__(self,
                 node_val,
                 parent = None,
                 child = None
                 ):
        self.nodeVal = node_val
        self.parent = parent
        self.child = []

    def assign_parent(self, parent):
        self.parent = parent

    def assign_child(self, child):
        self.child.append(child)

    def get_node(self):
        return self.nodeVal

    def get_parent(self):
        return self.parent

    def get_child(self):
        return self.child

    def remove_child(self, child):
        self.child.remove(child)

    """
    print
    
    Prints the parse tree generated by the parser, the starting point is the ParseNode object that called this function
    If desired, the parse tree printing may be started from any node if traceable
    
    node_level: indicates the current node level, default at 0
    """
    def print(self, node_level: int = 0):
        print('\t' * node_level + "'{0}': '{1}'".format(self.nodeVal.tokenType, self.nodeVal.tokenValue))
        node_level += 1
        for child in self.child:
            child.print(node_level)
