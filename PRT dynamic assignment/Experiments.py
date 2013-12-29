from __future__ import division
import Dynamics, Algorithms
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

IdleState_time = 0.0
ApproachingState_time = 0.0
SettingState_time = 0.0
TransitingState_time = 0.0
ParkingState_time = 0.0

data_accu_st = 0.0
data_accu_et = 0.0

def on_notify_customer_arrival(customer):
    if Dynamics.NumOfCustomerArrivals == int(NumOfTotalCustomer / 10):
        Dynamics.NumOfCustomerArrivals = 0
         
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
        global data_accu_st
        data_accu_st = customer.arriving_time

    if Dynamics.NumOfCustomerArrivals == NumOfTotalCustomer:
        global NumOfCustomerArrivals, Total_empty_travel_distance, NumOfPickedUpCustomer
        NumOfCustomerArrivals = Dynamics.NumOfCustomerArrivals
        Total_empty_travel_distance = Dynamics.Total_empty_travel_distance
        NumOfPickedUpCustomer = Dynamics.NumOfPickedUpCustomer
        global Total_travel_distance, Total_customers_flow_time, NumOfServicedCustomer 
        Total_travel_distance = Dynamics.Total_travel_distance 
        Total_customers_flow_time = Dynamics.Total_customers_flow_time 
        NumOfServicedCustomer = Dynamics.NumOfServicedCustomer 
        global Total_customers_waiting_time, MaxCustomerWaitingTime 
        Total_customers_waiting_time = Dynamics.Total_customers_waiting_time
        MaxCustomerWaitingTime = Dynamics.MaxCustomerWaitingTime 
        global IdleState_time, ApproachingState_time, SettingState_time, TransitingState_time, ParkingState_time
        IdleState_time = Dynamics.IdleState_time 
        ApproachingState_time = Dynamics.ApproachingState_time
        SettingState_time = Dynamics.SettingState_time 
        TransitingState_time = Dynamics.TransitingState_time
        ParkingState_time = Dynamics.ParkingState_time
        global data_accu_et
        data_accu_et = customer.arriving_time
        print '-------------------------------------------------------------------------------'
     
    print customer

def run_textWriteVersion(ex, dispatcher, meanTimeArrival, imbalanceLevel, numOfPRTs):
    # Generate all inputs: Network, Arrivals of customers, PRTs
    result_txt = open('experiment_FOFS/ex%d.txt' % (ex), 'w')
    result_txt.write('%s_meanTimeArrival(%.1f) imbalanceLevel(%.1f) numOfPRTs(%d)\n' % (str(dispatcher), meanTimeArrival, imbalanceLevel, numOfPRTs))
    Nodes, Edges = Dynamics.Network1()
    Customers = Dynamics.gen_Customer(meanTimeArrival, 5000, imbalanceLevel, Nodes)
    global NumOfTotalCustomer
    NumOfTotalCustomer = len(Customers)
    PRTs = Dynamics.gen_PRT(numOfPRTs, Nodes)
    Algorithms.init_algorithms(Nodes)
    Dynamics.init_dynamics(Nodes, PRTs, Customers, dispatcher)
    Dynamics.logger = logger_pass 
    Algorithms.on_notify_assignmentment_point = logger_pass  
    Dynamics.on_notify_customer_arrival = on_notify_customer_arrival 
    now = 1e400
    st = time()
    Dynamics.process_events(now)
    et = time() - st
    global NumOfCustomerArrivals, Total_empty_travel_distance, NumOfPickedUpCustomer, Total_travel_distance, Total_customers_flow_time, NumOfServicedCustomer, Total_customers_waiting_time, MaxCustomerWaitingTime
    global IdleState_time, ApproachingState_time, SettingState_time, TransitingState_time, ParkingState_time, data_accu_st, data_accu_et
    
    result_txt.write('%s\n' % str(ctime(st)))
    result_txt.write('computation time: %.1f\n' % (et))
    result_txt.write('\n')        
    result_txt.write('Measure------------------------------------------------------------------------------------------------\n')
    result_txt.write('T.TravedDist: %.1f\n' % (Total_travel_distance))
    result_txt.write('T.E.TravelDist: %.1f\n' % (Total_empty_travel_distance))
    result_txt.write('T.FlowTime: %.1f\n' % (Total_customers_flow_time))
    time_flow = data_accu_et - data_accu_st
    total_time_flow = time_flow * len(Dynamics.PRTs)
    result_txt.write('T.WaitTime: %.1f\n' % (Total_customers_waiting_time))
    result_txt.write('M.WaitTime: %.1f\n' % (MaxCustomerWaitingTime))
    result_txt.write('A.WaitTime: %.1f\n' % (Total_customers_waiting_time / NumOfCustomerArrivals))
    result_txt.write('IdleState_time: %.1f(%.1f%s)\n' % (IdleState_time, IdleState_time / total_time_flow * 100, '%'))
    result_txt.write('ApproachingState_time: %.1f(%.1f%s)\n' % (ApproachingState_time, ApproachingState_time / total_time_flow * 100, '%'))
    result_txt.write('SettingState_time: %.1f(%.1f%s)\n' % (SettingState_time, SettingState_time / total_time_flow * 100, '%'))
    result_txt.write('TransitingState_time: %.1f(%.1f%s)\n' % (TransitingState_time, TransitingState_time / total_time_flow * 100, '%'))
    result_txt.write('ParkingState_time: %.1f(%.1f%s)\n' % (ParkingState_time, ParkingState_time / total_time_flow * 100, '%'))
    result_txt.close()

def profile_solve():
    import cProfile, pstats
    args = (60.0, 500, 0.8, 80)
    dispatcher = Algorithms.NN5
    cProfile.runctx('run(0, 0, dispatcher, *args)', globals(), locals(), 'log/profile')
    s = pstats.Stats('log/profile')
    s.strip_dirs().sort_stats('cumulative', 'time').print_stats()

def run_excelWriteVersion(dispatchers, meanTimeArrivals, imbalanceLevel, numOfPRTs):
    from tempfile import TemporaryFile
    from xlwt import Workbook
    book = Workbook()
    sheet1 = book.add_sheet('Sheet 1')
    row1 = sheet1.row(0)
    compuTime, TTDist, ATDist, TETDist, AETDist, TWTime, AWTime, MWTime, TFTime, AFTime, Idle, Approaching, Setting, Transiting, Parking, DN, mTA, NOP = range(18)
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
                'dispatcher',
                'meanTimeArrivals',
                'numOfPRTs',
                ]
    
    for i, CN in enumerate(colNames):
        row1.write(i, CN)
    ex = 1
    for nPRTs in numOfPRTs:
        for MTA in meanTimeArrivals:
            for dispatcher in dispatchers:
                row = sheet1.row(ex)
                row.write(DN,dispatcher.__name__)
                row.write(mTA, MTA)
                row.write(NOP, nPRTs)
                
                Nodes, Edges = Dynamics.Network2()
                Customers = Dynamics.gen_Customer(MTA, 20, imbalanceLevel, Nodes)
                global NumOfTotalCustomer
                NumOfTotalCustomer = len(Customers)
                PRTs = Dynamics.gen_PRT(nPRTs, Nodes)
                Algorithms.init_algorithms(Nodes)
                Dynamics.init_dynamics(Nodes, PRTs, Customers, dispatcher)
                Dynamics.logger = logger_pass 
                Algorithms.on_notify_assignmentment_point = logger_pass  
                Dynamics.on_notify_customer_arrival = on_notify_customer_arrival 
                now = 1e400
                st = time()
                Dynamics.process_events(now)
                et = time() - st
                
                global NumOfCustomerArrivals, Total_empty_travel_distance, NumOfPickedUpCustomer, Total_travel_distance, Total_customers_flow_time, NumOfServicedCustomer, Total_customers_waiting_time, MaxCustomerWaitingTime
                global IdleState_time, ApproachingState_time, SettingState_time, TransitingState_time, ParkingState_time, data_accu_st, data_accu_et
                
                row.write(compuTime, et)
                
                row.write(TTDist,Total_travel_distance)
                row.write(ATDist,(Dynamics.Total_travel_distance / Dynamics.NumOfServicedCustomer))
                row.write(TETDist,Total_empty_travel_distance)
                row.write(AETDist,(Total_empty_travel_distance / NumOfPickedUpCustomer))
                row.write(TWTime,Total_customers_waiting_time)
                row.write(AWTime,(Total_customers_waiting_time / NumOfCustomerArrivals))
                row.write(MWTime,MaxCustomerWaitingTime)
                row.write(TFTime,Total_customers_flow_time)
                row.write(AFTime,(Total_customers_flow_time /NumOfServicedCustomer))
                row.write(Idle,IdleState_time)
                row.write(Approaching,ApproachingState_time)
                row.write(Setting,SettingState_time)
                row.write(Transiting,TransitingState_time)
                row.write(Parking,ParkingState_time)
                
                ex += 1
                
    book.save('dynamicsResults.xls')
    book.save(TemporaryFile())

if __name__ == '__main__':
    dispatcher = Algorithms.get_all_dispatchers().values()
    meanTimeArrival = (6.0, 7.0)
    imbalanceLevel = 0.5
    numOfPRTs = [30, 40]
     
    run_excelWriteVersion(dispatcher, meanTimeArrival, imbalanceLevel, numOfPRTs)
    
#     ex = 2000
#     for meanTimeArrival in (6.0, 7.0):
#         for dispatcher in (Algorithms.NN0, Algorithms.NN1, Algorithms.NN2, Algorithms.NN3, Algorithms.NN4, Algorithms.NN5):
#             run_textWriteVersion(ex, dispatcher, meanTimeArrival, 0.5, 40)
#             ex += 1
