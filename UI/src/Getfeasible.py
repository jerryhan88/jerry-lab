'''
Created on 2010-11-14

This is used for berth planning algorithm.
To check the feasibility of solutions.
'''

import parameter
import Interface

def chech_beyond_totoal_qc(qc_state, vessel):
    for t in range(vessel.best_berthing_range):
        if qc_state[t+vessel.best_berthing_time] + vessel.best_seed[t] > Interface.num_of_qc:
            return True
    return False
    
    
def get_request_berth_time(x1,y1,x2,y2):
    request_berth_time = []
    for t in range(y1-y2):
        for b in range(x2-x1):
            request_berth_time.append([x1+b,y2+t])

    return request_berth_time


def check_overlap(berth_state, request_area):
    for b,t in request_area:
        if berth_state[t][b] == 1:
            return True
    return False 


def check_length(length, begin_time, begin_position, berth_time_state):
    for i in range(length):
        if berth_time_state[begin_time][begin_position+i]==1:
            return False
    return True


def get_possible_time_range(vessel, begin_time, begin_position, berth_time_state, time_segment):
    max_time_range = 1
    for t in range(time_segment-begin_time):
        if_ok = True
        for b in range(vessel.length):
            if berth_time_state[begin_time + t][begin_position + b]==1:
                if_ok = False
                break
        if if_ok:
            max_time_range = max_time_range +1
        else:
            return max_time_range
    return max_time_range
    
    
##possible_position(location, time, max_time_range)
def get_possible_position(vessel, berth_time_state, time_segment):
    possible_position = []
    for t in range(time_segment):
        for b in range(parameter.length_of_berth - vessel.length + 1):
            if check_length(vessel.length, t+1, b+1, berth_time_state):
                max_time_range = get_possible_time_range(vessel, t+1, b+1, berth_time_state, time_segment)
                possible_position.append([b+1,t+1, max_time_range])
    return possible_position
                

def solve_primal(vessel, time_segment, berth_time_state, qc_state):
    min_objective = parameter.M
    min_t = 0
    min_b = 0
    min_seed = []
    possible_position = get_possible_position(vessel, berth_time_state, time_segment)
    #possible_position = [[29, 1, 13]]
    for i in range(len(possible_position)):
        cur_b, cur_t, max_range = possible_position[i]

        time_with_max_qc = vessel.total_operation/vessel.max_qc
        if vessel.total_operation%vessel.max_qc != 0:
            time_with_max_qc = time_with_max_qc + 1
        
        time_with_min_qc = vessel.total_operation/vessel.min_qc
        if vessel.total_operation%vessel.min_qc != 0:
            time_with_min_qc = time_with_min_qc + 1
        if max_range >= time_with_max_qc:
            objective = abs(cur_b - vessel.favorite_position)*parameter.penalty_of_not_at_favorite_position
            if vessel.eta > cur_t:
                objective = objective + parameter.penalty_of_arrival_before*(vessel.eta - cur_t)
            else:
                objective = objective + parameter.penalty_of_arrival_after*(cur_t - vessel.eta)

            if objective < min_objective:
                if max_range>time_with_min_qc:
                    min_objective_at_one_position, seed = get_min_objective_at_one_position(cur_b, cur_t, vessel, time_with_min_qc, time_with_max_qc, qc_state )
                else:
                    min_objective_at_one_position, seed = get_min_objective_at_one_position(cur_b, cur_t, vessel, max_range, time_with_max_qc,qc_state )
                if (min_objective_at_one_position+objective) < min_objective:
                    min_objective = min_objective_at_one_position+objective
                    min_t = cur_t
                    min_b = cur_b
                    min_seed=seed
    return min_t, min_b, min_seed[:]
    
        
def update_berth_time_state(vessel, berth_time_state):
    for b in range(vessel.length):
        for t in range(vessel.best_berthing_range):
            berth_time_state[t+vessel.best_berthing_time][b+vessel.best_berthing_location] = 1
    return berth_time_state
        
        
def get_min_objective_at_one_position(cur_b, cur_t, vessel, max_range, time_with_max_qc, qc_state):
   
    seed_list0 = []
    for time in range(time_with_max_qc, max_range):
        qc_assign_list = []
        get_seed(vessel.total_operation, time, qc_assign_list)
        seed_list0.append(qc_assign_list)
    
    reverse_seed_list = []
    for seed in seed_list0:
        if vessel.total_operation % len(seed) != 0:
            reverse_seed = seed[:]
            reverse_seed.reverse()
            reverse_seed_list.append(reverse_seed)
    
    seed_list0 = seed_list0 + reverse_seed_list
    seed_list=[]
    for seed in seed_list0:
        if seed_need_more_qc(seed, qc_state, cur_t)==False:
            seed_list.append(seed)
    min_value = parameter.M
    min_seed = []
    for seed in seed_list:
        value = 0
        departure_time = cur_t + len(seed)-1
        if departure_time > vessel.etd:
            value = value + parameter.penalty_of_delay_beyond_due * (departure_time - vessel.etd)
        if value < min_value :
            min_value = value
            min_seed = seed
    return min_value, min_seed
        
def seed_need_more_qc(seed, qc_state, cur_t):
    for i in range(len(seed)):
        if seed[i]+qc_state[cur_t+i]>Interface.num_of_qc:
            return True
    else:
        return False

def get_seed(num_of_jobs, time, qc_assign_list):
    if time == 1:
        qc_assign_list.append(num_of_jobs)
    else:
        job_each_time = num_of_jobs / time
        if num_of_jobs % time !=0:
            job_each_time = job_each_time + 1
        qc_assign_list.append(job_each_time)
        get_seed(num_of_jobs-job_each_time, time-1, qc_assign_list)

def update_qc_state(vessel, qc_state):
    for t in range(vessel.best_berthing_range):
        qc_state[vessel.best_berthing_time+t]+= vessel.best_seed[t]
        
    return qc_state

def get_feasible(time_segment, sorted_vessel_list):
    feasible_list = Interface.get_planned_vessel_list()
    infeasible_list = []
    berth_time_state = []
    qc_state = []
    for i in range(time_segment+1):
        berth_time_state.append([0]*(parameter.length_of_berth+1))
        qc_state.append(0)
    for vessel in sorted_vessel_list:
        request_berth_time=get_request_berth_time(vessel.best_berthing_location, vessel.best_berthing_time + vessel.best_berthing_range-1 ,vessel.best_berthing_location + vessel.length -1, vessel.best_berthing_time)
        if check_overlap(berth_time_state, request_berth_time) or chech_beyond_totoal_qc(qc_state, vessel):
            infeasible_list.append(vessel)
        else:
            berth_time_state = update_berth_time_state(vessel, berth_time_state)
            qc_state = update_qc_state(vessel, qc_state)
            feasible_list.append(vessel)
            
    print "Feasible: "
    for vessel in feasible_list:
        print vessel.best_berthing_location,vessel.best_berthing_time,vessel.best_seed 
        
    print "Infeasible: "
    for vessel in infeasible_list:
        print vessel.best_berthing_location,vessel.best_berthing_time,vessel.best_seed 
    
        
    for vessel in infeasible_list:
        min_t, min_b, min_seed = solve_primal(vessel, time_segment, berth_time_state, qc_state)
        vessel.best_berthing_time = min_t
        vessel.best_berthing_location = min_b
        vessel.best_seed = min_seed[:]
        vessel.best_berthing_range = len(min_seed)
        feasible_list.append(vessel)
        berth_time_state = update_berth_time_state(vessel, berth_time_state)
        qc_state = update_qc_state(vessel, qc_state)
        

        