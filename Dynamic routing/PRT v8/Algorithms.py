from __future__ import division
from math import sqrt
from munkres import Munkres


on_notify_assignmentment_point = lambda x: None

# For using Hungarian method, give long distance(cost) to augmented cell
Longest_dis = 100000000

def get_all_dispatchers():
    return {'NN0': NN0, 'NN1': NN1, 'NN2': NN2, 'NN3': NN3, 'NN4': NN4, 'NN5': NN5}

def reassignment(event_time, target_PRTs, target_customers, Nodes):
    for prt_id, customer_id in find_opt_matching(event_time, target_PRTs, target_customers, Nodes):
        chosen_prt = target_PRTs[prt_id]
        target_c = target_customers[customer_id]
        chosen_prt.re_assign_customer(event_time, target_c)

def NN0(event_time, PRTs, waiting_customers, Nodes):
    # Target PRT: I
    on_notify_assignmentment_point(None)
    target_PRTs = [prt for prt in PRTs if prt.state == 0]
    if not target_PRTs: return None
    target_customers = [customer for customer in waiting_customers if not customer.assigned_PRT]
    reassignment(event_time, target_PRTs, target_customers, Nodes)

def NN1(event_time, PRTs, waiting_customers, Nodes):
    # Target PRT: I/A
    on_notify_assignmentment_point(None)
    target_PRTs = [prt for prt in PRTs if prt.state == 0 or prt.state == 1 ]
    if not target_PRTs: return None
    target_customers = waiting_customers
    reassignment(event_time, target_PRTs, target_customers, Nodes)

def NN2(event_time, PRTs, waiting_customers, Nodes):
    # Target PRT: I/T
    on_notify_assignmentment_point(None)
    target_PRTs = [prt for prt in PRTs if prt.state == 0 or prt.state == 2 ]
    if not target_PRTs: return None
    target_customers = [customer for customer in waiting_customers if not customer.assigned_PRT]
    reassignment(event_time, target_PRTs, target_customers, Nodes)

def NN3(event_time, PRTs, waiting_customers, Nodes):
    # Target PRT: I/A/P
    on_notify_assignmentment_point(None)
    target_PRTs = [prt for prt in PRTs if prt.state != 2 ]
    if not target_PRTs: return None
    target_customers = waiting_customers
    reassignment(event_time, target_PRTs, target_customers, Nodes)

def NN4(event_time, PRTs, waiting_customers, Nodes):
    # Target PRT: I/A/T
    on_notify_assignmentment_point(None)
    target_PRTs = [prt for prt in PRTs if prt.state != 3 ]
    if not target_PRTs: return None
    target_customers = waiting_customers
    reassignment(event_time, target_PRTs, target_customers, Nodes)            

def NN5(event_time, PRTs, waiting_customers, Nodes):
    # Target PRT: I/A/T/P
    on_notify_assignmentment_point(None)
    target_PRTs = PRTs
    if not target_PRTs: return None
    target_customers = waiting_customers
    reassignment(event_time, target_PRTs, target_customers, Nodes)

def find_opt_matching(cur_time, target_PRTs, Customers, Nodes):
    from Dynamics import PRT_SPEED, ST_IDLE, ST_APPROACHING, ST_TRANSITING, ST_PARKING
    # Create_PRTbyCustomer_matrix
    row_size, col_size = len(target_PRTs), len(Customers)
    max_M_size = max(row_size, col_size)
    PRTbyCustomer_matrix = [[Longest_dis / PRT_SPEED] * max_M_size for _ in range(max_M_size)]
    
    for prt_id, prt in enumerate(target_PRTs):
        travel_distance = (cur_time - prt.last_planed_time) * PRT_SPEED
        for i, cus in enumerate(Customers):
            if prt.state == ST_IDLE:
                # Calculate remain distance
                remain_dis = 0
                
                # Calculate distance to location a customer is waiting
                _, path_e = find_SP(prt.arrived_n, cus.sn, Nodes)
                
            elif prt.state == ST_APPROACHING:
                # Calculate remain distance to next node
                _, next_n, xth = find_PRT_position_on_PATH(prt.path_e, travel_distance)
                remain_dis = sum([e.distance for e in prt.path_e[:xth]]) - travel_distance
                
                # Calculate distance to location a customer is waiting
                _, path_e = find_SP(next_n, cus.sn, Nodes)
                
            elif prt.state == ST_TRANSITING:
                # Calculate remain distance to destination of the boarding customer
                remain_dis = sum([e.distance for e in prt.path_e]) - travel_distance
                
                # Calculate distance to location a customer is waiting
                _, path_e = find_SP(prt.path_n[-1], cus.sn, Nodes)
                
            elif prt.state == ST_PARKING:
                # Calculate remain distance to next node
                _, next_n, xth = find_PRT_position_on_PATH(prt.path_e, travel_distance)
                assert next_n == prt.path_n[-1]
                remain_dis = sum([e.distance for e in prt.path_e[:xth]]) - travel_distance
                 
                # Calculate distance to location a customer is waiting
                _, path_e = find_SP(next_n, cus.sn, Nodes)
                
            else:
                assert False
            
            PRTbyCustomer_matrix[prt_id][i] = (sum([e.distance for e in path_e]) + remain_dis) / PRT_SPEED
    
    # Apply Hungarian method        
    hungarian_algo = Munkres()
    assignment_results = []
    for prt_id, customer_id in hungarian_algo.compute(PRTbyCustomer_matrix):
        if prt_id >= len(target_PRTs) or customer_id >= len(Customers):
            continue 
        # (prt, customer)
        assignment_results.append((prt_id, customer_id))
    return assignment_results

def find_PRT_position_on_PATH(path_e, travel_distance):
    sum_edges_distance = 0
    xth = 0
    for e in path_e:
        sum_edges_distance += e.distance
        xth += 1 
        if sum_edges_distance >= travel_distance:
            return e._from, e._to, xth
    else:
        assert False 

def find_SP(sn, en, Nodes):
    # Initialize node state for adapting Dijkstra algorithm
    for n in Nodes:
        n.init_node()
    
    # Update minimum distance
    sn.min_d = 0
    todo = [sn]
    while todo:
        n = todo.pop()
        n.visitiedCount += 1
        n.visited = True if n.visitiedCount == len(n.edges_inward) else False
                
        for e in n.edges_outward:
            consi_n = e._to
            dist = n.min_d + e.distance
            if consi_n.min_d >= dist:
                consi_n.min_d = dist
            if n.visitiedCount == 1:
                todo.append(consi_n)
        
        if en.visited:
            break
                
    # Find Path
    path_n = []
    path_e = []
    consi_n = en
    while consi_n:
        path_n.append(consi_n)
        for e in consi_n.edges_inward:
            if e._from.min_d + e.distance == consi_n.min_d:
                consi_n = e._from
                path_e.append(e)
                break 
        else:
            consi_n = None
    path_n.reverse()
    path_e.reverse()

    assert sn == path_n[0]
    assert en == path_n[-1] 
    
    return path_n, path_e

if __name__ == '__main__':
    pass
