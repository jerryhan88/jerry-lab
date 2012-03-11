from __future__ import division
import datetime

def dt_cmp(e1, e2):
    dt1_txt, dt2_txt = e1[0], e2[0]
    year, month, day, hour, minute, second = dt1_txt.split('-') 
    dt1 = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    year, month, day, hour, minute, second = dt2_txt.split('-') 
    dt2 = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    
    if dt1 < dt2:
        return -1
    elif dt1 == dt2:
        return 0
    elif dt1 > dt2:
        return 1

EVT = []
log_text = open('real_log.txt')
for l in log_text.readlines():
    e = l[:-1].split('\t')
    dt = e[0]
    EVT.append(e)
        
EVT.sort(dt_cmp)
revised_EVT = []
for e in EVT:
    e_txt = ''
    for i, data in enumerate(e):
        e_txt += data
        if i + 1 != len(e):
            e_txt += '_'
    revised_EVT.append(e_txt)

for e in revised_EVT:
    print e

f = open('real_log_sorted_by_dt', 'w')
    
f.write('\n'.join(revised_EVT))
