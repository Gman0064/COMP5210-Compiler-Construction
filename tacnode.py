### Python Imports
from dataclasses import dataclass


@dataclass
class VariableTAC:
    idNum: int
    var1: str
    op: str
    var2: str

    def __str__(self):
        return "v{0} = {1} {2} {3}".format(self.idNum, self.var1, self.op, self.var2)

    def get_id(self) -> str:
        return "v{}".format(self.idNum)


@dataclass
class ReturnTAC:
    var1: str
    op: str
    var2: str

    def __str__(self):
        return "return {0} {1} {2}".format(self.var1, self.op, self.var2)


# @dataclass
# class FunctionTAC:
#     var1: str
#     op: str
#     var2: str

#     def __to_str(self, node_level: int = 0):
#         return "return {1} {2} {3}".format(self.var1, self.op, self.var2)