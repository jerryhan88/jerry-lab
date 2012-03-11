from __future__ import division
import datetime

cs_pos = []

log_text = open('temp.txt')

for l in log_text.readlines():
    e = l[:-1].split('\n')
    cs_pos.append(e)

print cs_pos

max_bay_id = 0

for pos in cs_pos:
    bay_id = int(pos[0][3:5])
    if bay_id > max_bay_id:
        max_bay_id = bay_id
    if bay_id % 2 == 1:
        print '20ft'
        

#print  max_bay_id

if __name__ == '__main__':
    pass
