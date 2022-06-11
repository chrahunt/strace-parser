# strace-parser

Parse strace output to jsonl.

Requires strace output that was executed with the following arguments:

* `-xx` - so strings are escaped
* `-ttt` - unix timestamp with microsecond
* `-ff` - if applicable, as long as `-f` wasn't used

# Example

```shell
strace -xx -ttt /usr/bin/true 2> stracelog
./example.py
```
