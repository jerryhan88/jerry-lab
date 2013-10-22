from __future__ import division
from heapq import heappush, heappop
from math import sqrt
import Input_gen, Algorithms

BIG_NUM = 1000000

# Every resources are accessible
Nodes = Input_gen.gen_network0()

num_request = 100
Last_arriving_time = 300
Customers = Input_gen.gen_customer0(Nodes, num_request, Last_arriving_time)
num_PRT = 3
PRTs = Input_gen.gen_PRT0(num_PRT, Nodes)

Input_gen.write_input_info(Customers, PRTs)

# Prepare dynamics run
PRT_SPEED = 5
NN_number = 0
waiting_customers = []
event_queue = []

class Node():
    _id = 0
    def __init__(self, px, py):
        self.id = Node._id
        Node._id += 1
        self.px, self.py = px, py
        
        self.edges_inward = []
        self.edges_outward = []
        
    def init_node(self):
        self.visited = False
        self.min_d = BIG_NUM
    
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

class PRT():
    _id = 0
    def __init__(self, init_node):
        self.id = PRT._id
        PRT._id += 1
        self.arrived_n = init_node
        self.px, self.py = self.arrived_n.px, self.arrived_n.py 
    
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
                heappush(event_queue, (cur_time, chosen_prt.On_IdleToTransiting(cur_time, target_c, event_queue, PRTs, waiting_customers)))
        else:
            assert False
    
    def On_IdleToApproaching(self, cur_time, target_c):
        self.state = 1
        self.assigned_customer = target_c
        
        if NN_number <= 1:
            self.path_n, self.path_e = find_SP(self.arrived_n, self.assigned_customer.sn, self.nodes)
            self.last_planed_time = cur_time
            evt_change_point = cur_time + sum([e.distance for e in self.path_e]) / PRT_SPEED
            heappush(event_queue, (evt_change_point, self.On_ApproachingToTransiting(evt_change_point, event_queue, PRTs, waiting_customers)))
        return 'On_IdleToApproaching'

def select_NN(NN_number):
    return eval('Algorithms.NN%d' % num_NN)

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
