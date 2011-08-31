from __future__ import division #@UnresolvedImport
from input import ran_example
from random import seed #@UnresolvedImport

def set_cut_run(jobs, qcs_seq, init_ycs_seq, init_yts_seq, init_scheduled_js, init_qcs_primary_j, init_agreeable_yt_of_job, handling_v, init_qcs_num_of_flag, init_cut):
    for i in xrange(len(init_cut)):
        agreeable_yt_ids = [yt_id for yt_id, yt_t_f in enumerate(init_agreeable_yt_of_job[init_cut[i]]) if yt_t_f]
        for agree_yt_id in agreeable_yt_ids:
            ycs_seq = [x[:] for x in init_ycs_seq]
            yts_seq = [x[:] for x in init_yts_seq]
            planed_js = init_scheduled_js[:]
            qcs_primary_j = init_qcs_primary_j[:]
            agreeable_yt_of_job = [x[:] for x in init_agreeable_yt_of_job]
            qcs_num_of_flag = init_qcs_num_of_flag[:]
            cut = init_cut[:]
            
            
            if not planed_js[0] and planed_js[1] and not planed_js[2] and not planed_js[3]:
                print 'debug'
            
            
            
            chosen_j_id = cut.pop(i)
            handling_qc = handling_v[chosen_j_id][0]
            
            tar_j = chosen_j_id
            primary_j = qcs_primary_j[handling_qc]
            
            if qcs_num_of_flag[handling_qc] == 1 and chosen_j_id != qcs_primary_j[handling_qc] and agreeable_yt_of_job[qcs_primary_j[handling_qc]][agree_yt_id] and handling_v[primary_j][1] == handling_v[tar_j][1]:
                continue
            
            handling_yc = handling_v[chosen_j_id][1]
            handling_yt = agree_yt_id
            ycs_seq[handling_yc].append(chosen_j_id)
            yts_seq[handling_yt].append(chosen_j_id)
            qc_j_seq = qcs_seq[handling_qc]
            planed_js[chosen_j_id] = True
            '''update'''
            if chosen_j_id == qcs_primary_j[handling_qc] and chosen_j_id != qcs_seq[handling_qc][-1]:
                    adding_job_to_cut(cut, qc_j_seq, chosen_j_id, jobs, planed_js, qcs_primary_j[handling_qc], handling_v, len(init_yts_seq))
                    ''' find next primary job and revise # of flag '''
                    for x in xrange(qc_j_seq.index(chosen_j_id) + 1, len(qc_j_seq)):
                        if not planed_js[qc_j_seq[x]]:
                            qcs_primary_j[handling_qc] = qc_j_seq[x]
                            qcs_num_of_flag[handling_qc] = len([t_f for t_f in agreeable_yt_of_job[qcs_primary_j[handling_qc]] if t_f])
                            break
            elif chosen_j_id != qcs_primary_j[handling_qc]:
                    ''' set not agreeable yt in each jobs '''
                    for s_i in xrange(qc_j_seq.index(qcs_primary_j[handling_qc]), qc_j_seq.index(chosen_j_id)):
                        agreeable_yt_of_job[qc_j_seq[s_i]][handling_yt] = False
                    ''' revise # of flag '''
                    qcs_num_of_flag[handling_qc] = len([t_f for t_f in agreeable_yt_of_job[qcs_primary_j[handling_qc]] if t_f])
                    '''
                    there is two case
                    one is chosen_j == handling_qc.job_sequence[-1]
                    another is chosen_j != handling_qc.job_sequence[-1]
                    '''
                    if chosen_j_id != qc_j_seq[-1]:
                        adding_job_to_cut(cut, qc_j_seq, chosen_j_id, jobs, planed_js, qcs_primary_j[handling_qc], handling_v, len(init_yts_seq))
            if not cut:
                yield qcs_seq, ycs_seq, yts_seq
            else:
                for qcs_seq, ycs_seq, yts_seq in set_cut_run(jobs, qcs_seq, ycs_seq, yts_seq, planed_js, qcs_primary_j, agreeable_yt_of_job, handling_v, qcs_num_of_flag, cut):
                    print cut
                    yield qcs_seq, ycs_seq, yts_seq

def adding_job_to_cut(cut, qc_j_seq, chosen_j_id, jobs, planed_js, primary_j, handling_v, num_yts):
    ''' adding job which have condition for entering cut '''
    for x in xrange(qc_j_seq.index(chosen_j_id) + 1, len(qc_j_seq)):
        if jobs[qc_j_seq[x]].type == 'L' and not planed_js[qc_j_seq[x]]:
            ''' before appearing Loading job which is not scheduled'''
            break
        elif jobs[qc_j_seq[x]].type == 'D' and qc_j_seq[x] not in cut and not planed_js[qc_j_seq[x]] and not cycle_possiblility(jobs, qc_j_seq[x], qc_j_seq, primary_j, planed_js, handling_v, num_yts):
            cut.append(qc_j_seq[x])
            
def cycle_possiblility(jobs, tar_j, seq, primary_j, planed_js, handling_v, num_yts):
    if tar_j == primary_j:
        return False
    
    primary_j_index = None
    tar_j_index = None
    
    for i, j_id in enumerate(seq):
        if j_id == primary_j:
            primary_j_index = i
            continue
        if j_id == tar_j:
            tar_j_index = i
            break  
    '''check yc id of two jobs(primary_j, tar_j)'''
#    print seq
#    print 'primary_j : ', primary_j 
#    print 'tar_j : ', tar_j
#    print '~~~~~~~~~~~~~~~~~~~~~',tar_j_index# - primary_j_index
#    if handling_v[primary_j][1] == handling_v[tar_j][1] and (tar_j_index - primary_j_index) > num_yts :
    if handling_v[primary_j][1] == handling_v[tar_j][1] and (tar_j_index - primary_j_index - 1) > num_yts - 2 :
        feasible = False
        for x in xrange(primary_j_index+1, tar_j_index):
            if not planed_js[seq[x]]: break
        else:
            feasible = True
        if not feasible: return True
    
    for i in xrange(primary_j_index, tar_j_index):
        if jobs[seq[i]].type == 'L' and not planed_js[seq[i]]:
            return True
    return False

def initialize(jobs, init_qcs_seq, ycs_assign, num_yts):
    jobs.sort()
    qcs_seq = [[x.id for x in seq]for seq in init_qcs_seq]
    ycs_seq, yts_seq = [[] for _ in xrange(len(ycs_assign))], [[] for _ in xrange(num_yts)]
    planed_js, qcs_primary_j = [False] * len(jobs), [seq[0] for seq in qcs_seq]
    agreeable_yt_of_job = [[True for x in xrange(num_yts)] for _ in jobs]
    handling_qc = [None] * len(jobs) 
    for q_id, seq in enumerate(qcs_seq):
        for j in seq:
            handling_qc[j] = q_id
    handling_yc = [None] * len(jobs) 
    for y_id, seq in enumerate(ycs_assign):
        for j in seq:
            handling_yc[j.id] = y_id
    handling_v = [(handling_qc[i], handling_yc[i]) for i in xrange(len(jobs))]
    qcs_num_of_flag = [num_yts for _ in xrange(len(qcs_seq))]
    cut = []
    '''initialize cut'''
    for q_id, seq in enumerate(qcs_seq):
        for i, j_id in enumerate(seq):
            ''' all loading job will be in cut
                and discharging job before finding first loading job will be in cut 
                also discharging job which will cause cycle is filtered'''
            if i == 0: pass
            elif jobs[j_id].type == 'L': pass 
            elif cycle_possiblility(jobs, j_id, qcs_seq[q_id], qcs_primary_j[q_id], planed_js, handling_v, num_yts): continue
            cut.append(j_id)
            
    return jobs, qcs_seq, ycs_seq, yts_seq, planed_js, qcs_primary_j, agreeable_yt_of_job, handling_v , qcs_num_of_flag, cut

if __name__ == '__main__':
    seed(16)
    
    jobs, qcs_seq, ycs_assign, num_yts = ran_example(4, 1, 2, 2)
    jobs, qcs_seq, ycs_seq, yts_seq, planed_js, qcs_primary_j, agreeable_yt_of_job, handling_v, qcs_num_of_flag, cut = initialize(jobs, qcs_seq, ycs_assign, num_yts)
    
    print 'jobs : ', jobs
    print 'cut : ', cut
    
    count = 0    
    for qs, ys, ts in set_cut_run(jobs, qcs_seq, ycs_seq, yts_seq, planed_js, qcs_primary_j, agreeable_yt_of_job, handling_v, qcs_num_of_flag, cut):
        count +=1
        print count, qs, ys, ts
