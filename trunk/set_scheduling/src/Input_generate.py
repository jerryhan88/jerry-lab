from __future__ import division #@UnresolvedImport
from random import choice, randrange, seed, shuffle#@UnresolvedImport
from clasese import Job, QC, YC, YT

def gen_input(num_jobs, num_qcs, num_ycs, num_yts):
    seed(100)
#    seed(5)
    '''
    jobs = [job0, job1, job2, ...]
    qcs_seq = [[handling sequence of qc0],[handling sequence of qc1],[],...]
    ycs_assigns= [[assigned job of yc0],[assigned job of yc1],[],...]
    '''
    jobs = [Job(i, choice(['discharging', 'loading'])) for i in xrange(num_jobs)]
    qcs_seq = partition(num_jobs, num_qcs)
    for i, seq in enumerate(qcs_seq):
        for j in seq:
            jobs[j].handling_qc_id =i  
    ycs_assigns = partition(num_jobs, num_ycs)
    for i, seq in enumerate(ycs_assigns):
        for j in seq:
            jobs[j].handling_yc_id =i 
    '''
    make resources class
    '''
    qcs = [QC(i, tuple(qc_seq), num_yts) for i, qc_seq in enumerate(qcs_seq)]
    ycs = [YC(i, tuple(yc_assigns)) for i , yc_assigns in enumerate(ycs_assigns)]
    yts = [YT(i) for i in xrange(num_yts)]
    return jobs, qcs, ycs, yts

def partition(total_num, part_num):
    '''
    this function is for partition jobs
    '''
    parts = [[]for _ in xrange(part_num)]
    target = range(total_num)
    shuffle(target)
    for i, x in enumerate(target):
        if i < part_num:
            parts[i].append(x)
        else:
            parts[randrange(part_num)].append(x)
    return parts 

if __name__ == '__main__':
#    print partition(10, 3)
    num_jobs = 8
    num_qcs = 3
    num_ycs = 3
    num_yts = 4
    jobs, qcs, ycs, yts = gen_input(num_jobs, num_qcs, num_ycs, num_yts)
    print 'jobs id and type'
    print '    ', [(x.id, x.type)for x in jobs]
    for qc in qcs:
        print 'qc id : ', qc.id, '    sequence : ', qc.job_seq
    
    print ''    
    for yc in ycs:
        print 'yc id : ', yc.id, '    assigned job : ', yc.assigned_j
    
    print ''    
    for yt in yts:
        print 'yt id : ', yt.id    
