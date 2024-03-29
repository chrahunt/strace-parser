from importlib.resources import read_text

import pytest

import tests.data
from strace_parser.parser import get_parser


@pytest.mark.parametrize("line", read_text(tests.data, "samples.txt").splitlines())
def test_parser_parses(line):
    get_parser().parse(line + "\n")


@pytest.mark.parametrize("line", read_text(tests.data, "samples.txt").splitlines()[:20])
def test_parser_tree(line):
    print(get_parser().parse(line + "\n").pretty())
