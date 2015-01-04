from __future__ import division

from primes import primes as p0
from primes1 import primes as p1
from demo import f_test
f0 = p0
f1 = p1 

kmax = 1000

def test():
    # time it.
    from timeit import timeit
    print timeit("f0(kmax)",'from test import f0, kmax', number=10)
    print timeit("f1(kmax)",'from test import f1, kmax', number=10)

def test1():
    print f_test(12)

if __name__ == '__main__':
    test1()
