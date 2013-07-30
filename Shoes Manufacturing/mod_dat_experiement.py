from __future__ import division
from subprocess import call, CREATE_NEW_CONSOLE
from time import time, localtime

def opl_run(mod, dat):
    MOD_FILE = mod 
    DAT_FILE = dat
    SOL_FILE = 'Shoes Manufacturing.sol'
    
    st = time()    
    rv = call(['oplrun', MOD_FILE, DAT_FILE], creationflags=CREATE_NEW_CONSOLE)
    if rv == 1:
        print('opl execution ended with errors')
    
    calc_time = time() - st
    
    tf = open('test.txt', 'w')
    with open(SOL_FILE, 'r') as sf:
        obj_func_v = eval(sf.readline())
        tf.write('obj_func_v = %d, calc_time = %f\n' % (obj_func_v, calc_time))
        for line in sf:
            tf.write(str(line))
    tf.close()
    
    

if __name__ == '__main__':
    opl_run('Models collection/v8.mod', 'Data collection/ex6.dat')
    
    
    