from __future__ import division
from subprocess import call, CREATE_NEW_CONSOLE
from time import time, localtime

def ex3_4():
    n = 3;
    m = 4;
    T = 5;
    D = 6;
    beta = 7;
    C = 50;
    B = 35;
    
    f_l = [1, 3, 4, 2, 1];
    d_l = [2, 3, 3, 4, 5];
    d_max_j = [0] * m
    q_l = [40, 80, 85, 110, 110]
    aq_l = [0] * m
    Q_l = []
    
    for i, x in enumerate(f_l):
        ti = x - 1
        aq_l[ti] = aq_l[ti] + q_l[i]
        Q_l.append(aq_l[ti])
        
        if d_max_j[ti] < d_l[i]:
            d_max_j[ti] = d_l[i]
    
    b_j = [12, 10, 13, 20];
    w_j = [18, 15, 20, 25];
    
    C0_ij = [
#                 [35, 21, 28, 32],
#                 [24, 40, 28, 30],
#                 [36, 24, 34, 40]
                [10, 25, 30, 32],
                [25, 45, 30, 30],
                [35, 20, 35, 40]
            ];
    alpha_jk = [
                [1, 0.6, 0.8, 0.9],
                [0.6, 1, 0.65, 0.6],
                [0.8, 0.65, 1, 0.85],
                [0.9, 0.6, 0.85, 1]
                ];
                
    pairs = set()
    for i, C0_i in enumerate(C0_ij):
        for j in range(len(C0_i)):
            for k, C0 in enumerate(C0_i):
#                 print '%d, %d, %d: '% (i+1, j+1, k+1), C0_ij[i][k], alpha_jk[j][k] * C
                if C0_ij[i][k] >= alpha_jk[j][k] * C:
#                     print ' dominant: ', '%d, %d: ' % (j+1, k+1)
                    pass
                else:
#                     print '   considered', '%d, %d: ' % (j+1, k+1)
                    pairs.add((i + 1, j + 1, k + 1)) 
                    
    P = '{'
    counter = 0
    for i, j, k in pairs:
        if counter < len(pairs) - 1 : 
            P = P + '<%d,%d,%d>,' % (i, j, k)
        else : 
            P = P + '<%d,%d,%d>' % (i, j, k)
        counter += 1
    P = P + '}'
#     for x in [n, m, T, D, beta, C, B, f_l, d_l, Q_l, b_j, w_j, C0_ij, alpha_jk, P, len(pairs)]:
#         print x
#     '''
    DAT_FILE = 'Data collection/%s.dat' % ('ex3_4')
    MOD_FILE = 'Models collection/%s.mod' % ('v10_4')
    SOL_FILE = 'Models collection/Shoes Manufacturing.sol' 
     
    print('start time: %d.%d.%d' % (localtime()[3], localtime()[4], localtime()[5]))
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
        f.write('dmax_j = %s;\n' % str(d_max_j))
         
        f.write('b_j = %s;\n' % str(b_j))
        f.write('w_j = %s;\n' % str(w_j))
         
        f.write('C0_ij = %s;\n' % str(C0_ij))
        f.write('alpha_jk = %s;\n' % str(alpha_jk))
        f.write('P = %s;\n' % P)
#         f.write('complete')
    f.close()    
    
    st = time()    
    rv = call(['oplrun', MOD_FILE, DAT_FILE])
    if rv == 1:
        print('opl execution ended with errors')
        print('option(%d,%d,%d), end time: %d.%d.%d' % (localtime()[3], localtime()[4], localtime()[5])) 
    calc_time = time() - st
    print calc_time
    
    x = [[[0] * T] * m] * n
    
    x = []
    for i in range(n):
        j_temp = []
        for j in range(m):
            t_temp = []
            for t in range(T):
                t_temp.append(0)
            j_temp.append(t_temp)
        x.append(j_temp)
    
    y = []
    for i in range(n):
        j_temp = []
        for j in range(m):
            t_temp = []
            for t in range(T):
                t_temp.append(0)
            j_temp.append(t_temp)
        y.append(j_temp)
    
    z = []
    for i in range(n):
        j_temp = []
        for j in range(m):
            t_temp = []
            for t in range(T):
                t_temp.append(0)
            j_temp.append(t_temp)
        z.append(j_temp)
     
    tf = open('result.txt', 'w')
    with open(SOL_FILE, 'r') as sf:
        obj_func_v = eval(sf.readline())
        tf.write('obj_func_v = %d, calc_time = %f\n' % (obj_func_v, calc_time))
        for line in sf:
#             print line[:-1], 
#             print 'test  ',line[3],line[5],line[7],'  = ', line[12:-1] 
            
            i, j, t, v = int(line[3]) - 1, int(line[5]) - 1, int(line[7]) - 1, float(line[12:-1])
            
            if v == 0:
                continue
            else:
                if line[0] == 'x':
                    x[i][j][t] = v
                elif line[0] == 'y':
                    y[i][j][t] = v
                elif line[0] == 'z':
                    z[i][j][t] = v
            
#         print x
#         print y
#         print z
    
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
                if x[i][j][t] > vv:
                    vj = j + 1
                    vv = x[i][j][t]
            print '(%d,%d)' % (vj,int(round(vv))),
                
        print ''
    
    tf.close()
# '''

if __name__ == '__main__':
    ex3_4()
