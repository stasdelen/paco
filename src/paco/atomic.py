
import re
from .combinators import Parser, ParseError

class Char(Parser):
    def __init__(self, char : str) -> None:
        super().__init__()
        self.name = 'char(\'{}\')'.format(char)
        self.char = char
    
    def run(self, pos : int, tar : str):
        if (len(tar) > pos) and (tar[pos] == self.char):
            return (pos + 1, self.char)
        
        got = tar[pos] if len(tar) > pos else "EOF"
        msg = f"Excpected '{self.char}' but got '{got}'"
        raise ParseError(pos, pos + 1, msg, self)

class Literal(Parser):

    def __init__(self, literal : str) -> None:
        super().__init__()
        self.name = 'lit(\'{}\')'.format(literal)
        self.literal = literal
        self.length = len(literal)
    
    def run(self, pos : int, tar : str):
        if tar.startswith(self.literal,pos):
            return (pos + self.length, self.literal)
        if len(tar) > (pos + self.length-1):
            msg = f"Tried to match '{self.literal}' but got '{tar[pos:pos+self.length]}'"
            raise ParseError(pos, pos + self.length, msg, self)
        msg = f"Tried to match '{self.literal}' but got EOF"
        raise ParseError(pos, pos + self.length, msg, self)
        
class Regex(Parser):

    def __init__(self, rule : str) -> None:
        super().__init__()
        self.name = 'reg(r\'{}\')'.format(rule)
        self.rule = re.compile(rule)
    
    def run(self, pos : int, tar : str):
        m = self.rule.match(tar, pos)
        if m is None:
            msg = f"Couldn't match the rule: {self.rule}"
            raise ParseError(pos, pos, msg, self)
        return (m.end(), m.group())

class Tok(Parser):

    def __init__(self, tag : str, data = None):
        self.tag, self.data = tag, data
        if data:
            self.condition = lambda t : (t.type == tag) and (t.data == data)
        else:
            self.condition = lambda t : (t.type == tag)
    
    def run(self, pos : int, tar : list):
        if len(tar) > pos:
            tok = tar[pos]
            if self.condition(tok):
                return (pos + 1, tok.data)
            msg = 'Expected Token {} but got {}'.format((self.tag,self.data),tok)
            raise ParseError(tok.start, tok.end, msg, self)
        else:
            raise ParseError(pos, pos, 'Got EOF', self)
