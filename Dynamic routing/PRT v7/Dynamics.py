from __future__ import division
from random import randrange, random, uniform, seed
from math import sqrt
from numpy.random import poisson
from heapq import heappush, heappop
import Algorithms

on_notify_customer_arrival = lambda x: None

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
        return 'N%d->N%d' % (self._from.id, self._to.id)
    

ST_IDLE, ST_APPROACHING, ST_TRANSITING, ST_PARKING = 0, 1, 2, 3

class PRT():
    _id = 0
    def __init__(self, init_node):
        self.id = PRT._id
        PRT._id += 1
        
        self.arrived_n = init_node
        self.px, self.py = self.arrived_n.px, self.arrived_n.py
        self.path_n, self.path_e = [], []
        self.assigned_customer = None
        self.transporting_customer = None
        
        self.state = ST_IDLE
        self.last_planed_time = 0
        self.event_seq = [] 
    
    def __repr__(self):
        return 'PRT%d-Now N%d' % (self.id, self.arrived_n.id)
    
    def re_assign_customer(self, cur_time, target_c):
        if self.state == ST_IDLE :
            if self.arrived_n != target_c.sn:
                # Idle -> Approaching
                x = [cur_time, self.On_IdleToApproaching, target_c]
                heappush(event_queue, x)
                self.event_seq.append(x)
            else:
                assert self.arrived_n == target_c.sn
                # Idle -> Transiting
                x = [cur_time, self.On_IdleToTransiting, target_c]
                heappush(event_queue, x)
                self.event_seq.append(x)
        elif self.state == ST_TRANSITING:
            # When this PRT become idle, target_c will be assigned
            pass
        elif self.state == ST_APPROACHING:
            if self.assigned_customer != target_c:
                # Approaching -> Approaching
                # Even though this PRT approaching assigned customer
                # the PRT assigned to target_c has been changed
                x = [cur_time, self.On_ApproachingToApproaching, target_c]
                heappush(event_queue, x)
                self.event_seq.append(x)
        else:
            # parking to approaching
            assert False
    
    def On_ApproachingToApproaching(self, cur_time, target_c):
        assert self.state == ST_APPROACHING
        
        prev_c = self.assigned_customer 
        
        self.assigned_customer = target_c
        prev_PRT = target_c.assigned_PRT
        
        if prev_PRT and prev_PRT.assigned_customer == target_c:
            # check last event
            last_evt = prev_PRT.event_seq[-1]
            if last_evt[1] == prev_PRT.On_ApproachingToApproaching:
                # prev_PRT also reassigned, so we don't need to anything
                pass
            else:
                assert last_evt[1] == prev_PRT.On_ApproachingToTransiting
                # prev_PRT lost customer and don't have any assigned customer
                last_evt[1] = None
                x = (cur_time, prev_PRT.On_ApproachingToParking, target_c)
                heappush(event_queue, x)
                prev_PRT.event_seq.append(x)
        
        target_c.assigned_PRT = self
        
        # make already scheduled event A2T
        assert self.event_seq[-1][1] == self.On_ApproachingToApproaching
        A2T_event = self.event_seq[-2]
        assert A2T_event[1] == self.On_ApproachingToTransiting and A2T_event[2] != target_c 
        A2T_event[1] = None
        
        next_n = None
        sum_edges_distance = 0
        edges_counter = 0
        path_travel_distance = (cur_time - self.last_planed_time) * PRT_SPEED
        for e in self.path_e:
            sum_edges_distance += e.distance
            edges_counter += 1 
            if sum_edges_distance >= path_travel_distance:
                next_n = e._to
                break
        remain_dis = sum([e.distance for e in self.path_e[:edges_counter]]) - path_travel_distance
        
        if next_n == target_c.sn:
            self.path_n, self.path_e = Algorithms.find_SP(self.arrived_n, next_n, Nodes)
            evt_change_point = cur_time + remain_dis / PRT_SPEED
        else:
            passed_path_n, passed_path_e = Algorithms.find_SP(self.arrived_n, next_n, Nodes)
            path_n_Rerouted, path_e_Rerouted = Algorithms.find_SP(next_n, target_c.sn, Nodes)
            self.path_n = passed_path_n + path_n_Rerouted[1:]
            self.path_e = passed_path_e + path_e_Rerouted
            evt_change_point = cur_time + (remain_dis + sum([e.distance for e in path_e_Rerouted])) / PRT_SPEED 
            
        x = [evt_change_point, self.On_ApproachingToTransiting, target_c]
        heappush(event_queue, x)
        self.event_seq.append(x)
        
        logger('%.1f:    On_A2A - %s, prev_c:%s - new_c:%s' % (cur_time, self, prev_c, target_c))
             
    def On_ApproachingToParking(self, cur_time, target_c):
        assert self.state == ST_APPROACHING
        
        lost_customer = self.assigned_customer
        
        self.state = ST_PARKING
        self.assigned_customer = None
        assert lost_customer
        
        next_n = None
        sum_edges_distance = 0
        edges_counter = 0
        path_travel_distance = (cur_time - self.last_planed_time) * PRT_SPEED
        for e in self.path_e:
            sum_edges_distance += e.distance
            edges_counter += 1 
            if sum_edges_distance >= path_travel_distance:
                next_n = e._to
                break
        remain_dis = sum([e.distance for e in self.path_e[:edges_counter]]) - path_travel_distance
        
        evt_change_point = cur_time + remain_dis / PRT_SPEED
        x = [evt_change_point, self.On_ParkingToIdle, None]
        heappush(event_queue, x)
        self.event_seq.append(x)
        
        logger('%.1f:    On_A2P - %s, lost %s' % (cur_time, self, lost_customer))
    
    def On_ParkingToIdle(self, cur_time, args=None):
        assert self.state == ST_PARKING
        
        self.state = ST_IDLE
        self.arrived_n = self.path_n[0]
        logger('%.1f:    On_P2I - %s' % (cur_time, self))
    
    def On_IdleToApproaching(self, cur_time, target_c):
        assert self.state == ST_IDLE
        
        self.state = ST_APPROACHING
        self.assigned_customer = target_c
        target_c.assigned_PRT = self
        
        self.path_n, self.path_e = Algorithms.find_SP(self.arrived_n, self.assigned_customer.sn, Nodes)
        self.last_planed_time = cur_time

        evt_change_point = cur_time + sum([e.distance for e in self.path_e]) / PRT_SPEED
        x = [evt_change_point, self.On_ApproachingToTransiting, target_c]
        heappush(event_queue, x)
        self.event_seq.append(x)

        logger('%.1f:    On_I2A - %s, path: %s' % (cur_time, self, self.path_n))
        
    def On_ApproachingToTransiting(self, cur_time, target_c):
        assert self.state == ST_APPROACHING

        self.state = ST_TRANSITING
        self.transporting_customer = remove_A_customerInWaitingList(self.assigned_customer)
        assert self.transporting_customer
        
        self.assigned_customer = None
        self.arrived_n = self.transporting_customer.sn
        
        self.path_n, self.path_e = Algorithms.find_SP(self.transporting_customer.sn, self.transporting_customer.dn, Nodes)
        self.last_planed_time = cur_time
        evt_change_point = cur_time + sum([e.distance for e in self.path_e]) / PRT_SPEED
        x = [evt_change_point, self.On_TransitingToIdle, None]
        heappush(event_queue, x)
        self.event_seq.append(x)
        logger('%.1f:    On_A2T - %s, picking up customer - %s' % (cur_time, self, self.transporting_customer)) 

    def On_IdleToTransiting(self, cur_time, target_c):
        assert self.state == ST_IDLE
        
        self.state = ST_TRANSITING
        self.transporting_customer = remove_A_customerInWaitingList(target_c)
        assert self.transporting_customer
        
        self.path_n, self.path_e = Algorithms.find_SP(self.arrived_n, self.transporting_customer.dn, Nodes)
        self.last_planed_time = cur_time
        evt_change_point = cur_time + sum([e.distance for e in self.path_e]) / PRT_SPEED
        x = [evt_change_point, self.On_TransitingToIdle, None]
        heappush(event_queue, x)
        self.event_seq.append(x)
        logger('%.1f:    On_I2T - %s, picking up customer - %s' % (cur_time, self, self.transporting_customer))
    
    def On_TransitingToIdle(self, cur_time, args=None):
        assert self.state == ST_TRANSITING
        
        self.state = ST_IDLE
        self.arrived_n = self.transporting_customer.dn
        self.transporting_customer = None
        self.path_n, self.path_e = None, None
        dispatcher(cur_time, PRTs, waiting_customers, Nodes)
                
        logger('%.1f:    On_T2I - %s' % (cur_time, self))

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


# Prepare dynamics run
PRT_SPEED = 50
waiting_customers = []
event_queue = []

def remove_A_customerInWaitingList(target_customer):
    # remove servicing customer in waiting_customer
    for i, customer in enumerate(waiting_customers):
        if customer == target_customer:
            return waiting_customers.pop(i)

def logger(s):
    print s

def On_CustomerArrival(event_time, args=None):
    customer = Customers.pop(0)
    waiting_customers.append(customer)
    dispatcher(event_time, PRTs, waiting_customers, Nodes)
    
    on_notify_customer_arrival(customer)

    logger('%.1f: On_CustomerArrival - %s' % (event_time, customer))

def init_dynamics(_Nodes, _PRTs, _Customers, _dispatcher):
    global Nodes, PRTs, Customers, dispatcher
    Nodes, PRTs, Customers, dispatcher = _Nodes, _PRTs, _Customers, _dispatcher
    for customer in Customers:
        x = [customer.arriving_time, On_CustomerArrival, None]
        heappush(event_queue, x)

def process_events(now):
    while event_queue and event_queue[0][0] <= now:
        even_time, hdlr, args = heappop(event_queue)
#         print even_time, hdr, args
        if hdlr != None:
            hdlr(even_time, args)

# -----------------------------------------------------------------

def test():
    from time import sleep
    import Input_gen
    
    # Every resources are accessible
    Nodes, Edges = gen_network(*Input_gen.network0())
    Customers = gen_customer(Nodes)
    PRTs = gen_PRT(Input_gen.PRT_pos_ex0(), Nodes)
 
#     dispatcher = Algorithms.NN0
#     dispatcher = Algorithms.NN1
#     dispatcher = Algorithms.NN2
#     dispatcher = Algorithms.NN3
#     dispatcher = Algorithms.NN4
    dispatcher = Algorithms.NN5
     
    init_dynamics(Nodes, PRTs, Customers, dispatcher)
     
    now, time_end = 0.0, max(c.arriving_time for c in Customers) + 100
    while now < time_end:
        process_events(now)
        now += 1
        sleep(0.01)

# -----------------------------------------------------------------
def gen_network(ns_pos, ns_connection):
    Nodes = [Node(px, py) for px, py in ns_pos]
    Edges = []
    for pn, nn in ns_connection:
        Edges.append(Edge(Nodes[pn], Nodes[nn]))
    return Nodes, Edges

def gen_PRT(pos, Nodes):
    return [PRT(Nodes[init_pos]) for init_pos in pos]

def gen_customer(Nodes):
    Customers = []
    with open('Info. Arrivals of customers.txt', 'r') as fp:
        for line in fp:
            arrival_time_str, sd = line.split(',')
            arrival_time = float(arrival_time_str)
            sn_str, dn_str = sd.split('-')
            Customers.append(Customer(arrival_time, Nodes[int(sn_str)], Nodes[int(dn_str)]))
    return Customers

if __name__ == '__main__':
    test()
