'''
This is used for berth planning algorithm.
To calculate the upper bound
'''

import parameter
import Interface
def get_upper_bound(sorted_vessel_list):

    ## step 1.2, 1.3
    berth_time_state = []
    qc_state = []
    for vessel in sorted_vessel_list:
        vessel.berthing_location = vessel.favorite_position
        vessel.berthing_time = vessel.eta
        extend_time = vessel.etd - len(berth_time_state)
        if extend_time > 0:
            for i in range(extend_time):
                berth_time_state.append([0]*(parameter.length_of_berth+1))
                qc_state.append(0)

        request_berth_time = get_request_berth_time(vessel.favorite_position, vessel.berthing_time + vessel.etd - vessel.eta,vessel.favorite_position+vessel.length -1, vessel.berthing_time)
        while(check_overlap(berth_time_state, request_berth_time) or check_beyond_total_qc(qc_state, vessel)):
            vessel.berthing_time = vessel.berthing_time + 1
            extend_time = vessel.berthing_time + vessel.etd - vessel.eta - len(berth_time_state)
            if extend_time > 0:
                berth_time_state.append([0]*parameter.length_of_berth)
                qc_state.append(0)
            request_berth_time = get_request_berth_time(vessel.favorite_position, vessel.berthing_time + vessel.etd - vessel.eta,vessel.favorite_position+vessel.length, vessel.berthing_time)
        
        berth_time_state = update_berth_time_state(vessel, berth_time_state)
    
    ## for test
    print "Berthing_begin_time: ",    
    for i in sorted_vessel_list:
        print i.berthing_time,
    print ' '
      
    ## step 1.4
    Zub = 0
    for vessel in sorted_vessel_list:
        Zub = Zub + (parameter.penalty_of_arrival_after + parameter.penalty_of_delay_beyond_due) * (vessel.berthing_time - vessel.eta)
    print "Upper bound: ", Zub
    time_segment = len(berth_time_state)
    return Zub, time_segment
        
def update_berth_time_state(vessel, berth_time_state):
    for b in range(vessel.length):
        for t in range(vessel.etd-vessel.eta):
            berth_time_state[t+vessel.berthing_time][b+vessel.favorite_position] = 1
    return berth_time_state
        
def check_overlap(berth_state, request_area):
    for b,t in request_area:
        if berth_state[t][b] == 1:
            return True
    return False 


def check_beyond_total_qc(qc_state, vessel):
    for t in range(vessel.etd-vessel.eta):
        if qc_state[t+vessel.berthing_time] + vessel.qc_for_due > Interface.num_of_qc:
            return True
    return False
    
    
    
def get_request_berth_time(x1,y1,x2,y2):
    request_berth_time = []
    for t in range(y1-y2):
        for b in range(x2-x1):
            request_berth_time.append([x1+b,y2+t])

    return request_berth_time

