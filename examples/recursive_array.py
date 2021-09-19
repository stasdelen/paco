from paco.combinators import Lazy
from paco.atomic import Char
from paco.miscellaneous import (letters, numbers, optSpace)

lbra = Char('[').then(optSpace)
rbra = Char(']').then(optSpace)
comm = Char(',').then(optSpace)

array = Lazy().rename('array')
element = numbers.rename('int') | letters.rename('str') | array
array.p = optSpace >> lbra >> element.sepby(comm) << rbra << optSpace

def main():
    test_str = ' [ [1, 3, 5], [hi, howdy, bye], 42, [[1,2], [4,5]]] '
    print('Running on: ' + test_str)
    _, ar = array(test_str)
    print('(ar[0][2] == {}) ->'.format(ar[0][2]), ar[0][2] == '5')
    print('(ar[1][1] == {}) ->'.format(ar[1][1]), ar[1][1] == 'howdy')
    print('(ar[3][1][0] == {}) ->'.format(ar[3][1][0]), ar[3][1][0] == '4')

if __name__ == '__main__':
    exit(main())