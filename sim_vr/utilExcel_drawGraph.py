from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from xlrd import open_workbook
from xlwt import Workbook

def readTxext_writeExcel():
    for i, CN in enumerate(colNames):
            row1.write(i, CN)
    ex = 1
    
    book = Workbook()
    
    sheet1 = book.add_sheet(dispatcher.__name__)
    row1 = sheet1.row(0)
    
    S2J, J2D, PS, nOP, nOTC, AR, D, CTime, ETDT, ETDA, ETDSD, ETDMed, ETDMax, CWTT, CWTA, CWTSD, CWTMed, CWTMax, BTT, BTA, BTSD, BTMed, BTMax, CWNT, CWNA, CWNSD, CWNMed, CWNMax, Idle, Approaching, Setting, Transiting, Parking = range(33)
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
                
                'C.W.Number_Total',
                'C.W.Number_Average',
                'C.W.Number_S.D',
                'C.W.Number_Median',
                'C.W.Number_Max',
                
                'I.S.Time',
                'A.S.Time',
                'S.S.Time',
                'T.S.Time',
                'P.S.Time',
                ]
    
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
            
            row.write(CWNT, aCWT.sum())
            row.write(CWNA, aCWT.mean())
            row.write(CWNSD, aCWT.std())
            row.write(CWNMed, np.median(aCWT))
            row.write(CWNMax, aCWT.max())
            
            row.write(Idle, stateTimes['I'])
            row.write(Approaching, stateTimes['A'])
            row.write(Setting, stateTimes['S'])
            row.write(Transiting, stateTimes['T'])
            row.write(Parking, stateTimes['P'])
            ex += 1
            
    book.save('%s/dynamicsResults_order(%d).xls' % (fileSavePath, exOrder))
    book.save(TemporaryFile())

def readExcel_drawGraph():
#     _dispatchers = {D : None for D in ['FCFS','FOFO','NNBA_IA','NNBA_IAP','NNBA_I','NNBA_IATP','NNBA_IAT','NNBA_IT',]}
    _dispatchers = {D : None for D in ['NNBA_IA', 'NNBA_IAP', 'NNBA_I', 'NNBA_IATP', 'NNBA_IAT', 'NNBA_IT', ]}
    book = open_workbook('experimentResult/dynamicsResults.xls')
    
    for D in _dispatchers.keys():
        sh = book.sheet_by_name(D)
        ARs = []
        AaEDs, AaCWTs, AaBWTs = [], [], []
        MaEDs, MaCWTs, MaBWTs = [], [], []
        
        for row_index in range(1, sh.nrows):
            r = sh.row(row_index)
            if r[5].value > 0.18: continue
            ARs.append(r[5].value)
            AaEDs.append(r[9].value)
            MaEDs.append(r[12].value)
            
            AaCWTs.append(r[14].value)
            MaCWTs.append(r[17].value)
            
            AaBWTs.append(r[19].value)
            MaBWTs.append(r[22].value)
            
        _dispatchers[D] = (ARs, AaEDs, AaCWTs, AaBWTs, MaEDs, MaCWTs, MaBWTs)
    
    titleAndYlabel = [('EmptyTravel Average', 'Distance (m)'),
                      ('CustomerWaitingTime Average', 'Time (s)'),
                      ('BoardingWaiting Average', 'Time (s)'),
                      ('CustomerWaitingNumber Average', 'NumOfWating (person)'),
                      ('EmptyTravel Max', 'Distance (m)'),
                      ('CustomerWaiting Max', 'Time (s)'),
                      ('BoardingWaiting Max', 'Time (s)'),
                      ('CustomerWaitingNumber Max', 'NumOfWating (person)'),
                      ]
    
    for i, (title, ylabel) in enumerate(titleAndYlabel):
        saveMeasuresGraph(i + 1, title, ylabel, _dispatchers)
        
        
#         
#         
#         
#         for D in _dispatchers.keys():
#         ARs = []
#         AaEDs, AaCWTs, AaBWTs, AaCWNs = [], [], [], []
#         MaEDs, MaCWTs, MaBWTs, MaCWNs = [], [], [], []
#         for AR, (aED, aCWT, aBWT, aCWN) in _dispatchers[D]:
#             ARs.append(AR)
#             AaEDs.append(aED.mean())
#             AaCWTs.append(aCWT.mean())
#             AaBWTs.append(aBWT.mean())
#             AaCWNs.append(aCWN.mean())
#             MaEDs.append(aED.max())
#             MaCWTs.append(aCWT.max())
#             MaBWTs.append(aBWT.max())
#             MaCWNs.append(aCWN.max())
#         _dispatchers[D] = (ARs, AaEDs, AaCWTs, AaBWTs, AaCWNs, MaEDs, MaCWTs, MaBWTs, MaCWNs)
#     
#     titleAndYlabel = [('EmptyTravel Average', 'Distance (m)'),
#                       ('CustomerWaitingTime Average', 'Time (s)'),
#                       ('BoardingWaiting Average', 'Time (s)'),
#                       ('CustomerWaitingNumber Average', 'NumOfWating (person)'),
#                       ('EmptyTravel Max', 'Distance (m)'),
#                       ('CustomerWaiting Max', 'Time (s)'),
#                       ('BoardingWaiting Max', 'Time (s)'),
#                       ('CustomerWaitingNumber Max', 'NumOfWating (person)'),
#                       ]
#     
#     from readExcel_drawGraph import saveMeasuresGraph
#     
#     for i, (title, ylabel) in enumerate(titleAndYlabel):
#         saveMeasuresGraph(i + 1, title, ylabel, _dispatchers)
        
def saveMeasuresGraph(order, title, ylabel, _dispatchers):
    import os
    path = 'C:\Users\user\Desktop\experimentResult/graphFiles/summary'
    if not os.path.exists(path): os.makedirs(path)
    
    l = [((255 / 255, 0 / 255, 0 / 255), '-'),
          ((255 / 255, 0 / 255, 0 / 255), '-.'),
          ((0 / 255, 255 / 255, 0 / 255), '-'),
          ((0 / 255, 255 / 255, 0 / 255), '-.'),
          ((0 / 255, 0 / 255, 255 / 255), '-'),
          ((0 / 255, 0 / 255, 255 / 255), '-.'),
          ((0 / 255, 0 / 255, 0 / 255), '-'),
          ((0 / 255, 0 / 255, 0 / 255), '-.'),
        ]
    fig = plt.figure()
    fig.suptitle(title)
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(r'arrivalRate ($\lambda$)')
    ax.set_ylabel(ylabel)
    labels = []
    for i, D in enumerate(_dispatchers.keys()):
        plt.plot(_dispatchers[D][0], _dispatchers[D][order], c=l[i][0], ls=l[i][1])
        labels.append(r'%s' % (D))
    plt.legend(labels, ncol=4, loc='upper center',
           bbox_to_anchor=[0.5, 1.1],
           columnspacing=1.0, labelspacing=0.0,
           handletextpad=0.0, handlelength=1.5,
           fancybox=True, shadow=True)
    plt.savefig('%s/%s.png' % (path, title))
    plt.close(fig)

if __name__ == '__main__':
    run()
