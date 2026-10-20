# tiny_ini_file_escape_handler

Handles escape sequences in INI file values: `unescape_value` turns `\n`, `\t`, `\r`, `\\`, `\"`, and `\0` into their literal characters, and `escape_value` does the reverse for those same six characters.

```python
from tiny_ini_file_escape_handler import unescape_value, escape_value

raw = r'path\with\backslashes and a \n newline'
print(unescape_value(raw))      # path\with\backslashes and a newline\n...
print(escape_value('a"b\nc'))   # a\"b\nc
```

The library exists because INI files in the wild use backslash escapes ad hoc, and `configparser` does not interpret them, leaving values with literal `\n` in the middle of a string. Rather than pull in a parser, this module does the one narrow job of translating those escapes to and from their real characters.

One edge to know about: an unrecognised escape such as `\q` is passed through verbatim, backslash and all, rather than raising or dropping characters. This means round-tripping is not guaranteed for strings that contain unrecognised escapes — `unescape_value("\q")` returns `"\q"`, but `escape_value("\q")` returns `"\\q"`. That is intentional: the goal is fidelity for hand-written values, not a reversible codec for arbitrary strings.

A trailing lone backslash at the end of a value is preserved on unescape rather than silently dropped.
