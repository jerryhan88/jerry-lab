from __future__ import division
from igraph import Graph
import dlib
from itertools import izip
from random import choice

check_path = lambda x: None

on_notify_assignmentment_point = lambda x: None

priority_rate_earlyArrival = 0.0001

# For using Hungarian method, give long distance(cost) to augmented cell
Longest_dis = 100000000

def init_algorithms(_Nodes):
    global network, Nodes
    Nodes = _Nodes
    E, W = [], []
    for i, n in enumerate(Nodes):
        for e in n.edges_outward:
            E.append((e._from.no, e._to.no))
            W.append(e.distance / e.maxSpeed)
    network = Graph(len(Nodes), E, True, edge_attrs={'weight': W})

def on_notify_assignmentment_point(args=None):
    print '-----------------------------------------------------------------------(Re)assignment!!' 

def get_all_dispatchers():
    return {'FCFS': FCFS, 'NNBA-I': NNBA_I, 'NNBA-IA': NNBA_IA, 'NNBA-IT': NNBA_IT, 'NNBA-IAP': NNBA_IAP, 'NNBA-IAT': NNBA_IAT, 'NNBA-IATP': NNBA_IATP}

def reassignment(event_time, target_PRTs, target_customers, Nodes):
    _target_customers = target_customers[:]
    assignmet_result, PRTbyCustomer_matrix = find_opt_matching(event_time, target_PRTs, _target_customers, Nodes)
    
    # node --> {(distance, prt)}
    NDP = {}
    for pi, ci in assignmet_result:
        NDP.setdefault(_target_customers[ci].sn, []).append((-PRTbyCustomer_matrix[pi][ci], target_PRTs[pi]))
    for DP in NDP.itervalues():
        DP.sort()
    # node --> {(arrival time, customer)}
    NAC = {}
    for c in _target_customers:
        NAC.setdefault(c.sn, []).append((c.arriving_time, c))
    for AC in NAC.itervalues():
        AC.sort()
    # revised assignment
    assert len(NDP) <= len(NAC)
    RA = []
    for n, DP in NDP.iteritems():
        AC = NAC[n]
        assert len(DP) <= len(AC)
        RA.extend((p, c) for ((_, p), (_, c)) in izip(DP, AC))
    
    for chosen_prt, target_c in RA:
        chosen_prt.re_assign_customer(event_time, target_c)

def FOFS(event_time, PRTs, waiting_customers, Nodes):
    from Dynamics import ST_IDLE, PRT_SPEED
    on_notify_assignmentment_point(None)
    candi_customers = [customer for customer in waiting_customers if not customer.assigned_PRT and not customer.isSetupWaiting]
    if candi_customers:
        target_c = None
        
def find_nearestPRT(PRTs):
    from Dynamics import ST_IDLE, PRT_SPEED
    PRT_C_EAT = []
    # Estimated Arrival Time
    for prt in PRTs:
        if prt.state != ST_IDLE or prt.isSetupWaiting:
            continue
        else:
            _, path_e = find_SP(prt.arrived_n.no, target_c.sn.no)
            empty_travel_time = sum(e.distance / min(PRT_SPEED, e.maxSpeed) for e in path_e)
            PRT_C_EAT.append((prt, empty_travel_time))
    if PRT_C_EAT:  
        target_PRT = sorted(PRT_C_EAT, key=lambda PRT_C_EAT: PRT_C_EAT[1])[0][0]
        target_PRT.re_assign_customer(event_time, target_c)

def FCFS(event_time, PRTs, waiting_customers, Nodes):
    on_notify_assignmentment_point(None)
    candi_customers = [customer for customer in waiting_customers if not customer.assigned_PRT and not customer.isSetupWaiting]
    if len(candi_customers) == 1:
        # customer init. dispatching
        target_c = candi_customers[0]
        target_PRT = find_nearestPRT()
        
    elif len(candi_customers) > 1:
        # PRT init. dispatching
        target_c = candi_customers[0]
        
    else:
        assert len(candi_customers) == 0 
        # no reassignment
    if candi_customers:
        target_c = candi_customers[0]
        PRT_C_EAT = []
        # Estimated Arrival Time
        for prt in PRTs:
            if prt.state != ST_IDLE or prt.isSetupWaiting:
                continue
            else:
                _, path_e = find_SP(prt.arrived_n.no, target_c.sn.no)
                empty_travel_time = sum(e.distance / min(PRT_SPEED, e.maxSpeed) for e in path_e)
                PRT_C_EAT.append((prt, empty_travel_time))
        if PRT_C_EAT:  
            target_PRT = sorted(PRT_C_EAT, key=lambda PRT_C_EAT: PRT_C_EAT[1])[0][0]
            target_PRT.re_assign_customer(event_time, target_c) 
    
def NNBA_I(event_time, PRTs, waiting_customers, Nodes):
    from Dynamics import ST_IDLE
    # Target PRT: I
    on_notify_assignmentment_point(None)
    target_PRTs = [prt for prt in PRTs if not prt.isSetupWaiting and prt.state == ST_IDLE]
    if not target_PRTs: return None
    target_customers = [customer for customer in waiting_customers if not customer.assigned_PRT and not customer.isSetupWaiting]
    reassignment(event_time, target_PRTs, target_customers, Nodes)

def NNBA_IA(event_time, PRTs, waiting_customers, Nodes):
    from Dynamics import ST_IDLE, ST_APPROACHING
    # Target PRT: I/A
    on_notify_assignmentment_point(None)
    target_PRTs = [prt for prt in PRTs if not prt.isSetupWaiting and (prt.state == ST_IDLE or prt.state == ST_APPROACHING)]
    if not target_PRTs: return None
    target_customers = [c for c in waiting_customers if not c.isSetupWaiting]
    reassignment(event_time, target_PRTs, target_customers, Nodes)

def NNBA_IT(event_time, PRTs, waiting_customers, Nodes):
    from Dynamics import ST_IDLE, ST_TRANSITING
    # Target PRT: I/T
    on_notify_assignmentment_point(None)
    target_PRTs = [prt for prt in PRTs if prt.state == ST_IDLE or prt.state == ST_TRANSITING ]
    if not target_PRTs: return None
    target_customers = [customer for customer in waiting_customers if not customer.assigned_PRT and not customer.isSetupWaiting]
    reassignment(event_time, target_PRTs, target_customers, Nodes)

def NNBA_IAP(event_time, PRTs, waiting_customers, Nodes):
    from Dynamics import ST_IDLE, ST_APPROACHING, ST_PARKING
    # Target PRT: I/A/P
    on_notify_assignmentment_point(None)
    target_PRTs = [prt for prt in PRTs if not prt.isSetupWaiting and (prt.state == ST_IDLE or prt.state == ST_APPROACHING or prt.state == ST_PARKING)]
    if not target_PRTs: return None
    target_customers = [c for c in waiting_customers if not c.isSetupWaiting]
    reassignment(event_time, target_PRTs, target_customers, Nodes)

def NNBA_IAT(event_time, PRTs, waiting_customers, Nodes):
    from Dynamics import ST_IDLE, ST_APPROACHING, ST_TRANSITING
    # Target PRT: I/A/T
    on_notify_assignmentment_point(None)
    target_PRTs = [prt for prt in PRTs if not prt.isSetupWaiting and (prt.state == ST_IDLE or prt.state == ST_APPROACHING or prt.state == ST_TRANSITING)]
    if not target_PRTs: return None
    target_customers = [c for c in waiting_customers if not c.isSetupWaiting]
    reassignment(event_time, target_PRTs, target_customers, Nodes)            

def NNBA_IATP(event_time, PRTs, waiting_customers, Nodes):
    from Dynamics import ST_IDLE, ST_APPROACHING, ST_TRANSITING, ST_PARKING
    # Target PRT: I/A/T/P
    on_notify_assignmentment_point(None)
    target_PRTs = [prt for prt in PRTs if not prt.isSetupWaiting and (prt.state == ST_IDLE or prt.state == ST_APPROACHING or prt.state == ST_TRANSITING or prt.state == ST_PARKING)]
    if not target_PRTs: return None
    target_customers = [c for c in waiting_customers if not c.isSetupWaiting]
    reassignment(event_time, target_PRTs, target_customers, Nodes)

def find_opt_matching(cur_time, target_PRTs, target_customers, Nodes):
    from Dynamics import ST_IDLE, ST_APPROACHING, ST_TRANSITING, ST_PARKING, PRT_SPEED
    
    # Create_PRTbyCustomer_matrix
    row_size, col_size = len(target_PRTs), len(target_customers)
    max_M_size = max(row_size, col_size)
    PRTbyCustomer_matrix = [[-Longest_dis / PRT_SPEED] * max_M_size for _ in range(max_M_size)]
    
    for prt_id, prt in enumerate(target_PRTs):
        path_travel_time = cur_time - prt.last_planed_time
        for i, cus in enumerate(target_customers):
            if prt.state == ST_IDLE:
                # Calculate remain distance
                remain_travel_time = 0
                # Calculate distance to location a customer is waiting
                _, path_e = find_SP(prt.arrived_n.no, cus.sn.no)
                
            elif prt.state == ST_APPROACHING:
                # Calculate remain distance to next node
                _, next_n, xth = find_PRT_position_on_PATH(prt.path_e, path_travel_time)
                remain_travel_time = sum(e.distance / min(PRT_SPEED, e.maxSpeed) for e in prt.path_e[:xth]) - path_travel_time
                # Calculate distance to location a customer is waiting
                _, path_e = find_SP(next_n.no, cus.sn.no)
                
            elif prt.state == ST_TRANSITING:
                # Calculate remain distance to destination of the boarding customer
                remain_travel_time = sum(e.distance / min(PRT_SPEED, e.maxSpeed) for e in prt.path_e) - path_travel_time
                # Calculate distance to location a customer is waiting
                _, path_e = find_SP(prt.path_n[-1].no, cus.sn.no)
                
            elif prt.state == ST_PARKING:
                # Calculate remain distance to next node
                _, next_n, xth = find_PRT_position_on_PATH(prt.path_e, path_travel_time)
#                 assert next_n == prt.path_n[-1]
                remain_travel_time = sum(e.distance / min(PRT_SPEED, e.maxSpeed) for e in prt.path_e[:xth]) - path_travel_time
                 
                # Calculate distance to location a customer is waiting
                _, path_e = find_SP(next_n.no, cus.sn.no)
            else:
                assert False
            _, determinded_path_e = find_SP(cus.sn.no, cus.dn.no)
            processing_time = sum(e.distance / min(PRT_SPEED, e.maxSpeed) for e in determinded_path_e)
            PRTbyCustomer_matrix[prt_id][i] = -(processing_time + sum(e.distance / min(PRT_SPEED, e.maxSpeed) for e in path_e) + remain_travel_time)
    
    # Apply Hungarian method        
    assignment_results = []
    cost = dlib.matrix(PRTbyCustomer_matrix)
    for prt_id, customer_id in enumerate(dlib.max_cost_assignment(cost)):
        if prt_id >= len(target_PRTs) or customer_id >= len(target_customers):
            continue 
        # (prt, customer)
        assert target_PRTs[prt_id] and target_customers[customer_id]
        assignment_results.append((prt_id, customer_id))
    
    return assignment_results, PRTbyCustomer_matrix

def find_PRT_position_on_PATH(path_e, path_travel_time):
    from Dynamics import PRT_SPEED
    sum_travel_time = 0
    xth = 0
    for e in path_e:
        sum_travel_time += e.distance / min(PRT_SPEED, e.maxSpeed) 
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
            tentative_minTime = n.minTime + e.distance / e.maxSpeed
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
            if e._from.minTime + e.distance / e.maxSpeed == consi_n.minTime:
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

def find_SP(sn, dn):
    path_n, path_e = [], []
    
    if sn == dn:
        path_n.append(Nodes[sn])
    else:
        path = network.get_shortest_paths(sn, dn, 'weight')[0]
        
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
    assert sn == path_n[0].no
    assert dn == path_n[-1].no
    
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
