from __future__ import division #@UnresolvedImport

import Input
from clasese import Node, Edge, QC, YC

def run():
    #===========================================================================
    # STEP0
    # initialize
    # make all node and connect nodes by edges
    #===========================================================================
    jobs = Input.jobs
    qcs = Input.qcs
    ycs = Input.ycs
    yts = Input.yts
    not_yet_used_yt = yts[:]
    all_nodes = []
    possible_planable_n = []
    #===========================================================================
    # make nodes related with job
    #===========================================================================
    for job in jobs:
        maked_nodes = tuple([Node(job.id, i) for i in range(4)])
        target_qc = None
        target_yc = None
        for qc in qcs:
            if job in qc.job_sequence:
                target_qc = qc            
        for yc in ycs:
            if job in yc.job_list:
                target_yc = yc

        if job.state == 'discharging':
            Edge(maked_nodes[0], maked_nodes[1], target_qc, Input.qc_discharging_operation)
            Edge(maked_nodes[1], maked_nodes[2], None, Input.yt_operation_time[(target_qc, target_yc)])
            Edge(maked_nodes[2], maked_nodes[3], target_yc, Input.yc_discharging_operation)
        else:
            Edge(maked_nodes[0], maked_nodes[1], target_yc, Input.yc_loading_operation)
            Edge(maked_nodes[1], maked_nodes[2], None, Input.yt_operation_time[(target_qc, target_yc)])
            Edge(maked_nodes[2], maked_nodes[3], target_qc, Input.qc_loading_operation)
        job.nodes = maked_nodes
    #===========================================================================
    # append all node in all_nodes
    #===========================================================================
    for j in jobs:
        all_nodes.extend(j.nodes)
    #===========================================================================
    # connect nodes related with qcs
    #===========================================================================
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
                    target_end_n = jobs[current_j.id].nodes[2]
                    ready_time = Input.qc_ready_t_d_l
            else:
                target_start_n = jobs[prev_j.id].nodes[3]
                if current_j.state == 'discharging':
                    target_end_n = jobs[current_j.id].nodes[0]
                    ready_time = Input.qc_ready_t_l_d
                else:
                    target_end_n = jobs[current_j.id].nodes[2]
                    ready_time = Input.qc_ready_t_l_l
            Edge(target_start_n, target_end_n, qc.id, ready_time)
    #===========================================================================
    # initialize nodes related with qcs
    # and make possible_planable_n
    #===========================================================================
    for j in jobs:
        if j.state == 'loading':
            j.nodes[2].planed = True
            j.nodes[3].planed = True
            possible_planable_n.append(j.nodes[0])
        else:
            j.nodes[0].planed = True
    for qc in qcs:
        qc_start_n = qc.job_sequence[0].nodes[0]
        for e in qc_start_n.outgoings:
            if isinstance(e.vehicle, QC):
                possible_planable_n.append(e.end_n)
    while possible_planable_n:
        #===========================================================================
        # STEP1
        # calculate ET and LT on each node
        #===========================================================================
        #===========================================================================
        # calculate E_T    function
        #===========================================================================
        for node in [j.nodes[0] for j in jobs if not j.nodes[0].incomings]:
            for n in all_nodes:
                n.visited = False        
            todo = [node]
            while todo:
                n = todo.pop(0)
                n.visited = True
                for e in n.outgoings:
                    e.end_n.E_T = max(e.end_n.E_T, n.E_T + e.time)
                    if e.end_n.visited == False:
                        todo.append(e.end_n)        
        #===========================================================================
        # calculate L_T       function
        #===========================================================================
        end_nodes_of_jobs = [j.nodes[3] for j in jobs if not j.nodes[3].outgoings]    
        max_L_T = max([x.E_T for x in end_nodes_of_jobs])
        for node in end_nodes_of_jobs:
            node.L_T = max_L_T
            for n in all_nodes:
                n.visited = False
            todo = [node]
            while todo:
                n = todo.pop(0)
                n.l_visited = True    
                for edge in n.incomings:
                        edge.start_n.L_T = min(edge.start_n.L_T, n.L_T - edge.time)
                        if edge.start_n.e_visited == False:
                            todo.append(edge.start_n)
        #===========================================================================
        # revise node's L_T which is for yc's discharging operation
        #===========================================================================
        for j in jobs:
            if j.state == 'discharging' and j.nodes[2].planed == False:
                j.nodes[2].L_T = min(j.nodes[2].L_T, j.nodes[1].L_T + Input.yc_discharging_operation + Input.yc_discharging_operation)
                
        print 'possible_planable_n : ', [(x.id, x.order, x.E_T, x.L_T)for x in possible_planable_n]
        
        #===========================================================================
        # STEP2
        # find node whose L_T is minimum in possible_planable_n
        # if there are more than two nodes which is same minimum L_T, choice one which has bigger E_T
        #===========================================================================
        minL_T = min([n.L_T for n in possible_planable_n])
        min_L_T_nodes = [n for n in possible_planable_n if minL_T == n.L_T]
        min_L_T_nodes.sort(key=lambda Node:Node.E_T, reverse=True)
        cur_planed_node = possible_planable_n.pop(possible_planable_n.index(min_L_T_nodes[0]))
        cur_planed_node.planed = True
        print 'cur_planed_node : ', (cur_planed_node.id, cur_planed_node.order)  
        #===========================================================================
        # STEP3 and STEP4
        # choice next step decided by vehicle
        #===========================================================================
        cur_vehicle = cur_planed_node.outgoings[0].vehicle
        if isinstance(cur_vehicle, YC):
            #===========================================================================
            # STEP4
            # in this step, YC operate 
            # find YC whose job_list include cur_planed_node   
            #===========================================================================
            cur_j = jobs[cur_planed_node.id]
            for yc in ycs:
                if cur_j in yc.job_list:
                    cur_yc = yc
                    cur_yc.job_sequence.append(cur_j) 
            if cur_j.state == 'loading':
                possible_planable_n.append(cur_planed_node.outgoings[0].end_n)
            else:
                cur_j.nodes[3].planed = True
                if cur_yc.stop_position == None:
                    #===========================================================
                    # don't need to add Edge
                    #===========================================================
                    continue
                elif cur_yc.stop_position.state == 'loading':
                    Edge(cur_yc.stop_position.nodes[1], cur_j.nodes[2], cur_yc, Input.yc_ready_t_l_d)
                else:
                    Edge(cur_yc.stop_position.nodes[3], cur_j.nodes[2], cur_yc, Input.yc_ready_t_d_d)
            #===================================================================
            # save yc's stop_position for calculate next yc operation's ready time
            #===================================================================
            cur_yc.stop_position = cur_j
            
            print 'YC Node go step 4'
            print 'cur_vehicle : ', cur_vehicle.id
            print ''
        else:
            #===========================================================================
            # STEP3
            # in this step, YT operate 
            # find YT whose ready time is shorter than others
            # if chosen YT make a cycle, choose another one   
            #===========================================================================
            cur_j = jobs[cur_planed_node.id]
            cur_yt = None
            if not_yet_used_yt:
                cur_yt = not_yet_used_yt.pop(0)
            else:
                yt_and_ready_t_for_cur_j = []
                for yt in yts:
                    prev_vehicle = yt.stop_position.nodes[2].outgoings[0].vehicle
                    next_vehicle = cur_planed_node.incomings[0].vehicle        
                    yt_and_ready_t_for_cur_j.append((yt, Input.yt_operation_time[(prev_vehicle, next_vehicle)]))
                for cur_yt, ready_t in sorted(yt_and_ready_t_for_cur_j, key=lambda x:x[1]):
                    added_e = Edge(cur_yt.stop_position.nodes[2], cur_planed_node, cur_yt, ready_t)
                    
#                    possible_del_n = [j.nodes[0] for j in jobs if not j.nodes[0].incomings]
                    #============================================================
                    # check cycle 
                    #============================================================
                    possible_del_n = []
                    for n in all_nodes:
                        n.visited = False
                        for e in n.outgoings:
                            e.checked = False
                        if not n.incomings:
                            possible_del_n.append(n)
                    while possible_del_n:
                        n = possible_del_n.pop(0)                        
                        n.visited = True
                        for o_e in n.outgoings:
                            o_e.checked = True
                            for e in o_e.end_n.incomings:
                                if not e.checked:
                                    break
                            else:
                                possible_del_n.append(o_e.end_n)
                    if len([n for n in all_nodes if n.visited]) == len(all_nodes):
                        break
                    
                    print 'this edge make cycle'
                    added_e.del_edge()
                    added_e = None
                    cur_yt = None
                else:
                    assert False, 'exception!!! there is not available yt'

            print 'YT Node go step 3'
            print 'cur_vehicle : ', cur_yt.id
            print ''
            cur_yt.stop_position = cur_j
            for e in cur_j.nodes[1].outgoings: 
                if e.end_n.planed:
                    add_planable_node(e.end_n, possible_planable_n)
                else:
                    possible_planable_n.append(e.end_n)
            
    print 'algorithms is ended'
                
def add_planable_node(node, possible_planable_n):
    if [in_e for in_e in node.incomings if in_e.start_n.planed] == node.incomings:
        for e in node.outgoings:
            if e.end_n.planed:
                add_planable_node(e.end_n, possible_planable_n)
            else:
                possible_planable_n.append(e.end_n)


if __name__ == '__main__':
    run()
