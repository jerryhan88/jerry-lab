'''
Created on 2012. 7. 6.

@author: JerryHan
'''

from random import randrange, seed

def gen_problem(num_jobs, p_min, p_max, s_min, s_max, check_trianglur_ineq, seed_num=100):
    seed(seed_num)
    
    p_j = [randrange(p_min, p_max + 1) for _ in xrange(num_jobs)]
    s_jk = []
    temp_p = [randrange(s_max - s_min)for _ in xrange(num_jobs)]
    
    for j in xrange(num_jobs):
        seq_dep_time = []
        for k in xrange(num_jobs):
            if j == k :
                seq_dep_time.append('-')
            else:
                seq_dep_time.append(s_min + abs(temp_p[j] - temp_p[k]))
        s_jk.append(seq_dep_time)
    
    if check_trianglur_ineq:
        for j in xrange(num_jobs):
            for k in xrange(num_jobs):
                if j != k:
                    for i in xrange(num_jobs):
                        if i != j and i != k:
                            assert s_jk[j][i] + s_jk[i][k] >= s_jk[j][k], 'This problem don\'t satisfy triangular inequality'   
    
    return p_j, s_jk 

def problem_display(p_j, s_jk):
    print 'Processing time'
    print '    ', p_j
    
    print 'Setup time'
    for j in s_jk:
        print '    ', j

def ex1():
    return gen_problem(10, 2, 20, 5, 15, True)

if __name__ == '__main__':
    p_j, s_jk = gen_problem(10, 2, 20, 5, 15, True) 
    problem_display(p_j, s_jk)
