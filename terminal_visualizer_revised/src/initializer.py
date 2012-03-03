from __future__ import division
from vehicle_classes import QC, YC, SC
from others_classes import Vessel, Container, Evt
    
def run(real_log=True, checking_log=False):
    EVT = []
    if real_log:
        log_text = open('real_log_sorted_by_dt')
    else:
        log_text = open('maked_log_sorted_by_dt')
    
    for l in log_text.readlines():
        e = l[:-1].split('_')
        EVT.append(e)
    vessels, qcs , ycs, scs , containers = [], [], [], [], []
    
    if real_log:
        init_real_log(vessels, qcs, ycs, scs, containers, EVT)
    else:
        init_maked_log(vessels, qcs , ycs, scs , containers, EVT)
        
    if checking_log: 
        wrong_c = check_log(containers)
        wc_set, c_set = set(wrong_c), set(containers)
        print 'correct moving container : ', c_set - wc_set 
        print 'wrong moving container : ', wc_set
    
    return vessels, qcs , ycs, scs , containers

def init_maked_log(vessels, qcs , ycs, scs , containers, EVT):
    for e in EVT:
        vehicle = e[1]
        if vehicle[:3] == 'STS':
            #ex : 2011-08-23-10-00-00_STS01_OD1234_2011-08-23-09-45-00_TL_C01_SB05-05-12_DC_ABCDEF_02_N  
            dt, vehicle, _, _, work_type, c_id, pos, operation, v_name, v_voyage, state = e
            v_info = v_name + '/' + v_voyage
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
        elif vehicle[:3] == 'AYC':
            # ex : 2011-08-23-10-06-10_AYC01_OD1235AYC01_2011-08-23-10-05-05_TU_C09_B01-15-06-02_DC_ABCDEF_02_N
            dt, vehicle, _, _, work_type, c_id, pos, operation, v_name, v_voyage, state = e
            v_info = v_name + '/' + v_voyage
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
        elif vehicle[:2] == 'SC':
            # ex : 2011-08-23-11-42-30_SC07_OD1235SC07_2011-08-23-10-41-05_TU_C16_STS02-Lane02_LD_ABCDEF_02_N
            dt, vehicle, _, _, work_type, c_id, pos, operation, v_name, v_voyage, state = e
            v_info = v_name + '/' + v_voyage
            target_sc = None
            sc_id = int(vehicle[3:]) 
            for sc in scs:
                if sc.veh_id == sc_id:
                    target_sc = sc
                    break
            else:
                target_sc = SC(sc_id)
                scs.append(target_sc)
            target_sc.evt_seq.append(Evt(dt, vehicle, work_type, c_id, operation, v_info, state, pos))
        else:
            # ex : 2011-08-23-09-35-00_ABCDEF_02_AR_Bitt06
            ## assert vessel
            dt, v_name, v_voyage, work_type, pos = e
            vehicle = 'Vessel'
            v_info = v_name + '/' + v_voyage 
            assert pos[:4] == 'Bitt', 'this evt is not related with vessel' 
            target_v = None
            for v in vessels:
                if v.name == v_name and v.voyage == v_voyage:
                    target_v = v
                    break
            else:
                target_v = Vessel(v_name, v_voyage)
                vessels.append(target_v)
            target_v.evt_seq.append(Evt(dt, vehicle , work_type, None, None, v_info, None, pos))
        if vehicle != 'Vessel':
            target_c = None
            for c in containers:
                if c.c_id == c_id:
                    target_c = c
                    break
            else:
                target_c = Container(c_id)
                containers.append(target_c)
            target_c.evt_seq.append(Evt(dt, vehicle, work_type, c_id, operation, v_info, state, pos))
            
def init_real_log(vessels, qcs, ycs, scs, containers, EVT):
    #TODO
    # after receive vessel arrival and departure time
    # pleas revise this part
    start_evt = EVT[0]
    end_evt = EVT[-1]
    vehicle, pos, c_id, operation = 'Vessel', 'Bitt06', None, None 
    if len(start_evt) == 7: 
        dt, _, _, _, _, v_info, state = start_evt
    else: 
        dt, _, _, _, _, _, _, _, v_info, state = start_evt
    v_name, v_voyage_txt, _ = v_info.split('/')
    vessel = Vessel(v_name, int(v_voyage_txt))
    work_type = 'Arrival'
    vessel.evt_seq.append(Evt(dt, vehicle, work_type, c_id, operation, v_info, state, pos))
    if len(end_evt) == 7: 
        dt, _, _, _, _, v_info, state = end_evt
    else: 
        dt, _, _, _, _, _, _, _, v_info, state = end_evt
    work_type = 'Departure'
    vessel.evt_seq.append(Evt(dt, vehicle, work_type, c_id, operation, v_info, state, pos))
    vessels.append(vessel)
    for e in EVT:
        vehicle = e[1]
        if vehicle[:3] == 'STS':
            # ex : 2012-02-14-10-59-20_STS101_TwistLock_HLXU3395821_LOADING_MCEN/003/2012_N
            dt, vehicle, work_type, c_id, operation, v_info, state = e
            pos = None
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
            target_qc.evt_seq.append(Evt(dt, vehicle, work_type, c_id, operation, v_info, state))
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
            sc_id = int(vehicle[3:]) 
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
        target_c = None
        for c in containers:
            if c.c_id == c_id:
                target_c = c
                break
        else:
            target_c = Container(c_id)
            containers.append(target_c)
        target_c.evt_seq.append(Evt(dt, vehicle, work_type, c_id, operation, v_info, state, pos))
        
def check_log(containers):
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
