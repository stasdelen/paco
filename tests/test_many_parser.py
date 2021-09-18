import unittest
from paco.combinators import (Char, Regex, Many)

class TestManyParser(unittest.TestCase):

    def setUp(self):
        self.integer = Regex(r'[1-9][0-9]*')
        self.comm = Char(',') << Regex(r' *')
        self.rule = Many(self.integer << self.comm)

    def test_empty(self):
        (pos, res) = self.rule('')
        self.assertEqual(pos, 0)
        self.assertEqual(res, [])

    def test_return(self):
        text = '12, 15, 21, 42, 34,'
        self.assertEqual(self.rule(text),
                        (len(text), ['12', '15', '21', '42', '34']))

    def test_error(self):
        text = '12, 15, 21'
        (pos,res) = self.rule(text)
        self.assertEqual(pos, 8)
        self.assertEqual(res, ['12','15'])
