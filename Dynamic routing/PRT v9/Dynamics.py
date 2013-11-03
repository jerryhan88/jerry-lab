from __future__ import division
from math import sqrt, pi, cos, sin
from random import randrange, seed, expovariate
from numpy.random import poisson
from heapq import heappush, heappop
import Algorithms
#---------------------------------------------------------------------
# Network example
STATION, JUNCTION, DOT = 0, 1, 2

def findNode(nID):
    for n in Nodes:
        if n.id == nID:
            return n
    else:
        False

def Network1():
    c0 = 0
    c1 = c0 + 450
    c2 = c1 + 350
    c3 = c2 + 500
    
    r0 = 0
    r1 = r0 + 300 
    r2 = r1 + 500
    r3 = r2 + 450
    
    btwSJ = 70
    
    global Nodes
    Nodes = [
                Node('1', c0, r0, STATION), Node('1E', c0 + btwSJ, r0, JUNCTION), Node('1S', c0, r0 + btwSJ, JUNCTION),
                Node('2', c1, r0, STATION), Node('2E', c1 + btwSJ, r0, JUNCTION), Node('2W', c1 - btwSJ, r0, JUNCTION), Node('2S', c1, r0 + btwSJ, JUNCTION),
                Node('3', c2, r0, STATION), Node('3W', c2 - btwSJ, r0, JUNCTION), Node('3S', c2, r0 + btwSJ, JUNCTION),
                Node('4', c0, r1, STATION), Node('4E', c0 + btwSJ, r1, JUNCTION), Node('4N', c0, r1 - btwSJ, JUNCTION), Node('4S', c0, r1 + btwSJ, JUNCTION),
                Node('5', c1, r1, STATION), Node('5E', c1 + btwSJ, r1, JUNCTION), Node('5W', c1 - btwSJ, r1, JUNCTION), Node('5N', c1, r1 - btwSJ, JUNCTION), Node('5S', c1, r1 + btwSJ, JUNCTION),
                Node('6', c2, r1, STATION), Node('6E', c2 + btwSJ, r1, JUNCTION), Node('6W', c2 - btwSJ, r1, JUNCTION), Node('6S', c2, r1 + btwSJ, JUNCTION), Node('6N', c2, r1 - btwSJ, JUNCTION),
                Node('7', c3, r1, STATION), Node('7W', c3 - btwSJ, r1, JUNCTION), Node('7S', c3, r1 + btwSJ, JUNCTION),
                Node('8', c0, r2, STATION), Node('8E', c0 + btwSJ, r2, JUNCTION), Node('8N', c0, r2 - btwSJ, JUNCTION),
                Node('9', c1, r2, STATION), Node('9E', c1 + btwSJ, r2, JUNCTION), Node('9W', c1 - btwSJ, r2, JUNCTION), Node('9S', c1, r2 + btwSJ, JUNCTION), Node('9N', c1, r2 - btwSJ, JUNCTION),
                Node('10', c2, r2, STATION), Node('10E', c2 + btwSJ, r2, JUNCTION), Node('10W', c2 - btwSJ, r2, JUNCTION), Node('10S', c2, r2 + btwSJ, JUNCTION), Node('10N', c2, r2 - btwSJ, JUNCTION),
                Node('11', c3, r2, STATION), Node('11W', c3 - btwSJ, r2, JUNCTION), Node('11S', c3, r2 + btwSJ, JUNCTION), Node('11N', c3, r2 - btwSJ, JUNCTION),
                Node('12', c1, r3, STATION), Node('12E', c1 + btwSJ, r3, JUNCTION), Node('12N', c1, r3 - btwSJ, JUNCTION),
                Node('13', c2, r3, STATION), Node('13E', c2 + btwSJ, r3, JUNCTION), Node('13W', c2 - btwSJ, r3, JUNCTION), Node('13N', c2, r3 - btwSJ, JUNCTION),
                Node('14', c3, r3, STATION), Node('14W', c3 - btwSJ, r3, JUNCTION), Node('14N', c3, r3 - btwSJ, JUNCTION),
                
                Node('3E', c2 + btwSJ, r0, JUNCTION),
                Node('3-7.D1', c3 - ((r1 - r0) - btwSJ) + ((r1 - r0) - btwSJ) * cos((pi / 180) * -90 * (11 / 11)), r1 - btwSJ + ((r1 - r0) - btwSJ) * sin((pi / 180) * -90 * (11 / 11)), DOT),
                Node('3-7.D2', c3 - ((r1 - r0) - btwSJ) + ((r1 - r0) - btwSJ) * cos((pi / 180) * -90 * (10 / 11)), r1 - btwSJ + ((r1 - r0) - btwSJ) * sin((pi / 180) * -90 * (10 / 11)), DOT),
                Node('3-7.D3', c3 - ((r1 - r0) - btwSJ) + ((r1 - r0) - btwSJ) * cos((pi / 180) * -90 * (9 / 11)), r1 - btwSJ + ((r1 - r0) - btwSJ) * sin((pi / 180) * -90 * (9 / 11)), DOT),
                Node('3-7.D4', c3 - ((r1 - r0) - btwSJ) + ((r1 - r0) - btwSJ) * cos((pi / 180) * -90 * (8 / 11)), r1 - btwSJ + ((r1 - r0) - btwSJ) * sin((pi / 180) * -90 * (8 / 11)), DOT),
                Node('3-7.D5', c3 - ((r1 - r0) - btwSJ) + ((r1 - r0) - btwSJ) * cos((pi / 180) * -90 * (7 / 11)), r1 - btwSJ + ((r1 - r0) - btwSJ) * sin((pi / 180) * -90 * (7 / 11)), DOT),
                Node('3-7.D6', c3 - ((r1 - r0) - btwSJ) + ((r1 - r0) - btwSJ) * cos((pi / 180) * -90 * (6 / 11)), r1 - btwSJ + ((r1 - r0) - btwSJ) * sin((pi / 180) * -90 * (6 / 11)), DOT),
                Node('3-7.D7', c3 - ((r1 - r0) - btwSJ) + ((r1 - r0) - btwSJ) * cos((pi / 180) * -90 * (5 / 11)), r1 - btwSJ + ((r1 - r0) - btwSJ) * sin((pi / 180) * -90 * (5 / 11)), DOT),
                Node('3-7.D8', c3 - ((r1 - r0) - btwSJ) + ((r1 - r0) - btwSJ) * cos((pi / 180) * -90 * (4 / 11)), r1 - btwSJ + ((r1 - r0) - btwSJ) * sin((pi / 180) * -90 * (4 / 11)), DOT),
                Node('3-7.D9', c3 - ((r1 - r0) - btwSJ) + ((r1 - r0) - btwSJ) * cos((pi / 180) * -90 * (3 / 11)), r1 - btwSJ + ((r1 - r0) - btwSJ) * sin((pi / 180) * -90 * (3 / 11)), DOT),
                Node('3-7.D10', c3 - ((r1 - r0) - btwSJ) + ((r1 - r0) - btwSJ) * cos((pi / 180) * -90 * (2 / 11)), r1 - btwSJ + ((r1 - r0) - btwSJ) * sin((pi / 180) * -90 * (2 / 11)), DOT),
                Node('3-7.D11', c3 - ((r1 - r0) - btwSJ) + ((r1 - r0) - btwSJ) * cos((pi / 180) * -90 * (1 / 11)), r1 - btwSJ + ((r1 - r0) - btwSJ) * sin((pi / 180) * -90 * (1 / 11)), DOT),
                Node('7N', c3, r1 - btwSJ, JUNCTION),
                
                Node('12W', c1 - btwSJ, r3, JUNCTION),
                Node('12-8.D1', c1 - btwSJ + ((c1 - c0) - btwSJ) * cos((pi / 180) * (-180 + -90 * (10 / 11))), r2 + btwSJ + ((c1 - c0) - btwSJ) * sin((pi / 180) * (-180 + -90 * (10 / 11))), DOT),
                Node('12-8.D2', c1 - btwSJ + ((c1 - c0) - btwSJ) * cos((pi / 180) * (-180 + -90 * (9 / 11))), r2 + btwSJ + ((c1 - c0) - btwSJ) * sin((pi / 180) * (-180 + -90 * (9 / 11))), DOT),
                Node('12-8.D3', c1 - btwSJ + ((c1 - c0) - btwSJ) * cos((pi / 180) * (-180 + -90 * (8 / 11))), r2 + btwSJ + ((c1 - c0) - btwSJ) * sin((pi / 180) * (-180 + -90 * (8 / 11))), DOT),
                Node('12-8.D4', c1 - btwSJ + ((c1 - c0) - btwSJ) * cos((pi / 180) * (-180 + -90 * (7 / 11))), r2 + btwSJ + ((c1 - c0) - btwSJ) * sin((pi / 180) * (-180 + -90 * (7 / 11))), DOT),
                Node('12-8.D5', c1 - btwSJ + ((c1 - c0) - btwSJ) * cos((pi / 180) * (-180 + -90 * (6 / 11))), r2 + btwSJ + ((c1 - c0) - btwSJ) * sin((pi / 180) * (-180 + -90 * (6 / 11))), DOT),
                Node('12-8.D6', c1 - btwSJ + ((c1 - c0) - btwSJ) * cos((pi / 180) * (-180 + -90 * (5 / 11))), r2 + btwSJ + ((c1 - c0) - btwSJ) * sin((pi / 180) * (-180 + -90 * (5 / 11))), DOT),
                Node('12-8.D7', c1 - btwSJ + ((c1 - c0) - btwSJ) * cos((pi / 180) * (-180 + -90 * (4 / 11))), r2 + btwSJ + ((c1 - c0) - btwSJ) * sin((pi / 180) * (-180 + -90 * (4 / 11))), DOT),
                Node('12-8.D8', c1 - btwSJ + ((c1 - c0) - btwSJ) * cos((pi / 180) * (-180 + -90 * (3 / 11))), r2 + btwSJ + ((c1 - c0) - btwSJ) * sin((pi / 180) * (-180 + -90 * (3 / 11))), DOT),
                Node('12-8.D9', c1 - btwSJ + ((c1 - c0) - btwSJ) * cos((pi / 180) * (-180 + -90 * (2 / 11))), r2 + btwSJ + ((c1 - c0) - btwSJ) * sin((pi / 180) * (-180 + -90 * (2 / 11))), DOT),
                Node('12-8.D10', c1 - btwSJ + ((c1 - c0) - btwSJ) * cos((pi / 180) * (-180 + -90 * (1 / 11))), r2 + btwSJ + ((c1 - c0) - btwSJ) * sin((pi / 180) * (-180 + -90 * (1 / 11))), DOT),
                Node('8S', c0, r2 + btwSJ, JUNCTION),
                
                
                
                
           ]
    
    Edges = [Edge(findNode('1'), findNode('1E')), Edge(findNode('1S'), findNode('1')),
            Edge(findNode('2W'), findNode('2')), Edge(findNode('2E'), findNode('2')), Edge(findNode('2'), findNode('2S')),
            Edge(findNode('3'), findNode('3W')), Edge(findNode('3'), findNode('3E')), Edge(findNode('3S'), findNode('3')),
            Edge(findNode('4E'), findNode('4')), Edge(findNode('4'), findNode('4S')), Edge(findNode('4'), findNode('4N')),
            Edge(findNode('5'), findNode('5E')), Edge(findNode('5'), findNode('5W')), Edge(findNode('5S'), findNode('5')), Edge(findNode('5N'), findNode('5')),
            Edge(findNode('6E'), findNode('6')), Edge(findNode('6W'), findNode('6')), Edge(findNode('6'), findNode('6S')), Edge(findNode('6'), findNode('6N')),
            Edge(findNode('7'), findNode('7W')), Edge(findNode('7S'), findNode('7')), Edge(findNode('7N'), findNode('7')),
            Edge(findNode('8'), findNode('8E')), Edge(findNode('8S'), findNode('8')), Edge(findNode('8N'), findNode('8')),
            Edge(findNode('9E'), findNode('9')), Edge(findNode('9W'), findNode('9')), Edge(findNode('9'), findNode('9S')), Edge(findNode('9'), findNode('9N')),
            Edge(findNode('10'), findNode('10E')), Edge(findNode('10'), findNode('10W')), Edge(findNode('10S'), findNode('10')), Edge(findNode('10N'), findNode('10')),
            Edge(findNode('11W'), findNode('11')), Edge(findNode('11'), findNode('11S')), Edge(findNode('11'), findNode('11N')),
            Edge(findNode('12'), findNode('12E')), Edge(findNode('12'), findNode('12W')), Edge(findNode('12N'), findNode('12')),
            Edge(findNode('13W'), findNode('13')), Edge(findNode('13E'), findNode('13')), Edge(findNode('13'), findNode('13N')),
            Edge(findNode('14'), findNode('14W')), Edge(findNode('14N'), findNode('14')),
              
            Edge(findNode('1E'), findNode('2W')), Edge(findNode('3W'), findNode('2E')),
            Edge(findNode('4N'), findNode('1S')), Edge(findNode('2S'), findNode('5N')), Edge(findNode('6N'), findNode('3S')),
            Edge(findNode('5W'), findNode('4E')), Edge(findNode('5E'), findNode('6W')), Edge(findNode('7W'), findNode('6E')),
            Edge(findNode('4S'), findNode('8N')), Edge(findNode('9N'), findNode('5S')), Edge(findNode('6S'), findNode('10N')), Edge(findNode('11N'), findNode('7S')),
            Edge(findNode('8E'), findNode('9W')), Edge(findNode('10W'), findNode('9E')), Edge(findNode('10E'), findNode('11W')),
            Edge(findNode('9S'), findNode('12N')), Edge(findNode('13N'), findNode('10S')), Edge(findNode('11S'), findNode('14N')),
            Edge(findNode('12E'), findNode('13W')), Edge(findNode('14W'), findNode('13E')),
            
            
            Edge(findNode('1S'), findNode('1E')),
            Edge(findNode('2E'), findNode('2S')), Edge(findNode('2W'), findNode('2S')),
            Edge(findNode('3S'), findNode('3E')), Edge(findNode('3S'), findNode('3W')),
            Edge(findNode('4E'), findNode('4S')), Edge(findNode('4E'), findNode('4N')),
            Edge(findNode('5S'), findNode('5E')), Edge(findNode('5S'), findNode('5W')), Edge(findNode('5N'), findNode('5E')), Edge(findNode('5N'), findNode('5W')),
            Edge(findNode('6E'), findNode('6S')), Edge(findNode('6W'), findNode('6S')), Edge(findNode('6E'), findNode('6N')), Edge(findNode('6W'), findNode('6N')),
            Edge(findNode('7S'), findNode('7W')), Edge(findNode('7N'), findNode('7W')),
            Edge(findNode('8S'), findNode('8E')), Edge(findNode('8N'), findNode('8E')),
            Edge(findNode('9E'), findNode('9S')), Edge(findNode('9W'), findNode('9S')), Edge(findNode('9E'), findNode('9N')), Edge(findNode('9W'), findNode('9N')),
            Edge(findNode('10S'), findNode('10E')), Edge(findNode('10S'), findNode('10W')), Edge(findNode('10N'), findNode('10E')), Edge(findNode('10N'), findNode('10W')),
            Edge(findNode('11W'), findNode('11S')), Edge(findNode('11W'), findNode('11N')),
            Edge(findNode('12N'), findNode('12E')), Edge(findNode('12N'), findNode('12W')),
            Edge(findNode('13E'), findNode('13N')), Edge(findNode('13W'), findNode('13N')),
            Edge(findNode('14N'), findNode('14W')),
            
            Edge(findNode('3E'), findNode('3-7.D1')), Edge(findNode('3-7.D1'), findNode('3-7.D2')), Edge(findNode('3-7.D2'), findNode('3-7.D3')),
            Edge(findNode('3-7.D3'), findNode('3-7.D4')), Edge(findNode('3-7.D4'), findNode('3-7.D5')), Edge(findNode('3-7.D5'), findNode('3-7.D6')),
            Edge(findNode('3-7.D6'), findNode('3-7.D7')), Edge(findNode('3-7.D7'), findNode('3-7.D8')), Edge(findNode('3-7.D8'), findNode('3-7.D9')),
            Edge(findNode('3-7.D9'), findNode('3-7.D10')), Edge(findNode('3-7.D10'), findNode('3-7.D11')), Edge(findNode('3-7.D11'), findNode('7N')),
            
            Edge(findNode('12W'), findNode('12-8.D1')), Edge(findNode('12-8.D1'), findNode('12-8.D2')), Edge(findNode('12-8.D2'), findNode('12-8.D3')),
            Edge(findNode('12-8.D3'), findNode('12-8.D4')), Edge(findNode('12-8.D4'), findNode('12-8.D5')), Edge(findNode('12-8.D5'), findNode('12-8.D6')),
            Edge(findNode('12-8.D6'), findNode('12-8.D7')), Edge(findNode('12-8.D7'), findNode('12-8.D8')),Edge(findNode('12-8.D8'), findNode('12-8.D9')),
            Edge(findNode('12-8.D9'), findNode('12-8.D10')),Edge(findNode('12-8.D10'), findNode('8S')),
            
            
             ]    

    return Nodes, Edges


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

IdleState_time = 0.0
ApproachingState_time = 0.0
TransitingState_time = 0.0
ParkingState_time = 0.0

NumOfCustomerArrivals = 0

#---------------------------------------------------------------------
# Classes

class Node():
    BIG_NUM = 1000000
    def __init__(self, _id, px, py, nodeType):
        self.id = _id
        self.px, self.py = px, py
        self.nodeType = nodeType
        
        self.edges_inward = []
        self.edges_outward = []
        
    def init_node(self):
        self.visited = False
        self.visitiedCount = 0
        self.min_d = Node.BIG_NUM
    
    def __repr__(self):
        return '%s' % (self.id)
    
class Edge():
    _id = 0
    def __init__(self, _from, _to, maxSpeed=6):
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
        return '(C%d) %s->%s' % (self.id, self.sn.id, self.dn.id)

ST_IDLE, ST_APPROACHING, ST_TRANSITING, ST_PARKING = 0, 1, 2, 3

class PRT():
    _id = 0
    def __init__(self, init_node):
        self.id = PRT._id
        PRT._id += 1
        self.arrived_n = init_node
        self.px, self.py = self.arrived_n.px, self.arrived_n.py
        
        self.state = ST_IDLE
        self.stateChangingPoint = 0.0
        self.assigned_customer = None
        self.transporting_customer = None
        self.event_seq = []
        
        self.last_planed_time = 0.0
        self.path_n, self.path_e = [], []
    
    def __repr__(self):
        return 'PRT%d(S%d-%s)' % (self.id, self.state, self.arrived_n.id)
    
    def set_stateChange(self, state, cur_time):
        self.state, self.stateChangingPoint = state, cur_time
    
    def find_target_event_inEventSeq(self, cur_time, target_prt, event_name, args=None):
        if isinstance(args, Customer):
            for evt in target_prt.event_seq[::-1]:
                if evt[1] == event_name and evt[2] == args:
                    assert evt[0] >= cur_time
                    return evt  
            else:
                assert False
        else:
            for i, evt in enumerate(target_prt.event_seq[::-1]):
                if evt[1] == event_name:
                    assert evt[0] >= cur_time and target_prt.event_seq[len(target_prt.event_seq) - 2 - i][1] == args
                    return evt, target_prt.event_seq[len(target_prt.event_seq) - 2 - i]
            else:
                assert False
    
    def modify_passed_assignedPRT_event(self, cur_time, prev_PRT, target_c):
        # Modify event of tager_c's previous assigned PRT which is already scheduled
        if not prev_PRT:
            return None
        else:
            logger('                    There is the prev PRT for the target customer: %s' % (prev_PRT))
            if prev_PRT.assigned_customer == target_c:
                # Change event of On_ApproachingToTransiting on prev_PRT's event_seq
                A2T_EVT = self.find_target_event_inEventSeq(cur_time, prev_PRT, prev_PRT.On_ApproachingToTransiting, target_c)
                assert A2T_EVT 
                A2T_EVT[1] = None
                x = [cur_time, prev_PRT.On_ApproachingToParking, target_c]
                prev_PRT.event_seq.append(x)
                prev_PRT.On_ApproachingToParking(cur_time, target_c)
            else:
                assert prev_PRT.assigned_customer != target_c
    
    def re_assign_customer(self, cur_time, target_c):
        if self.state == ST_IDLE :
            if self.arrived_n != target_c.sn:
                # Idle -> Approaching
                x = [cur_time, self.On_IdleToApproaching, target_c]
                self.event_seq.append(x)
                self.On_IdleToApproaching(cur_time, target_c)
            else:
                # self.arrived_n == target_c.sn
                # Idle -> Transiting
                x = [cur_time, self.On_IdleToTransiting, target_c]
                self.event_seq.append(x)
                self.On_IdleToTransiting(cur_time, target_c)
        elif self.state == ST_APPROACHING:
            if self.assigned_customer != target_c:
                # Approaching -> Approaching
                # Even though this PRT approaching assigned customer
                # the PRT assigned to target_c has been changed
                x = [cur_time, self.On_ApproachingToApproaching, target_c]
                self.event_seq.append(x)
                self.On_ApproachingToApproaching(cur_time, target_c)
            else:
                # There is no assigned customer change
                assert self.assigned_customer == target_c
        elif self.state == ST_PARKING:
            if self.event_seq[-1][1] == self.On_ParkingToIdle and self.event_seq[-2][1] == self.On_ApproachingToParking:
                # This PRT temporally becomes parking state, but it is going to be approaching soon
                # This situation can be happened, because an assignment is processed by step by step
                x = [cur_time, self.On_ApproachingToApproaching, target_c]
                self.event_seq.append(x)
                self.On_ApproachingToApproaching(cur_time, target_c)
            else:
                assert False
        else:
            assert self.state == ST_TRANSITING
    
    def On_IdleToApproaching(self, cur_time, target_c):
        logger('%.1f:    On_I2A - %s, assigned customer %s' % (cur_time, self, target_c))
        assert self.state == ST_IDLE
        prev_PRT = target_c.assigned_PRT
        
        # Measure update
        global IdleState_time
        IdleState_time += cur_time - self.stateChangingPoint
        
        # State update
        self.set_stateChange(ST_APPROACHING, cur_time)
        self.assigned_customer = target_c
        target_c.assigned_PRT = self
        
        # Set things for next state
        self.path_n, self.path_e = Algorithms.find_SP(self.arrived_n, self.assigned_customer.sn, Nodes)
        self.last_planed_time = cur_time
        evt_change_point = cur_time + sum(e.distance for e in self.path_e) / PRT_SPEED
        x = [evt_change_point, self.On_ApproachingToTransiting, target_c]
        self.event_seq.append(x)
        heappush(event_queue, x)

        logger('            path: %s' % (self.path_n))
        
        # Modify event of tager_c's previous assigned PRT which is already scheduled
        self.modify_passed_assignedPRT_event(cur_time, prev_PRT, target_c)
    
    def On_IdleToTransiting(self, cur_time, target_c):
        logger('%.1f:    On_I2T - %s, picking up customer-%s' % (cur_time, self, target_c))
        assert self.state == ST_IDLE
        prev_PRT = target_c.assigned_PRT
        
        # Measure update
        global IdleState_time, Total_empty_travel_distance, Total_travel_distance, Total_customers_flow_time, NumOfPickedUpCustomer, NumOfServicedCustomer
        IdleState_time += cur_time - self.stateChangingPoint
        NumOfPickedUpCustomer += 1
        update_customerWaitingTimeMeasure(cur_time, -1)
            
        # State update
        self.set_stateChange(ST_TRANSITING, cur_time)
        self.transporting_customer = remove_A_customerInWaitingList(target_c)
        assert self.transporting_customer
        self.transporting_customer.assigned_PRT = self
        
        # Set things for next state
        self.path_n, self.path_e = Algorithms.find_SP(self.transporting_customer.sn, self.transporting_customer.dn, Nodes)
        self.last_planed_time = cur_time
        evt_change_point = cur_time + sum(e.distance for e in self.path_e) / PRT_SPEED
        x = [evt_change_point, self.On_TransitingToIdle, target_c]
        self.event_seq.append(x)
        heappush(event_queue, x)
        
        logger('            path: %s' % (self.path_n))
        
        # Modify event of tager_c's previous assigned PRT which is already scheduled
        self.modify_passed_assignedPRT_event(cur_time, prev_PRT, target_c)

    def On_ApproachingToApproaching(self, cur_time, target_c):
        if self.state == ST_PARKING:
            # This PRT temporally becomes parking state, but it is going to be approaching soon
            # This situation can be happened, because an assignment is processed by step by step
            P2I_EVT, A2P_EVT = self.find_target_event_inEventSeq(cur_time, self, self.On_ParkingToIdle, self.On_ApproachingToParking)
            P2I_EVT[1], A2P_EVT[1] = None, None
            self.state = ST_APPROACHING
        logger('%.1f:    On_A2A - %s, prev_c:%s - new_c:%s' % (cur_time, self, self.assigned_customer, target_c))
        assert self.state == ST_APPROACHING
        prev_customer = self.assigned_customer
        prev_PRT = target_c.assigned_PRT
        
        # Measure update
        global ApproachingState_time
        ApproachingState_time += cur_time - self.stateChangingPoint
        
        # State update
        self.set_stateChange(ST_APPROACHING, cur_time)
        self.assigned_customer = target_c
        target_c.assigned_PRT = self
        
        # Set things for next state
        travel_distance = (cur_time - self.last_planed_time) * PRT_SPEED
        _, next_n, xth = Algorithms.find_PRT_position_on_PATH(self.path_e, travel_distance)
        remain_dis = sum(e.distance for e in self.path_e[:xth]) - travel_distance
        
        if next_n == target_c.sn:
            # There is no need to change modification of path
            evt_change_point = cur_time + remain_dis / PRT_SPEED
        else:
            path_n_Rerouted, path_e_Rerouted = Algorithms.find_SP(next_n, target_c.sn, Nodes)
            self.path_n = self.path_n + path_n_Rerouted[1:]
            self.path_e = self.path_e + path_e_Rerouted
            evt_change_point = cur_time + (remain_dis + sum(e.distance for e in path_e_Rerouted)) / PRT_SPEED
        x = [evt_change_point, self.On_ApproachingToTransiting, target_c]
        self.event_seq.append(x)
        heappush(event_queue, x)
        logger('            path: %s' % (self.path_n))
        logger('            now, around N%d' % (next_n.id))
        
        # Modify event of tager_c's previous assigned PRT which is already scheduled
        self.modify_passed_assignedPRT_event(cur_time, prev_PRT, target_c)
        if prev_customer:
            A2T_EVT = self.find_target_event_inEventSeq(cur_time, self, self.On_ApproachingToTransiting, prev_customer)        
            A2T_EVT[1] = None        
    
    def On_ApproachingToTransiting(self, cur_time, target_c):
        logger('%.1f:    On_A2T - %s, picking up customer - %s' % (cur_time, self, target_c))
        assert self.state == ST_APPROACHING and self.assigned_customer == target_c
        
        # Measure update
        global ApproachingState_time, NumOfPickedUpCustomer, Total_empty_travel_distance, Total_travel_distance
        ApproachingState_time += cur_time - self.stateChangingPoint
        NumOfPickedUpCustomer += 1
        travel_distance = (cur_time - self.last_planed_time) * PRT_SPEED
        Total_empty_travel_distance += travel_distance 
        Total_travel_distance += travel_distance
        update_customerWaitingTimeMeasure(cur_time, -1)
        
        # State update
        self.set_stateChange(ST_TRANSITING, cur_time)
        self.arrived_n = self.assigned_customer.sn
        self.transporting_customer = remove_A_customerInWaitingList(self.assigned_customer)
        assert self.transporting_customer
        self.assigned_customer = None
        
        # Set things for next state
        self.path_n, self.path_e = Algorithms.find_SP(self.transporting_customer.sn, self.transporting_customer.dn, Nodes)
        self.last_planed_time = cur_time
        evt_change_point = cur_time + sum(e.distance for e in self.path_e) / PRT_SPEED
        x = [evt_change_point, self.On_TransitingToIdle, target_c]
        self.event_seq.append(x)
        heappush(event_queue, x)
        
        logger('            path: %s' % (self.path_n))

    def On_ApproachingToParking(self, cur_time, target_c):
        logger('%.1f:    On_A2P - %s, lost %s, ori Path: %s' % (cur_time, self, target_c, self.path_n))
        assert self.state == ST_APPROACHING and self.assigned_customer == target_c
        
        # Measure update
        global ApproachingState_time 
        ApproachingState_time += cur_time - self.stateChangingPoint
        
        # State update
        self.set_stateChange(ST_PARKING, cur_time)
        self.assigned_customer = None
        
        # Set things for next state
        travel_distance = (cur_time - self.last_planed_time) * PRT_SPEED
        _, next_n, xth = Algorithms.find_PRT_position_on_PATH(self.path_e, travel_distance)
        remain_dis = sum(e.distance for e in self.path_e[:xth]) - travel_distance
        self.path_n, self.path_e = self.path_n[:xth + 1], self.path_e[:xth]
        evt_change_point = cur_time + remain_dis / PRT_SPEED
        x = [evt_change_point, self.On_ParkingToIdle, None]
        self.event_seq.append(x)
        heappush(event_queue, x)
        
        logger('            parking node: %s' % (self.path_n[-1].id))

    def On_TransitingToIdle(self, cur_time, target_c):
        logger('%.1f:    On_T2I - %s' % (cur_time, self))    
        assert self.state == ST_TRANSITING
        
        # Measure update
        global TransitingState_time, NumOfServicedCustomer, Total_travel_distance, Total_customers_flow_time
        TransitingState_time += cur_time - self.stateChangingPoint
        NumOfServicedCustomer += 1
        travel_distance = (cur_time - self.last_planed_time) * PRT_SPEED
        Total_travel_distance += travel_distance
        Total_customers_flow_time += cur_time - target_c.arriving_time
        
        # State update
        self.set_stateChange(ST_IDLE, cur_time)
        self.arrived_n = self.transporting_customer.dn
        self.transporting_customer = None
        
        # Set things for next state
        self.path_n, self.path_e = None, None
        self.last_planed_time = cur_time
        dispatcher(cur_time, PRTs, waiting_customers, Nodes)
        
    def On_ParkingToIdle(self, cur_time, args=None):
        logger('%.1f:    On_P2I - %s, arriving node: %d' % (cur_time, self, self.path_n[-1].id))
        assert self.state == ST_PARKING
        
        # Measure update
        global ParkingState_time, Total_travel_distance, Total_empty_travel_distance
        ParkingState_time += cur_time - self.stateChangingPoint
        travel_distance = (cur_time - self.last_planed_time) * PRT_SPEED
        Total_empty_travel_distance += travel_distance
        Total_travel_distance += travel_distance
        
        # State update
        self.set_stateChange(ST_IDLE, cur_time)
        self.arrived_n = self.path_n[-1]
        
        # Set things for next state
        self.path_n, self.path_e = None, None
        self.last_planed_time = cur_time
        
    def On_ParkingToApproaching(self, cur_time, target_c):
        logger('%.1f:    On_P2A - %s, assigned customer %s' % (cur_time, self, target_c))
        assert self.state == ST_PARKING
        prev_PRT = target_c.assigned_PRT
        
        # Measure update
        global ParkingState_time
        ParkingState_time += cur_time - self.stateChangingPoint
        
        # State update
        self.set_stateChange(ST_APPROACHING, cur_time)
        
        # Set things for next state
        travel_distance = (cur_time - self.last_planed_time) * PRT_SPEED
        remain_dis = sum(e.distance for e in self.path_e) - travel_distance
        next_n = self.path_n[-1]
        if next_n == target_c.sn:
            # There is no need to change modification of path
            evt_change_point = cur_time + remain_dis / PRT_SPEED
        else:
            path_n_Rerouted, path_e_Rerouted = Algorithms.find_SP(next_n, target_c.sn, Nodes)
            self.path_n = self.path_n + path_n_Rerouted[1:]
            self.path_e = self.path_e + path_e_Rerouted
            evt_change_point = cur_time + (remain_dis + sum(e.distance for e in path_e_Rerouted)) / PRT_SPEED
        
        x = [evt_change_point, self.On_ApproachingToTransiting, target_c]
        self.event_seq.append(x)
        heappush(event_queue, x)
        
        # Modify event of tager_c's previous assigned PRT which is already scheduled
        self.modify_passed_assignedPRT_event(cur_time, prev_PRT, target_c)

#---------------------------------------------------------------------
# Generate things such as Network, PRT, Customer

def gen_Network(ns, ns_connection):
    Nodes = [Node(px, py, isStation) for px, py, isStation in ns]
    Edges = []
    for pn, nn in ns_connection:
        Edges.append(Edge(Nodes[pn], Nodes[nn]))
    return Nodes, Edges

def gen_Customer(average_arrival, num_customers, Nodes):
    seed(1)
    accu_pd = []
    pd = [expovariate(1.0 / average_arrival) for _ in range(num_customers)]
    for i, t in enumerate(pd):
        if i == 0:
            accu_pd.append(t)
            continue
        accu_pd.append(accu_pd[-1] + t)
    
    Customers = []
    for t in accu_pd:
        sn, dn = 0, 0
        while sn == dn or Nodes[sn].nodeType != STATION or Nodes[dn].nodeType != STATION:
            sn = randrange(len(Nodes))
            dn = randrange(len(Nodes))
        Customers.append(Customer(t, Nodes[sn], Nodes[dn]))
        
    customerArrivals_txt = open('Info. Arrivals of customers.txt', 'w')
    for c in Customers:
        t, sn, dn = c.arriving_time, c.sn.id, c.dn.id 
        customerArrivals_txt.write('%f,%s-%s\n' % (t, sn, dn))
    customerArrivals_txt.close()
        
    return Customers

def gen_PRT(numOfPRT, Nodes):
    PRTs = []
    for _ in range(numOfPRT):
        target_n_id = randrange(len(Nodes)) 
        while Nodes[target_n_id].nodeType != STATION:
            target_n_id = randrange(len(Nodes)) 
        PRTs.append(PRT(Nodes[target_n_id]))
    return PRTs

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

def update_customerWaitingTimeMeasure(cur_time, numOfCustomerChange):
    global Total_customers_waiting_time, NumOfWaitingCustomer, ChaningPointOfNWC, MaxCustomerWaitingTime  
    # Update measure
    customers_waiting_time = NumOfWaitingCustomer * (cur_time - ChaningPointOfNWC)
    if customers_waiting_time > MaxCustomerWaitingTime:
         MaxCustomerWaitingTime = customers_waiting_time
    Total_customers_waiting_time += customers_waiting_time 
    
    # Memorize things for the next calculation
    NumOfWaitingCustomer += numOfCustomerChange
    ChaningPointOfNWC = cur_time

def On_CustomerArrival(cur_time, target_c):
    logger('%.1f: On_CustomerArrival - %s' % (cur_time, target_c))
    customer = Customers.pop(0)
    assert customer == target_c
    waiting_customers.append(customer)
    
    # Measure update
    update_customerWaitingTimeMeasure(cur_time, 1)
    global NumOfCustomerArrivals
    NumOfCustomerArrivals += 1
    
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

def remove_A_customerInWaitingList(target_customer):
    # Remove servicing customer in waiting_customer
    for i, customer in enumerate(waiting_customers):
        if customer == target_customer:
            return waiting_customers.pop(i)

#---------------------------------------------------------------------
def test():
    from time import sleep
    import Network
    
    # Generate all inputs: Network, Arrivals of customers, PRTs
#     Nodes, Edges = gen_Network(*Network.network0())
    Nodes, Edges = Network1()
    Customers = gen_Customer(10.5, 2000, Nodes)
    PRTs = gen_PRT(10, Nodes)
#     path_n, path_e = Algorithms.find_SP(findNode('5E'), findNode('14'), Nodes) 
    
#     print path_n, path_e
#     assert False
    
    # Choose dispatcher
#     dispatcher = Algorithms.NN0
#     dispatcher = Algorithms.NN1
#     dispatcher = Algorithms.NN2
#     dispatcher = Algorithms.NN3
#     dispatcher = Algorithms.NN4
    dispatcher = Algorithms.NN5
    
    init_dynamics(Nodes, PRTs, Customers, dispatcher)
    
    now = 0.0
    while process_events(now):
        now += 1
        sleep(0.0001)

    print        
    print 'Measure------------------------------------------------------------------------------------------------'
    print 'T.TravedDist: %.1f, T.E.TravelDist: %.1f, T.FlowTime: %.1f, T.WaitTime: %.1f' % (Total_travel_distance, Total_empty_travel_distance, Total_customers_flow_time, Total_customers_waiting_time)
    
    print 'IdleState_time: %.1f, ApproachingState_time: %.1f, TransitingState_time: %.1f, ParkingState_time: %.1f' % (IdleState_time, ApproachingState_time, TransitingState_time, ParkingState_time)

def tests():
    from time import sleep
    import Network
    
    # Generage all inputs: Network, Arrivals of customers, PRTs
    Nodes, Edges = gen_Network(*Network.network0())
    for meanArrival, numOfCustomer, numOfPRT in [(4.0, 2000, 11), (1.0, 4000, 12), (10.5, 2000, 6), (3.0, 2000, 20), ]:
        for NN in [Algorithms.NN0, Algorithms.NN1, Algorithms.NN2, Algorithms.NN3, Algorithms.NN4, Algorithms.NN5]:
            dispatcher = NN
            Customers = gen_Customer(meanArrival, numOfCustomer, Nodes)
            PRTs = gen_PRT(numOfPRT, Nodes)
            
            init_dynamics(Nodes, PRTs, Customers, dispatcher)
            
            now = 0.0
            while process_events(now):
                now += 1
                
            print        
            print 'Measure------------------------------------------------------------------------------------------------'
            print 'T.TravedDist: %.1f, T.E.TravelDist: %.1f, T.FlowTime: %.1f, T.WaitTime: %.1f' % (Total_travel_distance, Total_empty_travel_distance, Total_customers_flow_time, Total_customers_waiting_time)
            
            print 'IdleState_time: %.1f, ApproachingState_time: %.1f, TransitingState_time: %.1f, ParkingState_time: %.1f' % (IdleState_time, ApproachingState_time, TransitingState_time, ParkingState_time)    
if __name__ == '__main__':
    test()
#     tests()
