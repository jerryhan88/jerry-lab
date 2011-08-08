from __future__ import division #@UnresolvedImport
import Input
from clasese import Node, Edge

def operate():
    jobs = Input.jobs
    qcs = Input.qcs
    ycs = Input.ycs
    for job in jobs:
        maked_nodes = tuple([Node(job.id, i) for i in range(4)])
#        print [(x.id, x.order) for x in maked_nodes]
        target_qc = None
        target_yc = None
        for qc in qcs:
            if job in qc.job_sequence:
                target_qc = qc            
        for yc in ycs:
            if job in yc.job_list:
                target_yc = yc
#        print job.id,target_qc.id, target_yc.id
        if job.state == 'discharging':
            Edge(maked_nodes[0], maked_nodes[1], target_qc, Input.qc_discharging_operation)
            yt_operation_time = find_yt_oper_t(target_qc, target_yc)
            Edge(maked_nodes[1], maked_nodes[2], None, yt_operation_time)
            Edge(maked_nodes[2], maked_nodes[3], target_yc, Input.yc_discharging_operation)
        else:
            Edge(maked_nodes[0], maked_nodes[1], target_yc, Input.yc_loading_operation)
            yt_operation_time = find_yt_oper_t(target_qc, target_yc)
            Edge(maked_nodes[1], maked_nodes[2], None, yt_operation_time)
            Edge(maked_nodes[2], maked_nodes[3], target_qc, Input.qc_loading_operation)
        job.nodes = maked_nodes
        
        
    for qc in qcs:
        for i in range(1, len(qc.job_sequence)):
            prev_j = qc.job_sequence[i - 1]
            current_j = qc.job_sequence[i]
            target_start_n = None
            target_end_n = None
            ready_time = None
            
            if prev_j.state == 'discharging':
                target_start_n = jobs[prev_j.id].nodes[1]                
                if current_j.state == 'discharging':
                    target_end_n = jobs[current_j.id].nodes[0]    
                    ready_time = Input.qc_ready_t_d_d
                else:
                    # current_j.state == loading
                    target_end_n = jobs[current_j.id].nodes[2]
                    ready_time = Input.qc_ready_t_d_l
            else:
                #prev_j.state == loading
                target_start_n = jobs[prev_j.id].nodes[3]
                if current_j.state == 'discharging':
                    target_end_n = jobs[current_j.id].nodes[0]
                    ready_time = Input.qc_ready_t_l_d
                else:
                    # current_j.state == loading
                    target_end_n = jobs[current_j.id].nodes[2]
                    ready_time = Input.qc_ready_t_l_l
            Edge(target_start_n, target_end_n, qc.id, ready_time)    
    all_nodes = []
    for j in jobs:
        all_nodes.extend(j.nodes)
    return all_nodes

def find_yt_oper_t(qc, yc):
    for key, value in Input.yt_moving_time.items():        
        if qc in list(key) and yc in list(key):
            return value