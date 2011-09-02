from __future__ import division #@UnresolvedImport
from set_cut_scheduling import set_cut_all_enumeration, initialize
from feasible_solution import search_feasible_sol
from input import ran_example
from random import seed #@UnresolvedImport 
def comparison():
#    seed(100) #0:D ,3:L ,1:D ,2:L
#    seed(10)

#    seed(99)  #1:D ,2:D ,0:D ,3:D 
#    seed(16)  #2:D ,0:D ,3:D ,1:D 
#    seed(17)  #0:L ,1:L ,2:L ,3:D 

    js, qcs, ya, num_yts = ran_example(4, 1, 2, 2)
#    js, qcs, ya, num_yts = ran_example(4, 2, 2, 3)
#    re_fea_sol, re_set_cut = set(), set()
    re_fea_sol, re_set_cut = [], []
    
    for qs, ys, ts in search_feasible_sol(js, qcs, ya, num_yts):
        q = tuple([tuple(x[:])for x in qs])
        y = [x[:]for x in ys]
        t = [x[:]for x in ts]
        re_fea_sol.append([q, y, t])


    jobs, qcs_seq, ycs_seq, yts_seq, planed_jobs, qcs_primary_j, agreeable_yts_of_jobs, handling_v, qcs_num_of_flag, cut = initialize(js, qcs, ya, num_yts)
    for ys, ts in set_cut_all_enumeration(cut, agreeable_yts_of_jobs, qcs_num_of_flag, qcs_primary_j, planed_jobs, ycs_seq, yts_seq, jobs, qcs_seq, handling_v):
        re_set_cut.append([qcs_seq, ys, ts])
    
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
            sq = list(q[:])
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
    print len(set_set_cut), set_set_cut
    
    print set_set_cut == set_fea_sol
    
    if set_set_cut == set_fea_sol:
        return True
    
if __name__ == '__main__':
#    seed(19)
#    comparison()
#'''
    seed_num = 0
    success_count = 0
    false_seed_nums = []
    while seed_num != 30:
        print '~~~~~~~~~~~~~~~~~~~', seed_num
        seed(seed_num)
        if comparison():
            success_count += 1
        else:
            false_seed_nums.append(seed_num)
        seed_num += 1
        
    print success_count
    print false_seed_nums
#'''