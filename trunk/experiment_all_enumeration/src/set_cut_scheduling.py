from __future__ import division #@UnresolvedImport
from input import ran_example
from clasese import QC, YC, YT, Deposit

def set_cut_run(jobs, qcs_seq, ycs_assign, num_yts, visualize=False):
#    jobs, qcs, ycs, yts = Input.small_problem()
#    jobs, qcs, ycs, yts = Input.big_problem()
    #===========================================================================
    # find job which satisfy cut's condition
    #===========================================================================
    
    qcs, ycs, yts = make_vehicles(jobs, qcs_seq, ycs_assign, num_yts) 
    
    
    cut = []
    for qc in qcs:
        is_first_loading_job_of_qc = True
        for i, j_id in enumerate(qc.job_seq):
            if j_id == qc.primary_j:
                #===============================================================
                # or if i == 0
                # it means first job of qc.job_seq
                #===============================================================
                cut.append(j_id)
            if jobs[j_id].type == 'L':
                #===============================================================
                # all loading job will be in cut
                # and discharging job before finding first loading job will be in cut
                #===============================================================
                if is_first_loading_job_of_qc:
                    for x in range(i + 1):
                        if qc.job_seq[x] == qc.primary_j: continue
                        #=======================================================
                        # discharging job will be in cut
                        #=======================================================
                        cut.append(qc.job_seq[x])
                    is_first_loading_job_of_qc = False
                    continue
                #===============================================================
                # after is_first_loading_job_of_qc = False
                # all loading job will be into cut
                #===============================================================
                cut.append(j_id)
                
    stack_for_cut = []
    scheduled_jobs = [False for _ in jobs]
    agreeable_yt_of_job = [[True for x in range(len(yts))] for _ in jobs]
    # node is for data saving
    init_node = Deposit(cut, scheduled_jobs, agreeable_yt_of_job, qcs, ycs, yts)
    stack_for_cut.append(init_node)
    count = 0
#    print stack_for_cut
    while stack_for_cut:
        node = stack_for_cut.pop()
        for i in range(len(node.cut)):
            agreeable_yt_ids = [yt_id for yt_id, yt_t_f in enumerate(node.agreeable_yt_of_job[node.cut[i]]) if yt_t_f]
            for agree_yt_id in agreeable_yt_ids:
                n_node = node.duplicate()
                chosen_j = n_node.cut.pop(i)
                handling_qc = n_node.qcs[jobs[chosen_j].handling_qc_id]
                if handling_qc.num_of_flag == 1 and chosen_j != handling_qc.primary_j and n_node.agreeable_yt_of_job[handling_qc.primary_j][agree_yt_id]:
                        continue
                #===============================================================
                # schedule chosen_j in job_seq of handling_yc and handling_yt 
                #===============================================================
                handling_yc = n_node.ycs[jobs[chosen_j].handling_yc_id]
                handling_yt = n_node.yts[agree_yt_id]
                handling_yc.job_seq.append(chosen_j)
                handling_yt.job_seq.append(chosen_j)
                
                qc_j_seq = handling_qc.job_seq
                n_node.scheduled_jobs[chosen_j] = True
                if chosen_j == handling_qc.primary_j and chosen_j != handling_qc.job_seq[-1]:
                    adding_job_to_cut(n_node.cut, qc_j_seq, chosen_j, jobs, n_node)
                    #===================================================================
                    # find next primary job and revise # of flag
                    #===================================================================
                    for x in range(list(qc_j_seq).index(chosen_j) + 1, len(qc_j_seq)):
                        if not n_node.scheduled_jobs[qc_j_seq[x]]:
                            handling_qc.primary_j = qc_j_seq[x]
                            handling_qc.primary_j_id_in_seq = x
                            handling_qc.num_of_flag = len([t_f for t_f in n_node.agreeable_yt_of_job[handling_qc.primary_j] if t_f])
                            break
                elif chosen_j != handling_qc.primary_j:
                    '''
                    set not agreeable yt in each jobs
                    '''
                    for s_i in range(handling_qc.primary_j_id_in_seq, list(handling_qc.job_seq).index(chosen_j)):
                        n_node.agreeable_yt_of_job[handling_qc.job_seq[s_i]][handling_yt.id] = False
                    '''
                    revise # of flag
                    '''
                    handling_qc.num_of_flag = len([t_f for t_f in n_node.agreeable_yt_of_job[handling_qc.primary_j] if t_f])
                    '''
                    there is two case
                    one is chosen_j == handling_qc.job_sequence[-1]
                    another is chosen_j != handling_qc.job_sequence[-1]
                    '''
                    if chosen_j != handling_qc.job_seq[-1]:
                        adding_job_to_cut(n_node.cut, qc_j_seq, chosen_j, jobs, n_node)
                else:
                    '''
                    chosen_j == handling_qc.primary_j and chosen_j == handling_qc.job_seq[-1]
                    '''
                    pass
                
                if n_node.cut:
                    '''
                    if n_node.cut == []
                    it means that all jobs are scheduled
                    '''
                    stack_for_cut.append(n_node)
                else:
                    count += 1
                    yield n_node.qcs, n_node.ycs, n_node.yts
                    if visualize:
                        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', count 
                        for qc_i, qc in enumerate(n_node.qcs):
                            print '    qc', qc_i, ' : ', qc.job_seq
                        for yc_i, yc in enumerate(n_node.ycs):
                            print '    yc', yc_i, ' : ', yc.job_seq
                        for yt_i, yt in enumerate(n_node.yts):
                            print '    yt', yt_i, ' : ', yt.job_seq

def adding_job_to_cut(cut, qc_j_seq, chosen_j, jobs, n_node):
    '''
    adding job which have condition for entering cut 
    '''
    for x in range(list(qc_j_seq).index(chosen_j) + 1, len(qc_j_seq)):
        if jobs[qc_j_seq[x]].type == 'D' and qc_j_seq[x] not in n_node.cut and not n_node.scheduled_jobs[qc_j_seq[x]]:
            cut.append(qc_j_seq[x])
        elif jobs[qc_j_seq[x]].type == 'L' and n_node.scheduled_jobs[qc_j_seq[x]]:
            continue
        else:
            '''
            jobs[qc_j_seq[x]].type == 'L'
            and n_node.scheduled_jobs[qc_j_seq[x]] is False
            '''
            break

def make_vehicles(jobs, qcs_seq, ycs_assign, num_yts):
    qcs_seq_id = []
    ycs_assign_id = []
    for i, seq in enumerate(qcs_seq):
        qcs_seq_id.append([j.id for j in seq])
        for j in seq:
            jobs[j.id].handling_qc_id = i  
    for i, seq in enumerate(ycs_assign):
        ycs_assign_id.append([j.id for j in seq])
        for j in seq:
            jobs[j.id].handling_yc_id = i
    
    qcs = [QC(i, tuple(qc_seq), num_yts) for i, qc_seq in enumerate(qcs_seq_id)]
    ycs = [YC(i, tuple(yc_assigns)) for i , yc_assigns in enumerate(ycs_assign_id)]
    yts = [YT(i) for i in xrange(num_yts)]
    return qcs, ycs, yts
    
if __name__ == '__main__':
    jobs, qcs_seq, ycs_assign, num_yts = ran_example(4, 1, 2, 2)
#    print qcs_seq
#    qcs, ycs, yts = make_vehicles(qcs_seq, ycs_assign, num_yts)
#    print qcs[0]
     
    for qs, ys, ts in set_cut_run(jobs, qcs_seq, ycs_assign, num_yts, True):
        pass
