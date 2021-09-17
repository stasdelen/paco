import re
from typing import Any


class Target:
    def __init__(self, text : str) -> None:
        self.text = text

    def inBound(self, pos : int) -> bool:
        return (len(self.text) > pos)
    
    def __getitem__(self, index):
        return self.text[index]


class Parser(object):


    def __init__(self) -> None:
        self.name = 'parser()'

    def run(self, pos : int, tar : Target):
        raise NotImplementedError
    
    def __add__(self, other):
        return Sequence(self, other)

    def __or__(self, other):
        return Choice(self, other)

    def __rshift__(self, other):
        return KeepRight(self, other)
    
    def __lshift__(self, other):
        return KeepLeft(self, other)

    def __call__(self, data : str, idx = 0):
        tar = Target(data)

        try:
            return self.run(idx, tar)
        except ParseError as e:
            return e
    
    def __str__(self) -> str:
        return self.name
    
    def map(self, func):
        return Map(self, func)
    
    def errmap(self, func):
        return ErrMap(self, func)

    def sepby(self, sep):
        return SepBy(self, sep)
    
    def between(self, left, right):
        return left >> self << right
    
    def inside(self, sur):
        return sur >> self << sur

    def then(self, other):
        return self << other
    
    def rename(self, name : str):
        self.name = name
        return self

class ParseError(Exception):
    def __init__(self, start : int, end : int, msg : str, parser : Parser) -> None:
        self.start = start
        self.end = end
        self.msg = msg
        self.parser = parser

    def __str__(self):
        return self.msg

class Char(Parser):
    def __init__(self, char : str) -> None:
        super().__init__()
        self.name = 'char(\'{}\')'.format(char)
        self.char = char
    
    def run(self, pos : int, tar : Target):
        if (tar.inBound(pos)) and (tar[pos] == self.char):
            return (pos + 1, self.char)
        
        got = tar[pos] if tar.inBound() else "EOF"
        msg = f"Excpected '{self.char}' but got '{got}'"
        raise ParseError(pos, pos + 1, msg, self)

class Literal(Parser):

    def __init__(self, literal : str) -> None:
        super().__init__()
        self.name = 'lit(\'{}\')'.format(literal)
        self.literal = literal
        self.length = len(literal)
    
    def run(self, pos : int, tar : Target):
        if tar.inBound(pos + self.length):
            if tar.text.startswith(self.literal,pos):
                    return (pos + self.length, self.literal)
            msg = f"Tried to match '{self.literal}' but got {tar[pos:pos+self.length]}"
            raise ParseError(pos, pos + self.length, msg, self)
        msg = f"Tried to match '{self.literal}' but got EOF"
        raise ParseError(pos, pos + self.length, msg, self)
        
class Regex(Parser):

    def __init__(self, rule : str) -> None:
        super().__init__()
        self.name = 'reg(r\'{}\')'.format(rule)
        self.rule = re.compile(rule)
    
    def run(self, pos : int, tar : Target):
        m = self.rule.match(tar[pos:])
        if m is None:
            msg = f"Couldn't match the rule: {self.rule}"
            raise ParseError(pos, pos, msg, self)
        return (pos + m.end(), m.group())

class Sequence(Parser):

    def __init__(self, *parsers) -> None:
        super().__init__()
        self.parsers = list(parsers)

    def __add__(self, other):
        self.parsers.append(other)
        return self

    def run(self, pos : int, tar : Target):
        data = list()
        for p in self.parsers:
            (pos, res) = p.run(pos, tar)
            data.append(res)
        return (pos, data)

class KeepRight(Parser):

    def __init__(self, *parsers) -> None:
        super().__init__()
        self.parsers = list(parsers)

    def __rshift__(self, other):
        self.parsers.append(other)
        return self

    def run(self, pos : int, tar : Target):
        for p in self.parsers:
            (pos, res) = p.run(pos, tar)
        return (pos, res)

class KeepLeft(Parser):

    def __init__(self, *parsers) -> None:
        super().__init__()
        self.parsers = list(parsers)

    def __lshift__(self, other):
        self.parsers.append(other)
        return self

    def run(self, pos : int, tar : Target):
        (pos, res) = self.parsers[0].run(pos, tar)
        for p in self.parsers[1:]:
            (pos, _) = p.run(pos, tar)
        return (pos, res)

class Choice(Parser):

    def __init__(self, *parsers) -> None:
        super().__init__()
        self.parsers = list(parsers)

    def __or__(self, other):
        self.parsers.append(other)
        return self

    def run(self, pos : int, tar: Target):
        for p in self.parsers:
            try:
                return p.run(pos, tar)
            except:
                continue
            
        msg = "No choice was left"
        return ParseError(pos, pos, msg, self)

class Many(Parser):

    def __init__(self, parser : Parser) -> None:
        super().__init__()
        self.parser = parser

    def run(self, pos : int, tar : Target):
        data = list()
        while True:
            try:
                (pos, res) = self.parser.run(pos, tar)
            except:
                break
            data.append(res)
        return (pos, data)

class SepBy(Parser):

    def __init__(self, tar : Parser, sep : Parser) -> None:
        super().__init__()
        self.tar = tar
        self.sep = sep

    def run(self, pos : int, tar : Target):
        (pos, res) = self.tar.run(pos, tar)
        data = [res]
        while True:
            try:
                (pos, _) = self.sep.run(pos, tar)
            except:
                break
            (pos, res) = self.tar.run(pos,tar)
            data.append(res)
            
        return (pos, data)

class Lazy(Parser):

    def __init__(self) -> None:
        super().__init__()
        self._parser = None
    
    def run(self, pos : int, tar : Target):
        if not self._parser :
            raise ParseError(pos, pos, "Lazy Parser was not set!", self)
        return self._parser.run(pos, tar)

    @property
    def p(self):
        return self._parser
    
    @p.setter
    def p(self, value):
        self._parser = value
        
class Map(Parser):

    def __init__(self, parser : Parser, func) -> None:
        super().__init__()
        self.parser = parser
        self.funcs = [func]
    
    def map(self, func) -> Parser:
        self.funcs.append(func)
        return self

    def run(self, pos : int, tar : Target):
        (pos, res) = self.parser.run(pos, tar)
        for f in self.funcs:
            res = f(res)
        return (pos, res)

class ErrMap(Parser):

    def __init__(self, parser : Parser, func) -> None:
        super().__init__()
        self.parser = parser
        self.func = func

    def run(self, pos : int, tar : Target):
        try:
            result = self.parser.run(pos, tar)
        except ParseError as e:
            result = self.func(e)
        return result
