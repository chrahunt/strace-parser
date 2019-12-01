from importlib.resources import read_text

import pytest
from lark import Token, Tree
from strace_parser.json_transformer import to_json
from strace_parser.parser import get_parser

from . import data


def assert_fully_serialized(obj):
    def _assert_fully_serialized(obj):
        assert not isinstance(obj, Tree), original
        assert not isinstance(obj, Token), original
        if isinstance(obj, dict):
            for k, v in obj.items():
                _assert_fully_serialized(k)
                _assert_fully_serialized(v)
        elif isinstance(obj, list):
            for v in obj:
                _assert_fully_serialized(v)
        else:
            assert isinstance(
                obj, (str, float, bool)
            ), f"Unexpected type {obj} in {original}"

    original = obj
    _assert_fully_serialized(obj)


@pytest.mark.parametrize("line", read_text(data, "samples.txt").splitlines())
def test_json_fully_transforms(line):
    tree = get_parser().parse(line + "\n")
    result = to_json(tree)
    assert_fully_serialized(result)


def test_json_transformer():
    text = (
        "1577836800.000000 connect("
        r'0<\x01\x23\x45>, {sa_family=AF_UNIX, sun_path="\x01\x23\x45"}, 123)'
        " = -123 ENOENT (No such file or directory) <0.000001>\n"
    )
    parser = get_parser()
    tree = parser.parse(text)
    result = to_json(tree)
    assert len(result) == 1
    line = result[0]
    assert {
        "timestamp": 1577836800.000000,
        "type": "syscall",
        "args": [
            {"type": "other", "value": r"0<\x01\x23\x45>"},
            {
                "type": "braced",
                "value": [
                    {
                        "type": "key_value",
                        "key": "sa_family",
                        "value": {"type": "other", "value": "AF_UNIX"},
                    },
                    {
                        "type": "key_value",
                        "key": "sun_path",
                        "value": {"type": "other", "value": r'"\x01\x23\x45"'},
                    },
                ],
            },
            {"type": "other", "value": "123"},
        ],
        "name": "connect",
        "result": "-123 ENOENT (No such file or directory) <0.000001>",
    } == line, f"Did not match {tree.pretty()}"
