# Python Imports
from typing import Any
import json

class Parser:

    def __init__(self):

        f = open("config/parser_tableV1", "r")
        f_data = f.read()
        f.close()

        self.config = json.loads(f_data)

    def parse(self, token_list: list):
        return None
