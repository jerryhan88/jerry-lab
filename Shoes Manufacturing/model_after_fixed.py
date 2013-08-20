from __future__ import division
from subprocess import call, CREATE_NEW_CONSOLE
from time import time, localtime

def ex3():
    
    n = 3;
    m = 4;
    T = 5;
    D = 6;
    beta = 7;
    C = 50;
    B = 35;
    
    f_l = [1, 2, 3, 4, 1, 2];
    d_l = [3, 3, 3, 5, 5, 5];
    q_l = [40, 40, 80, 85, 110, 110]
    aq_l = [0]*m
    Q_l = []
    for i, x in enumerate(f_l):
        fi = x -1
        aq_l[fi] = aq_l[fi]+ q_l[i]
        Q_l.append(aq_l[fi])
    
    b_j = [12, 10, 13, 20];
    w_j = [18, 15, 20, 25];
    
    C0_ij = [
                [35, 21, 28, 32],
                [24, 40, 28, 30],
                [36, 24, 34, 40]
            ];
    alpha_jk = [
                [1, 0.6, 0.8, 0.9],
                [0.6, 1, 0.65, 0.6],
                [0.8, 0.65, 1, 0.85],
                [0.9, 0.6, 0.85, 1]
                ];
                
    return n, m, T, D, beta, C, B, f_l, d_l, Q_l, b_j, w_j, C0_ij, alpha_jk

def ex3_2():
    
    n = 3;
    m = 4;
    T = 5;
    D = 6;
    beta = 7;
    C = 50;
    B = 35;
    
    f_l = [1, 2, 3, 4, 1, 2];
    d_l = [3, 3, 3, 5, 5, 5];
    q_l = [40, 40, 80, 85, 110, 110]
    aq_l = [0]*m
    Q_l = []
    d_max_j = [0]*m
    
    for i, x in enumerate(f_l):
        ti = x -1
        aq_l[ti] = aq_l[ti]+ q_l[i]
        Q_l.append(aq_l[ti])
        
        if d_max_j[ti] < d_l[i]:
            d_max_j[ti] =  d_l[i]
    
    b_j = [12, 10, 13, 20];
    w_j = [18, 15, 20, 25];
    
    C0_ij = [
                [35, 21, 28, 32],
                [24, 40, 28, 30],
                [36, 24, 34, 40]
            ];
    alpha_jk = [
                [1, 0.6, 0.8, 0.9],
                [0.6, 1, 0.65, 0.6],
                [0.8, 0.65, 1, 0.85],
                [0.9, 0.6, 0.85, 1]
                ];
                
    return n, m, T, D, beta, C, B, f_l, d_l, Q_l, d_max_j, b_j, w_j, C0_ij, alpha_jk

def opl_run(ex, mod):
    DAT_FILE = 'Data collection/%s.dat' % (ex)
    MOD_FILE = 'Models collection/%s.mod' % (mod)
    SOL_FILE = 'Shoes Manufacturing.sol' 
    n, m, T, D, beta, C, B, f_l, d_l, Q_l, d_max_j, b_j, w_j, C0_ij, alpha_jk = eval(ex + '()')
    
    print('%s, start time: %d.%d.%d' % (ex, localtime()[3], localtime()[4], localtime()[5]))
    with open(DAT_FILE, 'w') as f:
        f.write('n = %d;\n' % n)
        f.write('m = %d;\n' % m)
        f.write('T = %d;\n' % T)
        f.write('D = %d;\n' % D)
        f.write('beta = %d;\n' % beta)
        f.write('C = %d;\n' % C)
        f.write('B = %d;\n' % B)
        
        f.write('f_l = %s;\n' % str(f_l))
        f.write('d_l = %s;\n' % str(d_l))
        f.write('Q_l = %s;\n' % str(Q_l))
        f.write('d_max_j = %s;\n' % str(d_max_j))
        
        f.write('b_j = %s;\n' % str(b_j))
        f.write('w_j = %s;\n' % str(w_j))
        
        f.write('C0_ij = %s;\n' % str(C0_ij))
        f.write('alpha_jk = %s;\n' % str(alpha_jk))
    f.close()    
    
    st = time()    
#     rv = call(['oplrun', MOD_FILE, DAT_FILE], creationflags=CREATE_NEW_CONSOLE)
    rv = call(['oplrun', MOD_FILE, DAT_FILE])
    if rv == 1:
        print('opl execution ended with errors')
        print('%s, option(%d,%d,%d), end time: %d.%d.%d' % (ex, localtime()[3], localtime()[4], localtime()[5])) 
    
    calc_time = time() - st
    
    print calc_time  
    
#     sol_txt_file_name = MOD_FILE + '_' + ex + '_result.txt'
#     
#     tf = open(sol_txt_file_name, 'w')
#     with open(SOL_FILE, 'r') as sf:
#         obj_func_v = eval(sf.readline())
#         tf.write('obj_func_v = %d, calc_time = %f\n' % (obj_func_v, calc_time))
#         for line in sf:
#             tf.write(str(line))
#     tf.close()        

def examples_test(examples):
    for ex in examples:
        opl_run(ex)  

if __name__ == '__main__':
#     opl_run('ex3', 'v10')
    opl_run('ex3_2', 'v10_2')
#     ex3_2()
#     test_by_datFiles(['Shoes Manufacturing.dat', 'Indonesia_real_data.dat'], 'including_ct9.mod') 
#     examples_test(['real_data'])
#     examples_test(['ex3', 'ex4', 'real_data'])
