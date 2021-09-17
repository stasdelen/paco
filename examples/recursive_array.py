from paco.combinators import (Char, Lazy)
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
    print(array(test_str))

if __name__ == '__main__':
    exit(main())