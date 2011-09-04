'''
Created on 2010-11-12

The algorithm for berth planning
sort_vessel_list: sort the vessel according to their eta.
original_sort_vessel_list: get the information from db

'''
import Interface
import parameter
import Upperbound
import Lowerbound
import Getfeasible
import time
import QC_schedule

def sort_vessel_list(selected_vessel_list):
    ## step 1
    ## step 1.1 sort vessels in the increasing order of eta
    sorted_vessel_list = []
    vessel_list = Interface.get_vessel_list(selected_vessel_list)
    num_of_vessel = len(vessel_list)
    for i in range(num_of_vessel):
        min_eta = parameter.M
        current_vessel = Interface.Vessel
        for vessel in vessel_list:
            if vessel.eta < min_eta:
                min_eta = vessel.eta
                current_vessel = vessel
        sorted_vessel_list.append(current_vessel)
        vessel_list.remove(current_vessel)
    ## for test    
    ##for i in sorted_vessel_list:
    ##    print i.eta
    for vessel in sorted_vessel_list:
        print vessel.id, vessel.eta, vessel.etd, vessel.favorite_position, vessel.length, vessel.min_qc, vessel.max_qc, vessel.total_operation, vessel.qc_for_due
    return sorted_vessel_list


def original_sort_vessel_list():
    sorted_vessel_list = []
    vessel_list = Interface.original_get_vessel_list()
    num_of_vessel = len(vessel_list)
    for i in range(num_of_vessel):
        min_eta = parameter.M
        current_vessel = Interface.Vessel
        for vessel in vessel_list:
            if vessel.eta < min_eta:
                min_eta = vessel.eta
                current_vessel = vessel
        sorted_vessel_list.append(current_vessel)
        vessel_list.remove(current_vessel)
    ## for test    
    ##for i in sorted_vessel_list:
    ##    print i.eta
    for vessel in sorted_vessel_list:
        print vessel.id, vessel.eta, vessel.etd, vessel.favorite_position, vessel.length, vessel.min_qc, vessel.max_qc, vessel.total_operation, vessel.qc_for_due
    return sorted_vessel_list

    
    
def update_pi(sorted_vessel_list, time_segment, pi_j_list, pi_ij_list, lamada, Zub, Zlb):
    G_j_list = []
    for j in range(time_segment):
        G_j = 0
        for vessel in sorted_vessel_list:
            if vessel.berthing_time <= j + 1 and vessel.berthing_time + vessel.berthing_range - 1 >= j + 1 :
                G_j = G_j + vessel.seed[j - vessel.berthing_time + 1]
        G_j = G_j - Interface.num_of_qc
        G_j_list.append(G_j)
    G_ij_list = []
    for j in range(time_segment):
        G_ij_j_list = []
        for i in range(parameter.length_of_berth):
            G_ij= 0
            for vessel in sorted_vessel_list:
                if vessel.berthing_time <= j+1 and vessel.berthing_time + vessel.berthing_range - 1 >= j+1 and vessel.berthing_location <= i+1 and vessel.berthing_location + vessel.length - 1 >= i+1:
                    G_ij = G_ij +1
            G_ij = G_ij - 1
            G_ij_j_list.append(G_ij)
        G_ij_list.append(G_ij_j_list)
    
    sum_of_gj = 0
    for gj in G_j_list:
        sum_of_gj = sum_of_gj + gj*gj
    a1 = lamada*(Zub-Zlb)/sum_of_gj
    #print lamada, (Zub-Zlb), sum_of_gj
    sum_of_gij = 0
    for j in G_ij_list:
        for i in j:
            sum_of_gij = sum_of_gij + i*i
    a2 = lamada*(Zub-Zlb)/sum_of_gij
    #print "a", a1, a2
    for j in range(len(pi_j_list)):
        pi_j = pi_j_list[j]
        new_pi = pi_j + a1*G_j_list[j]
        if new_pi >0:
            pi_j_list[j] = new_pi
        else:
            pi_j_list[j] = 0
    
    for j in range(len(pi_ij_list)):
        for i in range(parameter.length_of_berth):
            pi_ij = pi_ij_list[j][i]
            new_pi = pi_ij + a2*G_ij_list[j][i]
            if new_pi >0:
                pi_ij_list[j][i] = new_pi
            else:
                pi_ij_list[j][i] = 0
   # print pi_j_list
    #print pi_ij_list
    return pi_j_list, pi_ij_list
    
def save_result(sorted_vessel_list):
    for vessel in sorted_vessel_list:
        vessel.best_berthing_location = vessel.berthing_location
        vessel.best_berthing_time = vessel.berthing_time
        vessel.best_seed = vessel.seed
        vessel.best_berthing_range = vessel.berthing_range  


def show_result(sorted_vessel_list, time_segment):
    print 
    print_list=[]
    for i in range(time_segment):
        print_list.append([0]*parameter.length_of_berth)
    
    for vessel in sorted_vessel_list:
        for b in range(vessel.length):
            for t in range(vessel.best_berthing_range):
                print_list[t+vessel.best_berthing_time-1][b+vessel.best_berthing_location-1] = vessel.best_seed[t]
    
    #print_list.reverse()
    for t in range(len(print_list)):
        for b in range(len(print_list[t])):
            if print_list[t][b]==0:
                print " ",
            else:
                print print_list[t][b],
        print " "
    

def run_algorithm(selected_vessel_list):
    time0=time.time()
    sorted_vessel_list = original_sort_vessel_list()
    Zub, time_segment = Upperbound.get_upper_bound(sorted_vessel_list)
    time_segment_for_get_feasible = time_segment + parameter.extra_time
    
    sorted_vessel_list = sort_vessel_list(selected_vessel_list)
    Zub, time_segment = Upperbound.get_upper_bound(sorted_vessel_list)
    #print time_segment
    
    time_segment = time_segment + parameter.extra_time
    pi_j_list = [0]*time_segment
    pi_ij_list = []
    for i in range(time_segment):
        pi_ij_list.append([0]*parameter.length_of_berth)
    
    lamada = 2.0
    Zmax = -1
    
    #for i in range(2):
    while(lamada>=0.005):  
        Zlb = Lowerbound.get_lower_bound(sorted_vessel_list,time_segment, pi_j_list, pi_ij_list)
        if Zlb > Zmax :
            Zmax = Zlb
            lamada = 2.0
            save_result(sorted_vessel_list)
            #print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        else:
            lamada = lamada / 2
        pi_j_list, pi_ij_list = update_pi(sorted_vessel_list, time_segment, pi_j_list, pi_ij_list, lamada, Zub, Zlb)
        #print "next loop"
    print Zmax
    for vessel in sorted_vessel_list:
        print vessel.best_berthing_location,vessel.best_berthing_time,vessel.best_seed 
    planned_vessel_list = Interface.get_planned_vessel_list()
    
    #From infeasible to feasible
    Getfeasible.get_feasible(time_segment_for_get_feasible, sorted_vessel_list)
    print "Final result: "
    for vessel in sorted_vessel_list:
        print vessel.best_berthing_location,vessel.best_berthing_time,vessel.best_seed
    
    try:
        Interface.update_db_berth(sorted_vessel_list)
    except:
        pass 
    
    #show_result(sorted_vessel_list, time_segment)
    
    print time.time()-time0
    
    sorted_vessel_list.extend(planned_vessel_list)
    QC_schedule.qc_schedule(sorted_vessel_list)
    
    return sorted_vessel_list


if __name__=='__main__':
    run_algorithm()
    
    
    
    
    