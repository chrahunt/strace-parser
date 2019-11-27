from typing import Any

from lark import Transformer, Tree


def convert(cls):
    def f(self, children):
        return cls(children[0])

    return f


def first_child():
    def f(self, children):
        return children[0]

    return f


class JsonTransformer(Transformer):
    def start(self, children):
        return children

    def line(self, children):
        timestamp, body = children
        body["timestamp"] = timestamp
        return body

    def syscall(self, children):
        name, args, result = children
        return {
            "type": "syscall",
            "name": name,
            "args": args,
            "result": result,
        }

    def args(self, children):
        return children

    def other(self, children):
        return {
            "type": "other",
            "value": str(children[0]),
        }

    def braced(self, children):
        return {
            "type": "braced",
            "value": children[0],
        }

    def bracketed(self, children):
        return {
            "type": "bracketed",
            "value": children[0],
        }

    def key_value(self, children):
        key, value = children
        return {
            "type": "key_value",
            "key": str(key),
            "value": value,
        }

    def alert_body(self, children):
        return {
            "type": "alert",
            "result": str(children[0]),
        }

    def function_like(self, children):
        name, args = children
        return {
            "type": "function",
            "name": str(name),
            "args": args,
        }

    def sigset(self, children):
        return {
            "type": "sigset",
            "negated": children[0].type == "NEGATED",
            "args": [str(c) for c in children[1:]],
        }

    key = convert(str)

    body = first_child()

    name = convert(str)

    result = convert(str)

    timestamp = convert(float)

    value = first_child()


def to_json(tree: Tree) -> Any:
    return JsonTransformer().transform(tree)
