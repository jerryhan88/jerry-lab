from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from xlrd import open_workbook

def run():
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
