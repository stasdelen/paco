import unittest
from paco.combinators import Lazy
from paco.atomic import Char

class TestLazyParser(unittest.TestCase):

    def setUp(self):
        self.pipe = Char('|')
        self.dot = Char('.')
        self.rule = Lazy()
        self.element = self.dot | self.rule
        self.rule.p = self.pipe + self.element + self.pipe

    def test_empty(self):
        result = self.rule('')
        err = self.pipe('')
        self.assertEqual(result.start, err.start)
        self.assertEqual(result.end, err.end)
        self.assertEqual(result.msg, err.msg)

    def test_return(self):
        text = '||.||'
        self.assertEqual(self.rule(text),
                        (len(text), ['|', ['|', '.', '|'], '|']))

    def test_error(self):
        text = '||.|'
        result = self.rule(text)
        err = self.pipe(text,len(text))
        self.assertEqual(result.start, err.start)
        self.assertEqual(result.end, err.end)
        self.assertEqual(result.msg, err.msg)