"""Core escape handling for INI file values.

The supported escape sequences are a small, fixed set chosen to match the
backslash escapes most commonly found in INI-flavoured files in the wild:

    \\n   ->  newline
    \\t   ->  tab
    \\r   ->  carriage return
    \\\\   ->  a literal backslash
    \\"   ->  a literal double quote
    \\0   ->  NUL  (U+0000)

A single decision that callers must know about: an unrecognised escape (e.g.
``\\q``) is passed through verbatim with the backslash intact, rather than
raising, silently dropping the backslash, or removing the offending letter.
Raising would force every caller to handle parser errors for a format that is
itself ad-hoc; dropping the backslash would corrupt data the user can see;
removing the letter would be hostile. Passing the pair through verbatim is the
only behaviour that loses no information.

Escaping (the reverse direction) only escapes the six characters listed above.
Any other byte in the string is left alone, which means round-tripping a string
that contained an unrecognised escape sequence is NOT guaranteed to preserve
it: ``unescape("\\q")`` returns ``"\\q"``, and ``escape("\\q")`` returns
``"\\\\q"``. This is documented and intentional. The library's job is to
make hand-written INI values safe to store and faithful to read, not to be a
general-purpose reversible codec.
"""

from typing import Mapping

# Kept as a module-level constant so the escape and unescape tables are easy
# to audit side by side. Adding a new escape means editing exactly this dict
# and its inverse below.
_UNESCAPE: Mapping[str, str] = {
    "n": "\n",
    "t": "\t",
    "r": "\r",
    "\\": "\\",
    '"': '"',
    "0": "\x00",
}

# The inverse mapping. Built explicitly rather than with dict inversion so
# the source of truth is obvious and the order reads naturally to humans.
_ESCAPE: Mapping[str, str] = {
    "\n": "\\n",
    "\t": "\\t",
    "\r": "\\r",
    "\\": "\\\\",
    '"': '\\"',
    "\x00": "\\0",
}


def unescape_value(value: str) -> str:
    """Unescape backslash sequences in an INI value.

    Args:
        value: The raw string taken verbatim from the INI file, including any
            backslash escapes.

    Returns:
        The string with recognised escape sequences replaced by their
        literal characters. Unrecognised escapes are passed through
        unchanged (backslash plus the following character).
    """
    result: list[str] = []
    i = 0
    n = len(value)
    while i < n:
        ch = value[i]
        if ch == "\\" and i + 1 < n:
            nxt = value[i + 1]
            # Look up the pair. If it is not a known escape, fall through to
            # the verbatim branch below by appending both characters.
            mapped = _UNESCAPE.get(nxt)
            if mapped is not None:
                result.append(mapped)
                i += 2
                continue
            # Unrecognised escape: keep the backslash and the letter exactly
            # as they appeared. See module docstring for the rationale.
            result.append("\\")
            result.append(nxt)
            i += 2
            continue
        # A trailing lone backslash at the end of the string is preserved
        # as-is rather than dropped; dropping it would silently change the
        # length of the value.
        result.append(ch)
        i += 1
    return "".join(result)


def escape_value(value: str) -> str:
    """Escape a string so it can be written verbatim into an INI value.

    Only the six characters with dedicated escapes (newline, tab, carriage
    return, backslash, double quote, NUL) are escaped. Everything else is
    left untouched.

    Args:
        value: The literal string to store.

    Returns:
        A string with backslash escapes inserted for the special characters.
    """
    result: list[str] = []
    for ch in value:
        escaped = _ESCAPE.get(ch)
        if escaped is not None:
            result.append(escaped)
        else:
            result.append(ch)
    return "".join(result)
