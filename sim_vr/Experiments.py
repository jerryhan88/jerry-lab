from __future__ import division
import data, Dynamics, Algorithms
from random import seed
from time import time, ctime
from math import sqrt

logger_pass = lambda x: None

NumOfTotalCustomer = 0

Total_travel_distance, Total_empty_travel_distance = (0.0,) * 2
NumOfCustomerArrivals, NumOfPickedUpCustomer, NumOfServicedCustomer = (0,) * 3
Total_customers_flow_time, Total_customers_waiting_time = (0.0,) * 2
distances, customersWaitingTimes, boardingWaitingTimes = [], [], []
stateTimes = {'I' : 0.0, 'A' : 0.0, 'S' : 0.0, 'T' : 0.0, 'P' : 0.0}
data_accu_st, data_accu_et = (0.0,) * 2 

def on_notify_customer_arrival(customer):
    print customer
    if Dynamics.NumOfCustomerArrivals == int(NumOfTotalCustomer / 10):
        Dynamics.Total_travel_distance, Dynamics.Total_empty_travel_distance = (0.0,) * 2
        Dynamics.NumOfWaitingCustomer, Dynamics.NumOfPickedUpCustomer, Dynamics.NumOfServicedCustomer = (0,) * 3
        Dynamics.Total_customers_flow_time, Dynamics.Total_customers_waiting_time = (0.0,) * 2
        Dynamics.distances, Dynamics.customersWaitingTimes, Dynamics.boardingWaitingTimes = [], [], []
        
        for k in Dynamics.stateTimes.iterkeys():
            Dynamics.stateTimes[k] = 0.0
        
        global data_accu_st
        data_accu_st = customer.arriving_time

    if Dynamics.NumOfCustomerArrivals == NumOfTotalCustomer:
        global Total_travel_distance, Total_empty_travel_distance
        global NumOfCustomerArrivals, NumOfPickedUpCustomer, NumOfServicedCustomer
        global Total_customers_flow_time, Total_customers_waiting_time
        global distances, customersWaitingTimes, boardingWaitingTimes
        global stateTimes
        
        Total_travel_distance = Dynamics.Total_travel_distance
        Total_empty_travel_distance = Dynamics.Total_empty_travel_distance
        
        NumOfCustomerArrivals = Dynamics.NumOfCustomerArrivals - int(NumOfTotalCustomer / 10)
        NumOfPickedUpCustomer = Dynamics.NumOfPickedUpCustomer
        NumOfServicedCustomer = Dynamics.NumOfServicedCustomer
        
        Total_customers_flow_time = Dynamics.Total_customers_flow_time 
        Total_customers_waiting_time = Dynamics.Total_customers_waiting_time
        
        distances = Dynamics.distances[:]
        customersWaitingTimes = Dynamics.customersWaitingTimes[:]
        boardingWaitingTimes = Dynamics.boardingWaitingTimes[:] 
        
        for k in Dynamics.stateTimes.iterkeys():
            stateTimes[k] = Dynamics.stateTimes[k]
        
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
        
        for k in stateTimes.iterkeys():
            print '%s state' % k, stateTimes[k]

def run_experiment(dispatchers, meanTimeArrivals):
    from tempfile import TemporaryFile
    from xlwt import Workbook
    seedNum = 2
    seed(seedNum)
    
    Dynamics.logger = logger_pass 
    Algorithms.on_notify_assignmentment_point = logger_pass  
    Dynamics.on_notify_customer_arrival = on_notify_customer_arrival
    
    #---------------------------------------------------------------------
    # parameter setting
    NUM_PRT = 50
    NUM_CUSTOMER = 2000  # 5000
    
    PRT_SPEED = 12  # unit (m/s)
    S2J_SPEED = 6
    J2D_SPEED = 9
    SETTING_TIME = (10.0, 60.0)  # unit (sec)
    
    book = Workbook()
    sheet1 = book.add_sheet('Sheet 1')
    row1 = sheet1.row(0)
    nOP, mTA, D, compuTime, TTDist, ATDist, TETDist, AETDist, TWTime, AWTime, MWTime, TFTime, AFTime, Idle, Approaching, Setting, Transiting, Parking, TBT, ABT = range(20)
    S2J, J2D, PS, nOP, nOTC, mTA, D, CTime, ETDT, ETDA, ETDSD, ETDMed, ETDMax, CWTT, CWTA, CWTSD, CWTMed, CWTMax, BTT, BTA, BTSD, BTMed, BTMax, TFT, AFT, Idle, Approaching, Setting, Transiting, Parking = range(30)
    colNames = [
                'S2J_SPEED',
                'J2D_SPEED',
                'PRT_SPEED',
                'numOfPRTs',
                'numOfTotalCustomers',
                'meanTimeArrivals',
                'dispatcher',
                'CTime',
                'E.T.Distance_Total',
                'E.T.Distance_Average',
                'E.T.Distance_S.D',
                'E.T.Distance_Median',
                'E.T.Distance_Max',
                'C.W.Time_Total',
                'C.W.Time_Average',
                'C.W.Time_S.D',
                'C.W.Time_Median',
                'C.W.Time_Max',
                'B.Time_Total',
                'B.Time_Average',
                'B.Time_S.D',
                'B.Time_Median',
                'B.Time_Max',
                'T.F.Time',
                'A.F.Time',
                'I.S.Time',
                'A.S.Time',
                'S.S.Time',
                'T.S.Time',
                'P.S.Time',
                ]
    
    for i, CN in enumerate(colNames):
        row1.write(i, CN)
    
    ex = 1
    for MTA in meanTimeArrivals:
        for dispatcher in dispatchers:
            global NumOfTotalCustomer
            global Total_travel_distance, Total_empty_travel_distance
            global NumOfCustomerArrivals, NumOfPickedUpCustomer, NumOfServicedCustomer
            global Total_customers_flow_time, Total_customers_waiting_time
            global distances, customersWaitingTimes, boardingWaitingTimes
            global stateTimes
            global data_accu_st, data_accu_et
            
            Network = data.Network1(S2J_SPEED, J2D_SPEED)
            Customers, PRTs = data.gen_instances(Network, MTA, NUM_CUSTOMER, NUM_PRT, PRT_SPEED)
            NumOfTotalCustomer = len(Customers)
            
            st = time()
            Dynamics.run(SETTING_TIME, PRT_SPEED, Network, PRTs, Customers, dispatcher)
            et = time() - st
            
            e_distance = sorted([d[1] for d in distances if d[0] == 'E'])
            customersWaitingTimes.sort()
            boardingWaitingTimes.sort()
            
            ETAverage = sum(e_distance) / len(e_distance)
            ETDeviation_2 = [(d - ETAverage) ** 2 for d in e_distance]
            CWAverage = sum(customersWaitingTimes) / len(customersWaitingTimes)
            CWDeviation_2 = [(w - CWAverage) ** 2 for w in customersWaitingTimes]
            BAverage = sum(boardingWaitingTimes) / len(boardingWaitingTimes)
            BDeviation_2 = [(w - BAverage) ** 2 for w in boardingWaitingTimes]
            
            TXT_FILE = 'experimentResult_txt/MTA(%.1f) dispatcher(%s)' % (MTA, dispatcher.__name__)
            with open(TXT_FILE, 'w') as f:
                f.write('Parameter------------------------------------------------------------------------------------------------\n')
                f.write('S2J_SPEED:%d\n' % S2J_SPEED)
                f.write('J2D_SPEED:%d\n' % J2D_SPEED)
                f.write('PRT_SPEED:%d\n' % PRT_SPEED)
                f.write('numOfPRTs:%d\n' % NUM_PRT)
                f.write('numOfTotalCustomers:%d\n' % NUM_CUSTOMER)
                f.write('meanTimeArrivals:%f\n' % MTA)
                f.write('dispatcher:%s\n' % dispatcher.__name__)
                f.write('Measure------------------------------------------------------------------------------------------------\n')
                f.write('CTime:%.1f\n' % et)
                
                f.write('E.T.Distance_Total:%.1f\n' % sum(e_distance))
                f.write('E.T.Distance_Average:%.1f\n' % ETAverage)
                f.write('E.T.Distance_S.D:%.1f\n' % (sum(ETDeviation_2) / len(ETDeviation_2)))
                f.write('E.T.Distance_Median:%.1f\n' % e_distance[len(e_distance) // 2])
                f.write('E.T.Distance_Max:%.1f\n' % max(e_distance))
                
                f.write('C.W.Time_Total:%.1f\n' % sum(customersWaitingTimes))
                f.write('C.W.Time_Average):%.1f\n' % CWAverage)
                f.write('C.W.Time_S.D):%.1f\n' % (sum(CWDeviation_2) / len(CWDeviation_2)))
                f.write('C.W.Time_Median:%.1f\n' % customersWaitingTimes[len(customersWaitingTimes) // 2])
                f.write('C.W.Time_Max:%.1f\n' % max(customersWaitingTimes))
                
                f.write('B.Time_Total:%.1f\n' % sum(boardingWaitingTimes))
                f.write('B.Time_Average:%.1f\n' % BAverage)
                f.write('B.Time_S.D:%.1f\n' % (sum(BDeviation_2) / len(BDeviation_2)))
                f.write('B.Time_Median:%.1f\n' % boardingWaitingTimes[len(boardingWaitingTimes) // 2])
                f.write('B.Time_Max:%.1f\n' % max(boardingWaitingTimes))
                
                f.write('T.F.Time:%.1f\n' % Total_customers_flow_time)
                f.write('A.F.Time:%.1f\n' % (Total_customers_flow_time / NumOfServicedCustomer))
                
                time_flow = data_accu_et - data_accu_st
                total_time_flow = time_flow * len(Dynamics.PRTs)
                f.write('I.S.Time: %.1f(%.1f%s)\n' % (stateTimes['I'], stateTimes['I'] / total_time_flow * 100, '%'))
                f.write('A.S.Time: %.1f(%.1f%s)\n' % (stateTimes['A'], stateTimes['A'] / total_time_flow * 100, '%'))
                f.write('S.S.Time: %.1f(%.1f%s)\n' % (stateTimes['S'], stateTimes['S'] / total_time_flow * 100, '%'))
                f.write('T.S.Time: %.1f(%.1f%s)\n' % (stateTimes['T'], stateTimes['T'] / total_time_flow * 100, '%'))
                f.write('P.S.Time: %.1f(%.1f%s)\n' % (stateTimes['P'], stateTimes['P'] / total_time_flow * 100, '%'))
            
            row = sheet1.row(ex)
            row.write(S2J, S2J_SPEED) 
            row.write(J2D, J2D_SPEED)
            row.write(PS, PRT_SPEED)
            row.write(nOP, NUM_PRT)
            row.write(nOTC, NUM_CUSTOMER) 
            row.write(mTA, MTA)
            row.write(D, dispatcher.__name__) 
            row.write(CTime, et) 
            row.write(ETDT, sum(e_distance))
            row.write(ETDA, ETAverage)
            row.write(ETDSD, sum(ETDeviation_2) / len(ETDeviation_2))
            row.write(ETDMed, e_distance[len(e_distance) // 2])
            row.write(ETDMax, max(e_distance))
            row.write(CWTT, sum(customersWaitingTimes))
            row.write(CWTA, CWAverage)
            row.write(CWTSD, sum(CWDeviation_2) / len(CWDeviation_2))
            row.write(CWTMed, customersWaitingTimes[len(customersWaitingTimes) // 2])
            row.write(CWTMax, max(customersWaitingTimes))
            row.write(BTT, sum(boardingWaitingTimes))
            row.write(BTA, BAverage)
            row.write(BTSD, sum(BDeviation_2) / len(BDeviation_2))
            row.write(BTMed, boardingWaitingTimes[len(boardingWaitingTimes) // 2])
            row.write(BTMax, max(boardingWaitingTimes))
            row.write(TFT, Total_customers_flow_time)
            row.write(AFT, Total_customers_flow_time / NumOfServicedCustomer)
            row.write(Idle, stateTimes['I'])
            row.write(Approaching, stateTimes['A'])
            row.write(Setting, stateTimes['S'])
            row.write(Transiting, stateTimes['T'])
            row.write(Parking, stateTimes['P'])
                    
            ex += 1
                
    book.save('dynamicsResults_4.xls')
    book.save(TemporaryFile())

def profile_solve():
    import cProfile, pstats
    args = (60.0, 500, 0.8, 80)
    dispatcher = Algorithms.NN5
    cProfile.runctx('run(0, 0, dispatcher, *args)', globals(), locals(), 'log/profile')
    s = pstats.Stats('log/profile')
    s.strip_dirs().sort_stats('cumulative', 'time').print_stats()

if __name__ == '__main__':
    dispatcher = Algorithms.get_all_dispatchers().values()
    meanTimeArrival = [4.0 + x * 0.1 for x in range(10)]
    run_experiment(dispatcher, meanTimeArrival)
