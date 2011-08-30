from __future__ import division #@UnresolvedImport
from input import ran_example
from random import seed #@UnresolvedImport

def run(init_jobs, init_qcs_seq, ycs_assignment, num_yts):
    jobs, qcs_seq, ycs_seq, yts_seq, planed_jobs, qcs_primary_j, agreeable_yt_of_job, handling_v, qcs_num_of_flag, cut = initialize(init_jobs, init_qcs_seq, ycs_assignment, num_yts)
    '''
    jobs : (0:D, 1:D, 2:D, 3:D) 
    qcs_seq : ((2, 0, 3, 1),) 
    ycs_seq : [[], []] 
    yts_seq : [[], []] 
    planed_jobs : [False, False, False, False]
    qcs_primary_j : [2] 
    agreeable_yt_of_job : [[True, True], [True, True], [True, True], [True, True]] 
    handling_v : [(0, 1), (0, 1), (0, 0), (0, 0)] 
    qcs_num_of_flag : [2] 
    cut : [2, 0, 3, 1] 
    '''
    
def initialize(init_jobs, init_qcs_seq, ycs_assignment, num_yts):
    init_jobs.sort()
    jobs = tuple(init_jobs)
    qcs_seq = [] 
    for seq in init_qcs_seq:
        qc_seq = [j.id for j in seq]
        qcs_seq.append(tuple(qc_seq))
    qcs_seq = tuple(qcs_seq)
    qcs_primary_j = [seq[0] for seq in qcs_seq] 
    ycs_seq, yts_seq = [[] for _ in xrange(len(ycs_assign))], [[] for _ in xrange(num_yts)] 
    handling_qc = [None] * len(jobs) 
    
    for q_id, seq in enumerate(qcs_seq):
        for j in seq:
            handling_qc[j] = q_id
    handling_yc = [None] * len(jobs) 
    for y_id, seq in enumerate(ycs_assign):
        for j in seq:
            handling_yc[j.id] = y_id
    handling_v = [(handling_qc[i], handling_yc[i]) for i in xrange(len(jobs))]
    planed_jobs, agreeable_yt_of_job = [False] * len(jobs), [[True for __ in xrange(num_yts)] for _ in jobs]
    qcs_num_of_flag = [num_yts] * len(qcs_seq)
    cut = []
    for q_id, seq in enumerate(qcs_seq):
        for i, j_id in enumerate(seq):
            ''' all loading job will be in cut
                and discharging job before finding first loading job will be in cut 
                also discharging job which will cause cycle is filtered'''
            if i == 0: pass
            elif jobs[j_id].type == 'L': pass 
            elif check_prev_loading_jobs(0, i, jobs, seq, planed_jobs): continue
            cut.append(j_id)
    return jobs, qcs_seq, ycs_seq, yts_seq, planed_jobs, qcs_primary_j, agreeable_yt_of_job, handling_v, qcs_num_of_flag, cut

def check_prev_loading_jobs(primary_j_index, target_j_index, jobs, qc_seq, planed_jobs):
    for i in xrange(primary_j_index, target_j_index):
        checking_j = qc_seq[i]
        if jobs[checking_j].type == 'L' and not planed_jobs[checking_j]: return True 
    else:
        return  False
        
if __name__ == '__main__':
    
    seed(16)
    jobs, qcs_seq, ycs_assign, num_yts = ran_example(4, 1, 2, 2)
    '''
    job : [3:D, 1:D, 2:D, 0:D]
    qcs_seq : [[2:D, 0:D, 3:D, 1:D]]
    ycs_assign : [[3:D, 2:D], [1:D, 0:D]]
    num_yts : 2
    '''
    run(jobs, qcs_seq, ycs_assign, num_yts)
