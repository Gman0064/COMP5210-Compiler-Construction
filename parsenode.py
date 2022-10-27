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
        return node_val

    def get_parent(self):
        return parent

    def get_child(self):
        return child

    def remove_child(self, child):
        self.child.remove(child)
