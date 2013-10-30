from __future__ import division
from math import sqrt
from random import randrange, seed
from numpy.random import poisson
from heapq import heappush, heappop
import Algorithms

#---------------------------------------------------------------------
# Classes

class Node():
    _id = 0
    BIG_NUM = 1000000
    def __init__(self, px, py, isStation):
        self.id = Node._id
        self.isStation = isStation
        Node._id += 1
        self.px, self.py = px, py
        
        self.edges_inward = []
        self.edges_outward = []
        
    def init_node(self):
        self.visited = False
        self.visitiedCount = 0
        self.min_d = Node.BIG_NUM
    
    def __repr__(self):
        return 'N%d(%s)' % (self.id, 'O' if self.isStation else 'X')
    
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
        return 'N%d->N%d' % (self._from.id, self._to.id)

class Customer():
    _id = 0
    def __init__(self, arriving_time, sn, dn):
        self.id = Customer._id
        Customer._id += 1
        self.arriving_time = arriving_time
        self.sn, self.dn = sn, dn
        
        self.assigned_PRT = None
    
    def __repr__(self):
        return '(C%d) N%d->N%d' % (self.id, self.sn.id, self.dn.id)

ST_IDLE, ST_APPROACHING, ST_TRANSITING, ST_PARKING = 0, 1, 2, 3

class PRT():
    _id = 0
    def __init__(self, init_node):
        self.id = PRT._id
        PRT._id += 1
        self.arrived_n = init_node
        self.px, self.py = self.arrived_n.px, self.arrived_n.py
        
        self.state = ST_IDLE
        self.assigned_customer = None
        self.transporting_customer = None
        self.event_seq = []
        
        self.last_planed_time = 0
        self.path_n, self.path_e = [], []
    
    def __repr__(self):
        return 'PRT%d-Now N%d' % (self.id, self.arrived_n.id)
    
    def re_assign_customer(self, cur_time, target_c):
        if self.state == ST_IDLE :
            if self.arrived_n != target_c.sn:
                # Idle -> Approaching
                self.On_IdleToApproaching(cur_time, target_c)
                self.event_seq.append(self.On_IdleToApproaching)
    
    def On_IdleToApproaching(self, cur_time, target_c):
        logger('%.1f:    On_I2A - %s, assigned customer %s, path: %s' % (cur_time, self, self.assigned_customer, self.path_n))
        assert self.state == ST_IDLE
        
        # Modify event already scheduled
        prev_PRT = target_c.assigned_PRT
        if prev_PRT and prev_PRT.assigned_customer == target_c:
            assert False
        
        # State update
        self.state = ST_APPROACHING
        self.assigned_customer = target_c
        target_c.assigned_PRT = self
        
        # Measure update
        IdleState_times += self.last_planed_time - cur_time
        
        # Set things for next state
        self.path_n, self.path_e = Algorithms.find_SP(self.arrived_n, self.assigned_customer.sn, Nodes)
        self.last_planed_time = cur_time
        evt_change_point = cur_time + sum([e.distance for e in self.path_e]) / PRT_SPEED
        x = [evt_change_point, self.On_ApproachingToTransiting, target_c]
        heappush(event_queue, x)
        self.event_seq.append(x)
        
        logger('%.1f:        path: %s' % (self.path_n))

#---------------------------------------------------------------------
# Generate things such as Network, PRT, Customer

def gen_Network(ns, ns_connection):
    Nodes = [Node(px, py, isStation) for px, py, isStation in ns]
    Edges = []
    for pn, nn in ns_connection:
        Edges.append(Edge(Nodes[pn], Nodes[nn]))
    return Nodes, Edges

def gen_Customer(average_arrival, num_customers, Nodes):
    accu_pd = []
    mu_assi = 10000
    mu = average_arrival * mu_assi
    pd = poisson(mu, num_customers)
    for i, t in enumerate(pd):
        if i == 0:
            accu_pd.append(t)
            continue
        accu_pd.append(accu_pd[-1] + t)
    
    Customers = []
    for t in accu_pd:
        sn, dn = 0, 0
        while sn == dn or not Nodes[sn].isStation or not Nodes[dn].isStation:
            sn = randrange(len(Nodes))
            dn = randrange(len(Nodes))
        Customers.append(Customer(t / mu_assi, Nodes[sn], Nodes[dn]))
        
    customerArrivals_txt = open('Info. Arrivals of customers.txt', 'w')
    for c in Customers:
        t, sn, dn = c.arriving_time, c.sn.id, c.dn.id 
        customerArrivals_txt.write('%f,%d-%d\n' % (t, sn, dn))
    customerArrivals_txt.close()
        
    return Customers

def gen_PRT(numOfPRT, Nodes):
    return [PRT(Nodes[randrange(len(Nodes))]) for _ in range(numOfPRT)]

#---------------------------------------------------------------------
# Prepare dynamics run
PRT_SPEED = 80
waiting_customers = []
event_queue = []

def init_dynamics(_Nodes, _PRTs, _Customers, _dispatcher):
    global Nodes, PRTs, Customers, dispatcher
    Nodes, PRTs, Customers, dispatcher = _Nodes, _PRTs, _Customers, _dispatcher
    for customer in Customers:
        x = [customer.arriving_time, On_CustomerArrival, customer]
        heappush(event_queue, x)

def logger(s):
    print s

on_notify_customer_arrival = lambda x: None

def On_CustomerArrival(cur_time, target_c):
    logger('%.1f: On_CustomerArrival - %s' % (cur_time, target_c))
    customer = Customers.pop(0)
    assert customer == target_c
    waiting_customers.append(customer)
    dispatcher(cur_time, PRTs, waiting_customers, Nodes)
    on_notify_customer_arrival(customer)

def process_events(now):
    while event_queue and event_queue[0][0] <= now:
        even_time, hdlr, args = heappop(event_queue)
        if hdlr != None:
            hdlr(even_time, args)
    if not event_queue:
        return False
    return True

#---------------------------------------------------------------------
# For calculating measure
Total_empty_travel_distance = 0.0
NumOfPickedUpCustomer = 0

Total_travel_distance = 0.0
Total_customers_flow_time = 0.0
NumOfServicedCustomer = 0

Total_customers_waiting_time = 0.0
NumOfWaitingCustomer = 0
ChaningPointOfNWC = 0.0
MaxCustomerWaitingTime = 0.0

IdleState_times = 0.0
ApproachingState_times = 0.0
TransitingState_times = 0.0
ParkingState_times = 0.0

#---------------------------------------------------------------------
def test():
    from time import sleep
    import Network
    seed(0)
    # Generage all inputs: Network, Arrivals of customers, PRTs
    Nodes, Edges = gen_Network(*Network.network0())
    Customers = gen_Customer(2.5, 2000, Nodes)
    PRTs = gen_PRT(10, Nodes)
    
    # Choose dispatcher
    dispatcher = Algorithms.NN0
#     dispatcher = Algorithms.NN1
#     dispatcher = Algorithms.NN2
#     dispatcher = Algorithms.NN3
#     dispatcher = Algorithms.NN4
#     dispatcher = Algorithms.NN5
    
    init_dynamics(Nodes, PRTs, Customers, dispatcher)
    
    now = 0.0
    while process_events(now):
        now += 1
        sleep(0.0001)
    
if __name__ == '__main__':
    test()
