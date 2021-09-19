import unittest
from paco.atomic import Tok
from paco.lexer import Token

class TestTokParser(unittest.TestCase):

    def test_empty(self):
        result = Tok('tag')([])
        self.assertEqual(result.start, 0)
        self.assertEqual(result.end, 0)
        self.assertEqual(result.msg, 'Got EOF')

    def test_return(self):
        result = Tok('this')([Token('this','anything',0,8)])
        self.assertEqual(result, (1,'anything'))
        result = Tok('literal','hello')([Token('literal','hello',0,5)])
        self.assertEqual(result, (1,'hello'))

    def test_error(self):
        result = Tok('hi')([Token('literal','hello',0,5)])
        self.assertEqual(result.start, 0)
        self.assertEqual(result.end, 5)
        self.assertEqual(result.msg, 'Expected Token (\'hi\', None) but got (t:literal, d:hello, @[0,5])')
