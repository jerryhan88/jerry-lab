from __future__ import division
from subprocess import call, CREATE_NEW_CONSOLE
from time import time, localtime

def ex3_5():
    n = 3;
    m = 4;
    T = 5;
    R = 5;
    fr = [1, 3, 4, 2, 1];
    dr = [2, 3, 3, 4, 5];
    qr = [40, 80, 85, 80, 70];
    A_i = [[1, 2, 4], [2, 3], [1, 4]];
    l_j = [12, 10, 13, 20];
    w_j = [18, 15, 20, 25];
    u_j = [2, 2, 1, 3];
    alpha_jk = [[1, 0.6, 0.8, 0.9],
                [0.6, 1, 0.65, 0.6],
                [0.8, 0.65, 1, 0.85],
                [0.9, 0.6, 0.85, 1]];
    C0_ij = [[10, 25, 30, 32],
            [25, 45, 30, 30],
            [35, 20, 35, 40]];
    beta = 7;
    C = 50;
    L = 35;
    
    return n, m, T, R, fr, dr, qr, A_i, l_j, w_j, u_j, alpha_jk, C0_ij, beta, C, L 

def ex6():
    n = 3;
    m = 4;
    T = 15;
    R = 15;
    fr = [  1,      1,      1,      1,      1,      2,      2,      2,      2,      3,      3,      3,      4,      4];
    dr = [  3,      6,      9,      12,     15,     3,      6,      9,      12,     4,      8,      12,     8,      15];
    qr = [  60,     60,     60,     60,     60,     50,     50,     50,     50,     80,     80,     80,     70,     70];
    A_i = [[1, 2, 4], 
           [2, 3], 
           [1, 4]];
    l_j = [ 12,     10,     13,     20]
    w_j = [ 18,     15,     20,     25]
    u_j = [ 2,      2,      1,      3]
    alpha_jk = [[   1,      0.2,    0.4,    0.6],
                [   0.2,    1,      0.6,    0.6],
                [   0.4,    0.6,    1,      0.5],
                [   0.6,    0.6,    0.5,    1]]
    C0_ij = [[  30,     25,     30,     30],
            [   25,     40,     30,     30],
            [   35,     20,     35,     40]]
    beta = 5
    C = 50
    L = 60
    
    return n, m, T, R, fr, dr, qr, A_i, l_j, w_j, u_j, alpha_jk, C0_ij, beta, C, L

def ex7():
    n = 3;
    m = 4;
    T = 10;
    R = 8;
    fr = [  1,      1,      1,      2,      2,      3,      3,      4];
    dr = [  3,      6,      9,      5,      10,     5,      10,     10];
    qr = [  70,     70,     70,     150,    150,    150,    150,    200];
    A_i = [[1, 2, 4], 
           [2, 3], 
           [1, 4]];
    l_j = [ 10,     10,     15,     20]
    w_j = [ 18,     15,     20,     25]
    u_j = [ 2,      2,      1,      3]
    alpha_jk = [[   1,      0.2,    0.4,    0.6],
                [   0.2,    1,      0.3,    0.6],
                [   0.4,    0.3,    1,      0.2],
                [   0.6,    0.6,    0.2,    1]]
    C0_ij = [[  30,     25,     30,     30],
            [   25,     40,     25,     30],
            [   30,     20,     35,     40]]
    beta = 5
    C = 50
    L = 60
    
    return n, m, T, R, fr, dr, qr, A_i, l_j, w_j, u_j, alpha_jk, C0_ij, beta, C, L

def ex8():
    n = 4
    m = 4
    T = 10
    R = 8
    fr = [  1,      1,      1,      2,      2,      3,      3,      4];
    dr = [  3,      6,      9,      5,      10,     5,      10,     10];
    qr = [  100,    100,    100,     200,    200,    150,    150,    200];
    A_i = [[1, 2, 3, 4], 
           [1, 2],
           [2, 3], 
           [2, 3, 4]]
    l_j = [ 20,     10,     15,     10]
    w_j = [ 18,     15,     20,     25]
    u_j = [ 2,      2,      1,      3]
    alpha_jk = [[   1,      0.8,    0.4,    0.9],
                [   0.8,    1,      0.5,    0.6],
                [   0.4,    0.5,    1,      0.2],
                [   0.9,    0.6,    0.2,    1]]
    C0_ij = [[  30,     25,     30,     35],
            [   25,     40,     25,     30],
            [   30,     20,     35,     40],
            [   20,     30,     20,     20]]
    beta = 5
    C = 50
    L = 60
    
    return n, m, T, R, fr, dr, qr, A_i, l_j, w_j, u_j, alpha_jk, C0_ij, beta, C, L

def ex9():
    n = 3;
    m = 4;
    T = 10;
    R = 8;
    fr = [  1,      1,      1,      2,      2,      3,      3,      4];
    dr = [  3,      6,      9,      5,      10,     5,      10,     10];
    qr = [  110,    110,    110,    220,    220,    150,    150,    200];
    A_i = [[1, 2, 4], 
           [2, 3], 
           [1, 4]];
    l_j = [ 10,     10,     15,     20]
    w_j = [ 18,     15,     20,     25]
    u_j = [ 2,      2,      1,      3]
    alpha_jk = [[   1,      0.2,    0.4,    0.6],
                [   0.2,    1,      0.3,    0.6],
                [   0.4,    0.3,    1,      0.2],
                [   0.6,    0.6,    0.2,    1]]
    C0_ij = [[  30,     25,     30,     30],
            [   25,     40,     25,     30],
            [   30,     20,     35,     40]]
    beta = 5
    C = 50
    L = 60
    
    return n, m, T, R, fr, dr, qr, A_i, l_j, w_j, u_j, alpha_jk, C0_ij, beta, C, L

def run(ex, p2, p3):
    
    n, m, T, R, fr, dr, qr, A_i, l_j, w_j, u_j, alpha_jk, C0_ij, beta, C, L = eval(ex + '()')
    
    DAT_FILE = 'Data collection/%s.dat' % (ex)
    MOD_FILE = 'Models collection/%s.mod' % ('v10_5')
    SOL_FILE = 'Models collection/Shoes Manufacturing.sol' 
#     ''' 
    print('start time: %d.%d.%d' % (localtime()[3], localtime()[4], localtime()[5]))
    with open(DAT_FILE, 'w') as f:
        f.write('n = %d;\n' % n)
        f.write('m = %d;\n' % m)
        f.write('T = %d;\n' % T)
        f.write('R = %d;\n' % R)
        f.write('fr = %s;\n' % str(fr))
        f.write('dr = %s;\n' % str(dr))
        f.write('qr = %s;\n' % str(qr))
        st_A_i = '['
        for a_i in A_i:
            st_A_i = st_A_i + '{'
            for i, j in enumerate(a_i):
                if i == len(a_i)-1:
                    st_A_i = st_A_i + '%d' % (j)
                else:
                    st_A_i = st_A_i + '%d,' % (j) 
            st_A_i = st_A_i + '}'
        st_A_i = st_A_i +']'        
        f.write('A_i = %s;\n' % st_A_i)
        f.write('l_j = %s;\n' % str(l_j))
        f.write('w_j = %s;\n' % str(w_j))
        f.write('u_j = %s;\n' % str(u_j))
        f.write('alpha_jk = %s;\n' % str(alpha_jk))
        f.write('C0_ij = %s;\n' % str(C0_ij))
        f.write('beta = %d;\n' % beta)
        f.write('C = %d;\n' % C)
        f.write('L = %d;\n' % L)
        f.write('p2 = %d;\n' % p2)
        f.write('p3 = %d;\n' % p3)
    f.close()    
    
    st = time()    
    rv = call(['oplrun', MOD_FILE, DAT_FILE])
    if rv == 1:
        print('opl execution ended with errors')
        print('option(%d,%d,%d), end time: %d.%d.%d' % (localtime()[3], localtime()[4], localtime()[5])) 
    calc_time = time() - st
    print calc_time
#     '''
    x = []
    for i in range(T):
        j_temp = []
        for j in range(n):
            t_temp = []
            for t in range(m):
                t_temp.append(0)
            j_temp.append(t_temp)
        x.append(j_temp)
    
    y = []
    for i in range(T):
        j_temp = []
        for j in range(n):
            t_temp = []
            for t in range(m):
                t_temp.append(0)
            j_temp.append(t_temp)
        y.append(j_temp)
    
    z = []
    for i in range(T):
        j_temp = []
        for j in range(n):
            t_temp = []
            for t in range(m):
                t_temp.append(0)
            j_temp.append(t_temp)
        z.append(j_temp)
    rst_t_n = '%s p2(%d) p3(%d).txt' %(ex, p2, p3) 
    tf = open(rst_t_n, 'w')
    with open(SOL_FILE, 'r') as sf:
        obj_func_v = eval(sf.readline())
        tf.write('obj_func_v = %d, calc_time = %f\n' % (obj_func_v, calc_time))
        for line in sf:
            dv, s_v = line.split('=')
            s_t, s_i, s_j = dv[dv.index('<')+1:dv.index('>')].split(' ')  
            t, i, j, v = int(s_t) - 1, int(s_i) - 1, int(s_j) - 1, float(s_v)
            if v == 0:
                continue
            else:
                if line[0] == 'x':
                    x[t][i][j] = v
                elif line[0] == 'y':
                    y[t][i][j] = v
                elif line[0] == 'z':
                    print t, i, j 
                    print line
                    print z
                    z[t][i][j] = v
    print ''
    print '        ',
    for t in range(1, T + 1):
        print '    %d' % t,
    print ''
     
    for i in range(n):
        print 'Line %d: ' % (i + 1),
        for t in range(T):
            vj = 0
            vv = 0
            for j in range(m):
                if x[t][i][j] > vv:
                    vj = j + 1
                    vv = x[t][i][j]
            print '(%d,%d)' % (vj, int(round(vv))),
                 
        print ''
    
    print ''
    print '        ',
    for t in range(1, T + 1):
        print '    %d' % t,
    print ''
     
    for i in range(n):
        print 'Line %d: ' % (i + 1),
        for t in range(T):
            vj = 0
            vv = 0
            for j in range(m):
                if z[t][i][j] > vv:
                    vj = j + 1
                    vv = z[t][i][j]
            print '(%d,%d)' % (vj, int(round(vv))),
                 
        print ''
    
    tf.write('\n')
    tf.write('         ',)
    for t in range(1, T + 1):
        tf.write('      %d' % t)
    tf.write('\n')
     
    for i in range(n):
        tf.write('Line %d:   ' % (i + 1))
        for t in range(T):
            vj = 0
            vv = 0
            for j in range(m):
                if x[t][i][j] > vv:
                    vj = j + 1
                    vv = x[t][i][j]
            tf.write(' (%d,%d)' % (vj, int(round(vv))))
                 
        tf.write('\n')
    
    tf.write('\n')
    tf.write('        ')
    for t in range(1, T + 1):
        tf.write('        %d' % t)
    tf.write('\n')
     
    for i in range(n):
        tf.write('Line %d: ' % (i + 1))
        for t in range(T):
            vj = 0
            vv = 0
            for j in range(m):
                if z[t][i][j] > vv:
                    vj = j + 1
                    vv = z[t][i][j]
            tf.write('    (%d,%d)' % (vj, int(round(vv))))
        tf.write('\n')
    tf.close()

if __name__ == '__main__':
#     run('ex3_5', 0, 0)
    for p2, p3 in [(0,0),(1,0),(0,1),(1,1)]:
        run('ex9', p2, p3)
    
