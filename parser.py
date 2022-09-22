# Python Imports
from typing import Any
import json


class Parser:

    def __init__(self):

        f = open("config/parser_tableV1", "r")
        f_data = f.read()
        f.close()

        self.config = json.loads(f_data)

        f2 = open("config/grammarV1", "r")
        f2_data = f2.read()
        f2.close()

        self.grammar = json.loads(f2_data)

    def parse(self, token_list: list):
        output = []
        output.push("invalid")
        output.push("0")
        token = token_list.popleft()
        while True:
            state = output.top()
            if self.config["Action"][state][token]["action"] == "shift":
                output.push(token)
                output.push(self.config["Action"][state][token]["num"])
                token = token_list.popleft()
            elif self.config["Action"][state][token]["action"] == "reduce":
                for _ in num((self.grammar[self.config["Action"][state][token][num]].size() - 1) * 2):
                    output.pop()
                state = output.top()
                reduction = self.grammar[self.config["Action"][state][token][num]][0]
                output.push(reduction)
                output.push(self.config[state][reduction])
            elif self.config["Action"][stete][token]["action"] == "acc":
                return output
            else:
                return 0
