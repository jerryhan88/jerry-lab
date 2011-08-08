from __future__ import division #@UnresolvedImport

import Input
from clasese import Node, Edge, QC, YC

def run():
    #===========================================================================
    # STEP0
    # initialize
    # make all node and connect nodes by edges
    #===========================================================================
#    jobs, qcs, ycs, yts, yt_operation_time = Input.exp_not_random()
    jobs, qcs, ycs, yts, yt_operation_time = Input.exp_random()    
    
    print 'yt_operation_time : ', [(k[0].id, k[1].id, v)for k,v in yt_operation_time.items()]
    
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
            Edge(maked_nodes[1], maked_nodes[2], None, yt_operation_time[(target_qc, target_yc)])
            Edge(maked_nodes[2], maked_nodes[3], target_yc, Input.yc_discharging_operation)
        else:
            Edge(maked_nodes[0], maked_nodes[1], target_yc, Input.yc_loading_operation)
            Edge(maked_nodes[1], maked_nodes[2], None, yt_operation_time[(target_qc, target_yc)])
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
        if not qc.job_sequence:
            continue
#        print qc.job_sequence
        qc_start_n = qc.job_sequence[0].nodes[0]
        for e in qc_start_n.outgoings:
            if isinstance(e.vehicle, QC):
                possible_planable_n.append(e.end_n)
    
    print 'qcs'
    for qc in qcs:
        print '    qc id : ', qc.id,'sequence : ', [(x.id, x.state) for x in qc.job_sequence] , 
    print ''
    print 'ycs'
    for yc in ycs:
        print '    yc id : ', yc.id,'sequence : ', [(x.id, x.state) for x in yc.job_list] , 
    print ''
    
    
    
    count = 0
    while possible_planable_n:
        count += 1
        print ''
        print 'the number of times : ', count
        print 'possible_planable_n : ', [(x.id, x.order)for x in possible_planable_n]
        #===========================================================================
        # STEP1
        # calculate ET and LT on each node
        #===========================================================================
        #===========================================================================
        # calculate E_T    function
        #===========================================================================
        calc_E_T(all_nodes)
        # calculate L_T       function
        #===========================================================================
        calc_L_T(all_nodes, jobs)        
        #===========================================================================
        for x in all_nodes:
            print (x.id, x.order, x.E_T, x.L_T), 
            if x.order == 3:
                print ''
        #===========================================================================
        # STEP2
        # find node whose L_T is minimum in possible_planable_n
        # if there are more than two nodes which is same minimum L_T, choice one which has bigger E_T
        #===========================================================================
        print 'planed_nodes : ', [(n.id, n.order) for n in all_nodes if n.planed]
        minL_T = min([n.L_T for n in possible_planable_n])
        min_L_T_nodes = [n for n in possible_planable_n if minL_T == n.L_T]
        min_L_T_nodes.sort(key=lambda Node:Node.E_T, reverse=True)
        cur_planed_node = possible_planable_n.pop(possible_planable_n.index(min_L_T_nodes[0]))
#        planed_nodes.append(cur_planed_node)
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
                if cur_yc.stop_position == None:
                    #===========================================================
                    # don't need to add Edge
                    #===========================================================
                    continue
                elif cur_yc.stop_position.state == 'loading':
                    added_e = Edge(cur_yc.stop_position.nodes[1], cur_j.nodes[2], cur_yc, Input.yc_ready_t_l_d)
                    print 'added_e : ', 'start', (added_e.start_n.id, added_e.start_n.order), 'end', (added_e.end_n.id, added_e.end_n.order), 'time', added_e.time
                else:
                    added_e = Edge(cur_yc.stop_position.nodes[3], cur_j.nodes[2], cur_yc, Input.yc_ready_t_d_d)
                    print 'added_e : ', 'start', (added_e.start_n.id, added_e.start_n.order), 'end', (added_e.end_n.id, added_e.end_n.order), 'time', added_e.time
                
                if is_cycle_existing(all_nodes):
                    assert False, 'exception!!! there is not available yt'
                        
                    
                for e in cur_planed_node.outgoings:
                    if e.end_n.planed:
#####                        print 'e.end_n.planed'
#####                        print (e.end_n.id,e.end_n.order, e.end_n.planed)
#####                        print len([in_e for in_e in e.end_n.incomings if in_e.start_n.planed]) , len(e.end_n.incomings)
#####                        
#####                        print 'len(e.end_n.outgoings) : ',len(e.end_n.outgoings)
#####                        
#####                        for e1 in e.end_n.outgoings:
#####                            if e1.end_n.planed:
#####                                print 'planed'
######                                add_planable_node(e.end_n, possible_planable_n)
#####                            else:
#####                                print 'not planed'
######                                possible_planable_n.append(e.end_n)
#####                        
#####                   
                        add_planable_node(e.end_n, possible_planable_n)
                    else:
#                        print 'e.end_n.planed  not!!!!'
                        cur_j.nodes[3].planed = True
#                        possible_planable_n.append(e.end_n)
                
                
                
            #===================================================================
            # save yc's stop_position for calculate next yc operation's ready time
            #===================================================================
            cur_yc.stop_position = cur_j
            
            print 'YC Node go step 4'
            print 'cur_vehicle : ', cur_vehicle.id
                 
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
                    yt_and_ready_t_for_cur_j.append((yt, yt_operation_time[(prev_vehicle, next_vehicle)]))
                print 'yt_and_ready_t_for_cur_j : ', [(x.id, y)for x, y in yt_and_ready_t_for_cur_j]
                for cur_yt, ready_t in sorted(yt_and_ready_t_for_cur_j, key=lambda x:x[1]):
                    added_e = Edge(cur_yt.stop_position.nodes[2], cur_planed_node, cur_yt, ready_t)
                    #============================================================
                    # check cycle 
                    #============================================================
#                    print 'added_e : ', (added_e.start_n.id,added_e.start_n.order), (added_e.end_n.id,added_e.end_n.order)
                    if not is_cycle_existing(all_nodes):
                        print 'added_e : ', 'start', (added_e.start_n.id, added_e.start_n.order), 'end', (added_e.end_n.id, added_e.end_n.order), 'time', added_e.time
                        break
                    
                    print 'this edge make cycle~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
                    added_e.del_edge()
                    added_e = None
                    cur_yt = None
                else:
                    assert False, 'exception!!! there is not available yt'
            print 'YT Node go step 3'
            print 'cur_vehicle : ', cur_yt.id
            cur_yt.stop_position = cur_j
            cur_yt.job_sequence.append(cur_j)
            for e in cur_j.nodes[1].outgoings: 
                if e.end_n.planed:
                    add_planable_node(e.end_n, possible_planable_n)
                else: 
                    for i_e in cur_planed_node.incomings:
                        if not i_e.start_n.planed:
                            break
                    else:
                        possible_planable_n.append(e.end_n)
        print 'ycs'
        for yc in ycs:
            print '    yc id :', yc.id,'sequence : ', [x.id for x in yc.job_sequence],'    ',
        print ''
        print 'yts'
        for yt in yts:
            print '    yt id :', yt.id,'sequence : ', [x.id for x in yt.job_sequence],'    ',
            
        print ''
    
    
        
#        for n in all_nodes:
#            print (n.id, n.order, n.E_T, n.L_T, n.planed), 'outgoings : ', [(e.end_n.id, e.end_n.order, e.time)for e in n.outgoings],
#            if len(n.outgoings) == 2:
#                print '    ',
#            else:
#                print '             ',
#            if n.order == 3:
#                print ''
        
       
    print 'algorithms is ended'
    
                
def add_planable_node(node, possible_planable_n):
    if len([in_e for in_e in node.incomings if in_e.start_n.planed]) == len(node.incomings):
        for e in node.outgoings:
            if e.end_n.planed:
                add_planable_node(e.end_n, possible_planable_n)
            else:
                if e.end_n not in possible_planable_n:
                    possible_planable_n.append(e.end_n)

def is_cycle_existing(all_nodes):
    possible_del_n = []
    for n in all_nodes:
        n.visited = False
        if not n.incomings:
            possible_del_n.append(n)
        for e in n.outgoings:
            e.checked = False
        
    while possible_del_n:
        n = possible_del_n.pop()                        
        n.visited = True
        for o_e in n.outgoings:
            o_e.checked = True
            for i_e in o_e.end_n.incomings:
                if not i_e.checked:
                    break
            else:
                possible_del_n.append(o_e.end_n)
    
    if len([n for n in all_nodes if n.visited]) != len(all_nodes):
        return True
    else:
        return False

def calc_E_T(all_nodes):
    todo = []
    for n in all_nodes:
        if not n.incomings:
            todo.append(n)
        for e in n.outgoings:
            e.checked = False
    while todo:
        n = todo.pop()
        for o_e in n.outgoings:
            o_e.checked = True
            E_Ts_of_next_n = []
            for i_e in o_e.end_n.incomings:
                if not i_e.checked:
                    break
                E_Ts_of_next_n.append(i_e.start_n.E_T + i_e.time)
            else:
                o_e.end_n.E_T = max(E_Ts_of_next_n)
                todo.append(o_e.end_n)
                
def calc_L_T(all_nodes, jobs):
    todo = []
    for n in all_nodes:
        if not n.outgoings:
            todo.append(n)
        for e in n.outgoings:
            e.checked = False
    
    max_L_T = max([n.E_T for n in todo])
    for n in todo:
        n.L_T = max_L_T
                
    while todo:
        n = todo.pop()
        for i_e in n.incomings:
            i_e.checked = True
            L_Ts_of_prev_n = []
            for o_e in i_e.start_n.outgoings:
                if not o_e.checked:
                    break
                L_Ts_of_prev_n.append(o_e.end_n.L_T - o_e.time)
            else:
                i_e.start_n.L_T = min(L_Ts_of_prev_n)
                todo.append(i_e.start_n)
    #===========================================================================
    # revise node's L_T which is for yc's discharging operation
    #===========================================================================
    for j in jobs:
        if j.state == 'discharging' and j.nodes[2].planed == False:
            j.nodes[2].L_T = min(j.nodes[2].L_T, j.nodes[1].L_T + Input.yc_discharging_operation + Input.yc_discharging_operation)



if __name__ == '__main__':
    run()
