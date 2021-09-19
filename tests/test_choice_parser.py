import unittest
from paco.combinators import Choice
from paco.atomic import (Char, Literal, Regex)

class TestChoiceParser(unittest.TestCase):

    def setUp(self):
        self.hello = Literal('hello')
        self.hi = Literal('hi')
        self.world = Literal('world')
        self.excl = Char('!')
        self.sp = Regex(r' +')
        self.sentence = (Choice(self.hello, self.hi) << self.sp) + self.world + (self.sp >> self.excl)

    def test_rshift(self):
        text = 'hello world !'
        sentence = ((self.hello | self.hi) << self.sp) + self.world + (self.sp >> self.excl)
        self.assertEqual(sentence(text),
                        (len(text), ['hello', 'world', '!']))
        
        text = 'hi world !'
        sentence = ((self.hello | self.hi) << self.sp) + self.world + (self.sp >> self.excl)
        self.assertEqual(sentence(text),
                        (len(text), ['hi', 'world', '!']))

    def test_empty(self):
        result = self.sentence('')
        err = Choice(self.hello,self.hi)('')
        self.assertEqual(result.start, err.start)
        self.assertEqual(result.end, err.end)
        self.assertEqual(result.msg, err.msg)

    def test_return(self):
        text = 'hello  world !'
        self.assertEqual(self.sentence(text),
                        (len(text), ['hello', 'world', '!']))

    def test_error(self):
        text = 'hello universe!'
        result = self.sentence(text)
        err = self.world(text, idx = 6)
        self.assertEqual(result.start, err.start)
        self.assertEqual(result.end, err.end)
        self.assertEqual(result.msg, err.msg)
