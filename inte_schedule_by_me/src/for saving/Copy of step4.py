from __future__ import division #@UnresolvedImport
import Input
from clasese import Edge

def operate(cur_planed_node, possible_planable_n):
    cur_j = Input.jobs[cur_planed_node.id]
    for yc in Input.ycs:
        if cur_j in yc.job_list:
            cur_yc = yc
            cur_yc.job_sequence.append(cur_j) 
    if cur_j.state == 'loading':
        possible_planable_n.append(cur_planed_node.outgoings[0].end_n)
    else:
        cur_j.nodes[3].planed = True
        if cur_yc.stop_position.state == None:
            return possible_planable_n
        elif cur_yc.stop_position.state == 'loading':
            Edge(cur_yc.stop_position.nodes[1], cur_j.nodes[2], cur_yc, Input.yc_ready_t_l_d)
        else:
            Edge(cur_yc.stop_position.nodes[3], cur_j.nodes[2], cur_yc, Input.yc_ready_t_d_d)
    cur_yc.stop_position = cur_j
    
    return possible_planable_n
    

         
        
#    print cur_planed_node
#    for e in cur_planed_node.outgoings:
#        end_n = e.end_n
#        if not end_n.planed:
#            possible_planable_n.append(end_n)
    