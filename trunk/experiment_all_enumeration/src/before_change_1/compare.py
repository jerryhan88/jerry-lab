from __future__ import division #@UnresolvedImport
from set_cut_scheduling import set_cut_run, initialize
from feasible_solution import search_feasible_sol
from input import ran_example
from random import seed #@UnresolvedImport 
from pprint import pprint #@UnresolvedImport
def comparison():
#    seed(100)
#    seed(10)

#    seed(99)  #1:D ,2:D ,0:D ,3:D 
    seed(16)  #2:D ,0:D ,3:D ,1:D 
#    seed(17)  #0:L ,1:L ,2:L ,3:D 

    js, qcs, ya, num_yts = ran_example(4, 1, 2, 2)
#    js, qcs, ya, num_yts = ran_example(4, 2, 2, 3)
#    re_fea_sol, re_set_cut = set(), set()
    re_fea_sol, re_set_cut = [],[]
    
    for qs, ys, ts in search_feasible_sol(js, qcs, ya, num_yts):
        q = [x[:]for x in qs]
        y = [x[:]for x in ys]
        t = [x[:]for x in ts]
        re_fea_sol.append([q, y, t])


    jobs, qcs_seq, ycs_seq, yts_seq, scheduled_js, qcs_primary_j, agreeable_yt_of_job, handling_v, qcs_num_of_flag, cut =  initialize(js, qcs, ya, num_yts)
    for qs, ys, ts in set_cut_run(jobs, qcs_seq, ycs_seq, yts_seq, scheduled_js, qcs_primary_j, agreeable_yt_of_job, handling_v, qcs_num_of_flag, cut):
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
        for i, q in enumerate(qs):
            sq = q[:]
            sq.append('QC' + str(i))
            qcs_seq.append(tuple(sq))
        ycs_seq = []
        for i, y in enumerate(ys):
            sy = y[:]
            sy.append('YC' + str(i))
            ycs_seq.append(tuple(sy))
        yts_seq = []
        for i, t in enumerate(ts):
            st = t[:]
            st.append('YT' + str(i))
            yts_seq.append(tuple(st))
        set_set_cut.add((tuple(qcs_seq), tuple(ycs_seq), tuple(yts_seq)))
    print len(set_set_cut),set_set_cut
    
    print set_set_cut == set_fea_sol
    
if __name__ == '__main__':
    comparison()
