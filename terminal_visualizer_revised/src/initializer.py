from __future__ import division
from vehicle_classes import QC, YC, SC
from others_classes import Vessel, Container, Evt
    
def run(real_log=True, checking_log=False):
    EVT = []
    log_text = open('real_log_sorted_by_dt')
    for l in log_text.readlines():
        e = l[:-1].split('_')
#        print e
#        assert False
        EVT.append(e)
#        print e
#    assert False
    vessels, qcs, ycs, scs, containers = [], [], [], [], []
    init_real_log(vessels, qcs, ycs, scs, containers, EVT)
    if checking_log: 
        wrong_c = check_c_log(containers)
        wc_set, c_set = set(wrong_c), set(containers)
        print 'correct moving container : ', len(c_set - wc_set), c_set - wc_set 
        print 'wrong moving container : ', len(wc_set), wc_set
        wrong_v = check_v_log(vessels, qcs, ycs, scs)
        print 'wrong moving vehicles : '
        for v in wrong_v:
            print v, v.wrong_evt_id, len(v.evt_seq)
    
#    for  v in vessels+ qcs + ycs+ scs:
#        print v, v.evt_seq
    return vessels, qcs , ycs, scs , containers

def init_real_log(vessels, qcs, ycs, scs, containers, EVT):
    for e in EVT:
        vehicle = e[1]
        if vehicle == 'Vessel':
            #ex : 2012-02-14-08-00-00_Vessel_Arrival_None_Bitt06_None_MCEN/003/2012_N
            dt, vehicle, work_type, c_id, pos, operation, v_info, state = e
            v_name, v_voyage_txt, _ = v_info.split('/')
            target_v = None
            for v in vessels:
                if v.name == v_name and v.voyage == int(v_voyage_txt):
                    target_v = v
                    break
            else:
                target_v = Vessel(v_name, int(v_voyage_txt))
                vessels.append(target_v)
            target_v.evt_seq.append(Evt(dt, vehicle, work_type, c_id, operation, v_info, state, pos))
        elif vehicle[:3] == 'STS':
            # ex : 2012-02-14-10-59-20_STS101_TwistLock_HLXU3395821_LOADING_MCEN/003/2012_N
            dt, vehicle, work_type, c_id, pos, operation, v_info, state = e
            #  when state is not 'N', what should I do?
            target_qc = None
            qc_id = int(vehicle[3:]) 
            for qc in qcs:
                if qc.veh_id == qc_id:
                    target_qc = qc
                    break
            else:
                target_qc = QC(qc_id)
                qcs.append(target_qc)
            target_qc.evt_seq.append(Evt(dt, vehicle, work_type, c_id, operation, v_info, state, pos))
        elif vehicle[:3] == 'ASC':
            # ex : 2012-02-14-09-02-44_ASC012_1186239_2012-02-14-09-01-13_TwistLock_DFSU2914565_A1-83-6-1_LOADING_MCEN/003/2012_N
            dt, vehicle, _, _, work_type, c_id, pos, operation, v_info, state = e
            #  when state is not 'N', what should I do?
            target_yc = None
            yc_id = int(vehicle[3:]) 
            for yc in ycs:
                if yc.veh_id == yc_id:
                    target_yc = yc
                    break
            else:
                target_yc = YC(yc_id)
                ycs.append(target_yc)
            target_yc.evt_seq.append(Evt(dt, vehicle, work_type, c_id, operation, v_info, state, pos))
        elif vehicle[:2] == 'SH':
            # ex : 2012-02-14-08-49-03_SH19_1185046_2012-02-14-08-48-16_TwistLock_CLHU2825928_STS101-Lane3_DISCHARGING_MCEN/003/2012_N
            dt, vehicle, _, _, work_type, c_id, pos, operation, v_info, state = e
            target_sc = None
            sc_id = int(vehicle[-2:]) 
            for sc in scs:
                if sc.veh_id == sc_id:
                    target_sc = sc
                    break
            else:
                target_sc = SC(sc_id)
                scs.append(target_sc)
            target_sc.evt_seq.append(Evt(dt, vehicle, work_type, c_id, operation, v_info, state, pos))
        else:
            assert False, 'there is not proper vehicle'
        if c_id != 'None' :
            target_c = None
            for c in containers:
                if c.c_id == c_id:
                    target_c = c
                    break
            else:
                target_c = Container(c_id)
                containers.append(target_c)
            target_c.evt_seq.append(Evt(dt, vehicle, work_type, c_id, operation, v_info, state, pos))

def check_v_log(vessels, qcs, ycs, scs):
    wront_v = []
    for v in vessels:
        ar_evt, dp_evt = v.evt_seq[0], v.evt_seq[1]
        if len(v.evt_seq) != 2 or ar_evt.work_type != 'Arrival'or dp_evt.work_type != 'Departure':
            wront_v.append(v)
            break
    for v in qcs + ycs + scs:
        ce_id = -1
        while ce_id != len(v.evt_seq):
            ce_id += 1
            ne_id = ce_id + 1
            if ne_id < len(v.evt_seq):
                ce, ne = v.evt_seq[ce_id], v.evt_seq[ne_id]
                c_ms_wt, n_ms_wt = ce.work_type, ne.work_type
                c_ms_dt, n_ms_dt = ce.dt, ne.dt
                if (c_ms_wt == 'TwistLock' and n_ms_wt == 'TwistLock') or (c_ms_wt == 'TwistUnlock' and n_ms_wt == 'TwistUnlock'):
                    if c_ms_dt!=n_ms_dt: 
                        v.wrong_evt_id = (ce_id, ce.c_id, c_ms_wt, ne_id, ne.c_id, n_ms_wt)
                        wront_v.append(v)
                    break
    return wront_v

def check_c_log(containers):
    wrong_log_containers = []
    for c in containers:
        cur_evt_id = -1
        while cur_evt_id != len(c.evt_seq):
            cur_evt_id += 1
            next_ms_id = cur_evt_id + 1
            cur_ms = c.evt_seq[cur_evt_id]
            if next_ms_id != len(c.evt_seq):
                next_ms = c.evt_seq[next_ms_id]
                c_ms_wt, n_ms_wt = cur_ms.work_type, next_ms.work_type
                if (c_ms_wt == 'TwistLock' and n_ms_wt == 'TwistLock')or (c_ms_wt == 'TwistUnlock' and n_ms_wt == 'TwistUnlock'):
                    wrong_log_containers.append(c)
                    break
            else:
                break
    return wrong_log_containers

if __name__ == '__main__':
    run(True, True)
#    run(False, True)
