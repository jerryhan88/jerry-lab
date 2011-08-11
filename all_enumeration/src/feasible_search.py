from __future__ import division #@UnresolvedImport
from input import ran_example
from all_solution_by_me import * #@UnresolvedImport
#from all_solution_by_prof import *
from itertools import *



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

if __name__ == '__main__':
#    search_feasible_sol(6, 2, 2, 3)
#    js, qs, ya, num_yts = ran_example(2, 1, 1, 1)
    js, qs, ya, num_yts = ran_example(4, 1, 1, 3)
#    js, qs, ya, num_yts = ran_example(6, 2, 2, 3)
#    js, qs, ya, num_yts = ran_example(2, 1, 1, 3)
 
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
