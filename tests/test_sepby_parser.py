import unittest
from paco.combinators import SepBy
from paco.atomic import (Char, Regex)

class TestSepByParser(unittest.TestCase):

    def setUp(self):
        self.integer = Regex(r'[1-9][0-9]*')
        self.comm = Char(',') << Regex(r' *')
        self.rule = SepBy(self.integer, self.comm)

    def test_empty(self):
        result = self.rule('')
        err = self.integer('')
        self.assertEqual(result.start, err.start)
        self.assertEqual(result.end, err.end)
        self.assertEqual(result.msg, err.msg)

    def test_return(self):
        text = '12, 15, 21, 42, 34'
        self.assertEqual(self.rule(text),
                        (len(text), ['12', '15', '21', '42', '34']))

    def test_error(self):
        text = '12, 15, '
        result = self.rule(text)
        err = self.integer(text,len(text))
        self.assertEqual(result.start, err.start)
        self.assertEqual(result.end, err.end)
        self.assertEqual(result.msg, err.msg)