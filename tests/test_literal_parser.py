import unittest
from paco.combinators import Literal

class TestLiteralParser(unittest.TestCase):

    def test_name(self):
        self.assertEqual(Literal('abcd').name, 'lit(\'abcd\')')

    def test_empty(self):
        result = Literal('howdy?')('')
        self.assertEqual(result.start, 0)
        self.assertEqual(result.end, 6)
        self.assertEqual(result.msg, 'Tried to match \'howdy?\' but got EOF')

    def test_return(self):
        result = Literal('hello world.')('hello world.')
        self.assertEqual(result, (12,'hello world.'))

    def test_error(self):
        result = Literal('hi')('hello')
        self.assertEqual(result.start, 0)
        self.assertEqual(result.end, 2)
        self.assertEqual(result.msg, 'Tried to match \'hi\' but got \'he\'')
