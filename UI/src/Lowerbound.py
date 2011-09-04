'''
Created on 2010-11-14

This is used for berth planning algorithm.
To calculate the lower bound
'''
import parameter
import Interface
def get_lower_bound(vessel_list,time_segment, pi_j, pi_ij):
    sum_of_objective = 0
    for vessel in vessel_list:
        min_objective = decomposed_primal_problems(vessel, time_segment, pi_j, pi_ij)
        #print min_objective
        sum_of_objective = sum_of_objective + min_objective


    sum_of_pi_ij = 0
    for i in pi_ij:
        for j in i:
            sum_of_pi_ij = sum_of_pi_ij + j
    sum_of_pi_j = 0
    for i in pi_j:
        sum_of_pi_j = sum_of_pi_j + i 
    sum_of_objective = sum_of_objective - sum_of_pi_ij - sum_of_pi_j * Interface.num_of_qc
    Zlb = sum_of_objective
    #print "Zlb", Zlb
    return Zlb  




def decomposed_primal_problems(vessel, time_segment, pi_j, pi_ij):
    min_objective = parameter.M
    min_t = 0
    min_b = 0
    min_seed = []
    improve = True 
    while(improve==True):
        improve = False
        neighbor_list = []
        for t in range(time_segment):
            for b in range(parameter.length_of_berth - vessel.length + 1):
                neighbor_list.append([b+1,t+1])

        for i in range(len(neighbor_list)):
            cur_b, cur_t = neighbor_list[i]

            objective = abs(cur_b - vessel.favorite_position)*parameter.penalty_of_not_at_favorite_position
            if vessel.eta > cur_t:
                objective = objective + parameter.penalty_of_arrival_before*(vessel.eta - cur_t)
            else:
                objective = objective + parameter.penalty_of_arrival_after*(cur_t - vessel.eta)
            if objective < min_objective:
                min_objective_at_one_position, new_seed = get_min_objective_at_one_position(cur_b, cur_t, vessel, pi_j, pi_ij)
                #print (min_objective_at_one_position+objective) , min_objective
                if (min_objective_at_one_position+objective) < min_objective:
                    min_objective = min_objective_at_one_position+objective
                    min_t = cur_t
                    min_b = cur_b
                    min_seed = new_seed                        
                    improve = True
                    #print min_b, min_t, min_seed, min_objective
    #print "each vessel result, ", min_b, min_t, min_seed, min_objective
    vessel.berthing_time = min_t
    vessel.berthing_position = min_b
    vessel.seed = min_seed
    vessel.berthing_range = len(min_seed)
    return min_objective


        
def get_min_objective_at_one_position(cur_b, cur_t, vessel, pi_j, pi_ij):
    time_with_min_qc = vessel.total_operation/vessel.min_qc
    if vessel.total_operation%vessel.min_qc != 0:
        time_with_min_qc = time_with_min_qc + 1
    
    time_with_max_qc = vessel.total_operation/vessel.max_qc
    if vessel.total_operation%vessel.max_qc != 0:
        time_with_max_qc = time_with_max_qc + 1
    
    seed_list = []
    for time in range(time_with_max_qc, time_with_min_qc):
        qc_assign_list = []
        get_seed(vessel.total_operation, time, qc_assign_list)
        seed_list.append(qc_assign_list)
    reverse_seed_list = []
    for seed in seed_list:
        if vessel.total_operation % len(seed) != 0:
            reverse_seed = seed[:]
            reverse_seed.reverse()
            reverse_seed_list.append(reverse_seed)
    
    seed_list = seed_list + reverse_seed_list
    
    min_value = parameter.M
    min_seed = []
    for seed in seed_list:
        
        value = get_seed_value(seed, cur_b, cur_t, vessel, pi_j, pi_ij)
        #print seed, value
        if value < min_value :
            min_value = value
            min_seed = seed
    #print cur_b, cur_t, min_seed,
    #print "////////", min_value
    return min_value, min_seed
        
        
# last 3 item of (10)
def get_seed_value(seed, cur_b, cur_t, vessel, pi_j, pi_ij):
    value = 0
    departure_time = cur_t + len(seed)
    if departure_time > vessel.etd:
        value = value + parameter.penalty_of_delay_beyond_due * (departure_time - vessel.etd)
    if departure_time-1 >= len(pi_ij):
        return parameter.M

    for t in range(cur_t, departure_time):
        for b in range(cur_b, cur_b+vessel.length):
            #print t,b
            value = value + pi_ij[t-1][b-1]     
   
    for i in range(len(seed)):
       # if len(seed) ==4:
        #    print "test, ",pi_j[cur_t+i-1]  ,          
                
        value = value + pi_j[cur_t+i-1]*seed[i]
    #if len(seed) ==4:
     #   print "test, ",value            
    return value
        

def get_seed(num_of_jobs, time, qc_assign_list):
    if time == 1:
        qc_assign_list.append(num_of_jobs)
    else:
        job_each_time = num_of_jobs / time
        if num_of_jobs % time !=0:
            job_each_time = job_each_time + 1
        qc_assign_list.append(job_each_time)
        get_seed(num_of_jobs-job_each_time, time-1, qc_assign_list)
    