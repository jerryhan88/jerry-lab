from __future__ import division
from random import randrange

n, m = 5, 6
l = [[0] * m for z in xrange(n)]

def display(a):
    print [a], '-' * 30
    for i in xrange(n):
        for j in xrange(m):
            print l[i][j],
        print
    print


def put(q):
    if q == 2:
        case_two(q)
    elif q == 3:
        case_three(q)
    elif q == 4:
        case_four(q)
    else:
        while True:
            i = random.randrange(n)
            j = random.randrange(m)
            if l[i][j] == 0:
                l[i][j] = q
                break

def get(i, j):
    if l[i][j] == 0:
        print 'There is nothing.'
        return 0
    k = l[i][j]
    l[i][j] = 0
    return k

def case_two(q):
    while True:
        ranN = randrange(n * m)
        i = ranN / m
        if l[i][j] == 0:
            if l[i][j - 1] == 1: continue
            if l[i][j + 1] == 1: continue
            if l[i - 1][j] == 1: continue
            if l[i + 1][j] == 1: continue
            l[i][j] = 2
            break
                    

            
def case_three(q):
    pass
def case_four(q):
    pass

if __name__ == '__main__':
    for a in xrange(1, 100):
        display(a)
        print 'put : 1, get : 2'
        
        w = input()
        assert w == 1 or w == 2

        if w == 1:
            print 'input the ID:',
            q = input()
            assert q == 1 or q == 2 or q == 3 or q == 4 or q == 5
            put(q)
        else:
            print 'input the position (i, j)',
            i, j = input()
            k = get(i, j)
            if k > 0:
                print 'The value is %d from (%d, %d).' % (k, i, j)
