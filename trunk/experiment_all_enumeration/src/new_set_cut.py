from __future__ import division #@UnresolvedImport
from input import ran_example
from random import seed #@UnresolvedImport

def run(init_jobs, init_qcs_seq, ycs_assignment, num_yts):
    jobs, qcs_seq, ycs_seq, yts_seq, planed_jobs, qcs_primary_j, agreeable_yts_of_jobs, handling_v, qcs_num_of_flag, cut = initialize(init_jobs, init_qcs_seq, ycs_assignment, num_yts)
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
    count = 0
    for qs, ys, ts in set_cut_all_enumeration(cut, agreeable_yts_of_jobs, qcs_num_of_flag, qcs_primary_j, planed_jobs, ycs_seq, yts_seq, jobs, qcs_seq, handling_v):
        count += 1
        print count, qs, ys, ts    
    
def set_cut_all_enumeration(init_cut, init_agreeable_yts_of_jobs, init_qcs_num_of_flag, init_qcs_primary_j, init_planed_jobs, init_ycs_seq, init_yts_seq, jobs, qcs_seq, handling_v):
    for i in xrange(len(init_cut)):
        assignable_yts_id = [yt_id for yt_id, yt_t_f in enumerate(init_agreeable_yts_of_jobs[init_cut[i]]) if yt_t_f]
        for assigned_yt in assignable_yts_id:
            data = [init_cut, init_agreeable_yts_of_jobs, init_ycs_seq, init_yts_seq, init_planed_jobs, init_qcs_primary_j, init_qcs_num_of_flag]
            d_data = [duplicate_data(l) for l in data]
            cut, agreeable_yts_of_jobs, ycs_seq, yts_seq, planed_jobs, qcs_primary_j, qcs_num_of_flag = tuple(d_data)
            
            if not set_cut_algorithm(cut.pop(i), assigned_yt, cut, agreeable_yts_of_jobs, qcs_num_of_flag, qcs_primary_j, planed_jobs, ycs_seq, yts_seq, jobs, qcs_seq, handling_v):
                '''
                if chosen_j is not plannable by assigne_yt,
                set_cut_algorithm will return 'False'.
                it means this job can not be plannable
                
                '''
                continue
            

#            if not cut:
#                yield qcs_seq, ycs_seq, yts_seq
#            else:
#                for qcs_seq, ycs_seq, yts_seq in (cut, agreeable_yts_of_jobs, qcs_num_of_flag, qcs_primary_j, planed_jobs, ycs_seq, yts_seq, jobs, qcs_seq, handling_v):
#                    print cut
#                    yield qcs_seq, ycs_seq, yts_seq
    
def set_cut_algorithm(chosen_j, assigned_yt, cut, agreeable_yts_of_jobs, qcs_num_of_flag, qcs_primary_j, planed_jobs, ycs_seq, yts_seq, jobs, qcs_seq, handling_v):
    handling_qc = handling_v[chosen_j][0]
    assigned_yc = handling_v[chosen_j][1]
    if job_not_plannable(qcs_num_of_flag[handling_qc], qcs_primary_j[handling_qc], chosen_j, agreeable_yts_of_jobs, qcs_seq[handling_qc], assigned_yc, assigned_yt, handling_v, len(yts_seq)):
        return False
    
def job_not_plannable(qc_num_of_flag, qc_primary_j, chosen_j, agreeable_yts_of_jobs, qc_seq, assigned_yc_of_c_j, assigned_yt, handling_v, num_yts):
    if qc_primary_j == chosen_j: return False
    elif qc_num_of_flag == 1 and qc_primary_j != chosen_j and agreeable_yts_of_jobs[qc_primary_j][assigned_yt]: return True
    elif check_same_yc(qc_primary_j, chosen_j, handling_v, qc_seq, agreeable_yts_of_jobs, num_yts): return True
    
def check_same_yc(qc_primary_j, chosen_j, handling_v, qc_seq, agreeable_yts_of_jobs, num_yts):
    same_yc_j_and_j_index = None
    primary_j_index = None
    chosen_j_index = None
    assigned_yc_of_c_j = handling_v[chosen_j][1]
    
    for i, j_id in enumerate(qc_seq):
        if j_id == qc_primary_j:
            primary_j_index = i
            continue
        if j_id == chosen_j:
            chosen_j_index = i
            break
    
    for x in xrange(primary_j_index, chosen_j_index):
        tar_j = qc_seq[x]
        tar_j_index = x
        assigned_yc_of_t_j = handling_v[tar_j][1]
        if assigned_yc_of_t_j == assigned_yc_of_c_j:
            same_yc_j_and_j_index = (tar_j, tar_j_index)
            break
    else:
        return True
    
    
    
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

def duplicate_data(l):
    if type(l[0]) == list: return [x[:]for x in l]
    else: return l[:]

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
