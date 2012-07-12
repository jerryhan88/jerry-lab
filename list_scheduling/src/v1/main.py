'''
Created on 2012. 7. 6.

@author: JerryHan
'''

import problem, sys
from enum_all_schedule import all_parallel_machine_schedules
from subprocess import call, CREATE_NEW_CONSOLE
from itertools import permutations
from time import time
def calc_min_Cmax_by_cplex(p_j, num_machine, s_jk):
    start_t = time()
    num_jobs = len(p_j)
    # find opt solution among all schedules
    min_Cmax = None
    MOD_FILE, DAT_FILE, SOL_FILE = 'list_scheduling.mod', 'list_scheduling.dat', 'list_scheduling.sol'
    Nbj = num_jobs
    Nbm = num_machine
    
    #setup time
    S = [list(x) for x in s_jk]
    for x in xrange(num_jobs):
        S[x][x] = sys.maxint 
    str_S = '['
    for start_j in S:
        str_S = str_S + str(start_j) + ','
    str_S = str_S[:-1] + ']'
    
    with open(DAT_FILE, 'w') as f:
        f.write('Nbj = %d;\n' % Nbj)
        f.write('Nbm = %d;\n' % Nbm)
        f.write('p = %s;\n' % str(p_j))
        f.write('s = %s;\n' % str_S)
    
    rv = call(['oplrun', MOD_FILE, DAT_FILE], creationflags=CREATE_NEW_CONSOLE)
    assert rv == 0, 'opl execution ended with errors: %d' % rv
    with open(SOL_FILE, 'r') as f:
        min_Cmax = eval(f.readline())
    min_Cmax = int(min_Cmax + 0.00001)
    end_t = time()
    print 'Opt schedule and value of min(Cmax)'
    print '    ', min_Cmax , 'calculating time : ', end_t - start_t  
    
    return min_Cmax

def calc_min_Cmax_among_lists(p_j, num_machine, s_jk):
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
    return min_Cmax_in_ls
    
def run(num_machine, p_j, s_jk):
    if calc_min_Cmax_by_cplex(p_j, num_machine, s_jk) != calc_min_Cmax_among_lists(p_j, num_machine, s_jk):
        print '                                incorrect!!'
        assert False
    print '                                correct!!'

if __name__ == '__main__':
#    run(*problem.ex1())
    for seed_num in xrange(1000):
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
        
#        run(*problem.gen_problem(3, 4, 2, 20, 5, 15, True, seed_num))
#        run(*problem.gen_problem(3, 7, 70, 130, 20, 80, True, seed_num))
#        run(*problem.gen_problem(3, 4, 70, 130, 20, 80, True, seed_num))
    
