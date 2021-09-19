from .atomic import Regex

LETTERS = Regex(r'[a-zA-Z]+')
'''One or more of the set [a-zA-Z]'''

LETTER = Regex(r'[a-zA-Z]')
'''Any char from the set [a-zA-Z]'''

STRING = Regex(r"'[^']*'")
'''Single quoted string like \'hi!\''''

NUMBERS = Regex(r'[0-9]+')
'''One or more of the set [0-9]'''

NUMBER = Regex(r'[0-9]')
'''Any digit from the set [0-9]'''

INTEGER = Regex(r'[1-9][0-9]*')
'''Integer'''

FLOAT = Regex(r'[0-9]*\.[0-9]+([Ee][+\-]?[0-9]+)*')
'''Float that can also include scientific notation'''

HEXD = Regex(r'0x[1-9a-fA-F][0-9a-fA-F]*')
'''Hexadecimal number that starts with 0x...'''

OWS = Regex(r'[ \t\n]*')
'''Zero or more White Space. Excepts; \' \', \'\\t\', \'\\n\''''

WS = Regex(r'[ \t\n]+')
'''One or more White Space. Excepts; \' \', \'\\t\', \'\\n\''''