from __future__ import division #@UnresolvedImport

def next_part(k, m, n, p):
    for i in xrange(n - 1, 0, -1):
        if k[i] < p - 1 and k[i] <= m[i - 1]:
            k[i] = k[i] + 1
            m[i] = max(m[i], k[i])
            for j in xrange(i + 1, n - (p - m[i]) + 1):
                k[j] = 0
                m[j] = m[i]
            for j in xrange(n - (p - m[i]) + 1, n):
                k[j] = m[j] = p - (n - j)
            return True
    return False

def make_partition(k, l):
    p = []
    for i in xrange(len(l)):
        j = k[i]
        if len(p) <= j:
            p.append([])
        p[j].append(l[i])
    return p
    
def partitions(l, p):
    n = len(l)
    k = [0] * n
    for i in xrange(n - p + 1, n):
        k[i] = i - (n - p)
    m = list(k)

    yield make_partition(k, l)

    while next_part(k, m, n, p):
        yield make_partition(k, l)
        
def part_perms(l, p):
    for ll in partitions(l, p):
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
    if l:
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
