from __future__ import division #@UnresolvedImport
from set_cut_scheduling import set_cut_all_enumeration, initialize
from feasible_solution import search_feasible_sol
from input import ran_example
from random import seed #@UnresolvedImport
from time import time 
def comparison(f, seed_num):
    js, qcs, ya, num_yts = ran_example(6, 2, 2, 3)
    re_fea_sol, re_set_cut = [], []
    print 'search_feasible start!!'
    count = 0
    start_t = time()
    for qs, ys, ts in search_feasible_sol(js, qcs, ya, num_yts):
        count += 1
        if count % 1000 == 0:
            print 'time : ', str(time() - start_t), '        doing search_feasible_sol...   count : ', count    
        q = tuple([tuple(x[:])for x in qs])
        y = [x[:]for x in ys]
        t = [x[:]for x in ts]
        re_fea_sol.append([q, y, t])
    print 'total : ', count
    print 'search_feasible end!!'
    
    
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
    s1 = (len(set_fea_sol), set_fea_sol)
    
    jobs, qcs_seq, ycs_seq, yts_seq, planed_jobs, qcs_primary_j, agreeable_yts_of_jobs, handling_v, qcs_num_of_flag, cut = initialize(js, qcs, ya, num_yts)
    for ys, ts in set_cut_all_enumeration(cut, agreeable_yts_of_jobs, qcs_num_of_flag, qcs_primary_j, planed_jobs, ycs_seq, yts_seq, jobs, qcs_seq, handling_v):
        re_set_cut.append([qcs_seq, ys, ts])
    
    
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
    s2 = (len(set_set_cut), set_set_cut)
    
#    print len(re_fea_sol), re_fea_sol
#    print len(re_set_cut), re_set_cut    
#    print len(set_fea_sol), set_fea_sol    
#    print len(set_set_cut), set_set_cut    
#    print set_set_cut == set_fea_sol
    r1_size, r1_content = s1
    r2_size, r2_content = s2
    if r1_size != r2_size:
        f.write('seed number : ' + str(seed_num))
        f.write('\n')
        f.write('r1_size : ' + str(r1_size) + '    r2_size : ' + str(r2_size))
        f.write('\n')
        for i, x in enumerate(r2_content):
            if x not in r1_content:
                f.write(str(i) + ' : ' + str(x))
                f.write('\n')
        f.write('\n')
    if set_set_cut == set_fea_sol:
        return True
    
    
    
if __name__ == '__main__':
#    seed(19)
#    comparison()
#'''
    total_num = 1
    seed_num = 0
    success_count = 0
    false_seed_nums = []
    f = file('result.txt', 'w')
    while seed_num != total_num:
#        print '~~~~~~~~~~~~~~~~~~~', seed_num
#        if seed_num % 2 == 0 :
#            print 'success/total : ', success_count, '/', total_num,   '    ', seed_num
            
        print 'start'
        seed(seed_num)
        if comparison(f, seed_num):
            success_count += 1
        else:
            false_seed_nums.append(seed_num)
        seed_num += 1
        print 'success/total : ', success_count, '/', total_num, '    ', seed_num
    print success_count, '/', total_num
#    print false_seed_nums
#'''
