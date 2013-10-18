from __future__ import division
from math import sqrt
from Algorithms import NN
from heapq import heappush, heappop

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
        self.transporting_customer = None
        
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
         
    def set_position(self, px, py):
        self.px, self.py = px, py
        
    def init_position(self, n):
        self.arrived_n = n
        self.set_position(n.px, n.py)
        
    def update_state(self, a_customer, time, event_queue):
        # state change
        # a time point is cur_state -> next_state
        # namely, the time is end of cur_state
        if self.state == 0:
            if self.arrived_n != a_customer.sn:
                # Idle -> Approaching
                self.state = 1
            else:
                assert self.arrived_n == a_customer.sn
                # Idle -> Transiting
                self.state = 2
        elif self.state == 1:
            if self.assigned_customer:
                # Approaching -> Transiting
                assert self.assigned_customer == a_customer
                self.state = 2
            else:
                # Approaching -> Parking
                assert not self.assigned_customer
                self.state = 3
        elif self.state == 2:
            if not self.assigned_customer:
                # Transiting -> Idle
                self.state = 0
            else:
                if self.arrived_n == a_customer.sn:
                    # Transiting -> Transiting
                    self.state = 2
                else:
                    assert self.arrived_n != a_customer.sn
                    # Transiting -> Approaching
                    self.state = 1
        else:
            assert self.state == 3
            ###  Check this part again!!!
            
            if self.assigned_customer:
                # Parking -> Approaching 
                self.state = 2
            else:
                # Parking -> Idle
                self.state = 1
    
    def IdleToApproaching(self, a_customer):
        self.assigned_customer = a_customer
        self.state = 1
    
    def IdleToTransiting(self, a_customer):
        self.transporting_customer = a_customer
        self.state = 2

def gen_customers(Nodes):
    event_queue = []
    with open('Input', 'r') as fp:
        for line in fp:
            c_id, t_s, sd = line.split(',')
            t = round(float(t_s), 1)
            sn, dn = sd.split('-')
            heappush(event_queue, (t, Customer(t, c_id, Nodes[int(sn)], Nodes[int(dn)])))
    return event_queue

def PRT_scenario1():
    PRTs = []
    for init_n in (4, 0, 3):
        prt = PRT()
        prt.init_position(Nodes[init_n])
        PRTs.append(prt)
    
    return PRTs

def run(PRTs, Nodes):
    reassignment_momonet = 0
    scopeOfPRT = 0
    assignment_changeable = False
    
    nn = NN(reassignment_momonet, scopeOfPRT, Nodes)
    event_queue = gen_customers(Nodes)
    
    waiting_customers = []
    
    while event_queue:
        t, event = heappop(event_queue)
        print t, event
        if isinstance(event, Customer):
            a_customer = event
            waiting_customers.append(a_customer)
            nn.call_reassignment(waiting_customers, PRTs, t, event_queue)
        else:
            # prt's events
            pass
if __name__ == '__main__':
    import input_gen
    Nodes, Edges = input_gen.network1()
    PRTs = PRT_scenario1()
    run(PRTs, Nodes)
