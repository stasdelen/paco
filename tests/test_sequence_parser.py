import unittest
from paco.combinators import (Char, Literal, Regex, Sequence)

class TestSequenceParser(unittest.TestCase):

    def setUp(self):
        self.hello = Literal('hello')
        self.world = Literal('world')
        self.excl = Char('!')
        self.sp = Regex(r' +')
        self.sentence = Sequence(self.hello, self.sp, self.world, self.sp, self.excl)

    def test_add(self):
        text = 'hello world !'
        sentence = self.hello + self.sp + self.world + self.sp + self.excl
        self.assertEqual(sentence(text),
                        (len(text), ['hello',' ', 'world', ' ', '!']))

    def test_empty(self):
        result = self.sentence('')
        err = self.hello('')
        self.assertEqual(result.start, err.start)
        self.assertEqual(result.end, err.end)
        self.assertEqual(result.msg, err.msg)

    def test_return(self):
        text = 'hello  world !'
        self.assertEqual(self.sentence(text),
                        (len(text), ['hello','  ', 'world', ' ', '!']))

    def test_error(self):
        text = 'hello universe!'
        result = self.sentence(text)
        err = self.world(text, idx = 6)
        self.assertEqual(result.start, err.start)
        self.assertEqual(result.end, err.end)
        self.assertEqual(result.msg, err.msg)
