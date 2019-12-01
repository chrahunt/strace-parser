from functools import lru_cache
from importlib.resources import read_text

from lark import Lark

from . import data


@lru_cache(1)
def get_parser() -> Lark:
    grammar = read_text(data, "grammar.txt")
    return Lark(grammar)
