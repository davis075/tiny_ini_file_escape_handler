import unittest

from tiny_ini_file_escape_handler import escape_value, unescape_value


class TestUnescapeValue(unittest.TestCase):
    def test_plain_string_passes_through(self):
        self.assertEqual(unescape_value("hello"), "hello")

    def test_newline_escape(self):
        self.assertEqual(unescape_value("a\\nb"), "a\nb")

    def test_tab_escape(self):
        self.assertEqual(unescape_value("a\\tb"), "a\tb")

    def test_carriage_return_escape(self):
        self.assertEqual(unescape_value("a\\rb"), "a\rb")

    def test_double_backslash_is_literal_backslash(self):
        self.assertEqual(unescape_value("a\\\\b"), "a\\b")

    def test_escaped_double_quote(self):
        self.assertEqual(unescape_value('a\\"b'), 'a"b')

    def test_nul_escape(self):
        self.assertEqual(unescape_value("a\\0b"), "a\x00b")

    def test_multiple_escapes_in_one_string(self):
        self.assertEqual(unescape_value("\\\\\\n\\t\\\\"), "\\\n\t\\")

    def test_unrecognised_escape_passed_through_verbatim(self):
        self.assertEqual(unescape_value("a\\qb"), "a\\qb")

    def test_trailing_lone_backslash_preserved(self):
        self.assertEqual(unescape_value("abc\\"), "abc\\")

    def test_empty_string(self):
        self.assertEqual(unescape_value(""), "")

    def test_only_backslashes(self):
        self.assertEqual(unescape_value("\\\\\\\\"), "\\\\")


class TestEscapeValue(unittest.TestCase):
    def test_plain_string_passes_through(self):
        self.assertEqual(escape_value("hello"), "hello")

    def test_newline_escaped(self):
        self.assertEqual(escape_value("a\nb"), "a\\nb")

    def test_tab_escaped(self):
        self.assertEqual(escape_value("a\tb"), "a\\tb")

    def test_carriage_return_escaped(self):
        self.assertEqual(escape_value("a\rb"), "a\\rb")

    def test_backslash_escaped(self):
        self.assertEqual(escape_value("a\\b"), "a\\\\b")

    def test_double_quote_escaped(self):
        self.assertEqual(escape_value('a"b'), 'a\\"b')

    def test_nul_escaped(self):
        self.assertEqual(escape_value("a\x00b"), "a\\0b")

    def test_empty_string(self):
        self.assertEqual(escape_value(""), "")

    def test_all_specials_together(self):
        self.assertEqual(
            escape_value("\n\t\r\\\"\x00"),
            "\\n\\t\\r\\\\\\\"\\0",
        )


if __name__ == "__main__":
    unittest.main()
