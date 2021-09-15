import re
from typing import Any
from dataclasses import dataclass

@dataclass
class Parsed:
    type : str
    start : int
    end : int
    data : Any

class Target:
    def __init__(self, text : str, pos = 0) -> None:
        self.text = text
        self.pos = pos

    def inBound(self) -> bool:
        return (len(self.text) > self.pos)
    
    def __getitem__(self, index):
        return self.text[index]


class Parser(object):


    def __init__(self) -> None:
        self.name = str()
    
    def setName(self, name : str) -> None:
        self.name = name

    def run(self, tar : Target) -> Parsed:
        raise NotImplementedError
    
    def __add__(self, other):
        return Sequence(self, other)

    def __or__(self, other):
        return Choice(self, other)

    def __rshift__(self, other):
        return KeepRight(self, other)
    
    def __lshift__(self, other):
        return KeepLeft(self, other)

    def __call__(self, data : str, idx = 0) -> Parsed:
        tar = Target(data, idx)

        try:
            parsed = self.run(tar)
            return parsed
        except ParseError as e:
            print(e.msg)
            return None
    
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

#Atomic Parsers : They do not manipulate the given input tar.

class Char(Parser):
    def __init__(self, char : str) -> None:
        super().__init__()
        self.name = 'char({})'.format(char)
        self.char = char
    
    def run(self, tar : Target) -> Parsed:
        if (tar.inBound()) and (tar[tar.pos] == self.char):
            return Parsed(self.name, tar.pos, tar.pos + 1, self.char)
        
        got = tar[tar.pos] if tar.inBound() else "EOF"
        msg = f"Excpected '{self.char}' but got '{got}'"
        raise ParseError(tar.pos, tar.pos + 1, msg, self)

class Literal(Parser):

    def __init__(self, literal : str) -> None:
        super().__init__()
        self.name = 'lit({})'.format(literal)
        self.literal = literal
        self.length = len(literal)
    
    def run(self, tar : Target) -> Parsed:
        if tar.inBound(tar.pos + self.length):
            for i in range(self.length):
                if self.literal[i] != tar[tar.pos + i]:
                    msg = f"Tried to match '{self.literal}' but got {tar[tar.pos:tar.pos+self.length]}"
                    raise ParseError(tar.pos, tar.pos + self.length, msg, self)

            return Parsed(self.name, tar.pos, tar.pos + self.length, self.literal)
        msg = f"Tried to match '{self.literal}' but got EOF"
        raise ParseError(tar.pos, tar.pos + self.length, msg, self)
        
class Regex(Parser):

    def __init__(self, rule : str) -> None:
        super().__init__()
        self.name = 'reg({})'.format(rule)
        self.rule = re.compile(rule)
    
    def run(self, tar : Target) -> Parsed:
        m = self.rule.match(tar[tar.pos:])
        if m is None:
            msg = f"Couldn't match the rule: {self.rule}"
            raise ParseError(tar.pos, tar.pos, msg, self)
        return Parsed(self.name, tar.pos, tar.pos + m.end(), m.group())

class Sequence(Parser):

    def __init__(self, *parsers) -> None:
        super().__init__()
        self.name = 'seq()'
        self.parsers = list(parsers)

    def __add__(self, other):
        self.parsers.append(other)
        return self

    def run(self, tar : Target) -> Parsed:
        data = list()
        for p in self.parsers:
            result = p.run(tar)
            tar.pos = result.end
            data.append(result)
            
        return Parsed(self.name, data[0].start, data[-1].end, data) 

class KeepRight(Parser):

    def __init__(self, *parsers) -> None:
        super().__init__()
        self.parsers = list(parsers)

    def __rshift__(self, other):
        self.parsers.append(other)
        return self

    def run(self, tar : Target) -> Parsed:
        start = tar.pos
        for p in self.parsers:
            result = p.run(tar)
            tar.pos = result.end
        result.start = start
        return result

class KeepLeft(Parser):

    def __init__(self, *parsers) -> None:
        super().__init__()
        self.parsers = list(parsers)

    def __lshift__(self, other):
        self.parsers.append(other)
        return self

    def run(self, tar : Target) -> Parsed:
        lresult = self.parsers[0].run(tar)
        tar.pos = lresult.end
        for p in self.parsers[1:]:
            result = p.run(tar)
            tar.pos = result.end
        lresult.end = tar.pos
        return lresult

class Choice(Parser):

    def __init__(self, *parsers) -> None:
        super().__init__()
        self.parsers = list(parsers)
        self.name = 'choice'

    def __or__(self, other):
        self.parsers.append(other)
        return self

    def run(self, tar: Target) -> Parsed:
        last_pos = tar.pos
        for p in self.parsers:
            try:
                result = p.run(tar)
            except:
                tar.pos = last_pos
                continue
            tar.pos = result.end
            return result
            
        msg = "No choice was left"
        return ParseError(tar.pos, tar.pos, msg, self)

class Many(Parser):

    def __init__(self, parser : Parser) -> None:
        super().__init__()
        self.name = 'many({})'.format(parser)
        self.parser = parser

    def run(self, tar : Target) -> Parsed:
        data = list()
        while True:
            try:
                result = self.parser.run(tar)
            except:
                break
            data.append(result)
            tar.pos = result.end
        return Parsed(self.name, data[0].start, data[-1].end, data)

class SepBy(Parser):

    def __init__(self, tar : Parser, sep : Parser) -> None:
        super().__init__()
        self.name = 'sepby({},{})'.format(tar,sep)
        self.tar = tar
        self.sep = sep

    def run(self, tar : Target) -> Parsed:
        result = self.tar.run(tar)
        data = [result]
        tar.pos = result.end
        while True:
            try:
                sepres = self.sep.run(tar)
            except:
                break
            tar.pos = sepres.end
            result = self.tar.run(tar)
            data.append(result)
            tar.pos = result.end
            
        return Parsed(self.name, data[0].start,data[-1].end, data)

class Lazy(Parser):

    def __init__(self) -> None:
        super().__init__()
        self._parser = None
    
    def run(self, tar : Target) -> Parsed:
        if self._parser == None:
            raise ParseError(tar.pos, tar.pos, "Lazy Parser was not set!", self)
        return self._parser.run(tar)

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

    def run(self, tar : Target) -> Parsed:
        result = self.parser.run(tar)
        for f in self.funcs:
            result.data = f(result.data)
        return result

class ErrMap(Parser):

    def __init__(self, parser : Parser, func) -> None:
        super().__init__()
        self.parser = parser
        self.func = func

    def run(self, tar : Target) -> Parsed:
        try:
            result = self.parser.run(tar)
        except ParseError as e:
            result = self.func(e)
        return result
