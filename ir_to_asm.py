#!/usr/bin/env python3
### Shebang for script execution

### Python Imports
import pprint
from dataclasses import dataclass

## need to do this??
from asmCode import Assembly
from tacnode import VariableTAC, ReturnTAC

operator = {"+": "ADD",
            "-": "SUB",
            "*": "MUL",
            "/": "DIV"}

registers = ("rax",
             "rbx",
             "rcx",
             "rdx",
             "rdi",
             "rbp",
             "rsp",
             "%r8",
             "%r9",
             "%r10",
             "%r11",
             "%r12",
             "%r13",
             "%r14",
             "%r15")

"""
Assembler Class

Responsible for translating the 3AC into x86 assembly code
The current state of the code is unfinished
"""
class Assembler():
    """
    __init__

    Initialize the assembler, reset register status and load the 3AC as input
    """
    def __init__(self,
                 tac_tree: dict):
        self.tac_tree = tac_tree
        self.register_used = [False] * 15
        self.register_value = [0] * 15
        self.asm_out = []
        self.used_reg = []

    """
    __check_register_used
    
    Return whether the value inside the register is used by previous code
    """
    def __check_register_used(self, index: int):
        return self.register_used[index]

    """
    __occupy_register
    
    Change the state of the register to used
    """
    def __occupy_register(self, index: int):
        self.register_used[index] = True

    """
    __release_register
    
    Change the state of the register to unused
    """
    def __release_register(self, index: int):
        self.register_used[index] = False


    """
    tac_to_asm
    
    The main algorithm for translating to assembly code
    
    UNFINISHED
    """
    def tac_to_asm(self):
        # iterate through each three address code
        for block in self.tac_tree:
            for tac in block:
                code = Assembly("nop", "", "")
                operand1, operand2 = 0
                if isinstance(tac, VariableTAC):
                    # check if both variables of 3AC are immediate values, if so generate two assembly instructions
                    if isinstance(tac.var1, int) and isinstance(tac.var2, int):
                        code = Assembly("movl", "$" + tac.var1, registers[5])
                        self.used_reg.append(registers[5])
                        self.asm_out.append(code)
                        code = Assembly(operator[tac.op], tac.var2, registers[self.used_reg[-1]])
                    else:
                        # check variable types and assign registers accordingly
                        if isinstance(tac.var1, str):
                            for i in range(2, len(self.register_used)):
                                if not self.__check_register_used(i):
                                    operand1 = i
                                    self.__occupy_register(i)
                                    break
                        elif isinstance(tac.var1, int):
                            operand1 = tac.var1
                        if isinstance(tac.var2, str):
                            for i in range(2, len(self.register_used)):
                               if not self.__check_register_used(i):
                                   operand2 = i
                                   self.__occupy_register(i)
                                   break
                        elif isinstance(tac.var2, int):
                            operand2 = tac.var2
                        code = Assembly(operator[tac.op], operand1, operand2)
                elif isinstance(tac, ReturnTAC):
                    code = Assembly("movb", tac.var2, "%rax")
            # add code into output
            self.asm_out.append(code)

