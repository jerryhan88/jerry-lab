from __future__ import division
from math import sqrt
from heapq import heappush, heappop
from Algorithms import NN0, NN1, NN2, NN3, find_SP
import Scenarios

PRT_SPEED = 10

# NN selection
PRTScope = 0
Reassignable = False
        
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
    
    def __repr__(self):
        return '%s N%d->N%d' % (self.id, self.sn.id, self.dn.id)
    
    def On_CustomerArrival(self, cur_time, waiting_customers, event_queue, PRTs, Nodes):
        global PRTScope, Reassignable
        
        chosenNN = None
        if PRTScope == 0:
             chosenNN = NN0
        elif PRTScope == 1:
            chosenNN = NN1
        else:
            assert PRTScope == 2
            if not Reassignable:
                chosenNN = NN2
            else:
                chosenNN = NN3
                
        waiting_customers.append(self)
        
        assignment_results, target_PRTs = chosenNN(PRTs, waiting_customers, Nodes)
        set_PRTs_behavior(target_PRTs, waiting_customers, assignment_results, cur_time, event_queue, PRTs)
        
        return 'On_CustomerArrival'
        
class PRT():
    _id = 0
    def __init__(self, Nodes):
        self.id = PRT._id
        PRT._id += 1
        self.px, self.py = None, None
        self.path_n = []
        self.path_e = []
        self.last_planed_time = 0
        self.assigned_customer = None
        self.transporting_customer = None
        
        self.nodes = Nodes
        
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
    
    def On_IdleToApproaching(self, cur_time, target_c, event_queue, PRTs, waiting_customers):
        self.state = 1
        self.assigned_customer = target_c
        global Reassignable, PRT_SPEED
        if not Reassignable:
            self.path_n, self.path_e = find_SP(self.arrived_n, self.assigned_customer.sn, self.nodes)
            self.last_planed_time = cur_time
            evt_change_point = cur_time + sum([e.distance for e in self.path_e])/ PRT_SPEED
            heappush(event_queue, (evt_change_point, self.On_ApproachingToTransiting(evt_change_point, event_queue, PRTs, waiting_customers)))
        return 'On_IdleToApproaching'
    
    def On_ApproachingToTransiting(self, cur_time, event_queue, PRTs, waiting_customers):
        self.state = 2
        self.transporting_customer = self.assigned_customer
        self.assigned_customer = None
        self.arrived_n = self.transporting_customer.sn
        self.path_n, self.path_e = find_SP(self.transporting_customer.sn, self.transporting_customer.dn, self.nodes)
        self.last_planed_time = cur_time
        evt_change_point = cur_time + sum([e.distance for e in self.path_e])/ PRT_SPEED
        heappush(event_queue, (evt_change_point, self.On_TransitingToIdle(evt_change_point, event_queue, PRTs, waiting_customers)))
        return 'On_ApproachingToTransiting'
        
    def On_TransitingToIdle(self, cur_time, event_queue, PRTs, waiting_customers):
        self.state = 0
        self.arrived_n = self.transporting_customer.dn
        chosenNN = None
        if PRTScope == 0:
             chosenNN = NN0
        elif PRTScope == 1:
            chosenNN = NN1
        else:
            assert PRTScope == 2
            if not Reassignable:
                chosenNN = NN2
            else:
                chosenNN = NN3
                
        assignment_results, target_PRTs = chosenNN(PRTs, waiting_customers, self.nodes)
        set_PRTs_behavior(target_PRTs, waiting_customers, assignment_results, cur_time, event_queue, PRTs)
        return 'On_TransitingToIdle'
    
    def On_IdleToTransiting(self, cur_time, target_c, event_queue, PRTs, waiting_customers):
        self.state = 2
        self.path_n, self.path_e = find_SP(self.arrived_n, self.assigned_customer.dn, self.nodes)
        self.last_planed_time = cur_time
        evt_change_point = cur_time + sum([e.distance for e in self.path_e])/ PRT_SPEED
        heappush(event_queue, (evt_change_point, self.On_TransitingToIdle(evt_change_point, event_queue, PRTs, waiting_customers)))
        self.transporting_customer = target_c
        return 'On_IdleToTransiting'
    
    def On_ApproachingToParking(self):
        pass 
    
    def On_ParkingToApproaching(self):
        pass
    
    def On_ParkingToIdle(self):
        pass  

def set_PRTs_behavior(target_PRTs, waiting_customers, assignment_results, cur_time, event_queue, PRTs):
    if assignment_results:
        for prt_id, customer_id in assignment_results:
            chosen_prt = target_PRTs[prt_id]
            target_c = waiting_customers[customer_id]
            if chosen_prt.state == 0:
                if chosen_prt.arrived_n != target_c.sn:
                    # Idle -> Approaching
                    heappush(event_queue, (cur_time, chosen_prt.On_IdleToApproaching(cur_time, target_c, event_queue, PRTs, waiting_customers)))
                else:
                    assert chosen_prt.arrived_n == target_c.sn
                    # Idle -> Transiting
                    heappush(event_queue, (cur_time, chosen_prt.On_IdleToTransiting(cur_time, target_c, event_queue, PRTs, waiting_customers)))
                    
            elif chosen_prt.state == 1:
                assert chosenNN == NN3 and chosen_prt.assigned_customer
                # Even though there is a assigned customer, the prt change the assigned customer by another
                # Approaching -> Approaching
                # The assigned_customer is changed, so path also should be changed
                heappush(event_queue, (cur_time, chosen_prt.ApproachingToApproaching(a_waiting_cus)))
                assert False, 'hello?'
                
# #                     # Approaching -> Transiting  ??
# #                     # find last passed node
# #                     lp_n = None
# #                     path_travel_distance = (cur_time - last_planed_time) * PRT_SPEED
# #                     sum_edges_distance = 0
# #                     for i, e in enumerate(prt.path_e):
# #                         sum_edges_distance += e.distance 
# #                         if sum_edges_distance >= path_travel_distance:
# #                             lp_n = e._from
# #                     dx = lp_n.px - prt.px  
# #                     dy = lp_n.py - prt.py
# #                         
# #                     if dx == 0 and dy == 0:
# #                         pass
                
            elif chosen_prt.state == 3:
                heappush(event_queue, (cur_time, chosen_prt.ParkingToApproaching(a_waiting_cus)))
            else:
                assert chosen_prt.state == 2
                pass

PRTs
waiting_customers = []

def run(PRTs, Nodes):

    with open('Input', 'r') as fp:
        for line in fp:
            c_id, t_s, sd = line.split(',')
            t = round(float(t_s), 1)
            sn, dn = sd.split('-')
            args = (c_id, Nodes[int(sn)], Nodes[int(dn)])
            x = (t, On_CustomerArrival(), args)
            heappush(event_queue, x)
            
            
            
            x[1] = None
    
    while event_queue:
        t, hdr, args = heappop(event_queue)
        if hdr != None:
            hdr(t, event_queue, args)
            print t, event

def On_CustomerArrival(t, event_queue, (c_id, src, dst)):
    c = Customer(c_id, src, dst)

if __name__ == '__main__':
    import input_gen
    Nodes, Edges = input_gen.network1()
    PRTs = Scenarios.scenario1(Nodes)
    run(PRTs, Nodes)
