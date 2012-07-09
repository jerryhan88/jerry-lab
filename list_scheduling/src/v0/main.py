'''
Created on 2012. 7. 6.

@author: JerryHan
'''

import problem, sys
from enum_all_schedule import all_parallel_machine_schedules
from itertools import permutations

def run(num_machine, p_j, s_jk):
    # find opt solution among all schedules
    min_Cmax = sys.maxint
    opt_schedule = None
    for S in all_parallel_machine_schedules(len(p_j), num_machine):
        Cmax = 0
        for j_seq in S:
            completion_t = 0
            for i, j in enumerate(j_seq):
                if i == 0:
                    completion_t += p_j[j]
                else:
                    completion_t += s_jk[j_seq[i - 1]][j] + p_j[j]
            if completion_t > Cmax:
                Cmax = completion_t
        if Cmax < min_Cmax:
            min_Cmax = Cmax
            opt_schedule = list(S)
    print 'Opt schedule and value of min(Cmax)'
    print '    ', min_Cmax, opt_schedule
    
    # List permutation
    Ls = [l for l in permutations(range(len(p_j)))]
    
    min_Cmax_in_ls = sys.maxint 
    
    for L in Ls:
        # Schedule construction by list
        machines = [[] for _ in xrange(num_machine)]
        c_t = [0]*num_machine
        for j in L:
            f_i = sys.maxint
            target_m = None
            for m_i, j_seq in enumerate(machines):
                if not j_seq:
                    j_seq.append(j)
                    c_t[m_i] += p_j[j]
                    break
                else:
                    expected_completion_t = c_t[m_i] + s_jk[j_seq[-1]][j] + p_j[j] 
                    if expected_completion_t < f_i:
                        f_i = expected_completion_t
                        target_m = m_i
            else: 
                c_t[target_m] += s_jk[machines[target_m][-1]][j] + p_j[j]
                machines[target_m].append(j)
                
        Cmax_of_list_schedulieng = 0
        for j_seq in machines:
            completion_t = 0
            for i, j in enumerate(j_seq):
                if i == 0:
                    completion_t += p_j[j]
                else:
                    completion_t += s_jk[j_seq[i - 1]][j] + p_j[j]
            if completion_t > Cmax_of_list_schedulieng:
                Cmax_of_list_schedulieng = completion_t
        
        if Cmax_of_list_schedulieng < min_Cmax_in_ls:
            min_Cmax_in_ls = Cmax_of_list_schedulieng  
                
    print 'result of list scheduling'
    print '    min Cmax : ', min_Cmax_in_ls
    
    
    if min_Cmax_in_ls != min_Cmax:
        print '                                incorrect!!'
        assert False
    ''' 
    else:
        for i, seq in enumerate(opt_schedule):
            for j, x in enumerate(seq):
                if machines[i][j] != x:
                    assert False
        print '                                correct!!'
    '''
    print '                                correct!!'

if __name__ == '__main__':
#    run(*problem.ex1())
    for seed_num in xrange(100):
        print 'seed number'
        print '    ', seed_num
#        run(*problem.gen_problem(3, 4, 2, 20, 5, 15, True, seed_num))
        run(*problem.gen_problem(3, 7, 30, 100, 5, 15, True, seed_num))
    