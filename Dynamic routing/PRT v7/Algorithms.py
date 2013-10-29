from __future__ import division
from math import sqrt
from munkres import Munkres

def get_all_dispatchers():
    return {'NN0': NN0, 'NN1': NN1, 'NN2': NN2, 'NN3': NN3, 'NN4': NN4, 'NN5': NN5}

on_notify_assignmentment_point = lambda x: None

Longest_dis = 0

def reassignment(event_time, target_PRTs, target_customers, Nodes):
    for prt_id, customer_id in find_opt_matching(event_time, target_PRTs, target_customers, Nodes):
        chosen_prt = target_PRTs[prt_id]
        target_c = target_customers[customer_id]
        chosen_prt.re_assign_customer(event_time, target_c)

def NN0(event_time, PRTs, waiting_customers, Nodes):
    on_notify_assignmentment_point(None)
    target_PRTs = [prt for prt in PRTs if prt.state == 0]
    if not target_PRTs: return None
    target_customers = [customer for customer in waiting_customers if not customer.assigned_PRT]
    reassignment(event_time, target_PRTs, target_customers, Nodes)

def NN1(event_time, PRTs, waiting_customers, Nodes):
    on_notify_assignmentment_point(None)
    target_PRTs = [prt for prt in PRTs if prt.state == 0 or prt.state == 2 ]
    if not target_PRTs: return None
    target_customers = [customer for customer in waiting_customers if not customer.assigned_PRT]
    reassignment(event_time, target_PRTs, target_customers, Nodes)

def NN2(event_time, PRTs, waiting_customers, Nodes):
    on_notify_assignmentment_point(None)
    target_PRTs = [prt for prt in PRTs if prt.state == 0 or prt.state == 1 ]
    if not target_PRTs: return None
    target_customers = waiting_customers
    reassignment(event_time, target_PRTs, target_customers, Nodes)

def NN3(event_time, PRTs, waiting_customers, Nodes):
    on_notify_assignmentment_point(None)
    target_PRTs = [prt for prt in PRTs if prt.state != 2 ]
    if not target_PRTs: return None
    target_customers = waiting_customers
    reassignment(event_time, target_PRTs, target_customers, Nodes)

def NN4(event_time, PRTs, waiting_customers, Nodes):
    on_notify_assignmentment_point(None)
    target_PRTs = [prt for prt in PRTs if prt.state != 3 ]
    if not target_PRTs: return None
    target_customers = waiting_customers
    reassignment(event_time, target_PRTs, target_customers, Nodes)            

def NN5(event_time, PRTs, waiting_customers, Nodes):
    on_notify_assignmentment_point(None)
    target_PRTs = PRTs
    if not target_PRTs: return None
    target_customers = waiting_customers
    reassignment(event_time, target_PRTs, target_customers, Nodes)

def find_opt_matching(cur_time, target_PRTs, customers, Nodes):
    NodeByNode_DMatrix = create_NodeByNode_DMatrix(Nodes)
    PRTbyCustomer_matrix = create_PRTbyCustomer_matrix(cur_time, target_PRTs, customers, NodeByNode_DMatrix)

    hungarian_algo = Munkres()
    assignment_results = []
    for prt_id, customer_id in hungarian_algo.compute(PRTbyCustomer_matrix):
        if prt_id >= len(target_PRTs) or customer_id >= len(customers):
            continue 
        # (prt, customer)
        assignment_results.append((prt_id, customer_id))
    return assignment_results

def create_PRTbyCustomer_matrix(cur_time, PRTs, customers, NodeByNode_DMatrix):
    from Dynamics import PRT_SPEED
    global Longest_dis
    row_size, col_size = len(PRTs), len(customers)
    max_M_size = max(row_size, col_size)
    
    PRTbyCustomer_matrix = [[Longest_dis / PRT_SPEED] * max_M_size for _ in range(max_M_size)]
    
    for prt_id, prt in enumerate(PRTs):
        for i, cus in enumerate(customers):
            if prt.state == 0:
                PRTbyCustomer_matrix[prt_id][i] = NodeByNode_DMatrix[prt.arrived_n.id][cus.sn.id] / PRT_SPEED
            elif prt.state == 1:
                # find next node
                next_n = None
                path_travel_distance = (cur_time - prt.last_planed_time) * PRT_SPEED
                sum_edges_distance = 0
                edges_counter = 0
                for e in prt.path_e:
                    sum_edges_distance += e.distance
                    edges_counter += 1 
                    if sum_edges_distance >= path_travel_distance:
                        next_n = e._to
                        break
                    
                remain_dis = sum([e.distance for e in prt.path_e[:edges_counter]]) - path_travel_distance
                 
                PRTbyCustomer_matrix[prt_id][i] = (NodeByNode_DMatrix[next_n.id][cus.sn.id] + remain_dis) / PRT_SPEED 
            elif prt.state == 2:
                path_travel_distance = (cur_time - prt.last_planed_time) * PRT_SPEED                
                distance = sum([e.distance for e in prt.path_e]) - path_travel_distance 
                PRTbyCustomer_matrix[prt_id][i] = (NodeByNode_DMatrix[prt.path_n[-1].id][cus.sn.id] + distance) / PRT_SPEED
            else:
                # if prt.state == 3  there is only one node in path
                assert prt.state == 3 and len(prt.path_n) == 1
                next_n = prt.path_n[-1]
                dx = next_n.px - prt.px  
                dy = next_n.py - prt.py
                remain_dis = sqrt(dx * dx + dy * dy) 
                PRTbyCustomer_matrix[prt_id][i] = (NodeByNode_DMatrix[next_n.id][cus.sn.id] + remain_dis) / PRT_SPEED
                
    return PRTbyCustomer_matrix

def create_NodeByNode_DMatrix(Nodes):
    NodeByNode_DMatrix = []
    for i in Nodes:
        from_i = []
        for j in Nodes:
            _ , path_e = find_SP(i, j, Nodes)
            distance = sum([e.distance for e in path_e])
            from_i.append(distance)
            # find longest_distance in network
            global Longest_dis
            if Longest_dis < distance: Longest_dis = distance   
        NodeByNode_DMatrix.append(from_i)
    return NodeByNode_DMatrix

def find_SP(sn, en, Nodes):
    for n in Nodes:
        n.init_node()
        
    sn.min_d = 0
    todo = [sn]
    
    while todo:
        n = todo.pop(0)
        n.visited = True
        for e in n.edges_outward:
            consi_n = e._to
            dist = n.min_d + e.distance
            if consi_n.min_d >= dist:
                consi_n.min_d = dist
            if not consi_n.visited and not [x for x in todo if consi_n.id == x.id] and consi_n != en:
                todo.append(consi_n)
    path_n = []
    path_e = []
    path_n.append(en)
    consi_n = en
    while consi_n:
        for e in consi_n.edges_inward:
            if e._from.min_d + e.distance == consi_n.min_d:
                consi_n = e._from
                path_e.append(e)
                break 
        else:
            consi_n = None
            break
        path_n.append(consi_n)
    path_n.reverse()
    path_e.reverse()

    return path_n, path_e


if __name__ == '__main__':
    import input_gen, Scenarios 
    
    Nodes, Edges = input_gen.network1()
#     PRTs, customers = scenario0()
#     PRTs, customers = scenario1()
    PRTs, customers = Scenarios.scenario2(Nodes)
#     PRTs, customers = Scenarios.scenario3(Nodes)

    print NN0(PRTs, customers, Nodes)
    print NN1(PRTs, customers, Nodes)
    assert False
    
    pc_M = nn.create_PRTbyCustomer_matrix(PRTs, customers, Nodes)
    metrix_display(pc_M)
    assignment_results = nn.find_opt_matching(PRTs, customers, pc_M)
        
    for prt_id, customer_id in assignment_results:
        print '%s: assigned customer is (%s)' % (PRTs[prt_id], customers[customer_id])
#     for prt in PRTs:
#         print 'PRT%d: assigned customer is (%s)' % (prt.id, prt.assigned_customer)  
