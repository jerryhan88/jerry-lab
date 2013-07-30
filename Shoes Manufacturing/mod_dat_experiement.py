from __future__ import division
from subprocess import call, CREATE_NEW_CONSOLE
from time import time, localtime

def opl_run(mod, dat):
    MOD_FILE = 'Models collection/' + mod 
    DAT_FILE = 'Data collection/' + dat
    SOL_FILE = 'Shoes Manufacturing.sol'
    
    st = time()    
    rv = call(['oplrun', MOD_FILE, DAT_FILE], creationflags=CREATE_NEW_CONSOLE)
    if rv == 1:
        print('opl execution ended with errors')
    
    calc_time = time() - st
    
    result_file_name = mod + '_' + dat + '.txt'
    
    tf = open(result_file_name, 'w')
    with open(SOL_FILE, 'r') as sf:
        obj_func_v = eval(sf.readline())
        tf.write('obj_func_v = %d, calc_time = %f\n' % (obj_func_v, calc_time))
        for line in sf:
            tf.write(str(line))
    tf.close()

if __name__ == '__main__':
    opl_run('including_ct9.mod', 'Indonesia_real_data.dat')