from __future__ import division #@UnresolvedImport
from random import seed, choice, shuffle, randrange #@UnresolvedImport
from clasese import Job#@UnresolvedImport
from itertools import *

def ex1():
    j0 , j1, j2, j3 = Job(0, 'D'), Job(1, 'L'), Job(2, 'L'), Job(3, 'D')
    js = [j0 , j1, j2, j3]
    qs = [[j0, j1], [j3, j2]]
    ya = [[j3, j1, j0], [j2]]
    num_yts = 2
    return js, qs, ya, num_yts

def ran_example(num_jobs, num_qcs, num_ycs, num_yts):
    seed(15)
    js = [Job(i, choice(['D', 'L'])) for i in xrange(num_jobs)]
    qs = partition(js, num_qcs)
    ya = partition(js, num_ycs)
    return js, qs, ya, num_yts
    

def partition(jobs, part_num):
    '''
    this function is for partition jobs
    '''
    parts = [[]for _ in xrange(part_num)]
    shuffle(jobs)
    for i, j in enumerate(jobs):
        if i < part_num:
            parts[i].append(j)
        else:
            parts[randrange(part_num)].append(j)
    return parts

if __name__ == '__main__':
    print ex1()
    print ran_example(4, 1, 2, 2)
