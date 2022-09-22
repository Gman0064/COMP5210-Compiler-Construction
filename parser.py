# Python Imports
from typing import Any
import json
from collections import deque


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
        output = ["invalid", "0"]
        token = token_list.pop(0)
        while True:
            state = str(output[-1])
            if self.config["Action"][state][token]["action"] == "shift":
                output.append(token)
                output.append(self.config["Action"][state][token]["num"])
                if len(token_list) != 0:
                    token = token_list.pop(0)
                else:
                    token = "eof"
            elif self.config["Action"][state][token]["action"] == "reduce":
                reduction = self.grammar[str(self.config["Action"][state][token]["num"])][0]
                size = len(self.grammar[str(self.config["Action"][state][token]["num"])])
                for _ in range((size - 1) * 2):
                    output.remove(output[-1])
                state = str(output[-1])
                output.append(reduction)
                output.append(self.config["Goto"][state][reduction])
            elif self.config["Action"][state][token]["action"] == "acc":
                return output
            else:
                return 1


def main():
    token_list = ["ident", "-", "num", "*", "ident"]
    parser = Parser()
    print(parser.parse(token_list))


if __name__ == "__main__":
    main()
