from job import *
from gen import *
import time

def get_optimal(qs, nt):
    # all jobs
    js = [j for j in chain(*qs)]

    # YC assignment
    b_max = max(j.block for j in js)
    ya = [[] for i in xrange(b_max + 1)]
    for j in chain(*qs):
        ya[j.block].append(j)

    # total iteration, iteration number
    ti = num_list_perms(ya)
    i = 0

    # current best
    best_ms = 1e400

    # total valids, invalids
    num_valids = 0
    num_invalids = 0

    start = time.time()
    
    for ys in list_permutations(ya):
        for ts in part_perms(js, nt):
            ms = calc_makespan(qs, ys, ts)
            if ms:
                num_valids += 1
                if ms < best_ms:
                    best_ms = ms
                    best_ys = [list(s) for s in ys]
                    best_ts = [list(s) for s in ts]
            else:
                num_invalids += 1

        i += 1
        print '%.3f %d/%d(%d%%) (%d/%d) %d' % (time.time() - start, i, ti, i * 100 / ti, num_valids, num_invalids, best_ms)

    return best_ms, best_ys, best_ts


if __name__ == '__main__':
    # jobs, QC schedule, and # of YTs
    #qs, nt = [[D(0), L(1), D(1)], [L(0), L(0)]], 2
    qs, nt = [[D(0), L(1), D(1)], [D(0), L(0), L(1)]], 3
    #qs, nt = [[D(0), L(1), D(1), D(2)], [D(0), L(0), L(2), L(0)]], 3

    ms, ys, ts = get_optimal(qs, nt)

    print
    print 'makespan', ms
    print 'qs', qs
    print 'ys', ys
    print 'ts', ts
