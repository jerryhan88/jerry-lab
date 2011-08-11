from __future__ import division #@UnresolvedImport
from random import seed, randrange #@UnresolvedImport

def next_part(k, m, n, p):
    for i in xrange(n - 1, -1, -1):
        if k[i] < p - 1:
            k[i] = k[i] + 1
            return True
        else:
            k[i] = 0
    return False

def make_partition(k, l, num_part):
#    n = len(l)
    p = [[] for _ in xrange(num_part)]
    for i in xrange(len(l)):
        j = k[i]
        p[j].append(l[i])
    return p
    
def partitions(l, p):
    seed(10)
    n = len(l)
    k = [0] * n
#    print k
    m = list(k)
    yield make_partition(k, l, p)
    while next_part(k, m, n, p):
        yield make_partition(k, l, p)
        
def part_perms(l, p):
    for ll in partitions(l, p):
#        print ll
        for x in list_permutations(ll):
            yield x

def next_perm(l, n):
    if n > 2:
        for p in next_perm(l, n - 1):
            yield p
    m = len(l) - n
    for c in xrange(n - 1):
        if n & 1 == 0 and c > 1:
            b = m + c + 1
        else:
            b = m + 1
        t = l[m]; l[m] = l[b]; l[b] = t
        yield l
        if n > 2:
            for p in next_perm(l, n - 1):
                yield p
                
def permutations(l):
#    if l:
    yield l
    for p in next_perm(l, len(l)):
        yield p
            
def list_permutations(ll):
    n = len(ll)
    # ls is copy of ll
    ls = [list(ll[i]) for i in xrange(n)]
    # init each permutation
    ys = [permutations(ls[i]) for i in xrange(n)]
    
    for i in xrange(n):
        ys[i].next()
    yield ls
    while True:
        i = 0
        while i < n:
            try:
                ys[i].next()
                break
            except StopIteration:
                # re-init ls[i] and ys[i]
                ls[i] = list(ll[i])
                ys[i] = permutations(ls[i])
                ys[i].next()
                i = i + 1
        if i == n:
            break
        yield ls


if __name__ == '__main__':
    i = 0
    l = range(5)

    '''
    s = set()
    for x in permutations(l):
        i = i + 1
        print i, x
        s.add(tuple(x))
    print i, len(s)
    '''

    '''
    for x in partitions(l, 3):
        i = i + 1
        print i, x
    '''

    '''
    ll = [[1, 2], [3, 4, 5], [6, 7, 8]]
    for x in list_permutations(ll):
        i = i + 1
        print i, x
    '''

#    '''
    for x in part_perms(l, 3):
        i = i + 1
        print i, x
#    '''
