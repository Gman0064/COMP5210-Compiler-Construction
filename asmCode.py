from dataclasses import dataclass

@dataclass
class Assembly:
    def __init__(self,
                 operator,
                 operand1,
                 operand2 = None,
                 label=None,
                 ):
        self.label = label,
        self.operator = operator
        self.operand1 = operand1
        self.operand2 = operand2

