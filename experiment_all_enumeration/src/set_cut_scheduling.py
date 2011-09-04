from __future__ import division #@UnresolvedImport
from input import ran_example
from random import seed #@UnresolvedImport
def job_not_plannable(qc_num_of_flag, qc_primary_j, chosen_j, planed_jobs, agreeable_yts_of_jobs, qc_seq, assigned_yc_of_c_j, assigned_yt, handling_v, num_yts, jobs):
    '''
    If chosen_j will cause cycle,
    this function will return True
    '''
    if qc_primary_j == chosen_j: return False
    elif qc_num_of_flag == 1 and qc_primary_j != chosen_j and agreeable_yts_of_jobs[qc_primary_j][assigned_yt]: return True
    
    if check_same_yc(qc_primary_j, chosen_j, handling_v, qc_seq, agreeable_yts_of_jobs, planed_jobs, num_yts, jobs):
        return True
    else:
        return False
    
def check_same_yc(qc_primary_j, chosen_j, handling_v, qc_seq, agreeable_yts_of_jobs, planed_jobs, num_yts, jobs):
    '''
    If chosen_j is not plannable,
    this function will return True 
    '''
    same_yc_j_index = None
    primary_j_index = None
    chosen_j_index = None
    assigned_yc_of_c_j = handling_v[chosen_j][1]
    assigned_yt_of_c_j = handling_v[chosen_j][2]
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
            same_yc_j_index = tar_j_index
            break
    else:
        return False
    
    same_yc_j = qc_seq[same_yc_j_index]
    
    if (chosen_j_index - same_yc_j_index + 1) > num_yts:
        if jobs[chosen_j].type == 'L':
            if jobs[same_yc_j].type == 'L':
                for tar_j_index in xrange(same_yc_j_index + 1, chosen_j_index):
                    tar_j = qc_seq[tar_j_index]
                    assigned_yt_of_t_j = handling_v[tar_j][2]
                    if planed_jobs[tar_j] and assigned_yt_of_c_j == assigned_yt_of_t_j: break
                else:
                    return False
                return True
            else:
                '''
                jobs[same_yc_j].type == 'D'
                '''
                 
                for tar_j_index in xrange(same_yc_j_index + 1, chosen_j_index):
                    tar_j = qc_seq[tar_j_index]
                    flag = len([t_f for t_f in agreeable_yts_of_jobs[tar_j]if t_f])
                    if not planed_jobs[tar_j] and flag == 1 : return True
                else:
                    return False
                
#                flag = len([t_f for t_f in agreeable_yts_of_jobs[same_yc_j]if t_f])
#                if flag ==1 : return True
                
                return False
        else:
            '''
            jobs[chosen_j].type == 'D'
            '''
            for tar_j_index in xrange(same_yc_j_index + 1, chosen_j_index):
                tar_j = qc_seq[tar_j_index]
                if not planed_jobs[tar_j]: break
            else:
                return False
            return True
    else:
        return False
    
def set_cut_algorithm(chosen_j, assigned_yt, cut, agreeable_yts_of_jobs, qcs_num_of_flag, qcs_primary_j, planed_jobs, ycs_seq, yts_seq, jobs, qcs_seq, handling_v):
    handling_qc = handling_v[chosen_j][0]
    assigned_yc = handling_v[chosen_j][1]
#    print handling_v
    handling_v[chosen_j][2] = assigned_yt
    if job_not_plannable(qcs_num_of_flag[handling_qc], qcs_primary_j[handling_qc], chosen_j, planed_jobs, agreeable_yts_of_jobs, qcs_seq[handling_qc], assigned_yc, assigned_yt, handling_v, len(yts_seq), jobs):
        return False
    update(chosen_j, planed_jobs, ycs_seq, yts_seq, agreeable_yts_of_jobs, qcs_num_of_flag, qcs_primary_j, cut, jobs, qcs_seq, handling_v)
    return True    
    
def update(chosen_j, planed_jobs, ycs_seq, yts_seq, agreeable_yts_of_jobs, qcs_num_of_flag, qcs_primary_j, cut, jobs, qcs_seq, handling_v):
    planed_jobs[chosen_j] = True
    handling_qc, handling_yc, handling_yt = tuple(handling_v[chosen_j])
    ycs_seq[handling_yc].append(chosen_j)
    yts_seq[handling_yt].append(chosen_j)
    
    qc_seq = qcs_seq[handling_qc]
    if chosen_j == qcs_primary_j[handling_qc] and chosen_j != qc_seq[-1]:
        adding_job_to_cut(cut, qc_seq, qcs_primary_j[handling_qc], chosen_j, planed_jobs, jobs)
        ''' find next primary job and revise # of flag '''
        for x in xrange(list(qc_seq).index(chosen_j) + 1, len(qc_seq)):
            tar_j = qc_seq[x]
            if not planed_jobs[tar_j]:
                qcs_primary_j[handling_qc] = tar_j 
                qcs_num_of_flag[handling_qc] = len([t_f for t_f in agreeable_yts_of_jobs[tar_j] if t_f])
                break
    elif chosen_j != qcs_primary_j[handling_qc]:
        ''' set not agreeable yt in each jobs '''
        for s_i in xrange(list(qc_seq).index(qcs_primary_j[handling_qc]), list(qc_seq).index(chosen_j)):
            agreeable_yts_of_jobs[qc_seq[s_i]][handling_yt] = False
        ''' revise # of flag '''
        qcs_num_of_flag[handling_qc] = len([t_f for t_f in agreeable_yts_of_jobs[qcs_primary_j[handling_qc]] if t_f])
        '''
        there is two case
        one is chosen_j == handling_qc.job_sequence[-1]
        another is chosen_j != handling_qc.job_sequence[-1]
        '''
        if chosen_j != qc_seq[-1]:
            adding_job_to_cut(cut, qc_seq, qcs_primary_j[handling_qc], chosen_j, planed_jobs, jobs)

def adding_job_to_cut(cut, qc_seq, primary_j, chosen_j_id, planed_jobs, jobs):
    ''' adding job which have condition for entering cut '''
    primary_j_index = None
    for i, j_id in enumerate(qc_seq):
        if j_id == primary_j:
            primary_j_index = i
            break
    for x in xrange(list(qc_seq).index(chosen_j_id) + 1, len(qc_seq)):
        if jobs[qc_seq[x]].type == 'L' and not planed_jobs[qc_seq[x]]:
            ''' before appearing Loading job which is not scheduled'''
            break
        elif jobs[qc_seq[x]].type == 'D' and qc_seq[x] not in cut and not planed_jobs[qc_seq[x]] and not check_prev_loading_jobs(primary_j_index, x, jobs, qc_seq, planed_jobs) :
            cut.append(qc_seq[x])

def run(init_jobs, init_qcs_seq, ycs_assignment, num_yts, for_debuging=False):
    jobs, qcs_seq, ycs_seq, yts_seq, planed_jobs, qcs_primary_j, agreeable_yts_of_jobs, handling_v, qcs_num_of_flag, cut = initialize(init_jobs, init_qcs_seq, ycs_assignment, num_yts)
#    print jobs , cut
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
    if for_debuging:
        f = file('set_cut_result.txt', 'w')
        f.write(str(jobs))
        f.write('\n')
        for order, ys, ts in d_set_cut_all_enumeration(f, cut, agreeable_yts_of_jobs, qcs_num_of_flag, qcs_primary_j, planed_jobs, ycs_seq, yts_seq, jobs, qcs_seq, handling_v):
            count += 1
            f.write('    '+ str(count) +' : '+ str(order) + str(qcs_seq) + str(ys) + str(ts))
            f.write('\n')
            print count, order, qcs_seq, ys, ts
        f.close()
    else:
        for ys, ts in set_cut_all_enumeration(cut, agreeable_yts_of_jobs, qcs_num_of_flag, qcs_primary_j, planed_jobs, ycs_seq, yts_seq, jobs, qcs_seq, handling_v):
            count += 1
    
def set_cut_all_enumeration(init_cut, init_agreeable_yts_of_jobs, init_qcs_num_of_flag, init_qcs_primary_j, init_planed_jobs, init_ycs_seq, init_yts_seq, jobs, qcs_seq, init_handling_v, init_order=[]):
    for i in xrange(len(init_cut)):
#        if init_cut == [0, 1] and i == 1:
#            print 'hi'
        assignable_yts_id = [yt_id for yt_id, yt_t_f in enumerate(init_agreeable_yts_of_jobs[init_cut[i]]) if yt_t_f]
        for assigned_yt in assignable_yts_id:
            data = [init_cut, init_agreeable_yts_of_jobs, init_ycs_seq, init_yts_seq, init_planed_jobs, init_qcs_primary_j, init_qcs_num_of_flag, init_handling_v]
            d_data = [duplicate_data(l) for l in data]
            cut, agreeable_yts_of_jobs, ycs_seq, yts_seq, planed_jobs, qcs_primary_j, qcs_num_of_flag, handling_v = tuple(d_data)
            if not set_cut_algorithm(cut.pop(i), assigned_yt, cut, agreeable_yts_of_jobs, qcs_num_of_flag, qcs_primary_j, planed_jobs, ycs_seq, yts_seq, jobs, qcs_seq, handling_v):
                continue
            if not cut:
                yield ycs_seq, yts_seq
            else:
                for ycs_seq, yts_seq in set_cut_all_enumeration(cut, agreeable_yts_of_jobs, qcs_num_of_flag, qcs_primary_j, planed_jobs, ycs_seq, yts_seq, jobs, qcs_seq, handling_v):
                    yield ycs_seq, yts_seq
    
def d_set_cut_all_enumeration(f, init_cut, init_agreeable_yts_of_jobs, init_qcs_num_of_flag, init_qcs_primary_j, init_planed_jobs, init_ycs_seq, init_yts_seq, jobs, qcs_seq, init_handling_v, init_order=[]):
    for i in xrange(len(init_cut)):
        if init_cut == [3, 0, 2] and i == 2:
            print 'hi'
        assignable_yts_id = [yt_id for yt_id, yt_t_f in enumerate(init_agreeable_yts_of_jobs[init_cut[i]]) if yt_t_f]
        for assigned_yt in assignable_yts_id:
            data = [init_cut, init_agreeable_yts_of_jobs, init_ycs_seq, init_yts_seq, init_planed_jobs, init_qcs_primary_j, init_qcs_num_of_flag, init_handling_v]
            d_data = [duplicate_data(l) for l in data]
            cut, agreeable_yts_of_jobs, ycs_seq, yts_seq, planed_jobs, qcs_primary_j, qcs_num_of_flag, handling_v = tuple(d_data)
            if not set_cut_algorithm(cut.pop(i), assigned_yt, cut, agreeable_yts_of_jobs, qcs_num_of_flag, qcs_primary_j, planed_jobs, ycs_seq, yts_seq, jobs, qcs_seq, handling_v):
                continue
            order = init_order[:]
            order.append(init_cut[i])
            if not cut:
                yield order, ycs_seq, yts_seq
            else:
                for order, ycs_seq, yts_seq in d_set_cut_all_enumeration(f, cut, agreeable_yts_of_jobs, qcs_num_of_flag, qcs_primary_j, planed_jobs, ycs_seq, yts_seq, jobs, qcs_seq, handling_v, order):
                    f.write(str(cut))
                    f.write('\n')
                    print cut
                    yield order, ycs_seq, yts_seq

def initialize(init_jobs, init_qcs_seq, ycs_assignment, num_yts):
    init_jobs.sort()
    jobs = tuple(init_jobs)
    qcs_seq = [] 
    for seq in init_qcs_seq:
        qc_seq = [j.id for j in seq]
        qcs_seq.append(tuple(qc_seq))
    qcs_seq = tuple(qcs_seq)
    qcs_primary_j = [seq[0] for seq in qcs_seq] 
    ycs_seq, yts_seq = [[] for _ in xrange(len(ycs_assignment))], [[] for _ in xrange(num_yts)] 
    handling_qc = [None] * len(jobs) 
    
    for q_id, seq in enumerate(qcs_seq):
        for j in seq:
            handling_qc[j] = q_id
    handling_yc = [None] * len(jobs) 
    for y_id, seq in enumerate(ycs_assignment):
        for j in seq:
            handling_yc[j.id] = y_id
    handling_yt = [None] * len(jobs)
    
    handling_v = [[handling_qc[i], handling_yc[i], handling_yt[i]] for i in xrange(len(jobs))]
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

def duplicate_data(l):
    if type(l[0]) == list: return [x[:]for x in l]
    else: return l[:]
    
if __name__ == '__main__':
    seed(0)
    jobs, qcs_seq, ycs_assign, num_yts = ran_example(6, 2, 2, 3)
    '''
    job : [3:D, 1:D, 2:D, 0:D]
    qcs_seq : [[2:D, 0:D, 3:D, 1:D]]
    ycs_assign : [[3:D, 2:D], [1:D, 0:D]]
    num_yts : 2
    '''
    run(jobs, qcs_seq, ycs_assign, num_yts, True)
    pass
