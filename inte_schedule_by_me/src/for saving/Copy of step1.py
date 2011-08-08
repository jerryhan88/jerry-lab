from __future__ import division #@UnresolvedImport
import Input


def operate(all_nodes, possible_planable_n = []):
    jobs = Input.jobs
    qcs = Input.qcs
    #===========================================================================
    # calculate T_E
    #===========================================================================
    first_nodes_of_jobs = [j.nodes[0] for j in jobs]
    for start in first_nodes_of_jobs: 
        calc_T_E(all_nodes, start)        
    #===========================================================================
    # calculate T_L
    #===========================================================================
    end_nodes_of_jobs = [j.nodes[3] for j in jobs]    
    max_T_L = max([x.T_E for x in end_nodes_of_jobs])
    for end in end_nodes_of_jobs:
        end.T_L = max_T_L
        calc_T_L(all_nodes, end)
    #===========================================================================
    # revise node's T_L which is for yc's discharging operation
    #===========================================================================
    for j in jobs:
        if j.state == 'discharging' and j.nodes[2].planed == False:
            j.nodes[2].T_L = min(j.nodes[2].T_L, j.nodes[1].T_L + Input.yc_discharging_operation + Input.yc_discharging_operation)
    #===========================================================================
    # before starting step2, find possible planable node
    # and sort by T_E of Node
    #===========================================================================
    if not possible_planable_n and not qcs[0].job_sequence[0].nodes[0].planed:
        for j in jobs:
            if j.state =='loading':
                possible_planable_n.append(j.nodes[0])
                #===================================================================
                # node related with qc are planed
                #===================================================================
                j.nodes[2].planed = True
                j.nodes[3].planed = True
            else:
                j.nodes[0].planed = True
        for qc in qcs:
            qc_start_n = qc.job_sequence[0].nodes[0]
            qc_start_n.planed = True
            for e in qc_start_n.outgoings:
                possible_planable_n.append(e.end_n)
        possible_planable_n.sort(key=lambda Node:Node.T_L)
        return possible_planable_n
#    for x in all_nodes:
#        print (x.id, x.order), x.T_E
#    print ''
#    
#    for x in all_nodes:
#        print (x.id, x.order), x.T_L
    
def calc_T_L(all_nodes, node):
    for n in all_nodes:
        n.visited = False
    todo = [node]
#    node.T_L = node.T_E
    while todo:
        n = todo.pop(0)
        n.l_visited = True    
        for edge in n.incomings:
                edge.start_n.T_L = min(edge.start_n.T_L, n.T_L - edge.time)
                if edge.start_n.e_visited == False:
                    todo.append(edge.start_n)
    
    
def calc_T_E(all_nodes, node):
    for n in all_nodes:
        n.visited = False        
    todo = [node]
    while todo:
        n = todo.pop(0)
        n.visited = True
        for e in n.outgoings:
            e.end_n.T_E = max(e.end_n.T_E, n.T_E + e.time)
            if e.end_n.visited == False:
                todo.append(e.end_n)
