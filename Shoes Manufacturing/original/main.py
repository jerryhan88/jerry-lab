from __future__ import division
from subprocess import call, CREATE_NEW_CONSOLE
from time import time, localtime

def ex1():
    
    n = 3;
    m = 4;
    T = 5;
    D = 6;
    beta = 7;
    C = 50;
    B = 40;
    
    f_l = [1, 3, 4, 1, 3, 2];
    d_l = [3, 3, 3, 5, 5, 5];
    Q_l = [90, 30, 80, 130, 120, 170];
    
    b_j = [15, 10, 10, 25];
    w_j = [18, 15, 14, 24];
    
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

def ex2():
    
    n = 3;
    m = 4;
    T = 5;
    D = 6;
    beta = 6;
    C = 50;
    B = 40;
    
    f_l = [1, 3, 4, 1, 3, 2];
    d_l = [3, 3, 3, 5, 5, 5];
    Q_l = [90, 30, 80, 130, 120, 170];
    
    b_j = [15, 10, 10, 25];
    w_j = [18, 15, 14, 24];
    
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


def ex5():
    
    n = 3;
    m = 4;
    T = 5;
    D = 6;
    beta = 7;
    C = 50;
    B = 40;
    
    f_l = [1, 3, 4, 1, 3, 2];
    d_l = [3, 3, 3, 3, 5, 5];
    Q_l = [90, 40, 80, 130, 120, 135];
    
    b_j = [15, 10, 10, 25];
    w_j = [18, 15, 14, 24];
    
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

def ex6():
    
    n = 3;
    m = 4;
    T = 5;
    D = 6;
    beta = 10;
    C = 50;
    B = 40;
    
    f_l = [1, 2, 3, 4, 1, 2];
    d_l = [3, 3, 3, 3, 5, 5];
    Q_l = [70, 70, 70, 70, 225, 225];
    
    b_j = [10, 10, 10, 10];
    w_j = [10, 25, 10, 25];
    
    lamda_ij = [
                [50, 50, 50, 50],
                [50, 50, 50, 50],
                [50, 50, 50, 50]
            ];
    alpha_jk = [
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1]
                ];
    
    return n, m, T, D, beta, C, B, f_l, d_l, Q_l, b_j, w_j, lamda_ij, alpha_jk

def fake_data():
    n = 15;
    m = 10;
    T = 25;
    D = 5;
    beta = 100;
    C = 2000;
    B = 8000;
    f_l = [3, 2, 3, 6, 9];
    d_l = [10, 11, 11, 11, 11];
    Q_l = [9738, 11268, 32826, 8034, 9264];
    b_j = [662, 580, 455, 296, 327, 562, 629, 633, 453, 654];
    w_j = [11.4, 8.4, 9.2, 8.5, 8.8, 6.75, 11.13, 10.38, 9.52, 9.11];
    alpha_jk = [
                [1, 0.92, 0.8, 0.8, 0.8, 0.85, 0.95, 0.92, 0.85, 0.92],
                [0.92, 1, 0.85, 0.85, 0.85, 0.8, 0.8, 0.82, 0.83, 0.8],
                [0.8, 0.85, 1, 0.92, 0.92, 0.8, 0.8, 0.8, 0.8, 0.8],
                [0.8, 0.85, 0.92, 1, 0.95, 0.8, 0.8, 0.8, 0.8, 0.8],
                [0.8, 0.85, 0.92, 0.95, 1, 0.8, 0.8, 0.8, 0.8, 0.8],
                [0.85, 0.8, 0.8, 0.8, 0.8, 1, 0.88, 0.84, 0.8, 0.91],
                [0.95, 0.8, 0.8, 0.8, 0.8, 0.88, 1, 0.95, 0.83, 0.82],
                [0.92, 0.82, 0.8, 0.8, 0.8, 0.84, 0.95, 1, 0.83, 0.8],
                [0.85, 0.83, 0.8, 0.8, 0.8, 0.8, 0.83, 0.83, 1, 0.85],
                [0.92, 0.8, 0.8, 0.8, 0.8, 0.91, 0.82, 0.8, 0.85, 1]
                ];
    lamda_ij = [
                [1950, 1600, 1600, 1600, 1600, 1800, 1830, 1880, 1600, 1600],
                [1830, 1600, 1600, 1600, 1600, 1600, 1850, 1600, 1600, 1950],
                [1880, 1600, 1950, 1600, 1600, 1600, 1600, 1600, 1600, 1600],
                [1950, 1600, 1600, 1600, 1600, 1600, 1880, 1950, 1600, 1600],
                [1950, 1600, 1600, 1600, 1600, 1890, 1810, 1920, 1600, 1600],
                [1600, 1950, 1600, 1600, 1600, 1600, 1600, 1600, 1600, 1600],
                [1600, 1600, 1600, 1600, 1600, 1600, 1600, 1600, 1950, 1600],
                [1600, 1600, 1750, 1780, 1950, 1600, 1600, 1600, 1950, 1600],
                [1600, 1600, 1950, 1780, 1790, 1600, 1600, 1600, 1600, 1600],
                [1600, 1600, 1950, 1680, 1950, 1600, 1600, 1600, 1600, 1600],
                [1600, 1600, 1950, 1680, 1950, 1600, 1600, 1600, 1600, 1600],
                [1600, 1600, 1950, 1680, 1950, 1600, 1600, 1600, 1600, 1600],
                [1600, 1900, 1950, 1680, 1690, 1600, 1600, 1600, 1600, 1600],
                [1600, 1600, 1950, 1680, 1690, 1600, 1600, 1600, 1600, 1600],
                [1600, 1600, 1950, 1680, 1690, 1600, 1600, 1600, 1600, 1600],
            ];
    
    return n, m, T, D, beta, C, B, f_l, d_l, Q_l, b_j, w_j, lamda_ij, alpha_jk

def real_data():
    n = 15;
    m = 10;
    T = 25;
    D = 71;
    beta = 100;
    C = 2000;
    B = 8000;
    f_l = [3, 2, 3, 6, 9, 1, 8, 2, 3, 9, 4, 1, 8, 2, 3, 6, 9, 4, 8, 1, 2, 3, 9, 4,
           1, 2, 3, 9, 8, 1, 8, 3, 9, 4, 8, 1, 3, 9, 5, 7, 1, 10, 2, 3, 6, 5, 7, 8,
           1, 10, 2, 3, 9, 4, 1, 8, 2, 3, 9, 7, 4, 8, 1, 3, 7, 9, 3, 8, 9, 1, 2];
    d_l = [10, 11, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
           12, 12, 12, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 15, 15, 15,
           15, 15, 16, 16, 16, 16, 16, 16, 25, 25, 25, 25, 25, 25, 25, 25, 25,
           25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25,
           25, 25, 25];
    Q_l = [9738, 11268, 32826, 8034, 9264, 8208, 486, 21708, 56850, 11574,
           3162, 15168, 1950, 34464, 88710, 25752, 27576, 7966, 16770, 26934,
           45324, 129057, 40752, 11794, 36972, 49098, 177573, 45900, 17424,
           49550, 19548, 191775, 55800, 13966, 21546, 63278, 209835, 58914,
           2310, 1974, 65318, 3702, 56574, 230487, 32952, 3180, 6174, 40182,
           68870, 4710, 61854, 243399, 63966, 15838, 70556, 40878, 66486, 255537,
           85074, 6846, 16654, 42960, 98834, 290655, 9834, 87756, 327852, 49746,
           89730, 112148, 70338];
    b_j = [662, 580, 455, 296, 327, 562, 629, 633, 453, 654];
    w_j = [11.4, 8.4, 9.2, 8.5, 8.8, 6.75, 11.13, 10.38, 9.52, 9.11];
    alpha_jk = [
                [1, 0.92, 0.8, 0.8, 0.8, 0.85, 0.95, 0.92, 0.85, 0.92],
                [0.92, 1, 0.85, 0.85, 0.85, 0.8, 0.8, 0.82, 0.83, 0.8],
                [0.8, 0.85, 1, 0.92, 0.92, 0.8, 0.8, 0.8, 0.8, 0.8],
                [0.8, 0.85, 0.92, 1, 0.95, 0.8, 0.8, 0.8, 0.8, 0.8],
                [0.8, 0.85, 0.92, 0.95, 1, 0.8, 0.8, 0.8, 0.8, 0.8],
                [0.85, 0.8, 0.8, 0.8, 0.8, 1, 0.88, 0.84, 0.8, 0.91],
                [0.95, 0.8, 0.8, 0.8, 0.8, 0.88, 1, 0.95, 0.83, 0.82],
                [0.92, 0.82, 0.8, 0.8, 0.8, 0.84, 0.95, 1, 0.83, 0.8],
                [0.85, 0.83, 0.8, 0.8, 0.8, 0.8, 0.83, 0.83, 1, 0.85],
                [0.92, 0.8, 0.8, 0.8, 0.8, 0.91, 0.82, 0.8, 0.85, 1]
                ];
    lamda_ij = [
                [1950, 1600, 1600, 1600, 1600, 1800, 1830, 1880, 1600, 1600],
                [1830, 1600, 1600, 1600, 1600, 1600, 1850, 1600, 1600, 1950],
                [1880, 1600, 1950, 1600, 1600, 1600, 1600, 1600, 1600, 1600],
                [1950, 1600, 1600, 1600, 1600, 1600, 1880, 1950, 1600, 1600],
                [1950, 1600, 1600, 1600, 1600, 1890, 1810, 1920, 1600, 1600],
                [1600, 1950, 1600, 1600, 1600, 1600, 1600, 1600, 1600, 1600],
                [1600, 1600, 1600, 1600, 1600, 1600, 1600, 1600, 1950, 1600],
                [1600, 1600, 1750, 1780, 1950, 1600, 1600, 1600, 1950, 1600],
                [1600, 1600, 1950, 1780, 1790, 1600, 1600, 1600, 1600, 1600],
                [1600, 1600, 1950, 1680, 1950, 1600, 1600, 1600, 1600, 1600],
                [1600, 1600, 1950, 1680, 1950, 1600, 1600, 1600, 1600, 1600],
                [1600, 1600, 1950, 1680, 1950, 1600, 1600, 1600, 1600, 1600],
                [1600, 1900, 1950, 1680, 1690, 1600, 1600, 1600, 1600, 1600],
                [1600, 1600, 1950, 1680, 1690, 1600, 1600, 1600, 1600, 1600],
                [1600, 1600, 1950, 1680, 1690, 1600, 1600, 1600, 1600, 1600],
            ];
    
    return n, m, T, D, beta, C, B, f_l, d_l, Q_l, b_j, w_j, lamda_ij, alpha_jk

def opl_run(ex, options):
    MOD_FILE, DAT_FILE, SOL_FILE = 'Shoes Manufacturing.mod', 'Shoes Manufacturing.dat', 'Shoes Manufacturing.sol'
    
    n, m, T, D, beta, C, B, f_l, d_l, Q_l, b_j, w_j, lamda_ij, alpha_jk = eval(ex + '()')
    
    for o1, o2, o3 in options:
        print('%s, option(%d,%d,%d), start time: %d.%d.%d' % (ex, o1, o2, o3, localtime()[3], localtime()[4], localtime()[5]))
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
            
            f.write('o1 = %d;\n' % o1)
            f.write('o2 = %d;\n' % o2)
            f.write('o3 = %d;\n' % o3)
        
        st = time()    
        rv = call(['oplrun', MOD_FILE, DAT_FILE], creationflags=CREATE_NEW_CONSOLE)
        if rv == 1:
            print('opl execution ended with errors')
            print('%s, option(%d,%d,%d), end time: %d.%d.%d' % (ex, o1, o2, o3, localtime()[3], localtime()[4], localtime()[5])) 
            continue
        calc_time = time() - st 
        
        sol_txt_file_name = ex + (' o1(%d) o2(%d) o3(%d).txt' % (o1, o2, o3))
        
        tf = open(sol_txt_file_name, 'w')
        with open(SOL_FILE, 'r') as sf:
            obj_func_v = eval(sf.readline())
            tf.write('obj_func_v = %d, calc_time = %f\n' % (obj_func_v, calc_time))
            for line in sf:
                tf.write(str(line))
        tf.close()        

def examples_test(examples, options):
    for ex in examples:
        opl_run(ex, options)  

if __name__ == '__main__':
#     options = [(1, 0, 1)
#                 ]
    options = [(1, 1, 1)
                ]
#     options = [(0, 0, 0), (1, 0, 0),
#                (0, 0, 1), (1, 0, 1),
#                (0, 1, 0), (1, 1, 0),
#                (0, 1, 1), (1, 1, 1)
#                ]
    
#     examples_test(['ex' + str(i) for i in [3]], options)
    examples_test(['real_data'], options)
#     examples_test(['fake_data'], options)