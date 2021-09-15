from ..tree.nodes import (Node, Parsed, Error)
from .parser_state import ParserState
import re
from typing import Any

class Parser(object):

    def __init__(self) -> None:
        self.name = str()
    
    def set_name(self, name : str) -> None:
        self.name = name

    def run(self, state : ParserState) -> Node:
        raise NotImplementedError
    
    def __add__(self, other):
        return Sequence(self, other)

    def __or__(self, other):
        return Choice(self, other)

    def __rshift__(self, other):
        return KeepRight(self, other)
    
    def __lshift__(self, other):
        return KeepLeft(self, other)

    def __call__(self, data : str, idx = 0) -> Node:
        state = ParserState(idx, data)

        parsed = self.run(state)
        if parsed.is_an(Error):
            parsed.log_error()
        return parsed
    
    def map(self, func):
        return Map(self, func)
    
    def er_map(self, func):
        return ErrMap(self, func)

    def sepby(self, sep):
        return SepBy(self, sep)
    
    def between(self, left, right):
        return left >> self << right
    
    def inside(self, sur):
        return sur >> self << sur

    def then(self, other):
        return self << other

    def ignore(self):
        def _ignore(result : Node) -> Node:
            result.ignore()
            return result
        return Map(self, _ignore)
    
    def rename(self, name : str):
        def _rename(result : Node) -> Node:
            result.ntype = name
            return result
        return Map(self, _rename)

#Atomic Parsers : They do not manipulate the given input state.

class Char(Parser):
    def __init__(self, char : str) -> None:
        super().__init__()
        self.char = char
    
    def run(self, state : ParserState) -> Node:
        if (state.in_bound()) and (state.target[state.pos] == self.char):
            return Parsed(state.pos, state.pos + 1, self.char)
        
        got = state.target[state.pos] if state.in_bound() else "EOF"
        msg = f"Excpected '{self.char}' but got '{got}'"
        return Error(state.pos, state.pos+1, msg, self)

class Literal(Parser):

    def __init__(self, literal : str) -> None:
        super().__init__()
        self.literal = literal
        self.length = len(literal)
    
    def run(self, state : ParserState) -> Node:
        for i in range(self.length):
            if (state.in_bound(ind=state.pos+i)) and \
                (self.literal[i] != state.target[state.pos + i]):
                
                got = state.target[state.pos:state.pos+self.length] \
                    if state.in_bound(state.pos+self.length) else "EOF"

                msg = f"Tried to match '{self.literal}' but got {got}"
                return Error(state.pos, state.pos + self.length, msg, self)
        return Parsed(state.pos, state.pos + self.length, self.literal)
        
class Regex(Parser):

    def __init__(self, rule : str) -> None:
        super().__init__()
        self.rule = re.compile(rule)
    
    def run(self, state : ParserState) -> Node:
        m = self.rule.match(state.text[state.pos:])
        if m is None:
            msg = f"Couldn't match the rule: {self.rule}"
            return Error(state.pos, state.pos, msg, self)
        return Parsed(state.pos, state.pos + m.end(), m.group())

#Combinators/Manipulators

class Sequence(Parser):

    def __init__(self, *parsers) -> None:
        super().__init__()
        self.parsers = list(parsers)

    def __add__(self, other):
        self.parsers.append(other)
        return self

    def run(self, state : ParserState) -> Node:
        children = list()
        for p in self.parsers:
            result = p.run(state)
            if result.is_an(Error) : return result
            state.pos = result.end
            children.append(result)
            
        parsed = Parsed(children[0].start, children[-1].end)
        parsed.add_children(*children)
        return parsed

class KeepRight(Parser):

    def __init__(self, *parsers) -> None:
        super().__init__()
        self.parsers = list(parsers)

    def __rshift__(self, other):
        self.parsers.append(other)
        return self

    def run(self, state : ParserState) -> Node:
        start = state.pos
        for p in self.parsers:
            result = p.run(state)
            if result.is_an(Error) : return result
            state.pos = result.end
        result.start = start
        return result

class KeepLeft(Parser):

    def __init__(self, *parsers) -> None:
        super().__init__()
        self.parsers = list(parsers)

    def __lshift__(self, other):
        self.parsers.append(other)
        return self

    def run(self, state : ParserState) -> Node:
        lresult = self.parsers[0].run(state)
        if lresult.is_an(Error) : return lresult
        state.pos = lresult.end
        for p in self.parsers[1:]:
            result = p.run(state)
            if result.is_an(Error) : return result
            state.pos = result.end
        lresult.end = result.end
        return lresult

class Choice(Parser):

    def __init__(self, *parsers) -> None:
        super().__init__()
        self.parsers = list(parsers)

    def __or__(self, other):
        self.parsers.append(other)
        return self

    def run(self, state: ParserState) -> Node:
        last_pos = state.pos
        for p in self.parsers:
            result = p.run(state)
            if not result.is_an(Error):
                state.pos = result.end
                return result
            state.pos = last_pos
        msg = "No choice was left"
        return Error(state.pos, state.pos, msg, self)

class Many(Parser):

    def __init__(self, parser : Parser) -> None:
        super().__init__()
        self.parser = parser

    def run(self, state : ParserState) -> Node:
        results = list()
        result = self.parser.run(state)
        if result.is_an(Error) : return result
        while not result.is_an(Error):
            state.pos = result.end
            results.append(result)
            result = self.parser.run(state)
        many_result = Parsed(results[0].start, result.end)
        many_result.add_children(*results)
        state.pos = result.end
        return many_result

class SepBy(Parser):

    def __init__(self, tar : Parser, sep : Parser) -> None:
        super().__init__()
        self.tar = tar
        self.sep = sep

    def run(self, state : ParserState) -> Node:
        result = self.tar.run(state)
        results = [result]
        if result.is_an(Error) : return result
        state.pos = result.end
        while True:
            sepres = self.sep.run(state)
            if sepres.is_an(Error):
                state.pos = sepres.start
                break
            state.pos = sepres.end
            result = self.tar.run(state)
            if result.is_an(Error) : return result
            results.append(result)
            state.pos = result.end
        sepb_result = Parsed(results[0].start, result.end)
        sepb_result.add_children(*results)
        return sepb_result

class Lazy(Parser):

    def __init__(self) -> None:
        super().__init__()
        self._parser = None
    
    def run(self, state : ParserState) -> Node:
        if self._parser == None:
            return Error(state.pos, state.pos, "Lazy Parser was not set!", self)
        return self.parser.run(state)

    @property
    def parser(self):
        return self._parser
    
    @parser.setter
    def parser(self, value):
        self._parser = value
        
class Map(Parser):

    def __init__(self, parser : Parser, func) -> None:
        super().__init__()
        self.parser = parser
        self.funcs = [func]
    
    def map(self, func) -> Parser:
        self.funcs.append(func)
        return self

    def run(self, state : ParserState) -> Node:
        result = self.parser.run(state)
        if result.is_an(Error) : return result
        for f in self.funcs:
            result = f(result)
        return result

class ErrMap(Parser):

    def __init__(self, parser : Parser, func) -> None:
        super().__init__()
        self.parser = parser
        self.func = func

    def run(self, state : ParserState) -> Node:
        result = self.parser.run(state)
        if result.is_an(Error):
            result = self.func(result)
        return result
