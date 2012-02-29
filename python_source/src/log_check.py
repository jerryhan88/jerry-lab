from __future__ import division
import datetime

EVT = []

log_text = open('log.txt')

#vessel_master_data = master_text.readline().split(', ')

for l in log_text.readlines():
    e = l[:-1].split('_')
    dt = e[0]
    
    EVT.append(e)
    
#print EVT

def dt_cmp(e1, e2):
    dt1_txt,dt2_txt = e1[0], e2[0]
    year, month, day, hour, minute, second = dt1_txt.split('-') 
    dt1 = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    year, month, day, hour, minute, second = dt2_txt.split('-') 
    dt2 = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    
    if dt1 < dt2:
        return -1
    elif dt1 == dt2:
        return 0
    elif dt1>dt2:
        return 1

EVT.sort(dt_cmp)

#print EVT

for e in EVT:
    print e

if __name__ == '__main__':
    pass
