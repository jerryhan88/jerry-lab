from __future__ import division #@UnresolvedImport
from input import ran_example
from itertools import chain #@UnresolvedImport

def search_feasible_sol(js, qs, ya, num_yts):
    for ys in list_permutations(ya):
        for ts in part_perms(js, num_yts):
            if not is_cycle(qs, ys, ts):
                yield (qs, ys, ts)
#            yield (qs, ys, ts)

def build_graph(qs, ys, ts, visualize=False):
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
    if visualize:
        # below part is for visualizing graph
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
            print '========' * 5
            print '', 'n_n',
            for i in xrange(max_num_n_n):
                for n in j.nodes:
                    if len(n.next_nodes) > i:
                        print n.next_nodes[i], '    ',
                    else :
                        print '        ',
                if i != max_num_n_n - 1:
                    print ''
                    print '      ',
            print ''
            print '    ',
            print '--------' * 5
            print '', 'p_n ',
            for i in xrange(max_num_p_n):
                for n in j.nodes:
                    if len(n.prev_nodes) > i:
                        print n.prev_nodes[i], '    ',
                    else :
                        print '        ',
                print ''
                print '      ',
            print ''
    todo = []
    for j in js:
        if not j.nodes[0].prev_nodes:
            todo.append(j.nodes[0])
    return todo                        

def is_cycle(qs, ys, ts):
    todo = build_graph(qs, ys, ts)
    if not todo:
        return True
    while todo:
        for i in xrange(len(todo)):
            node = todo[i]
            if node.check_delible():
                del todo[i]
                node.visited = True
                for n_n in node.next_nodes:
                    todo.append(n_n)
                break
        else:  # cycle!
            return True
    return False

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
    n = len(l)
    k = [0] * n
    m = list(k)
    yield make_partition(k, l, p)
    while next_part(k, m, n, p):
        yield make_partition(k, l, p)
        
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

def save_schedules(pb, S, fname):
    import pickle #@UnresolvedImport
    f = open(fname, 'wb')
    pickle.dump((pb, S), f)
    f.close()

def load_schedules(fname):
    import pickle #@UnresolvedImport
    f = open(fname, 'rb')
    pb, S = pickle.load(f)
    f.close()
    return pb, S

if __name__ == '__main__':
#    search_feasible_sol(6, 2, 2, 3)
#    js, qs, ya, num_yts = ran_example(2, 1, 1, 1)
    pb = js, qs, ya, num_yts = ran_example(4, 1, 1, 3)
#    js, qs, ya, num_yts = ran_example(6, 2, 2, 3)
#    js, qs, ya, num_yts = ran_example(2, 1, 1, 3)

    ''' 
    count = 0
    for qs, ys, ts in search_feasible_sol(js, qs, ya, num_yts):
        print ''
        print count
        count += 1
        for i, sq in enumerate(qs):
            print 'QC' + str(i) + ':' + str(sq),
        print ''
        for i, sy in enumerate(ys):
            print 'YC' + str(i) + ':' + str(sy),
        print ''
        for i, st in enumerate(ts):
            print 'YT' + str(i) + ':' + str(st), ' ',
        print ''
    '''

    S = []
    for s in search_feasible_sol(*pb):
        S.append([[list(seq) for seq in t] for t in s])
    print pb, S

    save_schedules(pb, S, 'test.pkl')
    
    pb, S = load_schedules('test.pkl')
    print pb, S

