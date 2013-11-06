from __future__ import division
import Dynamics, Algorithms
from time import time, ctime

logger_pass = lambda x: None

NumOfTotalCustomer = 0

Total_empty_travel_distance = 0.0
NumOfPickedUpCustomer = 0

Total_travel_distance = 0.0
Total_customers_flow_time = 0.0
NumOfServicedCustomer = 0

Total_customers_waiting_time = 0.0
MaxCustomerWaitingTime = 0.0

IdleState_time = 0.0
ApproachingState_time = 0.0
SettingState_time = 0.0
TransitingState_time = 0.0
ParkingState_time = 0.0

data_accu_st = 0.0
data_accu_et = 0.0

def on_notify_customer_arrival(customer):
    if Dynamics.NumOfCustomerArrivals > NumOfTotalCustomer / 10:
        Dynamics.Total_empty_travel_distance = 0.0
        Dynamics.NumOfPickedUpCustomer = 0
        
        Dynamics.Total_travel_distance = 0.0
        Dynamics.Total_customers_flow_time = 0.0
        Dynamics.NumOfServicedCustomer = 0
        
        Dynamics.Total_customers_waiting_time = 0.0
        Dynamics.NumOfWaitingCustomer = 0
        Dynamics.ChaningPointOfNWC = 0.0
        Dynamics.MaxCustomerWaitingTime = 0.0
        
        Dynamics.IdleState_time = 0.0
        Dynamics.ApproachingState_time = 0.0
        Dynamics.SettingState_time = 0.0
        Dynamics.TransitingState_time = 0.0
        Dynamics.ParkingState_time = 0.0
        
        data_accu_st = customer.arriving_time

    if Dynamics.NumOfCustomerArrivals == NumOfTotalCustomer:
        Total_empty_travel_distance = Dynamics.Total_empty_travel_distance
        NumOfPickedUpCustomer = Dynamics.NumOfPickedUpCustomer
        
        Total_travel_distance = Dynamics.Total_travel_distance 
        Total_customers_flow_time = Dynamics.Total_customers_flow_time 
        NumOfServicedCustomer = Dynamics.NumOfServicedCustomer 
        
        Total_customers_waiting_time = Dynamics.Total_customers_waiting_time
        MaxCustomerWaitingTime = Dynamics.MaxCustomerWaitingTime 
        
        IdleState_time = Dynamics.IdleState_time 
        ApproachingState_time = Dynamics.ApproachingState_time
        SettingState_time = Dynamics.SettingState_time 
        TransitingState_time = Dynamics.TransitingState_time
        ParkingState_time = Dynamics.ParkingState_time
        
        data_accu_et = customer.arriving_time
     
    print customer

def run(i, j, dispatcher, meanTimeArrival, numOfArrivingCustomer, imbalanceLevel, numOfPRTs):
    # Generate all inputs: Network, Arrivals of customers, PRTs
    result_txt = open('%d-%d.txt' % (i, j), 'w')
    result_txt.write('%s_meanTimeArrival(%.1f) numOfArrivingCustomer(%d) imbalanceLevel(%.1f) numOfPRTs(%d)\n' % (str(dispatcher), meanTimeArrival, numOfArrivingCustomer, imbalanceLevel, numOfPRTs))
    Nodes, Edges = Dynamics.Network1()
    Customers = Dynamics.gen_Customer(meanTimeArrival, numOfArrivingCustomer, imbalanceLevel, Nodes)
    global NumOfTotalCustomer
    NumOfTotalCustomer = len(Customers)
    PRTs = Dynamics.gen_PRT(numOfPRTs, Nodes)
    Dynamics.init_dynamics(Nodes, PRTs, Customers, dispatcher)
    Dynamics.logger = logger_pass 
    Algorithms.on_notify_assignmentment_point = logger_pass  
    Dynamics.on_notify_customer_arrival = on_notify_customer_arrival 
    now = 1e400
    st = time()
    Dynamics.process_events(now)
    et = time() - st
    result_txt.write('%s\n' % str(ctime(st)))
    result_txt.write('computation time: %.1f\n' % (et))
    result_txt.write('\n')        
    result_txt.write('Measure------------------------------------------------------------------------------------------------\n')
    result_txt.write('T.TravedDist: %.1f\n' % (Total_travel_distance))
    result_txt.write('T.E.TravelDist: %.1f\n' % (Total_empty_travel_distance))
    result_txt.write('T.FlowTime: %.1f\n' % (Total_customers_flow_time))
    result_txt.write('T.WaitTime: %.1f\n' % (Total_customers_waiting_time))
    total_tive_flow = (data_accu_st - data_accu_et) * len(Dynamics.PRTs)
    result_txt.write('IdleState_time: %.1f(%.1f%s)\n' % (IdleState_time, IdleState_time / total_tive_flow * 100, '%'))
    result_txt.write('ApproachingState_time: %.1f(%.1f%s)\n' % (ApproachingState_time, ApproachingState_time / total_tive_flow * 100, '%'))
    result_txt.write('SettingState_time: %.1f(%.1f%s)\n' % (SettingState_time, SettingState_time / total_tive_flow * 100, '%'))
    result_txt.write('TransitingState_time: %.1f(%.1f%s)\n' % (TransitingState_time, TransitingState_time / total_tive_flow * 100, '%'))
    result_txt.write('ParkingState_time: %.1f(%.1f%s)\n' % (ParkingState_time, ParkingState_time / total_tive_flow * 100, '%'))
    result_txt.close()

def profile_solve():
    print 'Using', solve.__module__
    import cProfile, pstats
    seed(25); H, L = problem.gen_uniform(6, 8, 0.6, 9)
    cProfile.runctx('solve(H, L, hfunc2)', globals(), locals(), 'log/profile')
    s = pstats.Stats('log/profile')
    s.strip_dirs().sort_stats('cumulative', 'time').print_stats()

if __name__ == '__main__':
    meanTimeArrival = (60.0, 180.0, 300.0)
    numOfArrivingCustomer = (5000, 5000, 5000)
    imbalanceLevel = (1.0, 0.5, 0.3)
    numOfPRTs = (40, 60, 80)
    for i, args in enumerate(zip(meanTimeArrival, numOfArrivingCustomer, imbalanceLevel, numOfPRTs)):
        for j, dispatcher in enumerate([Algorithms.NN0, Algorithms.NN1, Algorithms.NN2, Algorithms.NN3, Algorithms.NN4, Algorithms.NN5]):
            run(i, j, dispatcher, *args)
