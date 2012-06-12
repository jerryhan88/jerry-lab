'''
Created on 2012. 6. 12.

@author: Apple
'''

from subprocess import call, CREATE_NEW_CONSOLE

MOD_FILE, DAT_FILE= '../Implicit_enum_algo.mod', '../Implicit_enum_algo.dat'
n = [1,2,3]
with open(DAT_FILE, 'w') as f:
    f.write('n = %s;\n' % n)
    print n
#    f.write('LL = %d;\n' % LL)
#    f.write('l = %s;\n' % l)
#    f.write('p = %s;\n' % p)
#    f.write('b = %s;\n' % b)
#    f.write('c1 = %s;\n' % c1)
#    s = ('<%s>' % '>, <'.join('%d, %d' % (v1 + 1, v2 + 1) for v1, v2 in Ps) if Ps else '')
#    f.write('Ps = {%s};\n' % s)
#
#rv = call(['oplrun', MOD_FILE, DAT_FILE], creationflags = CREATE_NEW_CONSOLE)
#    assert rv == 0, 'opl execution ended with errors: %d' % rv
#    with open(SOL_FILE, 'r') as f:
#        Bo = eval(f.readline())