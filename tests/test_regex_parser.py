import unittest
from paco.combinators import Regex

class TestRegexParser(unittest.TestCase):

    def test_name(self):
        self.assertEqual(Regex(r'\"[^\"]*\"').name, 'reg(r\'\\"[^\\"]*\\"\')')

    def test_empty_target(self):
        result = Regex(r'(a|b)*abb')('')
        self.assertEqual(result.start, 0)
        self.assertEqual(result.end, 0)
        self.assertEqual(result.msg, 'Couldn\'t match the rule: re.compile(\'(a|b)*abb\')')

    def test_empty_rule(self):
        result = Regex(r'')('')
        self.assertEqual(result, (0, ''))

    def test_return(self):
        result = Regex(r'(a|b)*abb')('abababababb')
        self.assertEqual(result, (11,'abababababb'))

    def test_error(self):
        result = Regex(r'(a|b)*abb')('ababa')
        self.assertEqual(result.start, 0)
        self.assertEqual(result.end, 0)
        self.assertEqual(result.msg, 'Couldn\'t match the rule: re.compile(\'(a|b)*abb\')')

