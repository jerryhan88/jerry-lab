from __future__ import division
from math import sqrt
from munkres import Munkres, print_matrix

class NN:
    Longest_dis = 0
    def __init__(self, reassignment_momonet, scopeOfPRT, nodes):
        self.reassignment_momonet, self.scopeOfPRT = reassignment_momonet, scopeOfPRT
        self.nodes = nodes
        self.NodeByNode_DMatrix = self.create_NodeByNode_DMatrix()
        self.hungarian_algo = Munkres()
    
    def create_NodeByNode_DMatrix(self):
        NodeByNode_DMatrix = []
        for i in self.nodes:
            from_i = []
            for j in self.nodes:
                _ , path_e = self.find_SP(i, j)
                distance = sum([e.distance for e in path_e])
                from_i.append(distance)
                # find longest_distance in network
                if NN.Longest_dis < distance: NN.Longest_dis = distance   
            NodeByNode_DMatrix.append(from_i)
        return NodeByNode_DMatrix
    
    def create_PRTbyCustomer_matrix(self, PRTs, customers):
        row_size, col_size = len(PRTs), len(customers)
        max_M_size = max(row_size, col_size)
        
        PRTbyCustomer_matrix = [[NN.Longest_dis] * max_M_size for _ in range(max_M_size)]
        
        for prt_id, prt in enumerate(PRTs):
            for i, cus in enumerate(customers):
                if prt.state == 0:
                    PRTbyCustomer_matrix[prt_id][i] = self.NodeByNode_DMatrix[prt.arrived_n.id][cus.sn.id]
                elif prt.state == 1 or prt.state == 3:
                    dx = prt.next_n.px - prt.px  
                    dy = prt.next_n.py - prt.py
                    remain_dis = sqrt(dx * dx + dy * dy) 
                    PRTbyCustomer_matrix[prt_id][i] = self.NodeByNode_DMatrix[prt.next_n.id][cus.sn.id] + remain_dis 
                else:
                    assert prt.state == 2
                    dx = prt.arrived_n.px - prt.px  
                    dy = prt.arrived_n.py - prt.py
                    distance = sum([e.distance for e in prt.path_e]) - sqrt(dx * dx + dy * dy) 
                    PRTbyCustomer_matrix[prt_id][i] = self.NodeByNode_DMatrix[prt.dest_n.id][cus.sn.id] + distance
        
        return PRTbyCustomer_matrix
    
    def find_opt_matching(self, customers, PRTs, M):
        assignment_results = []
        for prt_id, customer_id in self.hungarian_algo.compute(M):
            if prt_id >= len(PRTs) or customer_id >= len(customers):
                continue 
            # (prt, customer)
            assignment_results.append((prt_id, customer_id))
        return assignment_results
    
    def find_SP(self, sn, en):
        for n in self.nodes:
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
                if not consi_n.visited and not [x for x in todo if consi_n.id == x.id]:
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

    def call_reassignment(self, waiting_customers, PRTs, cur_time, event_queue):
        target_PRTs = select_scopesOfPRT(scopeOfPRT, PRTs)
        if not target_PRTs:
            assert not waiting_customers
            return None
        assignment_results = self.find_opt_matching(waiting_customers, target_PRTs, M)
        
        for prt_id, customer_id in assignment_results:
            a_waiting_cus = waiting_customers[customer_id]
            a_prt = target_PRTs[prt_id]
            if a_prt.state == 0:
                event_et = cur_time
                if self.arrived_n != a_customer.sn:
                    # Idle -> Approaching
                    heappush(event_queue, (event_et, a_prt.IdleToApproaching(a_waiting_cus)))
                else:
                    assert self.arrived_n == a_customer.sn
                    # Idle -> Transiting
                    heappush(event_queue, (event_et, a_prt.IdleToTransiting(a_waiting_cus)))
            elif a_prt.state == 1:
                pass
            elif a_prt.state == 2:
                pass
            elif a_prt.state == 3:
                pass
                
            waiting_customers[customer_id] = None
        waiting_customers = [c for c in waiting_customers if c != None]
    
    def select_scopesOfPRT(self, PRTs):
        target_PRTs = []
        for prt in PRTs:
            if self.scopeOfPRT == 0:
                if prt.state != 0 : continue
            elif self.scopeOfPRT == 1:
                if prt.state == 2 : continue
            else:
                assert self.scopeOfPRT == 2
            target_PRTs.append(prt)
        return target_PRTs

def metrix_display(M):
    for r in M:
        for v in r:
            print '%.1f    ' % v,
        print

def scenario0():
    customers = []
    PRTs = []
    
    customers.append(Customer(10, 'C0', Nodes[2], Nodes[4]))
    customers.append(Customer(11, 'C1', Nodes[5], Nodes[7]))
    
    prt0 = PRT()
    prt0.init_position(Nodes[4])
    PRTs.append(prt0)
    
    prt1 = PRT()
    prt1.init_position(Nodes[0])
    PRTs.append(prt1)
    
    return PRTs, customers

def scenario1():
    customers = []
    PRTs = []
    
    customers.append(Customer(10, 'C0', Nodes[2], Nodes[4]))
    customers.append(Customer(11, 'C1', Nodes[5], Nodes[7]))
    
    for init_n in (4, 0, 3):
        prt = PRT()
        prt.init_position(Nodes[init_n])
        PRTs.append(prt)
    
    return PRTs, customers

def scenario2():
    # there is an transiting PRT
    customers = []
    PRTs = []
    
    customers.append(Customer(10, 'C0', Nodes[2], Nodes[4]))
    customers.append(Customer(11, 'C1', Nodes[5], Nodes[7]))
    
    for init_n in (4, 0, 3):
        prt = PRT()
        prt.init_position(Nodes[init_n])
        PRTs.append(prt)
    
    transiting_prt = PRTs[-1]
    transiting_prt.state = 2
    transiting_prt.next_n = Nodes[4]
    transiting_prt.dest_n = Nodes[8]
    
    return PRTs, customers

def scenario3():
    # there is an transiting PRT
    # there is an parking PRT
    customers = []
    PRTs = []
    
    customers.append(Customer(10, 'C0', Nodes[2], Nodes[4]))
    customers.append(Customer(11, 'C1', Nodes[5], Nodes[7]))
    customers.append(Customer(12, 'C2', Nodes[5], Nodes[8]))
    customers.append(Customer(12, 'C3', Nodes[2], Nodes[6]))
    
    for init_n in (4, 0, 3, 5):
        prt = PRT()
        prt.init_position(Nodes[init_n])
        PRTs.append(prt)
    
    transiting_prt = PRTs[-2]
    transiting_prt.state = 2
    transiting_prt.next_n = Nodes[4]
    transiting_prt.dest_n = Nodes[8]
    
    parking_prt = PRTs[-1]
    parking_prt.state = 3
    parking_prt.next_n = Nodes[6]
    parking_prt.px = (parking_prt.next_n.px + parking_prt.arrived_n.px) / 2
      
    parking_prt.py = (parking_prt.next_n.py + parking_prt.arrived_n.py) / 2 
    
    return PRTs, customers
    
if __name__ == '__main__':
    import input_gen
    from dynamics import PRT, Customer
    
    Nodes, Edges = input_gen.network1()
    nn = NN(Nodes)
#     PRTs, customers = scenario0()
#     PRTs, customers = scenario1()
#     PRTs, customers = scenario2()
    PRTs, customers = scenario3()
    
    pc_M = nn.create_PRTbyCustomer_matrix(PRTs, customers, Nodes)
    metrix_display(pc_M)
    assignment_results = nn.find_opt_matching(PRTs, customers, pc_M)
        
    for prt_id, customer_id in assignment_results:
        print '%s: assigned customer is (%s)' % (PRTs[prt_id], customers[customer_id])
#     for prt in PRTs:
#         print 'PRT%d: assigned customer is (%s)' % (prt.id, prt.assigned_customer)  
