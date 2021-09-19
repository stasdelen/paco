from paco.combinators import Lazy
from paco.atomic import Char
from paco.miscellaneous import (STRING, FLOAT, INTEGER, OWS)

lbra = Char('[') << OWS
rbra = Char(']') << OWS
comm = Char(',') << OWS


floatNum = FLOAT.map(lambda x : float(x))
intNum = INTEGER.map(lambda x : int(x))

array = Lazy()
element = (floatNum | intNum | STRING | array) << OWS
array.p = OWS >> lbra >> element.sepby(comm) << rbra

def main():
    test_str = " [ [1, 3, 2.57e-3], ['hi', 'howdy', 'bye'], 42.32, [ [1, 2], [4 , 5]] ] "
    print('Running on: ' + test_str)
    _, ar = array(test_str)
    print('Result: {}'.format(ar))
    
    print('(ar[0][2] == {})'.format(ar[0][2]))
    print('(ar[1][1] == {})'.format(ar[1][1]))
    print('(ar[2] == {})'.format(ar[2]))
    print('(ar[3][1][0] == {})'.format(ar[3][1][0]))

if __name__ == '__main__':
    exit(main())