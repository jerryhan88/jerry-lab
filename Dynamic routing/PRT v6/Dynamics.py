from __future__ import division
from random import randrange, random, uniform, seed
from math import sqrt
from numpy.random import poisson
from heapq import heappush, heappop
import Algorithms

seed(0)

def gen_network0():
    sx, sy = 800, 800
        
    ns_pos = [(sx * 0.1, sy * 0.1), (sx * 0.4, sy * 0.1), (sx * 0.75, sy * 0.1),
              (sx * 0.1, sy * 0.3), (sx * 0.4, sy * 0.3), (sx * 0.75, sy * 0.3),
              (sx * 1.0, sy * 0.3), (sx * 0.1, sy * 0.62), (sx * 0.4, sy * 0.62),
              (sx * 0.75, sy * 0.62), (sx * 1.0, sy * 0.62)]
    Nodes = [Node(px, py) for px, py in ns_pos]
    
    ns_connection = [(1, 0), (1, 2), (3, 4), (5, 4), (5, 6),
                     (8, 7), (8, 9), (10, 9), (0, 3), (4, 1),
                     (2, 5), (7, 3), (4, 8), (9, 5), (6, 10)]
    
    for pn, nn in ns_connection:
        Edge(Nodes[pn], Nodes[nn])
    
    return Nodes

def gen_PRT0(num_PRT, Nodes):
    return [PRT(Nodes[randrange(len(Nodes))]) for _ in range(num_PRT)]

def gen_customer0(Nodes, num_request, Last_arriving_time):
    mu_assi = 10000
    assumed_rambda = Last_arriving_time / num_request
    mu = assumed_rambda * mu_assi
    pd = poisson(mu, num_request)

    accu_pd = []
    for i, t in enumerate(pd):
        if i == 0:
            accu_pd.append(t)
            continue
        accu_pd.append(accu_pd[-1] + t)
    
    Customers = []
    for t in accu_pd:
        sn = randrange(len(Nodes))
        dn = randrange(len(Nodes))
        while sn == dn:
            dn = randrange(len(Nodes))
        Customers.append(Customer(t/mu_assi, Nodes[sn], Nodes[dn]))
        
    return Customers

def write_input_info(Customers, PRTs):
    
    txt = open('Info. Customers & PRTs.txt', 'w')
    txt.write('Customers Info.\n')
    for c in Customers:
        _id, arriving_time, sn, dn = c.id, c.arriving_time, c.sn.id, c.dn.id
        txt.write('C%d,%.1f,%d-%d\n' % (_id, arriving_time, sn, dn))
    txt.write('\n')
    txt.write('PRTs Info.\n')
    for prt in PRTs:
        _id, init_n = prt.id, prt.arrived_n.id
        txt.write('PRT%d, N%d\n' % (_id, init_n))
    txt.close()

class Node():
    _id = 0
    BIG_NUM = 1000000
    def __init__(self, px, py):
        self.id = Node._id
        Node._id += 1
        self.px, self.py = px, py
        
        self.edges_inward = []
        self.edges_outward = []
        
    def init_node(self):
        self.visited = False
        self.min_d = Node.BIG_NUM
    
    def __repr__(self):
        return 'N%d' % self.id
    
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
    
class PRT():
    _id = 0
    def __init__(self, init_node):
        self.id = PRT._id
        PRT._id += 1
        self.arrived_n = init_node
        self.px, self.py = self.arrived_n.px, self.arrived_n.py
        self.state = 0 
    
    def __repr__(self):
        return 'PRT%d, Now %d' % (self.id, self.arrived_n.id)
    
    def re_assign_customer(self, cur_time, target_c):
        if self.state == 0 :
            if self.arrived_n != target_c.sn:
                # Idle -> Approaching
                x = (cur_time, self.On_IdleToApproaching, target_c)
                heappush(event_queue, x)
            else:
                assert self.arrived_n == target_c.sn
                # Idle -> Transiting
                x = (cur_time, self.On_IdleToTransiting, target_c)
                heappush(event_queue, (cur_time, x))
                
        else:
            assert False
    
    def On_IdleToApproaching(self, cur_time, target_c):
        assert False
        self.state = 1
        self.assigned_customer = target_c
        
        if NN_number <= 1:
            self.path_n, self.path_e = find_SP(self.arrived_n, self.assigned_customer.sn, self.nodes)
            self.last_planed_time = cur_time
            evt_change_point = cur_time + sum([e.distance for e in self.path_e]) / PRT_SPEED
            heappush(event_queue, (evt_change_point, self.On_ApproachingToTransiting(evt_change_point, event_queue, PRTs, waiting_customers)))
        else:
            # find already set events related with this prt's state change in even_queue 
            pass
        
        return 'On_IdleToApproaching'

    def On_IdleToTransiting(self, cur_time, target_c):
        assert False
        self.state = 2
        self.path_n, self.path_e = find_SP(self.arrived_n, self.assigned_customer.dn, self.nodes)
        self.last_planed_time = cur_time
        evt_change_point = cur_time + sum([e.distance for e in self.path_e])/ PRT_SPEED
        heappush(event_queue, (evt_change_point, self.On_TransitingToIdle(evt_change_point, event_queue, PRTs, waiting_customers)))
        self.transporting_customer = target_c
        return 'On_IdleToTransiting'

class Customer():
    _id = 0
    def __init__(self, arriving_time, sn, dn):
        self.id = Customer._id
        Customer._id += 1
        self.arriving_time = arriving_time
        self.sn, self.dn = sn, dn
        
        self.assigned_PRT = None
    
    def __repr__(self):
        return 'C%d N%d->N%d (t:%.1f)' % (self.id, self.sn.id, self.dn.id, self.arriving_time)


# Every resources are accessible
Nodes = gen_network0()

num_request = 100
Last_arriving_time = 300
Customers = gen_customer0(Nodes, num_request, Last_arriving_time)
num_PRT = 3
PRTs = gen_PRT0(num_PRT, Nodes)

write_input_info(Customers, PRTs)

# Prepare dynamics run
PRT_SPEED = 5
NN_number = 0
waiting_customers = []
event_queue = []
    
def select_NN(NN_number):
    return eval('Algorithms.NN%d' % NN_number)

def On_CustomerArrival(event_time, args=None):
    customer = Customers.pop(0)
    waiting_customers.append(customer)
    chosenNN = select_NN(NN_number)
    chosenNN(event_time, PRTs, waiting_customers, Nodes)
    
    return 'On_CustomerArrival'

def run():
    for customer in Customers:
        x = (customer.arriving_time, On_CustomerArrival, None)
        heappush(event_queue, x)
    
    while event_queue:
        even_time, hdr, args = heappop(event_queue)
        if hdr != None:
            hdr(even_time, args)


if __name__ == '__main__':
    run()
