from __future__ import division
from math import sqrt
from munkres import Munkres
from igraph import Graph
import dlib

check_path = lambda x: None

on_notify_assignmentment_point = lambda x: None

# For using Hungarian method, give long distance(cost) to augmented cell
Longest_dis = 100000000

def on_notify_assignmentment_point(args=None):
    print '-----------------------------------------------------------------------(Re)assignment!!' 

def get_all_dispatchers():
    return {'NN0': NN0, 'NN1': NN1, 'NN2': NN2, 'NN3': NN3, 'NN4': NN4, 'NN5': NN5}

def reassignment(event_time, target_PRTs, target_customers, Nodes):
    _target_customers = target_customers[:]
    for prt_id, customer_id in find_opt_matching(event_time, target_PRTs, _target_customers, Nodes):
        chosen_prt = target_PRTs[prt_id]
        target_c = _target_customers[customer_id]
        chosen_prt.re_assign_customer(event_time, target_c)

def NN0(event_time, PRTs, waiting_customers, Nodes):
    from Dynamics import ST_IDLE
    # Target PRT: I
    on_notify_assignmentment_point(None)
    target_PRTs = [prt for prt in PRTs if prt.state == ST_IDLE]
    if not target_PRTs: return None
    target_customers = [customer for customer in waiting_customers if not customer.assigned_PRT]
    reassignment(event_time, target_PRTs, target_customers, Nodes)

def NN1(event_time, PRTs, waiting_customers, Nodes):
    from Dynamics import ST_IDLE, ST_APPROACHING
    # Target PRT: I/A
    on_notify_assignmentment_point(None)
    target_PRTs = [prt for prt in PRTs if prt.state == ST_IDLE or prt.state == ST_APPROACHING ]
    if not target_PRTs: return None
    target_customers = waiting_customers
    reassignment(event_time, target_PRTs, target_customers, Nodes)

def NN2(event_time, PRTs, waiting_customers, Nodes):
    from Dynamics import ST_IDLE, ST_TRANSITING
    # Target PRT: I/T
    on_notify_assignmentment_point(None)
    target_PRTs = [prt for prt in PRTs if prt.state == ST_IDLE or prt.state == ST_TRANSITING ]
    if not target_PRTs: return None
    target_customers = [customer for customer in waiting_customers if not customer.assigned_PRT]
    reassignment(event_time, target_PRTs, target_customers, Nodes)

def NN3(event_time, PRTs, waiting_customers, Nodes):
    from Dynamics import ST_IDLE, ST_APPROACHING, ST_PARKING
    # Target PRT: I/A/P
    on_notify_assignmentment_point(None)
    target_PRTs = [prt for prt in PRTs if prt.state == ST_IDLE or prt.state == ST_APPROACHING or prt.state == ST_PARKING]
    if not target_PRTs: return None
    target_customers = waiting_customers
    reassignment(event_time, target_PRTs, target_customers, Nodes)

def NN4(event_time, PRTs, waiting_customers, Nodes):
    from Dynamics import ST_IDLE, ST_APPROACHING, ST_TRANSITING
    # Target PRT: I/A/T
    on_notify_assignmentment_point(None)
    target_PRTs = [prt for prt in PRTs if prt.state == ST_IDLE or prt.state == ST_APPROACHING or prt.state == ST_TRANSITING]
    if not target_PRTs: return None
    target_customers = waiting_customers
    reassignment(event_time, target_PRTs, target_customers, Nodes)            

def NN5(event_time, PRTs, waiting_customers, Nodes):
    from Dynamics import ST_IDLE, ST_APPROACHING, ST_TRANSITING, ST_PARKING
    # Target PRT: I/A/T/P
    on_notify_assignmentment_point(None)
    target_PRTs = [prt for prt in PRTs if prt.state == ST_IDLE or prt.state == ST_APPROACHING or prt.state == ST_TRANSITING or prt.state == ST_PARKING]
    if not target_PRTs: return None
    target_customers = waiting_customers
    reassignment(event_time, target_PRTs, target_customers, Nodes)

def find_opt_matching(cur_time, target_PRTs, target_customers, Nodes):
    from Dynamics import PRT_SPEED, ST_IDLE, ST_APPROACHING, ST_TRANSITING, ST_PARKING
    # Create_PRTbyCustomer_matrix
    row_size, col_size = len(target_PRTs), len(target_customers)
    max_M_size = max(row_size, col_size)
    PRTbyCustomer_matrix = [[-Longest_dis / PRT_SPEED] * max_M_size for _ in range(max_M_size)]
    
    for prt_id, prt in enumerate(target_PRTs):
        travel_distance = (cur_time - prt.last_planed_time) * PRT_SPEED
        path_travel_time = cur_time - prt.last_planed_time
        for i, cus in enumerate(target_customers):
            if prt.state == ST_IDLE:
                # Calculate remain distance
                remain_travel_time = 0
                # Calculate distance to location a customer is waiting
                _, path_e = find_SP(prt.arrived_n, cus.sn, Nodes)
                
            elif prt.state == ST_APPROACHING:
                # Calculate remain distance to next node
                _, next_n, xth = find_PRT_position_on_PATH(prt.path_e, path_travel_time)
                remain_travel_time = sum(e.distance // min(PRT_SPEED, e.maxSpeed) for e in prt.path_e[:xth]) - path_travel_time
                # Calculate distance to location a customer is waiting
                _, path_e = find_SP(next_n, cus.sn, Nodes)
                
            elif prt.state == ST_TRANSITING:
                # Calculate remain distance to destination of the boarding customer
                remain_travel_time = sum(e.distance // min(PRT_SPEED, e.maxSpeed) for e in prt.path_e) - path_travel_time
                # Calculate distance to location a customer is waiting
                _, path_e = find_SP(prt.path_n[-1], cus.sn, Nodes)
                
            elif prt.state == ST_PARKING:
                # Calculate remain distance to next node
                _, next_n, xth = find_PRT_position_on_PATH(prt.path_e, path_travel_time)
#                 assert next_n == prt.path_n[-1]
                remain_travel_time = sum(e.distance // min(PRT_SPEED, e.maxSpeed) for e in prt.path_e[:xth]) - path_travel_time
                 
                # Calculate distance to location a customer is waiting
                _, path_e = find_SP(next_n, cus.sn, Nodes)
            else:
                assert False
            
            PRTbyCustomer_matrix[prt_id][i] = -sum(e.distance // min(PRT_SPEED, e.maxSpeed) for e in path_e) + remain_travel_time
    
    # Apply Hungarian method        
    assignment_results = []
    cost = dlib.matrix(PRTbyCustomer_matrix)
    for prt_id, customer_id in enumerate(dlib.max_cost_assignment(cost)):
        if prt_id >= len(target_PRTs) or customer_id >= len(target_customers):
            continue 
        # (prt, customer)
        assert target_PRTs[prt_id] and target_customers[customer_id]
        assignment_results.append((prt_id, customer_id))
    
    return assignment_results

def find_PRT_position_on_PATH(path_e, path_travel_time):
    from Dynamics import PRT_SPEED
    sum_travel_time = 0
    xth = 0
    for e in path_e:
        sum_travel_time += e.distance // min(PRT_SPEED, e.maxSpeed) 
        xth += 1 
        if sum_travel_time >= path_travel_time:
            return e._from, e._to, xth
    else:
        assert False 

def find_SP0(sn, en, Nodes):
    # Initialize node state for adapting Dijkstra algorithm
    for n in Nodes:
        n.init_node()
    
    # Update minimum distance
    sn.minTime = 0
    sn.visited = True
    todo = [sn]
    while todo:
        n = todo.pop()
        if not n.visited:
            for e in n.edges_inward:
                if not e._from.visited:
                    break
            else:
                n.visited = True
        for e in n.edges_outward:
            consi_n = e._to
            tentative_minTime = n.minTime + e.distance // e.maxSpeed
            if consi_n.minTime >= tentative_minTime:
                consi_n.minTime = tentative_minTime
                if not consi_n.visited and consi_n not in todo:
                    todo.append(consi_n)
                
    # Find Path
    path_n = []
    path_e = []
    consi_n = en
    while consi_n:
        path_n.append(consi_n)
        for e in consi_n.edges_inward:
            if e._from.minTime + e.distance // e.maxSpeed == consi_n.minTime:
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

def find_SP(sn, dn, Nodes):
    path_n = []
    path_e = []
    
    if sn == dn:
        path_n.append(sn)
    else:
        E = []
        W = []
        for n in Nodes:
            for e in n.edges_outward:
                E.append((Nodes.index(e._from), Nodes.index(e._to)))
                W.append(e.distance // e.maxSpeed)
        g = Graph(len(Nodes), E, True, edge_attrs={'weight': W})
        path = g.get_shortest_paths(Nodes.index(sn), Nodes.index(dn), 'weight')[0]
        
        for i, n_index in enumerate(path):
            n = Nodes[n_index]
            path_n.append(n)
            if i != 0 :
                for e in n.edges_inward:
                    if e._from == Nodes[path[i - 1]]:
                        path_e.append(e)
                        break
                else:
                    assert False
    assert sn == path_n[0]
    assert dn == path_n[-1] 
    
    return path_n, path_e

def test_path_find():
    import Dynamics
    from Dynamics import Network1, findNode
    Nodes, Edges = Network1()
    Dynamics.Nodes = Nodes
    path_n, path_e = find_SP0(findNode('5'), findNode('10'), Nodes)
    print path_n, path_e
    path_n, path_e = find_SP(findNode('5'), findNode('10'), Nodes)
    print path_n, path_e
    
def test_assignment():
    import dlib
    cost = dlib.matrix([[1, 2, 6],
                        [5, 3, 6],
                        [4, 5, 0]])
    assignment = dlib.max_cost_assignment(cost)
    print "optimal assignments: ", assignment
    return None
if __name__ == '__main__':
#     test_path_find()
    test_assignment() 
