'''
Created on 2012. 7. 6.

@author: JerryHan
'''

import problem, sys
from enum_all_schedule import all_parallel_machine_schedules
from itertools import permutations
from time import time
def calc_min_Cmax_among_shceuldes(p_j, num_machine, s_jk):
    start_t = time()
    # find opt solution among all schedules
    min_Cmax = sys.maxint
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
    end_t = time()
    print 'Opt schedule and value of min(Cmax)'
    print '    min Cmax : ', min_Cmax, 'calculating time : ', end_t - start_t
    return min_Cmax

def calc_min_Cmax_among_lists(p_j, num_machine, s_jk):
    start_t = time()
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
    end_t = time()
                
    print 'result of list scheduling'
    print '    min Cmax : ', min_Cmax_in_ls, 'calculating time : ', end_t - start_t
    return min_Cmax_in_ls

def run(num_machine, p_j, s_jk):
    if calc_min_Cmax_among_lists(p_j, num_machine, s_jk) != calc_min_Cmax_among_shceuldes(p_j, num_machine, s_jk):
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
    
    '''
    # make list L from Opt schedule
    L = []
    expected_possible_assign_time = [0]*num_machine
    tj_in_seq = [0]*num_machine
    min_a_t = min(expected_possible_assign_time)
    while True:
        tj = None
        for i, EPAT in enumerate(expected_possible_assign_time):
            if min_a_t == EPAT and min_a_t != sys.maxint:
                tj = opt_schedule[i][tj_in_seq[i]]
                L.append(tj)
                tj_in_seq[i] += 1
                if tj_in_seq[i] != len(opt_schedule[i]):
                    if tj_in_seq[i] ==1:
                        expected_possible_assign_time[i] += p_j[tj]
                    else:
                        prev_j = opt_schedule[i][tj_in_seq[i]-2]
                        expected_possible_assign_time[i] += s_jk[prev_j][tj] + p_j[tj]
                else:
                    expected_possible_assign_time[i] = sys.maxint
                min_a_t = min(expected_possible_assign_time)
                break
        else:
            break
    print 'List of opt schedule'
    print '    ', L    
    '''

def test_one():
    run(*problem.gen_problem(3, 6, 70, 130, 20, 80, True, 0))

def test_random_many():
    for seed_num in xrange(100):
        print 'seed number'
        print '    ', seed_num
        print 'machine 3, job 5'
        run(*problem.gen_problem(3, 5, 70, 130, 20, 80, True, seed_num))
        print 'machine 3, job 8'
        run(*problem.gen_problem(3, 8, 70, 130, 20, 80, True, seed_num))
        print 'machine 4, job 8'
        run(*problem.gen_problem(4, 8, 70, 130, 20, 80, True, seed_num))
        print 'machine 5, job 10'
        run(*problem.gen_problem(5, 10, 70, 130, 20, 80, True, seed_num))
        

if __name__ == '__main__':
#    run(*problem.ex1())
    test_one()
    #test_random_many()
