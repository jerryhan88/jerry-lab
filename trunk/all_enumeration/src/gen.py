from __future__ import division #@UnresolvedImport
from random import seed, choice, shuffle, randrange #@UnresolvedImport
from clasese import Job#@UnresolvedImport
from itertools import *


def generate(num_jobs, num_qcs, num_ycs, num_yts):
    seed(15)
    js = [Job(i, choice(['D', 'L'])) for i in xrange(num_jobs)]

    # input
    qs = input_partition(js, num_qcs)
    ya = input_partition(js, num_ycs)
    count = 0
    for ys in list_permutations(ya):
        for ts in part_perms(js, num_yts):
            count += 1
            if is_cycle(qs, ys, ts):
                print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', count
                print qs
                print ys
                print ts
                print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'

def build_graph(qs, ys, ts):
    js = [j for j in chain(*qs)]
    for j in js:
        j.make_nodes(4)
    for sq in qs:
        for j in xrange(len(sq) - 1):
            cur_j = sq[j]
            next_j = sq[j + 1]
            if cur_j.type == 'D' and next_j.type == 'D':
                cur_j.nodes[1].next_nodes.append(next_j.nodes[0])
                next_j.nodes[0].prev_nodes.append(cur_j.nodes[1])
            elif cur_j.type == 'D' and next_j.type == 'L':
                cur_j.nodes[1].next_nodes.append(next_j.nodes[2])
                next_j.nodes[2].prev_nodes.append(cur_j.nodes[1])
            elif cur_j.type == 'L' and next_j.type == 'D':
                cur_j.nodes[3].next_nodes.append(next_j.nodes[0])
                next_j.nodes[0].prev_nodes.append(cur_j.nodes[3])
            else:
                '''
                cur_j.type == 'L' and next_j.type == 'L':
                '''
                cur_j.nodes[3].next_nodes.append(next_j.nodes[2])
                next_j.nodes[2].prev_nodes.append(cur_j.nodes[3])
                
    for sy in ys:
        for j in xrange(len(sy) - 1):
            cur_j = sy[j]
            next_j = sy[j + 1]
            if cur_j.type == 'D' and next_j.type == 'D':
                cur_j.nodes[3].next_nodes.append(next_j.nodes[2])
                next_j.nodes[2].prev_nodes.append(cur_j.nodes[3])
            elif cur_j.type == 'D' and next_j.type == 'L':
                cur_j.nodes[3].next_nodes.append(next_j.nodes[0])
                next_j.nodes[0].prev_nodes.append(cur_j.nodes[3])
            elif cur_j.type == 'L' and next_j.type == 'D':
                cur_j.nodes[1].next_nodes.append(next_j.nodes[2])
                next_j.nodes[2].prev_nodes.append(cur_j.nodes[1])
            else:
                '''
                cur_j.type == 'L' and next_j.type == 'L':
                '''
                cur_j.nodes[1].next_nodes.append(next_j.nodes[0])
                next_j.nodes[0].prev_nodes.append(cur_j.nodes[1])
    for st in ts:
        for j in xrange(len(st) - 1):
            cur_j = st[j]
            next_j = st[j + 1]
            cur_j.nodes[2].next_nodes.append(next_j.nodes[1])
            next_j.nodes[1].prev_nodes.append(cur_j.nodes[2])
                        
    
    for j in js:
        print 'Job', j
        max_num_n_n = 0
        max_num_p_n = 0
        for n in j.nodes:
            if len(n.next_nodes) > max_num_n_n:
                max_num_n_n = len(n.next_nodes)
            if len(n.prev_nodes) > max_num_p_n:
                max_num_p_n = len(n.prev_nodes) 
            print '    ', n,
        print '' 
        print '    ',
        print '========'*5
        print '', 'n_n',
        for i in xrange(max_num_n_n):
            for n in j.nodes:
                if len(n.next_nodes) > i:
                    print n.next_nodes[i],'    ',
                else :
                    print '        ',
            if i != max_num_n_n -1:
                print ''
                print '      ',
        print ''
        print '    ',
        print '--------'*5
        print '', 'p_n ',
        for i in xrange(max_num_p_n):
            for n in j.nodes:
                if len(n.prev_nodes) > i:
                    print n.prev_nodes[i],'    ',
                else :
                    print '        ',
            print ''
            print '      ',
        print ''
        
                
#            if len(n.next_nodes) > 1 or (n.next_nodes and n.order == 3):
#                print n 
         
    
    


def is_cycle(qs, ys, ts):
    todo = build_graph(qs, ys, ts)
    makespan = 0
    while todo:
        for i in xrange(len(todo)):
            node = todo[i]
            if node.remove_and_update_t():
                if makespan < node.t:
                    makespan = node.t
                del todo[i]
                break
        else:  # cycle!
            return None
    return makespan

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

def input_partition(jobs, part_num):
    '''
    this function is for partition jobs
    '''
    parts = [[]for _ in xrange(part_num)]
    shuffle(jobs)
    for i, j in enumerate(jobs):
        if i < part_num:
            parts[i].append(j)
        else:
            parts[randrange(part_num)].append(j)
    return parts


if __name__ == '__main__':
#    generate(6, 2, 2, 3)
    j0 = Job(0, 'D')
    j1 = Job(1, 'L')
    j2 = Job(2, 'L')
    j3 = Job(3, 'D')
    qs = [[j0, j1], [j3, j2]]
    ys = [[j3, j1, j0], [j2]]
    ts = [[j2], [j0], [j1, j3]]
    build_graph(qs, ys, ts)
    
