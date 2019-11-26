"""Given an strace output file, normalize it so it is useful as test data. e.g.

cat strace.log | python scripts/fix_test_data.py | sort | uniq
"""
import fileinput
import re


_file_re = re.compile(
    r"(?P<before>.*?)\d+<(?:\\x[0-9a-f][0-9a-f])+>(?P<after>.*)"
)
_string_re = re.compile(
    r'(?P<before>.*?)"(?:\\x[0-9a-f][0-9a-f])+"(?P<after>.*)'
)
_hex_re = re.compile(
    r"(?P<before>.*?)0x[0-9a-f]+(?P<after>.*)"
)
_num_re = re.compile(
    r"\b\d+\b"
)


def process(line):
    parts = line.split()

    # Numbers
    for i, part in enumerate(parts):
        parts[i] = _num_re.sub("123", part)

    # Fixed timestamp
    parts[0] = "1577836800.000000"

    # Fixed hex literals
    for i, part in enumerate(parts):
        if "0x" in part:
            m = _hex_re.match(part)
            if m:
                before, after = m.group("before"), m.group("after")
                parts[i] = f"{before}0x012345{after}"

    # Shorter and consistent strings.
    for i, part in enumerate(parts):
        if r'"\x' in part:
            m = _string_re.match(part)
            if m:
                before, after = m.group("before"), m.group("after")
                parts[i] = f'{before}"\\x01\\x23\\x45"{after}'

    # Fixed file paths
    for i, part in enumerate(parts):
        if r"<\x" in part:
            m = _file_re.match(part)
            if m:
                before, after = m.group("before"), m.group("after")
                parts[i] = f"{before}0<\\x01\\x23\\x45>{after}"

    # Fixed durations
    last_part = parts[-1]
    if last_part.startswith("<") and last_part.endswith(">"):
        parts[-1] = "<0.000001>"

    return " ".join(parts)


def main():
    for line in fileinput.input():
        print(process(line))


if __name__ == "__main__":
    main()
