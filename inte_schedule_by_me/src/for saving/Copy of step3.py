from __future__ import division #@UnresolvedImport
import Input
from clasese import QC, YC
def add_planable_node(node, possible_planable_n):
#    print '[in_e for in_e in node.incomings if in_e.start_n.planed] : '
#    print [(in_e.start_n.id, in_e.start_n.order) for in_e in node.incomings if in_e.start_n.planed]
#    print 'len(node.incomings)'
#    print len(node.incomings)
    if [in_e for in_e in node.incomings if in_e.start_n.planed] == node.incomings:
#        print 'hi'
        for e in node.outgoings:
#            print (e.end_n.id,e.end_n.order, e.end_n.planed)
            if e.end_n.planed:
                add_planable_node(e.end_n, possible_planable_n)
            else:
                possible_planable_n.append(e.end_n)
    
#    elif not [in_e for in_e in node.incomings if in_e.start_n.planed]:
#        possible_planable_n.append(node)
#        
#        
#    for e in node.outgoings:
#        if e.end_n.planed:
#            if [in_e for in_e in e.end_n.incomings if in_e.start_n.planed] == len(e.end_n.incomings):
#                add_planable_node(e.end_n, possible_planable_n)
#            else:
#                break
#        else:    
#            possible_planable_n.append(e.end_n)

def operate(cur_planed_node, possible_planable_n):
    cur_j = Input.jobs[cur_planed_node.id]
    cur_yt = None
    for yt in Input.yts:
        if yt.stop_position == None:
            cur_yt = yt
            for e in cur_j.nodes[2].outgoings:
                if isinstance(e.vehicle, QC) or isinstance(e.vehicle, YC): 
                    cur_yt.stop_position = e.vehicle  
            break
#    print 'cur_yt : ', cur_yt.id
    print 'cur_vehicle : ',cur_yt.id
#    if cur_yt.id == 'YT2':
#        print 'break'
#    
#        print [x.vehicle for x in cur_j.nodes[1].outgoings]
    for e in cur_j.nodes[1].outgoings:
        if e.vehicle == None:
            e.vehicle = cur_yt
#        print 'e.vehicle : ',e.vehicle 
        if e.end_n.planed:
#            print 'cur_n : ',(cur_j.nodes[1].id, cur_j.nodes[1].order)
            add_planable_node(e.end_n, possible_planable_n)
#            print 'add_planable_node operated?'
#            print [(x.id, x.order, x.T_L) for x in possible_planable_n]
        else:
            possible_planable_n.append(e.end_n)
#            print 'this operated?'
#            print [(x.id, x.order, x.T_L) for x in possible_planable_n]
    print ''
    return possible_planable_n
#    return possible_planable_n
        