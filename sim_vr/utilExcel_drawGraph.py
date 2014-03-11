from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from xlrd import open_workbook
from xlwt import Workbook
from os import listdir, path
from xlutils.copy import copy

def readTxext_writeExcel():
    dirPath = r'C:\experimentResult'
    exFP = '%s/experimentResult.xls' % (dirPath)
    if not path.isfile(exFP):
        import Algorithms
        wb = Workbook()
        for dispatcher in Algorithms.get_all_dispatchers().keys():
            st = wb.add_sheet(dispatcher)
            row = st.row(0)
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
            for i, CN in enumerate(colNames):
                row.write(i, CN)
    
    txtPath = '%s/textFiles' % (dirPath)
    for f in [ f for f in listdir(txtPath)]:
        rb = open_workbook(exFP)
        wb = copy(rb)
        with open('%s/%s' % (txtPath, f), 'r') as fp:
            ls = [w.strip() for w in fp.readlines()]
            _, D = ls[6].split(':')
            
            print D
            
            st_index, modi_row = None, None
            for i, s in enumerate(rb.sheets()):
                if s.name == D:
                    st_index = i
                    modi_row = rb.sheet_by_index(st_index).nrows
                    break
            else:
                assert False
            
            st = wb.get_sheet(st_index)
            row = st.row(modi_row)
            for i, l in enumerate(ls):
                _, v = l.split(':')
                # Except name of dispatcher, change v's type to number
                if i != 6: v = eval(v)
                row.write(i, v)
        wb.save(exFP)
    
    

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
    readTxext_writeExcel()
#     run()
