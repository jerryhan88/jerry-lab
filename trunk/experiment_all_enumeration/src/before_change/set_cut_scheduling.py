from __future__ import division #@UnresolvedImport
from input import ran_example
from random import seed #@UnresolvedImport

def set_cut_run(jobs, qcs_seq, init_ycs_seq, init_yts_seq, init_scheduled_js, init_qcs_primary_j, init_agreeable_yt_of_job, handling_v, init_qcs_num_of_flag, init_cut):
    for i in xrange(len(init_cut)):
        agreeable_yt_ids = [yt_id for yt_id, yt_t_f in enumerate(init_agreeable_yt_of_job[init_cut[i]]) if yt_t_f]
        for agree_yt_id in agreeable_yt_ids:
            ycs_seq = [x[:] for x in init_ycs_seq]
            yts_seq = [x[:] for x in init_yts_seq]
            scheduled_js = init_scheduled_js[:]
            qcs_primary_j = init_qcs_primary_j[:]
            agreeable_yt_of_job = [x[:] for x in init_agreeable_yt_of_job]
            qcs_num_of_flag = init_qcs_num_of_flag[:]
            cut = init_cut[:]
            chosen_j_id = cut.pop(i)
#            print chosen_j_id
#            print cut
            handling_qc = handling_v[chosen_j_id][0]
            if qcs_num_of_flag[handling_qc] == 1 and chosen_j_id != qcs_primary_j[handling_qc] and agreeable_yt_of_job[qcs_primary_j[handling_qc]][agree_yt_id]:
                continue
            handling_yc = handling_v[chosen_j_id][1]
            handling_yt = agree_yt_id
            ycs_seq[handling_yc].append(chosen_j_id)
            yts_seq[handling_yt].append(chosen_j_id)
            qc_j_seq = qcs_seq[handling_qc]
            scheduled_js[chosen_j_id] = True
            '''update'''
            if chosen_j_id == qcs_primary_j[handling_qc] and chosen_j_id != qcs_seq[handling_qc][-1]:
                    adding_job_to_cut(cut, qc_j_seq, chosen_j_id, jobs, scheduled_js)
                    ''' find next primary job and revise # of flag '''
                    for x in xrange(qc_j_seq.index(chosen_j_id) + 1, len(qc_j_seq)):
                        if not scheduled_js[qc_j_seq[x]]:
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
                        adding_job_to_cut(cut, qc_j_seq, chosen_j_id, jobs, scheduled_js)           
            if not cut:
                yield qcs_seq, ycs_seq, yts_seq
            else:
                for qcs_seq, ycs_seq, yts_seq in set_cut_run(jobs, qcs_seq, ycs_seq, yts_seq, scheduled_js, qcs_primary_j, agreeable_yt_of_job, handling_v, qcs_num_of_flag, cut):
                    yield qcs_seq, ycs_seq, yts_seq

def adding_job_to_cut(cut, qc_seq, chosen_j_id, jobs, scheduled_js):
    ''' adding job which have condition for entering cut '''
    for x in xrange(qc_seq.index(chosen_j_id) + 1, len(qc_seq)):
        if jobs[qc_seq[x]].type == 'L' and not scheduled_js[qc_seq[x]]:
            ''' before appearing Loading job which is not scheduled'''
            break
        elif jobs[qc_seq[x]].type == 'D' and qc_seq[x] not in cut and not scheduled_js[qc_seq[x]]:
            cut.append(qc_seq[x])

def initialize(jobs, init_qcs_seq, ycs_assign, num_yts):
    jobs.sort()
    qcs_seq = [[x.id for x in seq]for seq in init_qcs_seq]
    ycs_seq, yts_seq = [[] for _ in xrange(len(ycs_assign))], [[] for _ in xrange(num_yts)]
    scheduled_js, qcs_primary_j = [False] * len(jobs), [seq[0] for seq in qcs_seq]
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
    if len(jobs) == len([x for x in jobs if x.type == 'D']):
        cut = [x.id for x in jobs]
    else:    
        for q_id, seq in enumerate(qcs_seq):
            is_first_loading_job_of_qc = True
            for i, j_id in enumerate(seq):
                if j_id == qcs_primary_j[q_id]: cut.append(j_id)
                ''' or if i == 0     it means first job of qc.job_seq '''
                if jobs[j_id].type == 'L':
                    ''' all loading job will be in cut
                        and discharging job before finding first loading job will be in cut '''
                    if is_first_loading_job_of_qc:
                        for x in xrange(i + 1):
                            if seq[x] == qcs_primary_j[q_id]: continue
                            ''' discharging job will be in cut '''
                            cut.append(seq[x])
                        is_first_loading_job_of_qc = False
                        continue
                    ''' after is_first_loading_job_of_qc = False
                        all loading job will be into cut'''
                    cut.append(j_id)
    return jobs, qcs_seq, ycs_seq, yts_seq, scheduled_js, qcs_primary_j, agreeable_yt_of_job, handling_v , qcs_num_of_flag, cut

if __name__ == '__main__':
    seed(16)
    jobs, qcs_seq, ycs_assign, num_yts = ran_example(4, 1, 2, 2)
    jobs, qcs_seq, ycs_seq, yts_seq, scheduled_js, qcs_primary_j, agreeable_yt_of_job, handling_v, qcs_num_of_flag, cut = initialize(jobs, qcs_seq, ycs_assign, num_yts)
    print jobs
    print cut
    
    
#    for qs, ys, ts in set_cut_run(jobs, qcs_seq, ycs_seq, yts_seq, scheduled_js, qcs_primary_j, agreeable_yt_of_job, handling_v, qcs_num_of_flag, cut):
#        print qs, ys, ts
        
        
        
#    set_cut_run(jobs, qcs_seq, ycs_seq, yts_seq, scheduled_js, qcs_primary_j, agreeable_yt_of_job, cut)
#    print jobs, qcs_seq, ycs_assign, num_yts
