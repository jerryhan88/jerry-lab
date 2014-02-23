from __future__ import division
import data, Dynamics, Algorithms
from random import seed
from time import time, ctime

logger_pass = lambda x: None

NumOfTotalCustomer = 0
NumOfCustomerArrivals = 0

Total_empty_travel_distance = 0.0
NumOfPickedUpCustomer = 0

Total_travel_distance = 0.0
Total_customers_flow_time = 0.0
NumOfServicedCustomer = 0

Total_customers_waiting_time = 0.0
MaxCustomerWaitingTime = 0.0

stateTimes = {'I' : 0.0, 'A' : 0.0, 'S' : 0.0, 'T' : 0.0, 'P' : 0.0}

IdleState_time = 0.0
ApproachingState_time = 0.0
SettingState_time = 0.0
TransitingState_time = 0.0
ParkingState_time = 0.0

Total_boarding_waiting_time = 0.0

data_accu_st, data_accu_et= (0.0, ) * 2 

def on_notify_customer_arrival(customer):
    if Dynamics.NumOfCustomerArrivals == int(NumOfTotalCustomer / 10):
        Dynamics.Total_empty_travel_distance = 0.0
        Dynamics.NumOfPickedUpCustomer = 0
          
        Dynamics.Total_travel_distance = 0.0
        Dynamics.Total_customers_flow_time = 0.0
        Dynamics.NumOfServicedCustomer = 0
          
        Dynamics.Total_customers_waiting_time = 0.0
        Dynamics.NumOfWaitingCustomer = 0
        Dynamics.ChaningPointOfNWC = 0.0
        Dynamics.MaxCustomerWaitingTime = 0.0
          
          
        for k in Dynamics.stateTimes.iterkeys():
            Dynamics.stateTimes[k] = 0.0
        
#         Dynamics.IdleState_time = 0.0
#         Dynamics.ApproachingState_time = 0.0
#         Dynamics.SettingState_time = 0.0
#         Dynamics.TransitingState_time = 0.0
#         Dynamics.ParkingState_time = 0.0
        
        Dynamics.Total_boarding_waiting_time = 0.0
        
        global data_accu_st
        data_accu_st = customer.arriving_time

    if Dynamics.NumOfCustomerArrivals == NumOfTotalCustomer:
        global NumOfCustomerArrivals, Total_empty_travel_distance, NumOfPickedUpCustomer
        NumOfCustomerArrivals = Dynamics.NumOfCustomerArrivals - int(NumOfTotalCustomer / 10)
        Total_empty_travel_distance = Dynamics.Total_empty_travel_distance
        NumOfPickedUpCustomer = Dynamics.NumOfPickedUpCustomer
        global Total_travel_distance, Total_customers_flow_time, NumOfServicedCustomer 
        Total_travel_distance = Dynamics.Total_travel_distance 
        Total_customers_flow_time = Dynamics.Total_customers_flow_time 
        NumOfServicedCustomer = Dynamics.NumOfServicedCustomer
        global Total_customers_waiting_time, MaxCustomerWaitingTime 
        Total_customers_waiting_time = Dynamics.Total_customers_waiting_time
        MaxCustomerWaitingTime = Dynamics.MaxCustomerWaitingTime 
#         global IdleState_time, ApproachingState_time, SettingState_time, TransitingState_time, ParkingState_time
        global stateTimes
        
        IdleState_time = Dynamics.IdleState_time 
        ApproachingState_time = Dynamics.ApproachingState_time
        SettingState_time = Dynamics.SettingState_time 
        TransitingState_time = Dynamics.TransitingState_time
        ParkingState_time = Dynamics.ParkingState_time
        
        global Total_boarding_waiting_time
        Total_boarding_waiting_time = Dynamics.Total_boarding_waiting_time 
        
        global data_accu_et
        data_accu_et = customer.arriving_time
        print '-------------------------------------------------------------------------------'
     
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
    NUM_CUSTOMER = 10#5000
    CUSTOMER_ARRIVAL_INTERVAL = 4.2
    
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
                row.write(Idle, round(IdleState_time, 2))
                row.write(Approaching, round(ApproachingState_time, 2))
                row.write(Setting, round(SettingState_time, 2))
                row.write(Transiting, round(TransitingState_time, 2))
                row.write(Parking, round(ParkingState_time, 2))
                row.write(TBT, round(Total_boarding_waiting_time, 2))
                row.write(ABT, round((Total_boarding_waiting_time / NumOfServicedCustomer), 2))
                
                ex += 1
                
    book.save('dynamicsResults10.xls')
    book.save(TemporaryFile())

if __name__ == '__main__':
    dispatcher = Algorithms.get_all_dispatchers().values()
#     meanTimeArrival = (3.5, )
#     meanTimeArrival = (4.1, )
    meanTimeArrival = (5.0, )
    numOfPRTs = [40, ]
    
    run_excelWriteVersion(dispatcher[2:3], meanTimeArrival, numOfPRTs)
