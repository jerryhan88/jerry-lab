from __future__ import division
import data, Dynamics, Algorithms
from random import seed
from time import time, ctime
from math import sqrt
from tempfile import TemporaryFile
import numpy as np
import matplotlib.pyplot as plt


# init. folders
fileSavePath = 'C:\experimentResult'
textFilesPath = fileSavePath + '/textFiles'
graphFilesPath = fileSavePath + '/graphFiles'
graphWT_FilesPath = graphFilesPath + '/waitingTime'
graphSMM_FilesPath = graphFilesPath + '/summary'



logger_pass = lambda x: None

NumOfTotalCustomer = 0

# measuresCollectionPoint
measuresCSP, measuresCEP = (0.0,) * 2

distances, customersWaitingTimes, boardingWaitingTimes, customerWaitingNums = [], [], [], []

stateTimes = {'I' : 0.0, 'A' : 0.0, 'S' : 0.0, 'T' : 0.0, 'P' : 0.0}

def on_notify_customer_arrival(customer):
    print customer
    if Dynamics.NumOfCustomerArrivals == int(NumOfTotalCustomer / 5):
        global measuresCSP
        measuresCSP = customer.arriving_time
        
        Dynamics.distances, Dynamics.customersWaitingTimes, Dynamics.boardingWaitingTimes, Dynamics.customerWaitingNums = [], [], [], []
        
        for k in Dynamics.stateTimes.iterkeys():
            Dynamics.stateTimes[k] = 0.0
        
    if Dynamics.NumOfCustomerArrivals == NumOfTotalCustomer:
        global distances, customersWaitingTimes, boardingWaitingTimes, customerWaitingNums
        global stateTimes
        global measuresCEP
        measuresCEP = customer.arriving_time
        
        distances = Dynamics.distances[:]
        customersWaitingTimes = Dynamics.customersWaitingTimes[:]
        boardingWaitingTimes = Dynamics.boardingWaitingTimes[:]
        customerWaitingNums = Dynamics.customerWaitingNums[:] 
        
        for k in Dynamics.stateTimes.iterkeys():
            stateTimes[k] = Dynamics.stateTimes[k]
        
        Dynamics.end_dynamics()
        
        print '-------------------------------------------------------------------------------'
        for k in stateTimes.iterkeys():
            print '%s state' % k, stateTimes[k]

def run_eachInstance(PRT_SPEED, S2J_SPEED, J2D_SPEED, SETTING_TIME, NUM_CUSTOMER, NUM_PRT, dispatcher, arrivalRate):
    Dynamics.logger = logger_pass 
    Algorithms.on_notify_assignmentment_point = logger_pass  
    Dynamics.on_notify_customer_arrival = on_notify_customer_arrival
    
    
    global NumOfTotalCustomer
    global distances, customersWaitingTimes, boardingWaitingTimes, customerWaitingNums
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
    for n, ct, wc, l in [('current', cCT, cWC, 'b-'), ('average', aCT, aWC, 'r--'), ('maxInStation', sCT, sWC, 'g-.')]:
        plt.plot(ct, wc, l)
        labels.append(r'%s' % (n))
    plt.legend(labels, ncol=3, loc='upper center',
               bbox_to_anchor=[0.5, 1.1],
               columnspacing=1.0, labelspacing=0.0,
               handletextpad=0.0, handlelength=1.5,
               fancybox=True, shadow=True)
    
    global measuresCSP, measuresCEP
    plt.annotate('MCSP', xy=(measuresCSP, 1), xytext=(measuresCSP * 2, 1.5),
                 arrowprops=dict(facecolor='red', shrink=0.05),
                 )
    plt.annotate('MCEP', xy=(measuresCEP, 1), xytext=(measuresCEP, 1.5),
                 arrowprops=dict(facecolor='red', shrink=0.05),
                 )
    
    FileName = '%s/dispatcher(%s) arrivalRate(%.4f).png' % (graphWT_FilesPath, dispatcher.__name__, arrivalRate)
    
    plt.savefig(FileName)
    plt.close(fig)
    measuresCSP = 0.0
    measuresESP = 0.0
    
    aED = np.array([d[1] for d in distances if d[0] == 'E'], float)
    aCWT = np.array(customersWaitingTimes, float)
    aBWT = np.array(boardingWaitingTimes, float)
    aCWN = np.array(customerWaitingNums)
    
    TXT_FILE = '%s/dispatcher(%s) arrivalRate(%.4f).txt' % (textFilesPath, dispatcher.__name__, arrivalRate)
    with open(TXT_FILE, 'w') as f:
        # Parameter------------------------------------------------------------------------------------------------
        f.write('S2J_SPEED:%d\n' % S2J_SPEED)
        f.write('J2D_SPEED:%d\n' % J2D_SPEED)
        f.write('PRT_SPEED:%d\n' % PRT_SPEED)
        f.write('numOfPRTs:%d\n' % NUM_PRT)
        f.write('numOfTotalCustomers:%d\n' % NUM_CUSTOMER)
        f.write('arrivalRate:%f\n' % arrivalRate)
        f.write('dispatcher:%s\n' % dispatcher.__name__)
        # Measure------------------------------------------------------------------------------------------------
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
        
        f.write('C.W.Number_Total:%.1f\n' % aCWN.sum())
        f.write('C.W.Number_Average:%.1f\n' % aCWN.mean())
        f.write('C.W.Number_S.D:%.1f\n' % aCWN.std())
        f.write('C.W.Number_Median:%.1f\n' % np.median(aCWN))
        f.write('C.W.Number_Max:%.1f\n' % aCWN.max())
        
        time_flow = measuresCEP - measuresCSP
        total_time_flow = time_flow * len(Dynamics.PRTs)
        f.write('I.S.Time: %.1f\n' % (stateTimes['I']))
        f.write('A.S.Time: %.1f\n' % (stateTimes['A']))
        f.write('S.S.Time: %.1f\n' % (stateTimes['S']))
        f.write('T.S.Time: %.1f\n' % (stateTimes['T']))
        f.write('P.S.Time: %.1f\n' % (stateTimes['P']))
def run_experiment(NUM_PRT, NUM_CUSTOMER, repetition, dispatchers, arrivalRates):
    import os
#     seedNum = 2
#     seed(seedNum)
    for p in [fileSavePath, textFilesPath, graphFilesPath, graphWT_FilesPath, graphSMM_FilesPath]:
        if not os.path.exists(p): os.makedirs(p)
    
    PRT_SPEED = 1200  # unit (cm/s)
    S2J_SPEED = 600
    J2D_SPEED = 900
    SETTING_TIME = (10.0, 60.0)  # unit (sec)
    
    for dispatcher in dispatchers:
        for arrivalRate in arrivalRates:
            run_eachInstance(PRT_SPEED, S2J_SPEED, J2D_SPEED, SETTING_TIME, NUM_CUSTOMER, NUM_PRT, dispatcher, arrivalRate)
            
def profile_solve():
    import cProfile, pstats, os
    PRT_SPEED = 12  # unit (m/s)
    S2J_SPEED = 6
    J2D_SPEED = 9
    SETTING_TIME = (10.0, 60.0)  # unit (sec)
    Network = data.Network1(S2J_SPEED, J2D_SPEED)
    Customers, PRTs = data.gen_instances(Network, 0.3, 200, 50, PRT_SPEED)
    dispatcher = Algorithms.NNBA_IATP
    args = (SETTING_TIME, PRT_SPEED, Network, PRTs, Customers, dispatcher)
    profilePath = 'log/profile'
    if not os.path.exists(profilePath): os.makedirs(profilePath)
    
    cProfile.runctx('Dynamics.run(*args)', globals(), locals(), profilePath)
    s = pstats.Stats(profilePath)
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

    # parameter setting
    NUM_PRT = 50
    NUM_CUSTOMER = 2000
    
    repetition = 1
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
    arrivalRates = list(np.arange(0.1, 0.2, 0.005))
    
    run_experiment(NUM_PRT, NUM_CUSTOMER, repetition, dispatcher[:1], arrivalRates)  # FCFS
    run_experiment(NUM_PRT, NUM_CUSTOMER, repetition, dispatcher[1:2], arrivalRates)  # FOFO 
    run_experiment(NUM_PRT, NUM_CUSTOMER, repetition, dispatcher[2:3], arrivalRates)  # NNBA_I 
    run_experiment(NUM_PRT, NUM_CUSTOMER, repetition, dispatcher[3:4], arrivalRates)  # NNBA_IT  
    run_experiment(NUM_PRT, NUM_CUSTOMER, repetition, dispatcher[4:5], arrivalRates)  # NNBA_IA
    run_experiment(NUM_PRT, NUM_CUSTOMER, repetition, dispatcher[5:6], arrivalRates)  # NNBA_IAP
    run_experiment(NUM_PRT, NUM_CUSTOMER, repetition, dispatcher[6:7], arrivalRates)  # NNBA_IAT
    run_experiment(NUM_PRT, NUM_CUSTOMER, repetition, dispatcher[7:8], arrivalRates)  # NNBA_IATP
