from __future__ import division
import datetime
from random import randrange, seed
seed(100)
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

f = open('test.txt', 'w')
EVT = []
log_text = open('real_log.txt')
sts_tl_loading = []
for l in log_text.readlines():
    e = l[:-1].split('_')
    dt = e[0]
    if e[1][:3] == 'STS' and e[4][:4] == 'Lane':
        e[4] = e[1] + '-' + e[4]
#        print e
    if e[1][:3] == 'STS' and len(e) == 9 and e[2] == 'TwistUnlock':
        e.pop()
#    if e[1][:3] == 'STS'and e[2] == 'TwistUnlock' and e[5] == 'DISCHARGING':
    if e[1][:3] == 'STS' and e[2] == 'TwistLock'and e[5] == 'DISCHARGING':
        sb = e[-1]
        bay_id = int(sb[:2])
        if bay_id % 4 == 0 or bay_id % 4 == 1 or bay_id % 4 == 3:
            e[-1] = '%d' % (bay_id - 2) + e[-1][2:]
        pos = e.pop()
        e[4] = pos
    if e[1][:3] == 'STS' and e[2] == 'TwistLock'and e[5] == 'LOADING':
        if e[4] == 'OCRCHECK':
            continue
        sts_tl_loading.append(e)
        
    if e[1][:3] == 'STS' and e[2] == 'TwistUnlock'and e[5] == 'LOADING':
        sb = e[4]
        bay_id = int(sb[:2])
        if bay_id % 4 == 0 or bay_id % 4 == 1 or bay_id % 4 == 3:
            st = bay_id - 2
            if st < 10:
                st = '0' + str(bay_id - 2)
            else:
                st = str(bay_id - 2)
            e[4] = st + e[4][2:]
            
    if e[1][:2] == 'SH':
        if e[3] == '':
            e[3] = '2012-03-19-13-55-39'
            
#    if e[1][:2] == 'SH' and e[4] =='TwistLock' and e[7] == 'LOADING':

    EVT.append(e)
ori_EVT = EVT[:]
EVT = []
for e in ori_EVT:
    if e[1][:2] == 'SH' and e[4] == 'TwistUnlock' and e[7] == 'LOADING':
        for ie in sts_tl_loading:
            if ie[3] == e[5] and ie[4] != e[6]:
                e[6] = ie[4]
    
#    if e[1][:2] == 'SH':
#    if e[1][:3] == 'ASC':             
    c_id = None 
    if e[1][:3] == 'ASC' and len(e) == len('2012-03-19-06-50-26_ASC021_1290568_2012-03-19-06-47-55_TwistUnlock_GESU6804037_LM-A2-TP3_LOADING_HNVN/002/2012_N'.split('_')):
        c_id = e[5]
    elif e[1][:3] == 'STS' and len(e) == len('2012-03-19-12-33-17_STS101_TwistLock_TPHU8144329_STS101-Lane3_LOADING_HNVN/002/2012_N'.split('_')):
        c_id = e[3]
    elif e[1][:2] == 'SH' and len(e) == len('2012-03-19-12-33-35_SH11_1290336_2012-03-19-12-32-44_TwistLock_UACU3562734_LM-A4-TP2_LOADING_HNVN/002/2012_N'.split('_')):
        c_id = e[5]
    elif e[1] == 'Vessel':
        pass
    else:
        print e
        assert False
    if c_id in ['TRIU0615820', 'TPHU8144329', 'HJCU1458916', 'UACU3680423', 'UACU5432154', 'UACU3372380', 'HJCU1232174', 'TRLU8986041', 'HJCU4292114', 'DFSU4310841', 'DFSU6856955', 'TRLU3153438', 'IPXU3989333', 'UACU8016654', 'HJCU2115871', 'HJCU8150993', 'TGHU0392423', 'UACU5522957', 'BMOU9509536', 'HJCU8311228', 'WWWU9802682', 'FCIU3676473', 'HJCU8056380',
                'HJCU1566119',
                'CBHU8884682',
                'CBHU6116849',
                'CBHU8415010',
                'UACU5008845',
                'HJCU3205476',
                'CBHU5950693']:

        continue
    EVT.append(e)
        
EVT.sort(dt_cmp)

ori_EVT = EVT[:]
EVT = []
for e in ori_EVT:
    if e[1][:3] == 'STS':
        if e[4][:3] != 'STS':
            stack_id = e[4][3:5]
            if int(stack_id) > 13:
                e[4] = e[4][:3] + '0' + str(randrange(1,12)) + e[4][5:] 
            e[4] = 'SB' + e[4]
            for i, t in enumerate(e):
                if i != len(e) - 1:
                    f.write(t + '_')
                else:
                    f.write(t + '\n')
    EVT.append(e)

revised_EVT = []
for e in EVT:
    e_txt = ''
    for i, data in enumerate(e):
        e_txt += data
        if i + 1 != len(e):
            e_txt += '_'
    revised_EVT.append(e_txt)

#for e in revised_EVT:
#    print e


f = open('real_log_sorted_by_dt', 'w')
    
f.write('\n'.join(revised_EVT))
