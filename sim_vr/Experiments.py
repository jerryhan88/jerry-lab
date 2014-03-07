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

# measuresCollectionPoint
measuresCSP, measuresCEP = (0.0,) * 2

distances, customersWaitingTimes, boardingWaitingTimes = [], [], []
stateTimes = {'I' : 0.0, 'A' : 0.0, 'S' : 0.0, 'T' : 0.0, 'P' : 0.0}

def on_notify_customer_arrival(customer):
    print customer
    if Dynamics.NumOfCustomerArrivals == int(NumOfTotalCustomer / 10):
        global measuresCSP
        measuresCSP = customer.arriving_time
        
        Dynamics.distances, Dynamics.customersWaitingTimes, Dynamics.boardingWaitingTimes = [], [], []
        
        for k in Dynamics.stateTimes.iterkeys():
            Dynamics.stateTimes[k] = 0.0
        
    if Dynamics.NumOfCustomerArrivals == NumOfTotalCustomer:
        global distances, customersWaitingTimes, boardingWaitingTimes
        global stateTimes
        global measuresCEP
        measuresCEP = customer.arriving_time
        
        distances = Dynamics.distances[:]
        customersWaitingTimes = Dynamics.customersWaitingTimes[:]
        boardingWaitingTimes = Dynamics.boardingWaitingTimes[:] 
        
        for k in Dynamics.stateTimes.iterkeys():
            stateTimes[k] = Dynamics.stateTimes[k]
        
        Dynamics.end_dynamics()
        
        print '-------------------------------------------------------------------------------'
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
    NUM_CUSTOMER = 3000
    
    PRT_SPEED = 1200  # unit (cm/s)
    S2J_SPEED = 600
    J2D_SPEED = 900
    SETTING_TIME = (10.0, 60.0)  # unit (sec)
    
    S2J, J2D, PS, nOP, nOTC, AR, D, CTime, ETDT, ETDA, ETDSD, ETDMed, ETDMax, CWTT, CWTA, CWTSD, CWTMed, CWTMax, BTT, BTA, BTSD, BTMed, BTMax, Idle, Approaching, Setting, Transiting, Parking = range(28)
    colNames = [
                'S2J_SPEED',
                'J2D_SPEED',
                'PRT_SPEED',
                'numOfPRTs',
                'numOfTotalCustomers',
                'arrivalRate',
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
            global distances, customersWaitingTimes, boardingWaitingTimes
            global stateTimes
            Dynamics.WaitingCustomerChanges, Dynamics.WaitingTimeChanges = [], []
            
            Network = data.Network1(PRT_SPEED, S2J_SPEED, J2D_SPEED)
            Customers, PRTs = data.gen_instances(Network, arrivalRate, NUM_CUSTOMER, NUM_PRT, PRT_SPEED)
            NumOfTotalCustomer = len(Customers)
            
            st = time()
            Dynamics.run(SETTING_TIME, PRT_SPEED, Network, PRTs, Customers, dispatcher)
            et = time() - st
            
            # Present system performance by Graph
            cCT, cWC = [], []
            for ct, wc in Dynamics.WaitingCustomerChanges:
                cCT.append(ct)
                cWC.append(wc)
            aCT, aWC = [], []
            for ct, wt in Dynamics.WaitingTimeChanges:
                aCT.append(ct)
                aWC.append(wt / ct)
            sCT, sWC = [], []
            for ct, wc in Dynamics.maxNumOfCustomer_inStation:
                sCT.append(ct)
                sWC.append(wc)
            
            fig = plt.figure()
            fig.suptitle('Customer waiting')
            ax = fig.add_subplot(111)
            fig.subplots_adjust(top=0.85)
            ax.set_xlabel('Time (sec)')
            ax.set_ylabel('Customer (person)')
            labels = []
            for n, ct, wc, l in [('current',cCT, cWC, 'b-'), ('average',aCT, aWC, 'r--'), ('maxInStation',sCT, sWC, 'g-.')]:
                plt.plot(ct, wc, l)
                labels.append(r'%s' % (n))
            plt.legend(labels, ncol=3, loc='upper center',
                       bbox_to_anchor=[0.5, 1.1],
                       columnspacing=1.0, labelspacing=0.0,
                       handletextpad=0.0, handlelength=1.5,
                       fancybox=True, shadow=True)
#             plt.plot(cCT, cWC, 'b-', aCT, aWC, 'r--', sCT, sWC, 'g-.')
            
            global measuresCSP, measuresCEP
            plt.annotate('MCSP', xy=(measuresCSP, 1), xytext=(measuresCSP * 2, 1.5),
                         arrowprops=dict(facecolor='red', shrink=0.05),
                         )
            plt.annotate('MCEP', xy=(measuresCEP, 1), xytext=(measuresCEP, 1.5),
                         arrowprops=dict(facecolor='red', shrink=0.05),
                         )
            FileName = 'experimentResult/waitingTimeGraph/dispatcher(%s) arrivalRate(%.4f).png' % (dispatcher.__name__, arrivalRate)
            plt.savefig(FileName)
            plt.close(fig)
            measuresCSP = 0.0
            measuresESP = 0.0
            
            aED = np.array([d[1] for d in distances if d[0] == 'E'], float)
            aCWT = np.array(customersWaitingTimes, float)
            aBWT = np.array(boardingWaitingTimes, float)
            _dispatchers[dispatcher.__name__].append((arrivalRate, (aED, aCWT, aBWT)))
            
            TXT_FILE = 'experimentResult/textFiles/dispatcher(%s) arrivalRate(%.4f).txt' % (dispatcher.__name__, arrivalRate)
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
                
                f.write('E.T.Distance_Total:%.1f\n' % (aED.sum() / 100))
                f.write('E.T.Distance_Average:%.1f\n' % (aED.mean() / 100))
                f.write('E.T.Distance_S.D:%.1f\n' % (aED.std() / 100))
                f.write('E.T.Distance_Median:%.1f\n' % (np.median(aED) / 100))
                f.write('E.T.Distance_Max:%.1f\n' % (aED.max() / 100))
                
                f.write('C.W.Time_Total:%.1f\n' % aCWT.sum())
                f.write('C.W.Time_Average:%.1f\n' % aCWT.mean())
                f.write('C.W.Time_S.D:%.1f\n' % aCWT.std())
                f.write('C.W.Time_Median:%.1f\n' % np.median(aCWT))
                f.write('C.W.Time_Max:%.1f\n' % aCWT.max())
                 
                f.write('B.Time_Total:%.1f\n' % aBWT.sum())
                f.write('B.Time_Average:%.1f\n' % aBWT.mean())
                f.write('B.Time_S.D:%.1f\n' % aBWT.std())
                f.write('B.Time_Median:%.1f\n' % np.median(aBWT))
                f.write('B.Time_Max:%.1f\n' % aBWT.max())
                
                time_flow = measuresCEP - measuresCSP
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
            row.write(ETDT, (aED.sum() / 100))
            row.write(ETDA, (aED.mean() / 100))
            row.write(ETDSD, (aED.std() / 100))
            row.write(ETDMed, (np.median(aED) / 100))
            row.write(ETDMax, (aED.max() / 100))
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
            row.write(Idle, stateTimes['I'])
            row.write(Approaching, stateTimes['A'])
            row.write(Setting, stateTimes['S'])
            row.write(Transiting, stateTimes['T'])
            row.write(Parking, stateTimes['P'])
            ex += 1
    book.save('experimentResult/dynamicsResults_order(%d).xlsx' % (exOrder))
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
    
    titleAndYlabel = [('EmptyTravel Average', 'Distance (m)'),
                      ('CustomerWaiting Average', 'Time (s)'),
                      ('BoardingWaiting Average', 'Time (s)'),
                      ('EmptyTravel Max', 'Distance (m)'),
                      ('CustomerWaiting Max', 'Time (s)'),
                      ('BoardingWaiting Max', 'Time (s)'),
                      ]
    
    from readExcel_drawGraph import saveMeasuresGraph
    
    for i, (title, ylabel) in enumerate(titleAndYlabel):
        saveMeasuresGraph(i + 1, title, ylabel, _dispatchers)

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
                    Algorithms.FCFS,
                    Algorithms.FOFO,
                    Algorithms.NNBA_I,
                    Algorithms.NNBA_IT,
                    Algorithms.NNBA_IA,
                    Algorithms.NNBA_IAP,
                    Algorithms.NNBA_IAT,
                    Algorithms.NNBA_IATP,
                    ]
#     arrivalRates = list(np.arange(0.128, 0.130, 0.0001))
    
#     arrivalRates = list(np.arange(0.15, 0.153, 0.001))
#     arrivalRates = list(np.arange(0.154, 0.158, 0.001))
    arrivalRates = list(np.arange(0.159, 0.160, 0.001))
#     run_experiment(dispatcher[:1], arrivalRates, 1)  # FCFS
#     run_experiment(dispatcher[1:2], arrivalRates, 2)  # FOFO 
#     run_experiment(dispatcher[2:3], arrivalRates, 3)  # NNBA_I 
#     run_experiment(dispatcher[3:4], arrivalRates, 4)  # NNBA_IT  
#     run_experiment(dispatcher[4:5], arrivalRates, 5)  # NNBA_IA
#     run_experiment(dispatcher[5:6], arrivalRates, 6)  # NNBA_IAP
    run_experiment(dispatcher[6:7], arrivalRates, 7)  # NNBA_IAT
#     run_experiment(dispatcher[7:8], arrivalRates, 8)  # NNBA_IATP
