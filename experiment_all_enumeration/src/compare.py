from __future__ import division #@UnresolvedImport
from set_cut_scheduling import set_cut_run
from feasible_solution import search_feasible_sol
from input import ran_example
from random import seed #@UnresolvedImport 
from pprint import pprint #@UnresolvedImport
def comparison():
    seed(100)
    js, qcs, ya, num_yts = ran_example(4, 1, 2, 2)
#    re_fea_sol, re_set_cut = set(), set()
    re_fea_sol, re_set_cut = [],[]
    
    for qs, ys, ts in search_feasible_sol(js, qcs, ya, num_yts):
        q = [x[:]for x in qs]
        y = [x[:]for x in ys]
        t = [x[:]for x in ts]
###        fea_sol = []
##        qcs_seq = []
##        for i, s in enumerate(qs):
##            s.append('QC' + str(i))
##            qcs_seq.append(tuple(s))
##        ycs_seq = []
##        for i, s in enumerate(ys):
##            s.append('YC' + str(i))
##            ycs_seq.append(tuple(s))
##        yts_seq = []
##        for i, s in enumerate(ts):
##            s.append('YT' + str(i))
##            yts_seq.append(tuple(s))
##        re_fea_sol.add((tuple(qcs_seq), tuple(ycs_seq), tuple(yts_seq)))
            
        re_fea_sol.append([q, y, t])

    for qs, ys, ts in set_cut_run(js, qcs, ya, num_yts):
        re_set_cut.append([qs, ys, ts])
    
    print len(re_fea_sol), re_fea_sol
    print len(re_set_cut), re_set_cut
    
    set_fea_sol = set()
    for qs, ys, ts in re_fea_sol:
        qcs_seq = []
        for i, s in enumerate(qs):
            sq = [x.id for x in s] 
            sq.append('QC' + str(i))
            qcs_seq.append(tuple(sq))
        ycs_seq = []
        for i, s in enumerate(ys):
            sy = [x.id for x in s]
            sy.append('YC' + str(i))
            ycs_seq.append(tuple(sy))
        yts_seq = []
        for i, s in enumerate(ts):
            st = [x.id for x in s]
            st.append('YT' + str(i))
            yts_seq.append(tuple(st))
        set_fea_sol.add((tuple(qcs_seq), tuple(ycs_seq), tuple(yts_seq)))
    print len(set_fea_sol), set_fea_sol 
    
    
    set_set_cut = set()
    for qs, ys, ts in re_set_cut:
        qcs_seq = []
        for q in qs:
            sq = list(q.job_seq)
            sq.append('QC' + str(q.id))
            qcs_seq.append(tuple(sq))
#            print sq 
        ycs_seq = []
        for y in ys:
            sy = list(y.job_seq)
            sy.append('YC' + str(y.id))
            ycs_seq.append(tuple(sy))
        yts_seq = []
        for t in ts:
            st = list(t.job_seq)
            st.append('YT' + str(t.id))
            yts_seq.append(tuple(st))
        set_set_cut.add((tuple(qcs_seq), tuple(ycs_seq), tuple(yts_seq)))
    print len(set_set_cut),set_set_cut
    
if __name__ == '__main__':
    comparison()
