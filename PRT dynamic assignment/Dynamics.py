from __future__ import division
from math import sqrt
from random import uniform
from heapq import heappush, heappop
import Algorithms

#---------------------------------------------------------------------
# node type and states of PRT
TRANSFER, STATION, JUNCTION, DOT = range(4)
ST_IDLE, ST_APPROACHING, ST_SETTING, ST_TRANSITING, ST_PARKING = range(5)
SETTING_TIME = None
PRT_SPEED = None

# event queue for simulation and current customers in system (simulation)
waiting_customers = []
event_queue = []

#---------------------------------------------------------------------
# For calculating measure
WaitingCustomerChanges = []
WaitingTimeChanges = []

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
SettingState_time = 0.0
TransitingState_time = 0.0
ParkingState_time = 0.0

Total_boarding_waiting_time = 0.0

NumOfCustomerArrivals = 0

# check arrival of customer
on_notify_customer_arrival = lambda x: None

def findNode(nID):
    for n in Nodes:
        if n.id == nID:
            return n
    else:
        False

# Classes
class Node():
    BIG_NUM = 1000000
    def __init__(self, _id, px, py, nodeType, numOfBerth=0):
        self.id = _id
        self.px, self.py = px, py
        self.nodeType = nodeType
        self.numOfBerth = numOfBerth
        self.no = None
        self.settingPRTs = []
        self.setupWaitingPRTs = []
        
        self.edges_inward = []
        self.edges_outward = []
        
    def init_node(self):
        self.visited = False
        self.visitiedCount = 0
        self.minTime = Node.BIG_NUM
    
    def __repr__(self):
        return '%s' % (self.id)
    
class Edge():
    _id = 0
    def __init__(self, _from, _to, maxSpeed=12):
        self.id = Edge._id
        Edge._id += 1
        self._from, self._to = _from, _to
        self.maxSpeed = maxSpeed
        
        delX = self._from.px - self._to.px
        delY = self._from.py - self._to.py
        self.distance = sqrt(delX * delX + delY * delY)
        
        self._from.edges_outward.append(self)
        self._to.edges_inward.append(self)
        
    def __repr__(self):
        return '%s->%s' % (self._from.id, self._to.id)

class Customer():
    def __init__(self, _id, arriving_time, sn, dn):
        self.id = _id
        self.arriving_time = arriving_time
        self.sn, self.dn = sn, dn
        
        self.assigned_PRT = None
        self.isSetupWaiting = False
        self.boardingWaitingStartTime = 0.0
    
    def __repr__(self):
        return '(C%d) %s->%s' % (self.id, self.sn.id, self.dn.id)

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
        self.isSetupWaiting = False
        
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
    
    def check_settingPRTs_inNode(self, evt, cur_time, target_c):
        targetS = None
        if evt == 'T2I' or evt == 'A2S':
            targetS = self.path_n[-1]
        else:
            assert evt == 'I2S'
            targetS = self.arrived_n
        assert len(targetS.settingPRTs) <= targetS.numOfBerth
            
        # new arrival PRT
        if len(targetS.settingPRTs) >= targetS.numOfBerth:
            self.isSetupWaiting = True
            target_c.isSetupWaiting = True
            target_c.boardingWaitingStartTime = cur_time
            targetS.setupWaitingPRTs.append(self)
            return False
        else:
            self.isSetupWaiting = False
            target_c.isSetupWaiting = False
            if target_c.boardingWaitingStartTime:
                target_c.boardingWaitingTime = cur_time - target_c.boardingWaitingStartTime
            else:
                target_c.boardingWaitingTime = 0
            return True
    
    def modify_passed_assignedPRT_event(self, cur_time, prev_PRT, target_c):
        # Modify event of tager_c's previous assigned PRT which is already scheduled
        if not prev_PRT:
            return None
        else:
            logger('                    There is the prev PRT for the target customer: %s' % (prev_PRT))
            if prev_PRT.assigned_customer == target_c:
                # Change event of On_ApproachingToTransiting on prev_PRT's event_seq
                A2T_EVT = self.find_target_event_inEventSeq(cur_time, prev_PRT, prev_PRT.On_ApproachingToSetting, target_c)
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
                x = [cur_time, self.On_IdleToSetting, target_c]
                self.event_seq.append(x)
                self.On_IdleToSetting(cur_time, target_c)
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
    
    def On_IdleToSetting(self, cur_time, target_c):
        logger('%.1f:    On_I2S - %s, ready for customer %s' % (cur_time, self, target_c))
        assert self.state == ST_IDLE
        
        if not self.check_settingPRTs_inNode('I2S', cur_time, target_c):
            return None
        
        prev_PRT = target_c.assigned_PRT
        
        # Measure update
        global IdleState_time, Total_empty_travel_distance, Total_travel_distance, Total_customers_flow_time, NumOfPickedUpCustomer, NumOfServicedCustomer
        IdleState_time += cur_time - self.stateChangingPoint
        NumOfPickedUpCustomer += 1
        update_customerWaitingTimeMeasure(cur_time, -1)
            
        # State update
        self.set_stateChange(ST_SETTING, cur_time)
        self.transporting_customer = remove_A_customerInWaitingList(target_c)
        assert self.transporting_customer
        self.transporting_customer.assigned_PRT = self
        self.arrived_n.settingPRTs.append(self)
        
        # Set things for next state
        evt_change_point = cur_time + uniform(*SETTING_TIME)
        x = [evt_change_point, self.On_SettingToTransiting, target_c]
        self.event_seq.append(x)
        heappush(event_queue, x)
        
        # Modify event of tager_c's previous assigned PRT which is already scheduled
        self.modify_passed_assignedPRT_event(cur_time, prev_PRT, target_c)
    
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
        self.path_n, self.path_e = Algorithms.find_SP(self.arrived_n.no, self.assigned_customer.sn.no)
        self.last_planed_time = cur_time
        global PRT_SPEED
        evt_change_point = cur_time + sum(e.distance / min(PRT_SPEED, e.maxSpeed) for e in self.path_e)
        x = [evt_change_point, self.On_ApproachingToSetting, target_c]
        self.event_seq.append(x)
        heappush(event_queue, x)

        logger('            path: %s' % (self.path_n))
        
        # Modify event of tager_c's previous assigned PRT which is already scheduled
        self.modify_passed_assignedPRT_event(cur_time, prev_PRT, target_c)

    def On_ApproachingToSetting(self, cur_time, target_c):
        logger('%.1f:    On_A2S - %s, ready for customer %s' % (cur_time, self, target_c))
        assert self.state == ST_APPROACHING and self.assigned_customer == target_c
        
        if not self.check_settingPRTs_inNode('A2S', cur_time, target_c):
            return None
        
        # Measure update
        global ApproachingState_time, NumOfPickedUpCustomer, Total_empty_travel_distance, Total_travel_distance
        ApproachingState_time += cur_time - self.stateChangingPoint
        NumOfPickedUpCustomer += 1
        travel_distance = sum(e.distance for e in self.path_e)
        Total_empty_travel_distance += travel_distance 
        Total_travel_distance += travel_distance
        update_customerWaitingTimeMeasure(cur_time, -1)
        
        # State update
        self.set_stateChange(ST_SETTING, cur_time)
        self.arrived_n = self.assigned_customer.sn
        self.transporting_customer = remove_A_customerInWaitingList(self.assigned_customer)
        assert self.transporting_customer
        self.assigned_customer = None
        self.arrived_n.settingPRTs.append(self)
        
        
        # Set things for next state
        evt_change_point = cur_time + uniform(*SETTING_TIME)
        x = [evt_change_point, self.On_SettingToTransiting, target_c]
        self.event_seq.append(x)
        heappush(event_queue, x)
    
    def On_SettingToTransiting(self, cur_time, target_c):
        logger('%.1f:    On_S2T - %s, picking up customer-%s' % (cur_time, self, target_c))
        assert self.state == ST_SETTING
        
        # Measure update
        global SettingState_time
        SettingState_time += cur_time - self.stateChangingPoint
            
        # State update
        self.set_stateChange(ST_TRANSITING, cur_time)
        # Update settingPRTs in target node
        self.arrived_n.settingPRTs.remove(self)
        
        # Set things for next state
        self.path_n, self.path_e = Algorithms.find_SP(self.transporting_customer.sn.no, self.transporting_customer.dn.no)
        self.last_planed_time = cur_time
        global PRT_SPEED
        evt_change_point = cur_time + sum(e.distance / min(PRT_SPEED, e.maxSpeed) for e in self.path_e)
        x = [evt_change_point, self.On_TransitingToIdle, target_c]
        self.event_seq.append(x)
        heappush(event_queue, x)
        
        logger('            path: %s' % (self.path_n))
        
        # # check setupWaitingPRT
        
        if self.arrived_n.setupWaitingPRTs:
            firstWaitingPRT = self.arrived_n.setupWaitingPRTs.pop(0)
            firstWaitingPRT.event_seq[-1][1](cur_time, firstWaitingPRT.event_seq[-1][2])

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
        path_travel_time = cur_time - self.last_planed_time
        _, next_n, xth = Algorithms.find_PRT_position_on_PATH(self.path_e, path_travel_time)
        global PRT_SPEED
        remain_travel_time = sum(e.distance / min(PRT_SPEED, e.maxSpeed) for e in self.path_e[:xth]) - path_travel_time
        
        
        if next_n == target_c.sn:
            # There is no need to change modification of path
            evt_change_point = cur_time + remain_travel_time
        else:
            path_n_Rerouted, path_e_Rerouted = Algorithms.find_SP(next_n.no, target_c.sn.no)
            self.path_n = self.path_n[:xth] + path_n_Rerouted[1:]
            self.path_e = self.path_e[:xth] + path_e_Rerouted
            evt_change_point = cur_time + remain_travel_time + sum(e.distance / min(PRT_SPEED, e.maxSpeed) for e in path_e_Rerouted)
        x = [evt_change_point, self.On_ApproachingToSetting, target_c]
        self.event_seq.append(x)
        heappush(event_queue, x)
        logger('            path: %s' % (self.path_n))
        logger('            now, around %s' % (next_n.id))
        
        # Modify event of tager_c's previous assigned PRT which is already scheduled
        self.modify_passed_assignedPRT_event(cur_time, prev_PRT, target_c)
        if prev_customer:
            A2T_EVT = self.find_target_event_inEventSeq(cur_time, self, self.On_ApproachingToSetting, prev_customer)        
            A2T_EVT[1] = None        

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
        path_travel_time = cur_time - self.last_planed_time
        _, next_n, xth = Algorithms.find_PRT_position_on_PATH(self.path_e, path_travel_time)
        global PRT_SPEED
        remain_travel_time = sum(e.distance / min(PRT_SPEED, e.maxSpeed) for e in self.path_e[:xth]) - path_travel_time
        
        if next_n.nodeType == STATION or next_n.nodeType == TRANSFER:
            path_n_to_nearStation, path_e_to_nearStation = [next_n], []
        else:
            if next_n.nodeType != JUNCTION:
                _, _, NextJ_id = next_n.id.split('-')
            else:
                assert next_n.nodeType == JUNCTION
                NextJ_id = next_n.id
            NextS_id = NextJ_id[:-1] 
            path_n_to_nearStation, path_e_to_nearStation = Algorithms.find_SP(findNode(NextJ_id).no, findNode(NextS_id).no)
        
        evt_change_point = cur_time + remain_travel_time + sum(e.distance / min(PRT_SPEED, e.maxSpeed) for e in path_e_to_nearStation)
        self.path_n, self.path_e = self.path_n[:xth] + path_n_to_nearStation, self.path_e[:xth] + path_e_to_nearStation
        x = [evt_change_point, self.On_ParkingToIdle, None]
        self.event_seq.append(x)
        heappush(event_queue, x)
        
        logger('            parking node: %s' % (self.path_n[-1].id))
        
        assert self.path_n[-1].nodeType == STATION or self.path_n[-1].nodeType == TRANSFER

    def On_TransitingToIdle(self, cur_time, target_c):
        logger('%.1f:    On_T2I - %s, servicing customer (C%d)' % (cur_time, self, target_c.id))    
        assert self.state == ST_TRANSITING
        
        if not self.check_settingPRTs_inNode('T2I', cur_time, target_c):
            return None
        
        # Measure update
        global TransitingState_time, NumOfServicedCustomer, Total_travel_distance, Total_customers_flow_time, Total_boarding_waiting_time
        TransitingState_time += cur_time - self.stateChangingPoint
        NumOfServicedCustomer += 1
        travel_distance = sum(e.distance for e in self.path_e)
        Total_travel_distance += travel_distance
        Total_customers_flow_time += cur_time - target_c.arriving_time
        Total_boarding_waiting_time += target_c.boardingWaitingTime
        
        # State update
        self.set_stateChange(ST_IDLE, cur_time)
        self.arrived_n = self.transporting_customer.dn
        self.transporting_customer = None
        
        # Set things for next state
        self.path_n, self.path_e = None, None
        self.last_planed_time = cur_time
        dispatcher(cur_time, PRTs, waiting_customers, Nodes)
        
    def On_ParkingToIdle(self, cur_time, args=None):
        logger('%.1f:    On_P2I - %s, arriving node: %s' % (cur_time, self, self.path_n[-1].id))
        assert self.path_n[-1].nodeType == STATION or self.path_n[-1].nodeType == TRANSFER 
        assert self.state == ST_PARKING
        
        # Measure update
        global ParkingState_time, Total_travel_distance, Total_empty_travel_distance
        ParkingState_time += cur_time - self.stateChangingPoint
        travel_distance = sum(e.distance for e in self.path_e)
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
        path_travel_time = cur_time - self.last_planed_time
        _, next_n, xth = Algorithms.find_PRT_position_on_PATH(self.path_e, path_travel_time)
        global PRT_SPEED
        remain_travel_time = sum(e.distance / min(PRT_SPEED, e.maxSpeed) for e in self.path_e[:xth]) - path_travel_time
        next_n = self.path_n[-1]
        
        if next_n == target_c.sn:
            # There is no need to change modification of path
            evt_change_point = cur_time + remain_travel_time
        else:
            path_n_Rerouted, path_e_Rerouted = Algorithms.find_SP(next_n.no, target_c.sn.no)
            self.path_n = self.path_n + path_n_Rerouted[1:]
            self.path_e = self.path_e + path_e_Rerouted
            evt_change_point = cur_time + remain_travel_time + sum(e.distance / min(PRT_SPEED, e.maxSpeed) for e in path_e_Rerouted)
        x = [evt_change_point, self.On_ApproachingToSetting, target_c]
        self.event_seq.append(x)
        heappush(event_queue, x)
        
        # Modify event of tager_c's previous assigned PRT which is already scheduled
        self.modify_passed_assignedPRT_event(cur_time, prev_PRT, target_c)

def init_dynamics(_Nodes, _PRTs, _Customers, _dispatcher):
    global Total_empty_travel_distance, NumOfPickedUpCustomer, Total_travel_distance, Total_customers_flow_time, NumOfServicedCustomer  
    Total_empty_travel_distance = 0.0
    NumOfPickedUpCustomer = 0
    Total_travel_distance = 0.0
    Total_customers_flow_time = 0.0
    NumOfServicedCustomer = 0
    global Total_customers_waiting_time, NumOfWaitingCustomer, ChaningPointOfNWC, MaxCustomerWaitingTime  
    Total_customers_waiting_time = 0.0
    NumOfWaitingCustomer = 0
    ChaningPointOfNWC = 0.0
    MaxCustomerWaitingTime = 0.0
    global IdleState_time, ApproachingState_time, SettingState_time, TransitingState_time, ParkingState_time 
    IdleState_time = 0.0
    ApproachingState_time = 0.0
    SettingState_time = 0.0
    TransitingState_time = 0.0
    ParkingState_time = 0.0
    global NumOfCustomerArrivals
    NumOfCustomerArrivals = 0
    global Total_boarding_waiting_time
    Total_boarding_waiting_time = 0.0

    global Nodes, PRTs, Customers, dispatcher
    Nodes, PRTs, Customers, dispatcher = _Nodes, _PRTs, _Customers, _dispatcher
    
    for customer in Customers:
        x = [customer.arriving_time, On_CustomerArrival, customer]
        heappush(event_queue, x)

def logger(s):
    print s

def update_customerWaitingTimeMeasure(cur_time, numOfCustomerChange):
    global Total_customers_waiting_time, NumOfWaitingCustomer, ChaningPointOfNWC, MaxCustomerWaitingTime, WaitingCustomerChanges, WaitingTimeChanges

    # Update measure
    customers_waiting_time = NumOfWaitingCustomer * (cur_time - ChaningPointOfNWC)
    if customers_waiting_time > MaxCustomerWaitingTime:
        MaxCustomerWaitingTime = customers_waiting_time
    Total_customers_waiting_time += customers_waiting_time

    # Memorize things for the next calculation
    if NumOfWaitingCustomer == 0 :
        if numOfCustomerChange == -1: 
            NumOfWaitingCustomer = 0
        else:
            assert numOfCustomerChange == 1
            NumOfWaitingCustomer += numOfCustomerChange
    else:
        NumOfWaitingCustomer += numOfCustomerChange
    ChaningPointOfNWC = cur_time
    
    if WaitingCustomerChanges and WaitingCustomerChanges[-1][0] == cur_time:
        WaitingCustomerChanges.pop()
    WaitingCustomerChanges.append((cur_time, NumOfWaitingCustomer))
    
    if WaitingTimeChanges and WaitingTimeChanges[-1][0] == cur_time:
        WaitingTimeChanges.pop()
    WaitingTimeChanges.append((cur_time, Total_customers_waiting_time))
    

def On_CustomerArrival(cur_time, target_c):
    logger('%.1f: On_CustomerArrival - %s' % (cur_time, target_c))
    customer = Customers.pop(0)
    assert customer == target_c
    waiting_customers.append(customer)
    
    # Measure update
    update_customerWaitingTimeMeasure(cur_time, 1)
    global NumOfCustomerArrivals
    NumOfCustomerArrivals += 1
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
def run(_SETTING_TIME, _PRT_SPEED, Network, PRTs, Customers, dispatcher=None, useVisualizer=False):
    from time import sleep
    global SETTING_TIME, PRT_SPEED
    SETTING_TIME = _SETTING_TIME
    PRT_SPEED = _PRT_SPEED
    
    # Network
    #  Nodes, Edges = Network
    Algorithms.init_algorithms(Network[0])
    
    if useVisualizer:
        import wx, Visualizer
        app = wx.PySimpleApp()
        win = Visualizer.MainFrame(Network, PRTs, Customers)
        win.Show(True)
        app.MainLoop()
    else:
        init_dynamics(Network[0], PRTs, Customers, dispatcher)
        now = 0.0
        while process_events(now):
            now += 1
            sleep(0.0001)

if __name__ == '__main__':
    pass
