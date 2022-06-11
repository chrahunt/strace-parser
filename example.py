#!/usr/bin/env python
import strace_parser.parser
import strace_parser.json_transformer

with open("stracelog") as infile:
    strace = infile.read()

tree = strace_parser.parser.get_parser().parse(strace)
jsonl = strace_parser.json_transformer.to_json(tree)
print(jsonl)
