from __future__ import division
import data, Dynamics, Algorithms
from random import seed
from time import time, ctime
from math import sqrt
from tempfile import TemporaryFile
from xlwt import Workbook
import numpy as np
import matplotlib.pyplot as plt

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

def run_experiment(dispatchers, meanTimeArrivals, exOrder):
#     seedNum = 2
#     seed(seedNum)
    
    Dynamics.logger = logger_pass 
    Algorithms.on_notify_assignmentment_point = logger_pass  
    Dynamics.on_notify_customer_arrival = on_notify_customer_arrival
    
    #---------------------------------------------------------------------
    '''
    # parameter setting
    NUM_PRT = 50
    NUM_CUSTOMER = 2000  # 5000
    
    PRT_SPEED = 12  # unit (m/s)
    S2J_SPEED = 6
    J2D_SPEED = 9
    SETTING_TIME = (10.0, 60.0)  # unit (sec)
    '''
    # parameter setting
    NUM_PRT = 50
    NUM_CUSTOMER = 5000
    
    PRT_SPEED = 1200  # unit (cm/s)
    S2J_SPEED = 600
    J2D_SPEED = 900
    SETTING_TIME = (10.0, 60.0)  # unit (sec)
    
    S2J, J2D, PS, nOP, nOTC, AR, D, CTime, ETDT, ETDA, ETDSD, ETDMed, ETDMax, CWTT, CWTA, CWTSD, CWTMed, CWTMax, BTT, BTA, BTSD, BTMed, BTMax, TFT, AFT, Idle, Approaching, Setting, Transiting, Parking = range(30)
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
    book = Workbook()
    # _dispatchers: Dispatcher : (ArivalRate, Measures)
    #   for drawing Graph
    _dispatchers = {D : [] for D in Algorithms.get_all_dispatchers().keys()}
    for dispatcher in dispatchers:
        sheet1 = book.add_sheet(dispatcher.__name__)
        row1 = sheet1.row(0)
        for i, CN in enumerate(colNames):
            row1.write(i, CN)
        ex = 1
        for arrivalRate in arrivalRates:
            global NumOfTotalCustomer
            global Total_travel_distance, Total_empty_travel_distance
            global NumOfCustomerArrivals, NumOfPickedUpCustomer, NumOfServicedCustomer
            global Total_customers_flow_time, Total_customers_waiting_time
            global distances, customersWaitingTimes, boardingWaitingTimes
            global stateTimes
            global data_accu_st, data_accu_et
            Dynamics.WaitingCustomerChanges, Dynamics.WaitingTimeChanges = [], []
            
            Network = data.Network1(PRT_SPEED, S2J_SPEED, J2D_SPEED)
            Customers, PRTs = data.gen_instances(Network, arrivalRate, NUM_CUSTOMER, NUM_PRT, PRT_SPEED)
            NumOfTotalCustomer = len(Customers)
            
            st = time()
            Dynamics.run(SETTING_TIME, PRT_SPEED, Network, PRTs, Customers, dispatcher)
            et = time() - st
            
            # Present system performance by Graph
            CT, WT, AWT = [], [], []
            for ct, wt in Dynamics.WaitingTimeChanges:
                CT.append(ct)
                WT.append(wt)
                AWT.append(sum(WT) / ct)
                
            fig = plt.figure()
            plt.plot(CT, WT, 'b-', CT, AWT, 'r--')
            fig.suptitle('Customer waiting')
            ax = fig.add_subplot(111)
            fig.subplots_adjust(top=0.85)
            ax.set_xlabel('Time (sec)')
            ax.set_ylabel('Customer (person)')
            FileName = 'experimentResult/waitingTimeGraph/arrivalRate(%.3f) dispatcher(%s).png' % (arrivalRate, dispatcher.__name__)
            plt.savefig(FileName)
            plt.close(fig)
            
            aED = np.array([d[1] for d in distances if d[0] == 'E'], float)
            aCWT = np.array(customersWaitingTimes, float)
            aBWT = np.array(boardingWaitingTimes, float)
            _dispatchers[dispatcher.__name__].append((arrivalRate, (aED, aCWT, aBWT)))
            
            TXT_FILE = 'experimentResult/textFiles/arrivalRate(%.3f) dispatcher(%s)' % (arrivalRate, dispatcher.__name__)
            with open(TXT_FILE, 'w') as f:
                f.write('Parameter------------------------------------------------------------------------------------------------\n')
                f.write('S2J_SPEED:%d\n' % S2J_SPEED)
                f.write('J2D_SPEED:%d\n' % J2D_SPEED)
                f.write('PRT_SPEED:%d\n' % PRT_SPEED)
                f.write('numOfPRTs:%d\n' % NUM_PRT)
                f.write('numOfTotalCustomers:%d\n' % NUM_CUSTOMER)
                f.write('arrivalRate:%f\n' % arrivalRate)
                f.write('dispatcher:%s\n' % dispatcher.__name__)
                f.write('Measure------------------------------------------------------------------------------------------------\n')
                f.write('CTime:%.1f\n' % et)
                
                f.write('E.T.Distance_Total:%.1f\n' % aED.sum())
                f.write('E.T.Distance_Average:%.1f\n' % aED.mean())
                f.write('E.T.Distance_S.D:%.1f\n' % aED.std())
                f.write('E.T.Distance_Median:%.1f\n' % np.median(aED))
                f.write('E.T.Distance_Max:%.1f\n' % aED.max())
                
                f.write('C.W.Time_Total:%.1f\n' % aCWT.sum())
                f.write('C.W.Time_Average):%.1f\n' % aCWT.mean())
                f.write('C.W.Time_S.D):%.1f\n' % aCWT.std())
                f.write('C.W.Time_Median:%.1f\n' % np.median(aCWT))
                f.write('C.W.Time_Max:%.1f\n' % aCWT.max())
                 
                f.write('B.Time_Total:%.1f\n' % aBWT.sum())
                f.write('B.Time_Average:%.1f\n' % aBWT.mean())
                f.write('B.Time_S.D:%.1f\n' % aBWT.std())
                f.write('B.Time_Median:%.1f\n' % np.median(aBWT))
                f.write('B.Time_Max:%.1f\n' % aBWT.max())
                
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
            row.write(AR, arrivalRate)
            row.write(D, dispatcher.__name__) 
            row.write(CTime, et) 
            row.write(ETDT, aED.sum())
            row.write(ETDA, aED.mean())
            row.write(ETDSD, aED.std())
            row.write(ETDMed, np.median(aED))
            row.write(ETDMax, aED.max())
            row.write(CWTT, aCWT.sum())
            row.write(CWTA, aCWT.mean())
            row.write(CWTSD, aCWT.std())
            row.write(CWTMed, np.median(aCWT))
            row.write(CWTMax, aCWT.max())
            row.write(BTT, aBWT.sum())
            row.write(BTA, aBWT.mean())
            row.write(BTSD, aBWT.std())
            row.write(BTMed, np.median(aBWT))
            row.write(BTMax, aBWT.max())
            row.write(TFT, Total_customers_flow_time)
            row.write(AFT, Total_customers_flow_time / NumOfServicedCustomer)
            row.write(Idle, stateTimes['I'])
            row.write(Approaching, stateTimes['A'])
            row.write(Setting, stateTimes['S'])
            row.write(Transiting, stateTimes['T'])
            row.write(Parking, stateTimes['P'])
            ex += 1
    book.save('experimentResult/dynamicsResults_order(%d).xls' % (exOrder))
    book.save(TemporaryFile())
    
    for D in _dispatchers.keys():
        ARs = []
        AaEDs, AaCWTs, AaBWTs = [], [], []
        MaEDs, MaCWTs, MaBWTs = [], [], []
        for AR, (aED, aCWT, aBWT) in _dispatchers[D]:
            ARs.append(AR)
            AaEDs.append(aED.mean())
            AaCWTs.append(aCWT.mean())
            AaBWTs.append(aBWT.mean())
            MaEDs.append(aED.max())
            MaCWTs.append(aCWT.max())
            MaBWTs.append(aBWT.max())
        _dispatchers[D] = (ARs, AaEDs, AaCWTs, AaBWTs, MaEDs, MaCWTs, MaBWTs)
    
    titleAndYlabel = [('EmptyTravel Average', 'Distance (cm)'),
                      ('CustomerWaiting Average', 'Time (s)'),
                      ('BoardingWaiting Average', 'Time (s)'),
                      ('EmptyTravel Max', 'Distance (cm)'),
                      ('CustomerWaiting Max', 'Time (s)'),
                      ('BoardingWaiting Max', 'Time (s)'),
                      ]
    for i, (title, ylabel) in enumerate(titleAndYlabel):
        saveMeasuresGraph(i + 1, title, ylabel, _dispatchers)

def saveMeasuresGraph(order, title, ylabel, _dispatchers):
    # ls = [(RGB color, ), marker]
    ls = [((255 / 255, 0 / 255, 0 / 255), 'v'),
          ((0 / 255, 255 / 255, 0 / 255), '<'),
          ((0 / 255, 0 / 255, 255 / 255), '^'),
          ((255 / 255, 128 / 255, 255 / 255), '>'),
          ((0 / 255, 255 / 255, 255 / 255), 'p'),
          ((255 / 255, 0 / 256, 255 / 255), 'o'),
          ((255 / 255, 128 / 255, 64 / 255), 'x'),
          ((128 / 255, 0 / 255, 64 / 255), 's'),
          ]
        
    fig = plt.figure()
    fig.suptitle(title)
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(r'arrivalRate ($\lambda$)')
    ax.set_ylabel(ylabel)
    num_plots = len(_dispatchers)
    labels = []
    for i, D in enumerate(_dispatchers.keys()):
        plt.plot(_dispatchers[D][0], _dispatchers[D][order], c=ls[i][0], marker=ls[i][1])
        labels.append(r'%s' % (D))
    plt.legend(labels, ncol=4, loc='upper center',
           bbox_to_anchor=[0.5, 1.1],
           columnspacing=1.0, labelspacing=0.0,
           handletextpad=0.0, handlelength=1.5,
           fancybox=True, shadow=True)
    plt.savefig('experimentResult/summaryGraph/%s.png' % (title))
    plt.close(fig)

def profile_solve():
    import cProfile, pstats
    PRT_SPEED = 12  # unit (m/s)
    S2J_SPEED = 6
    J2D_SPEED = 9
    SETTING_TIME = (10.0, 60.0)  # unit (sec)
    Network = data.Network1(S2J_SPEED, J2D_SPEED)
    Customers, PRTs = data.gen_instances(Network, 0.3, 200, 50, PRT_SPEED)
    dispatcher = Algorithms.NNBA_IATP
    args = (SETTING_TIME, PRT_SPEED, Network, PRTs, Customers, dispatcher)
    
    cProfile.runctx('Dynamics.run(*args)', globals(), locals(), 'log/profile')
    s = pstats.Stats('log/profile')
    s.strip_dirs().sort_stats('cumulative', 'time').print_stats()

def test_variousCustomer():
    seed(2)
    PRT_SPEED = 12  # unit (m/s)
    S2J_SPEED = 6
    J2D_SPEED = 9
    SETTING_TIME = (10.0, 60.0)  # unit (sec)
    for x in range(3):
        for y in range(4):
            Network = data.Network1(S2J_SPEED, J2D_SPEED)
            Customers, PRTs = data.gen_instances(Network, 0.2, 2000, 50, PRT_SPEED)
            customerArrivals_txt = open('Info. Arrivals of customers_%d_%d.txt' % (x, y), 'w')
            for c in Customers:
                t, sn, dn = c.arriving_time, c.sn.id, c.dn.id 
                customerArrivals_txt.write('%f,%s-%s\n' % (t, sn, dn))
            customerArrivals_txt.close()

if __name__ == '__main__':
#     test_variousCustomer()
#     profile_solve()
    dispatcher = [
                    Algorithms.FOFS,
                    Algorithms.FCFS,
                    Algorithms.NNBA_I,
                    Algorithms.NNBA_IT,
                    Algorithms.NNBA_IA,
                    Algorithms.NNBA_IAP,
                    Algorithms.NNBA_IAT,
                    Algorithms.NNBA_IATP,
                    ]
    
    arrivalRates = [0.2 + x * 0.05 for x in range(5)]
    run_experiment(dispatcher[:3], arrivalRates, 3)
    run_experiment(dispatcher[3:4], arrivalRates, 4)
    run_experiment(dispatcher[4:5], arrivalRates, 5)
    run_experiment(dispatcher[5:6], arrivalRates, 6)
    run_experiment(dispatcher[6:7], arrivalRates, 7)
    run_experiment(dispatcher[7:8], arrivalRates, 8)
