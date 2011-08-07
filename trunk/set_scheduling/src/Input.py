from __future__ import division #@UnresolvedImport
import Input_generate
'''
Input_generate.gen_input(10, 2, 2, 3)
# of jobs, qcs, ycs, yts
'''
def big_problem():
    return Input_generate.gen_input(10, 2, 2, 3)

def small_problem():
    return Input_generate.gen_input(3, 2, 2, 2)