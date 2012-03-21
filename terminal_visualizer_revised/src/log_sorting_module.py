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
    e = l[:-1].split('_')
    dt = e[0]
#    if e[4] == 'OCRCHECK':
#        e[4] = 'TwistLock'
#    c_id = None
#    if len(e) == len('2012-03-03-02-09-09_STS103_TwistLock_MRKU6817080_A7-21-7-5_LOADING_WALS/002/2012_N'.split('_')):
#        c_id = e[3]
#    elif len(e) == len('2012-03-03-02-14-03_ASC131_1244718_2012-03-03-02-12-59_TwistLock_MSKU3366180_B5-27-2-4_LOADING_WALS/002/2012_N'.split('_')):
#        c_id = e[5]
#    elif len(e) == len('2012-03-03-05-46-00_SH19_1245049_2012-03-03-05-44-00_TwistLock_TTNU1412090_LM-A6-TP3_LOADING_WALS/002/2012_N'.split('_')):    
#        c_id = e[5]
#    elif e[1] == 'Vessel':
#        c_id = None
#    else:
#        assert False
#    if c_id in ['MSKU2192572', 'MRKU8001100', 'TRLU3668829', 'MRKU7535137', 'IPXU3051594', 'MSKU2373890', 'MRKU7630936', 'MSKU4220760', 'MSKU7144324', 'CAXU6658754', 'MSKU3161323', 'PONU2020022', 'MAEU6796171', 'MRKU7285660', 'MSKU5278134', 'MSKU2691313', 'MSKU3597045', 'MSKU4403334', 'MSKU5972926', 'MSKU2486772', 'MSKU2562152', 'MSKU2596532', 'MSKU2354040', 'MSKU2969940', 'MRKU6995272', 'MRKU7246582', 'MRKU6991507', 'INBU3276542', 'MSKU5828586', 'MSKU7786432', 'MSKU5999188', 'PONU2012080', 'GLDU5586298', 'MSKU4025825', 'MSKU7977969', 'MSKU2762356', 'MRKU6557933', 'MRKU7274563', 'MSKU2370226', 'MSKU7989086', 'MSKU7332770', 'MRKU7254700', 'MSKU7916238', 'MSKU7962423', 'POCU0448316', 'MRKU7468424', 'PONU0408092', 'MRKU7730010', 'MSKU4232740', 'PONU0051831', 'MSKU2577980', 'MSKU3835760', 'PONU0689575', 'MSKU5046925', 'PONU0867466', 'MRKU7638407', 'CAIU2477798', 'MSKU7910538', 'MSKU7470589', 'MRKU8217948', 'MSKU3157827', 'CAIU2390810', 'MAEU7867942', 'MRKU7001213',
#                'POCU0329960']:
#            continue
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
