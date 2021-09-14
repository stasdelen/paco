from paco.parsers.combinators import (Char, Lazy)
from paco.parsers.miscellaneous import (letters, numbers, optSpace)

lbra = Char('[').inside(optSpace)
rbra = Char(']').inside(optSpace)
comm = Char(',').inside(optSpace)

array = Lazy().rename('array')
element = numbers.rename('int') | letters.rename('str') | array
array.parser = lbra >> element.sepby(comm) << rbra

def main():
    test_str = ' [ [1, 3, 5], [hi, howdy, bye], 42, [[1,2], [4,5]]] '
    print('Running on: ' + test_str)
    print(array(test_str))

if __name__ == '__main__':
    exit(main())