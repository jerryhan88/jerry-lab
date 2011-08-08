from __future__ import division #@UnresolvedImport

def operate(possible_planable_n):
    minT_L = min([n.T_L for n in possible_planable_n])
    min_T_L_nodes = [n for n in possible_planable_n if minT_L == n.T_L]
#    print [(x.id, x.order, x.T_L)for x in min_T_L_nodes]
    min_T_L_nodes.sort(key=lambda Node:Node.T_E, reverse = True)
#    min_T_L_nodes.reverse()
    cur_planed_node = possible_planable_n.pop(possible_planable_n.index(min_T_L_nodes[0]))
    cur_planed_node.planed = True 
    return cur_planed_node