from __future__ import division #@UnresolvedImport
from set_cut_scheduling import set_cut_run
from feasible_solution import search_feasible_sol
from input import ran_example
from random import seed#@UnresolvedImport 

def comparison():
    seed(100)
    js, qcs, ya, num_yts = ran_example(4, 1, 2, 2)
    re_set_cut, re_fea_sol = [], []
    
    for qs, ys, ts in search_feasible_sol(js, qcs, ya, num_yts):
        re_fea_sol.append([qs, ys, ts])

    for qs, ys, ts in set_cut_run(js, qcs, ya, num_yts):
        re_set_cut.append([qs, ys, ts])
    
    print len(re_fea_sol), re_fea_sol
    print len(re_set_cut), re_set_cut

if __name__ == '__main__':
    comparison()
