import unittest
from paco.atomic import Char

class TestCharParser(unittest.TestCase):

    def test_name(self):
        self.assertEqual(Char('a').name, 'char(\'a\')')

    def test_empty(self):
        result = Char('q')('')
        self.assertEqual(result.start, 0)
        self.assertEqual(result.end, 1)
        self.assertEqual(result.msg, 'Excpected \'q\' but got \'EOF\'')

    def test_return(self):
        result = Char('a')('a')
        self.assertEqual(result, (1,'a'))

    def test_error(self):
        result = Char('a')('b')
        self.assertEqual(result.start, 0)
        self.assertEqual(result.end, 1)
        self.assertEqual(result.msg, 'Excpected \'a\' but got \'b\'')

