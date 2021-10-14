import re
from typing import NamedTuple

class Token(NamedTuple('Token',type=str,data=str,start=int,end=int)):
    def __repr__(self) -> str:
        return '(t:{}, d:{}, @[{},{}])'.format(self.type, self.data, self.start, self.end)

def lexx(regexes):
    regs = [(n, re.compile(r)) for n,r in regexes]
    def tokenizer(text, i=0):
        tokens = []
        while i < len(text):
            res = None
            for (n,r) in regs:
                res = r.match(text,i)
                if res:
                    if n : tokens.append(Token(n,res.group(),i,res.end()))
                    i = res.end()
                    break
            if not res:
                raise Exception('Unknown token \'{}\' @{}.'.format(text[i], i))
        return tokens
    return tokenizer

def lexx2(regexes):
    namedRules = [('(?P<{}>{})'.format(name, rule) if name else '({})'.format(rule)) for name, rule in regexes]
    rule = '|'.join(namedRules)
    r = re.compile(rule)
    
    def tokenizer(text):
        tokens = []
        for match in r.finditer(text):
                if match.lastgroup:
                    tokens.append(Token(match.lastgroup, match.group(), match.start(), match.end()))
        if tokens[-1].end < len(text):
                raise Exception('Unrecognized character \'{}\''.format(text[tokens[-1].end]))
        return tokens
    return tokenizer
