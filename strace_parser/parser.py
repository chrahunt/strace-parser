from functools import lru_cache
from importlib.resources import read_text

from lark import Lark

import strace_parser.data


@lru_cache
def get_parser() -> Lark:
    grammar = read_text(strace_parser.data, "grammar.txt")
    return Lark(grammar)
