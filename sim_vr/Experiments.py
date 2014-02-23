from __future__ import division
import data, Dynamics, Algorithms
from random import seed
from time import time, ctime

logger_pass = lambda x: None

NumOfTotalCustomer = 0

Total_travel_distance, Total_empty_travel_distance = (0.0,) * 2
NumOfCustomerArrivals, NumOfPickedUpCustomer, NumOfServicedCustomer = (0,) * 3
Total_customers_flow_time, Total_customers_waiting_time, MaxCustomerWaitingTime = (0.0,) * 3
distances, customersWaitingtimes = [], []
stateTimes = {'I' : 0.0, 'A' : 0.0, 'S' : 0.0, 'T' : 0.0, 'P' : 0.0}
Total_boarding_waiting_time = 0.0
data_accu_st, data_accu_et = (0.0,) * 2 

def on_notify_customer_arrival(customer):
    if Dynamics.NumOfCustomerArrivals == int(NumOfTotalCustomer / 10):
        Dynamics.Total_travel_distance, Dynamics.Total_empty_travel_distance = (0.0,) * 2
        Dynamics.NumOfWaitingCustomer, Dynamics.NumOfPickedUpCustomer, Dynamics.NumOfServicedCustomer = (0,) * 3
        Dynamics.Total_customers_flow_time, Dynamics.Total_customers_waiting_time = (0.0,) * 2
        Dynamics.MaxCustomerWaitingTime = 0.0
        Dynamics.distances, Dynamics.customersWaitingtimes = [], []
        
        for k in Dynamics.stateTimes.iterkeys():
            Dynamics.stateTimes[k] = 0.0
        
        Dynamics.Total_boarding_waiting_time = 0.0
        
        global data_accu_st
        data_accu_st = customer.arriving_time

    if Dynamics.NumOfCustomerArrivals == NumOfTotalCustomer:
        global Total_travel_distance, Total_empty_travel_distance
        global distances
        global NumOfCustomerArrivals, NumOfPickedUpCustomer, NumOfServicedCustomer
        global Total_customers_flow_time, Total_customers_waiting_time, MaxCustomerWaitingTime
        global stateTimes
        global Total_boarding_waiting_time
        
        Total_travel_distance = Dynamics.Total_travel_distance
        Total_empty_travel_distance = Dynamics.Total_empty_travel_distance
        
        NumOfCustomerArrivals = Dynamics.NumOfCustomerArrivals - int(NumOfTotalCustomer / 10)
        NumOfPickedUpCustomer = Dynamics.NumOfPickedUpCustomer
        NumOfServicedCustomer = Dynamics.NumOfServicedCustomer
        
        Total_customers_flow_time = Dynamics.Total_customers_flow_time 
        Total_customers_waiting_time = Dynamics.Total_customers_waiting_time
        MaxCustomerWaitingTime = Dynamics.MaxCustomerWaitingTime 
        
        for k in Dynamics.stateTimes.iterkeys():
            stateTimes[k] = Dynamics.stateTimes[k]
        
        Total_boarding_waiting_time = Dynamics.Total_boarding_waiting_time 
        
        global data_accu_et
        data_accu_et = customer.arriving_time
        Dynamics.end_dynamics()
        print '-------------------------------------------------------------------------------'
        
        print 'Total_travel_distance', Total_travel_distance
        print 'Total_empty_travel_distance', Total_empty_travel_distance
        
        print 'NumOfCustomerArrivals', NumOfCustomerArrivals
        print 'NumOfPickedUpCustomer', NumOfPickedUpCustomer
        print 'NumOfServicedCustomer', NumOfServicedCustomer
        
        print 'Total_customers_flow_time', Total_customers_flow_time 
        print 'Total_customers_waiting_time', Total_customers_waiting_time
        print 'MaxCustomerWaitingTime', MaxCustomerWaitingTime 
        
        for k in stateTimes.iterkeys():
            print '%s state', stateTimes[k]
        
        print 'Total_boarding_waiting_time', Total_boarding_waiting_time
        
        assert False
     
    print customer

def profile_solve():
    import cProfile, pstats
    args = (60.0, 500, 0.8, 80)
    dispatcher = Algorithms.NN5
    cProfile.runctx('run(0, 0, dispatcher, *args)', globals(), locals(), 'log/profile')
    s = pstats.Stats('log/profile')
    s.strip_dirs().sort_stats('cumulative', 'time').print_stats()

def run_excelWriteVersion(dispatchers, meanTimeArrivals, numOfPRTs):
    from tempfile import TemporaryFile
    from xlwt import Workbook
    book = Workbook()
    sheet1 = book.add_sheet('Sheet 1')
    row1 = sheet1.row(0)
    compuTime, TTDist, ATDist, TETDist, AETDist, TWTime, AWTime, MWTime, TFTime, AFTime, Idle, Approaching, Setting, Transiting, Parking, TBT, ABT, DN, mTA, NOP = range(20)
    colNames = [
                'CTime',
                'T.TravedDist',
                'A.TravedDist',
                'T.E.TravedDist',
                'A.E.TravedDist',
                'T.W.Time',
                'A.W.Time',
                'M.W.Time',
                'T.F.Time',
                'A.F.Time',
                'I.Time',
                'A.Time',
                'S.Time',
                'T.Time',
                'P.Time',
                'T.B.Time',
                'A.B.Time',
                'dispatcher',
                'meanTimeArrivals',
                'numOfPRTs',
                ]
    
    for i, CN in enumerate(colNames):
        row1.write(i, CN)
    
    Dynamics.logger = logger_pass 
    Algorithms.on_notify_assignmentment_point = logger_pass  
    Dynamics.on_notify_customer_arrival = on_notify_customer_arrival
    
    seed(2)
    #---------------------------------------------------------------------
    # parameter setting
    NUM_PRT = 50
    NUM_CUSTOMER = 10  # 5000
    CUSTOMER_ARRIVAL_INTERVAL = 100.2
    
    PRT_SPEED = 12  # unit (m/s)
    S2J_SPEED = 6
    J2D_SPEED = 9
    SETTING_TIME = (45.0, 60.0)  # unit (sec)
    
    ex = 1
    for nPRTs in numOfPRTs:
        for MTA in meanTimeArrivals:
            for dispatcher in dispatchers:
                row = sheet1.row(ex)        
                row.write(DN, dispatcher.__name__)
                row.write(mTA, MTA)
                row.write(NOP, nPRTs)
                
                Network = data.Network1(S2J_SPEED, J2D_SPEED)
                Customers, PRTs = data.gen_instances(Network, CUSTOMER_ARRIVAL_INTERVAL, NUM_CUSTOMER, NUM_PRT, PRT_SPEED)
                global NumOfTotalCustomer
                NumOfTotalCustomer = len(Customers)
                
                st = time()
                Dynamics.run(SETTING_TIME, PRT_SPEED, Network, PRTs, Customers, dispatcher)
                et = time() - st
                
                global NumOfCustomerArrivals, Total_empty_travel_distance, NumOfPickedUpCustomer, Total_travel_distance, Total_customers_flow_time, NumOfServicedCustomer, Total_customers_waiting_time, MaxCustomerWaitingTime
                global IdleState_time, ApproachingState_time, SettingState_time, TransitingState_time, ParkingState_time, Total_boarding_waiting_time, data_accu_st, data_accu_et
                
                row.write(compuTime, round(et, 2))
                
                row.write(TTDist, round(Total_travel_distance, 2))
                row.write(ATDist, round((Total_travel_distance / NumOfServicedCustomer), 2))
                row.write(TETDist, round(Total_empty_travel_distance, 2))
                row.write(AETDist, round((Total_empty_travel_distance / NumOfPickedUpCustomer), 2))
                row.write(TWTime, round(Total_customers_waiting_time, 2))
                row.write(AWTime, round((Total_customers_waiting_time / NumOfCustomerArrivals), 2))
                row.write(MWTime, round(MaxCustomerWaitingTime, 2))
                row.write(TFTime, round(Total_customers_flow_time, 2))
                row.write(AFTime, round((Total_customers_flow_time / NumOfServicedCustomer), 2))
                
                row.write(Idle, round(stateTimes['I'], 2))
                row.write(Approaching, round(stateTimes['A'], 2))
                row.write(Setting, round(stateTimes['S'], 2))
                row.write(Transiting, round(stateTimes['T'], 2))
                row.write(Parking, round(stateTimes['P'], 2))
                
                row.write(TBT, round(Total_boarding_waiting_time, 2))
                row.write(ABT, round((Total_boarding_waiting_time / NumOfServicedCustomer), 2))
                
                ex += 1
                
    book.save('dynamicsResults10.xls')
    book.save(TemporaryFile())

if __name__ == '__main__':
    dispatcher = Algorithms.get_all_dispatchers().values()
#     meanTimeArrival = (3.5, )
#     meanTimeArrival = (4.1, )
    meanTimeArrival = (5.0,)
    numOfPRTs = [40, ]
    
    run_excelWriteVersion(dispatcher[2:3], meanTimeArrival, numOfPRTs)
