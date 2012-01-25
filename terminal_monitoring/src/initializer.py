from __future__ import division
from input import Evts
from classes import Vessel, QC, YC, SC, Container


def read_DB(start_time, end_time):
    pass

def run(start_time, end_time, db_read = False):
    if db_read:
#        E = read_DB(start_time, end_time)
        E = Evts
    else:
        E = Evts
    vechicles = []
    vessels = []
    qcs = []
    ycs = []
    scs = []
    containers = []
    for e in E:
        ec = e.split('_')
        if len(ec) == 5:
            # make vessel
            #  evt ex : '2011-08-23-09-35-00_ABCDEF_02_AR_Bitt11'
            _datetime, v_name, voyage, state, position = ec
            target_v = None
            for v in vessels:
                if v.name == v_name and v.voyage == voyage:
                    target_v = v
                    break
            else:
                target_v = Vessel(v_name, voyage)
                vessels.append(target_v)
            target_v.evt_seq.append((_datetime, state, position))
        else:
            # make others vehicles
            vehicle = ec[1]
            target_c_id = None
            if vehicle[:2] == 'ST':
                # QC evt
                #  evt ex : '2011-08-23-10-00-00_STS01_OD1234_2011-08-23-09-45-00_TL_C01_SB05-05-12_ABCDEF_02_N'
                _datetime, v_name, _, _, operation, c_id, position, _, vessel, voyage, state = ec
                if position == 'OCR':
                    continue
                # TODO
                #  when state is not 'N', what should I do?
                qc_id = vehicle[-2:] 
                target_qc = None
                for q in qcs:
                    if q.name[-2:] == qc_id:
                        target_qc = q
                        break
                else:
                    target_qc = QC(v_name)
                    qcs.append(target_qc)
                target_qc.evt_seq.append((_datetime, vessel, voyage, position, c_id, operation))
                
            elif vehicle[:2] == 'AY':
                # YC evt
                #  evt ex : '2011-08-23-10-05-20_AYC01_OD1235AYC01_2011-08-23-10-05-05_TL_C09_B01-TP02_ABCDEF_02_N'
                # ?? are vessel and voyage needed?
                _datetime, v_name, _, _, operation, c_id, position, _, _, _, state = ec
                yc_id = vehicle[-2:] 
                target_yc = None
                for y in ycs:
                    if y.name[-2:] == yc_id:
                        target_yc = y
                        break
                else:
                    target_yc = YC(v_name)
                    ycs.append(target_yc) 
                target_yc.evt_seq.append((_datetime, position, c_id, operation))
            else:
                # SC evt
                _datetime, v_name, _, _, operation, c_id, position, _, _, _, state = ec
                sc_id = vehicle[-2:] 
                target_sc = None
                for s in scs:
                    if s.name[-2:] == sc_id:
                        target_sc = s
                        break
                else:
                    target_sc = SC(v_name)
                    scs.append(target_sc) 
                target_sc.evt_seq.append((_datetime, position, c_id, operation))
            
            target_c_id = c_id
            target_c = None
            for c in containers:
                if c._id == target_c_id:
                    target_c = c
                    break
            else:
                target_c = Container(target_c_id)
                containers.append(target_c)
            target_c.moving_seq.append((_datetime, position, v_name))
    
    for v in [vessels, qcs, ycs, scs]:
        vechicles.append(v)
        
    return vechicles, containers
    
#yard = [objects of Yard_block]
if __name__ == '__main__':
    vs, cs = run(1,2)
    for v in vs:
        for x in v:
            if isinstance(x, Vessel):
                print 'vessel ',
            elif isinstance(x, QC):
                print 'qc ',
            elif isinstance(x, YC):
                print 'yc ',
            elif isinstance(x, SC):
                print 'sc ',
            print x.name, ':', x.evt_seq
    print ''
    for c in cs:
        print c._id, ':', c.moving_seq
