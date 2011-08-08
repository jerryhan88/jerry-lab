from __future__ import division #@UnresolvedImport

import step0, step1, step2, step3, step4
from clasese import YC

def run():
    #===========================================================================
    # STEP0
    # initialize
    # make all node and connect node by edge
    #===========================================================================
    all_nodes = step0.operate()
    #===========================================================================
    # STEP1
    # calculate ET and LT on each node
    # make process graph and return possible planable node which is sorted by T_E of Node
    #===========================================================================
    possible_planable_n = step1.operate(all_nodes)
    while possible_planable_n:
        cur_planed_node = step2.operate(possible_planable_n)
        cur_vehicle =cur_planed_node.outgoings[0].vehicle
        print (cur_planed_node.id ,cur_planed_node.order, cur_planed_node.T_L), [(x.id, x.order, x.T_L) for x in possible_planable_n]
        if isinstance(cur_vehicle,YC):
            print 'YC Node go step 4'
            print 'cur_vehicle : ',cur_vehicle.id
            print ''
#            print (cur_planed_node.id, cur_planed_node.order)

            possible_planable_n = step4.operate(cur_planed_node, possible_planable_n)
        else:
            print 'YT Node go step 3'
            possible_planable_n = step3.operate(cur_planed_node, possible_planable_n)
#            possible_planable_n = step3.operate(cur_planed_node)
        step1.operate(all_nodes)
#    for x in all_nodes:
#        print 'current node : ', (x.id, x.order)
#        print 'incomings node : ',  [[(j.start_n.id, j.start_n.order)] for j in x.incomings]
#        print 'outgoings node : ',  [[(j.end_n.id, j.end_n.order)] for j in x.outgoings]
    

    
if __name__ == '__main__':
    run()
    
