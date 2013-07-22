from __future__ import division
from subprocess import call, CREATE_NEW_CONSOLE
from time import time, localtime

def real_data():
    n = 8;
    m = 5;
    T = 11;
    D = 12;
    beta = 100;
    C = 2000;
    B = 4500;
    f_l = [2,3,1,4,1,2,3,4,1,3,2,5];
    d_l = [6,7,8,9,10,10,10,10,11,11,11,11];
    Q_l = [11268,23088,8034,9264,16242,21708,47598,14736,23202,49062,34464,49625];
    b_j = [662, 580, 455, 296, 327];
    w_j = [11.42, 8.44, 9.23, 8.48, 8.77];
    lamda_ij = [[1950, 1600, 1600, 1600, 1600], 
                [1600, 1600, 1950, 1780, 1790], 
                [1600, 1600, 1950, 1680, 1950], 
                [1600, 1600, 1950, 1680, 1950], 
                [1600, 1600, 1950, 1680, 1950], 
                [1600, 1900, 1950, 1680, 1690], 
                [1600, 1600, 1950, 1680, 1690], 
                [1600, 1600, 1950, 1680, 1690]];
    alpha_jk = [[1, 0.92, 0.8, 0.8, 0.8], 
                [0.92, 1, 0.85, 0.85, 0.85], 
                [0.8, 0.85, 1, 0.92, 0.92], 
                [0.8, 0.85, 0.92, 1, 0.95], 
                [0.8, 0.85, 0.92, 0.95, 1]];
                
    return n, m, T, D, beta, C, B, f_l, d_l, Q_l, b_j, w_j, lamda_ij, alpha_jk



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
    Q_l = [40, 40, 80, 85, 150, 150];
    
    b_j = [12, 10, 13, 20];
    w_j = [18, 15, 20, 25];
    
    lamda_ij = [
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
                
    return n, m, T, D, beta, C, B, f_l, d_l, Q_l, b_j, w_j, lamda_ij, alpha_jk

def ex4():
    
    n = 3;
    m = 5;
    T = 5;
    D = 6;
    beta = 7;
    C = 50;
    B = 35;
    
    f_l = [1, 3, 4, 5, 1, 2];
    d_l = [3, 3, 3, 5, 5, 5];
    Q_l = [40, 40, 80, 85, 120, 120];
    
    b_j = [12, 10, 13, 20, 13];
    w_j = [18, 15, 20, 25, 18];
    
    lamda_ij = [
                [35, 21, 28, 32, 26],
                [24, 40, 28, 30, 36],
                [36, 24, 34, 40, 24]
            ];
    alpha_jk = [
                [1,     0.6,    0.8,    0.9,    0.7],
                [0.6,   1,      0.65,   0.6,    0.9],
                [0.8,   0.65,   1,      0.85,   0.7],
                [0.9,   0.6,    0.85,   1,      0.6],
                [0.7,   0.9,    0.7,    0.6,    1]
                ];
                
    return n, m, T, D, beta, C, B, f_l, d_l, Q_l, b_j, w_j, lamda_ij, alpha_jk


def opl_run(ex):
#     for MOD_FILE in ['original.mod', 'excluding_ct9.mod', 'including_ct9.mod', 'v2.mod', 'v3.mod']:
    for MOD_FILE in ['v4.mod']:
        DAT_FILE, SOL_FILE = 'Shoes Manufacturing.dat', 'Shoes Manufacturing.sol'
        
        n, m, T, D, beta, C, B, f_l, d_l, Q_l, b_j, w_j, lamda_ij, alpha_jk = eval(ex + '()')
        
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
            f.write('b_j = %s;\n' % str(b_j))
            f.write('w_j = %s;\n' % str(w_j))
            
            f.write('lamda_ij = %s;\n' % str(lamda_ij))
            f.write('alpha_jk = %s;\n' % str(alpha_jk))
            
        st = time()    
        rv = call(['oplrun', MOD_FILE, DAT_FILE], creationflags=CREATE_NEW_CONSOLE)
        if rv == 1:
            print('opl execution ended with errors')
            print('%s, option(%d,%d,%d), end time: %d.%d.%d' % (ex, localtime()[3], localtime()[4], localtime()[5])) 
        
        calc_time = time() - st 
        
        sol_txt_file_name = MOD_FILE + '_' + ex + '_result.txt'
        
        tf = open(sol_txt_file_name, 'w')
        with open(SOL_FILE, 'r') as sf:
            obj_func_v = eval(sf.readline())
            tf.write('obj_func_v = %d, calc_time = %f\n' % (obj_func_v, calc_time))
            for line in sf:
                tf.write(str(line))
        tf.close()        

def examples_test(examples):
    for ex in examples:
        opl_run(ex)  

def test_by_datFiles(dats, modFile):
    MOD_FILE = modFile
    SOL_FILE = 'Shoes Manufacturing.sol'
    for dat in dats:
        DAT_FILE = dat
        st = time()    
        rv = call(['oplrun', MOD_FILE, DAT_FILE], creationflags=CREATE_NEW_CONSOLE)
        if rv == 1:
            print('opl execution ended with errors')
        calc_time = time() - st 
        
        sol_txt_file_name = MOD_FILE + '_' + DAT_FILE + '_result.txt'
        
        tf = open(sol_txt_file_name, 'w')
        with open(SOL_FILE, 'r') as sf:
            obj_func_v = eval(sf.readline())
            tf.write('obj_func_v = %d, calc_time = %f\n' % (obj_func_v, calc_time))
            for line in sf:
                tf.write(str(line))
        tf.close()

if __name__ == '__main__':
    test_by_datFiles(['Shoes Manufacturing.dat', 'Indonesia_real_data.dat'], 'including_ct9.mod') 
#     examples_test(['real_data'])
#     examples_test(['ex3', 'ex4', 'real_data'])
