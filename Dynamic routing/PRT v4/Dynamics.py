from __future__ import division
from math import sqrt
from Algorithms import NN
from heapq import heappush, heappop
import wx
class Node():
    _id = 0
    MAXD = 10000
    def __init__(self, px, py):
        self.id = Node._id
        self.px, self.py = None, None
        
        self.edges_inward = []
        self.edges_outward = []
        
        self.set_position(px, py)
        self.visited = False
        self.min_d = None
        
        self.cus_queue = []

        Node._id += 1
        
    def init_node(self):
        self.visited = False
        self.min_d = Node.MAXD
    
    def __repr__(self):
        return 'N%d' % self.id
    
    def set_position(self, px, py):
        self.px, self.py = px, py
        
class Edge():
    _id = 0
    def __init__(self, _from, _to):
        self.id = Edge._id
        Edge._id += 1
        self._from, self._to = _from, _to
        delX = self._from.px - self._to.px
        delY = self._from.py - self._to.py
        self.distance = sqrt(delX * delX + delY * delY)
        
        self._from.edges_outward.append(self)
        self._to.edges_inward.append(self)
        
    def __repr__(self):
        return 'Edge %d, N%d -> N%d' % (self.id, self._from.id, self._to.id)
          
class Customer():
    def __init__(self, re_time, _id, sn, dn):
        self.re_time, self.id, self.sn, self.dn = re_time, _id, sn, dn

#         self.marked = False
    
    def __repr__(self):
        return '%s N%d->N%d' % (self.id, self.sn.id, self.dn.id)
        
class PRT():
    _id = 0
    PRT_SPEED = 5
    def __init__(self):
        self.id = PRT._id
        PRT._id += 1
        self.px, self.py = None, None
        self.path_n = []
        self.path_e = []
        self.assigned_customer = None
        self.arrived_n = None
        self.next_n = None
        self.dest_n = None
        # PRT state
        #  S0: Idle, S1: Approaching, S2: Transiting, S3: Parking
        self.state = 0   
        
        
        #------------------------------
#         self.target_n = None
#         
#         self.riding_cus = None
#         
#         self.ETA = 1e400
#         self.sin_theta = 0.0
#         self.cos_theta = 0.0
        
    def __repr__(self):
        return 'PRT%d' % self.id
    
    def set_assi_cus(self, customer):
        self.assigned_customer = customer
         
    def set_position(self, px, py):
        self.px, self.py = px, py
        
    def init_position(self, n):
        self.arrived_n = n
        self.set_position(n.px, n.py)

def gen_customers(Nodes):
    event_queue = []
    with open('Input', 'r') as fp:
        for line in fp:
            c, t_s, sd = line.split(',')
            t = round(float(t_s), 1)
            sn, dn = sd.split('-')
#             print t, c, sn, dn
            heappush(event_queue, (t, Customer(t, c, Nodes[int(sn)], Nodes[int(dn)])))
    return event_queue

def select_scopesOfPRT(level, PRTs):
    considered_PRT = []
    for prt in PRTs:
        if level == 0:
            if prt.state != 0 : continue
        elif level == 1:
            if prt.state == 2 : continue
        else:
            assert level == 2
        considered_PRT.append(prt)
    return considered_PRT

def next_event(event_queue):
    while event_queue:
        yield heappop(event_queue)


def PRT_scenario1():
    PRTs = []
    
    for init_n in (4, 0, 3):
        prt = PRT()
        prt.init_position(Nodes[init_n])
        PRTs.append(prt)
    
    return PRTs

if __name__ == '__main__':
    import input_gen
    Nodes, Edges = input_gen.network1()
    nn = NN(Nodes)
    event_queue = gen_customers(Nodes)
    PRTs = PRT_scenario1()
    
    cus_interception_allowed = False
    scopeOfPRT = 0
    update_op = 0
    
    waiting_customers = []
    for t, Class in next_event(event_queue):
        if isinstance(Class, Customer):
            print t, Class
            if update_op == 0:
                waiting_customers.append(Class)
                assignable_PRTs = select_scopesOfPRT(scopeOfPRT, PRTs)
                if not assignable_PRTs:
                    continue
                M = nn.create_PRTbyCustomer_matrix(assignable_PRTs, waiting_customers, Nodes)
                assignment_results = nn.find_opt_matching(PRTs, waiting_customers, M)
                if not cus_interception_allowed:
                    for prt_id, customer_id in assignment_results:
                        assignable_PRTs[prt_id].set_assi_cus(waiting_customers[customer_id])
                        assert assignable_PRTs[prt_id].state == 0
                        assignable_PRTs[prt_id].state = 1
                        heappush(event_queue, (t, assignable_PRTs[prt_id]))
                        waiting_customers[customer_id] = None
                    waiting_customers = [c for c in waiting_customers if c != None]
        else:
            assert isinstance(Class, PRT)
            print t, ' prt', Class, Class.state
    
# while self.ordered_output:
#     yield heappop(self.ordered_output)