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
                raise Exception('Unknown token @{}.'.format(i))
        return tokens
    return tokenizer