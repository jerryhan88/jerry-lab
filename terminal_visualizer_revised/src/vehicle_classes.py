from __future__ import division
from datetime import timedelta
from parameter_function import container_hs, container_vs, calc_proportional_pos, change_b_color
from storage_classes import Block, QB
from others_classes import Vessel
import wx, math

class Vehicles(object):
    def __init__(self):
        self.veh_id, self.name = None, None
        self.evt_seq, self.target_evt_id, self.evt_start, self.evt_end = [], 0, True, False
        self.tg_time, self.tg_pos, self.tg_container, self.tg_work_type, self.tg_px, self.tg_py = None, None, None, None, None, None
        self.px, self.py = None, None
        self.pe_time, self.pe_px, self.pe_py = None, None, None
        self.holding_containers = {}
    def __repr__(self):
        return str(self.name + str(self.veh_id))
    def set_evt_data(self, cur_evt_id):
        pass
    def update_pos(self, simul_time):
        pass
    def update_container_ownership(self, simul_time):
        pass
    def draw(self, gc):
        pass
        
class QC(Vehicles):
    Vessels, QBs = None, None
    sx, sy = container_hs * 0.6 , container_hs * 10 
    tro_sx, tro_sy = container_hs * 0.5, container_vs * 0.8
    class Trolly(Vehicles):
        def __init__(self):
            Vehicles.__init__(self)
        def draw(self, gc, holding_containers):
            for c in holding_containers.values():
                old_tr = gc.GetTransform()
                gc.Translate(0, -QC.sy)
                c.draw(gc)
                gc.SetTransform(old_tr)
            ##draw trolly
            tr, tg, tb = (4, 189, 252)
            t_color = wx.Colour(tr, tg, tb)         
            gc.SetPen(wx.Pen('cyan', 0))
            gc.SetBrush(wx.Brush(t_color))
            gc.DrawRectangle(-QC.tro_sx / 2, -QC.tro_sy / 2 - QC.sy, QC.tro_sx, QC.tro_sy)
            
    def __init__(self, veh_id):
        Vehicles.__init__(self)
        self.name = 'STS'
        self.veh_id = veh_id
        self.target_v, self.target_qb = None, None
        self.trolly = self.Trolly()
        #trolley moving start time
        self.tro_ms_time = None
        #trolley moving end time and operating start time
        self.tro_mf_time = None
        self.calc_tro_ori_py = lambda res : res.py - (self.py - QC.sy)
            
    def calc_tro_ori_py(self, res):
        if isinstance(res, Vessel): py = res.anchored_py
        elif isinstance(res, QB): py = res.py
        else: assert False
        return py - (self.py - QC.sy) 

    def calc_qc_pos(self, evt_id, is_calc_tg):
        pos, pe_pos = self.evt_seq[evt_id].pos, None
        wt, oper = self.evt_seq[evt_id].work_type, self.evt_seq[evt_id].operation
        pe_evt_id = evt_id - 1
        if pe_evt_id != -1: pe_pos = self.evt_seq[pe_evt_id].pos
        if is_calc_tg and wt == 'TwistLock' and oper == 'LOADING':
            ne_pos = self.evt_seq[evt_id+1].pos
            bay_id = int(ne_pos[2:4])
            px = self.target_v.px + self.target_v.bay_pos_info[bay_id]
            return px 
            
        if pe_pos:
            if pos[:2] == 'SB' and pe_pos[7:-2] == 'Lane':
                bay_id = int(pos[2:4])
                px = self.target_v.px + self.target_v.bay_pos_info[bay_id]
            elif pos[7:-2] == 'Lane' and pe_pos[:2] == 'SB':
                bay_id = int(pe_pos[2:4]) 
                px = self.target_v.px + self.target_v.bay_pos_info[bay_id]
            elif pos[7:-2] == 'Lane' and pe_pos[7:-2] == 'Lane':
                ne_pos = self.evt_seq[evt_id + 1].pos
                bay_id = int(ne_pos[2:4]) 
                px = self.target_v.px + self.target_v.bay_pos_info[bay_id]
            elif pos[:2] == 'SB' and pe_pos[:2] == 'SB':
                assert False
        else:
            bay_id = int(pos[2:4]) 
            px = self.target_v.px + self.target_v.bay_pos_info[bay_id]
        return px
    
    def calc_tro_pos(self, target_evt_id):
        evt = self.evt_seq[target_evt_id]
        pos, wt, oper = evt.pos, evt.work_type, evt.operation
        if wt == 'TwistLock' and oper == 'DISCHARGING' or (wt == 'TwistUnlock' and oper == 'LOADING'):
            stack_id = int(pos[5:7])
            py = self.calc_tro_ori_py(self.target_v) + self.target_v.stack_pos_info[stack_id]
        elif (wt == 'TwistUnlock' and oper == 'DISCHARGING') or (wt == 'TwistLock' and oper == 'LOADING'):
            qb_id = int(pos[-2:])
            self.target_qb = QC.QBs[qb_id]
            py = self.calc_tro_ori_py(self.target_qb) + self.target_qb.v_c_pos_info
        else:
            assert False 
        return py    
    
    def set_evt_data(self, target_evt_id, simul_clock):
        self.target_evt = self.evt_seq[target_evt_id]
        self.tg_time = self.target_evt.dt
        v_name, v_voyage_txt, _ = self.target_evt.v_info.split('/')
        if self.target_v == None or self.target_v.name != v_name:    
            for v in QC.Vessels:
                if v.name == v_name and v.voyage == int(v_voyage_txt):
                    self.target_v = v
                    break
            else:
                assert False, 'There is not target Vessel'
        self.tg_px = self.calc_qc_pos(target_evt_id, True)
        self.trolly.tg_py = self.calc_tro_pos(target_evt_id)
        
        if target_evt_id == 0:
            self.pe_time = self.tg_time - timedelta(seconds=5)
            self.pe_px = self.px = self.tg_px
            self.trolly.pe_px, self.trolly.pe_py = self.trolly.px, self.trolly.py = 0 , container_hs * 4
        else:
            if self.evt_start:
                pe_id = target_evt_id - 1
                self.pe_time = self.evt_seq[pe_id].dt
                self.pe_px = self.calc_qc_pos(pe_id, False)
                self.trolly.pe_px, self.trolly.pe_py = self.trolly.px, self.trolly.py = 0 , self.calc_tro_pos(pe_id)
            self.trolly.py = self.trolly.pe_py
            self.px = self.pe_px
        time_interval = self.tg_time - self.pe_time
        assert 0 <= time_interval.total_seconds() < 3600 * 24, False
        self.tro_ms_time = self.pe_time + timedelta(seconds=time_interval.total_seconds() * (1 / 5))
        self.tro_mf_time = self.pe_time + timedelta(seconds=time_interval.total_seconds() * (4 / 5))
        self.update_pos(simul_clock)
                
    def update_pos(self, simul_clock):
#        evt = self.evt_seq[self.target_evt_id]
#        pos, wt, oper, tg_container = evt.pos, evt.work_type, evt.operation, evt.c_id
#        if wt == 'TwistLock' and oper == 'LOADING':
#            target_qb = QC.QBs[int(pos[-2:])]
#            if tg_container in target_qb.holding_containers:
#                self.tg_px = target_qb.holding_containers[tg_container].px
#            
        if self.pe_time <= simul_clock < self.tro_ms_time:
            #straddler moving
            self.px = self.pe_px + calc_proportional_pos(self.pe_px, self.tg_px, self.pe_time, self.tro_ms_time, simul_clock)
        elif self.tro_ms_time <= simul_clock < self.tro_mf_time:
            self.px = self.tg_px
            #trolly moving
            self.trolly.py = self.trolly.pe_py + calc_proportional_pos(self.trolly.pe_py, self.trolly.tg_py, self.tro_ms_time, self.tro_mf_time, simul_clock)
        elif self.tro_mf_time <= simul_clock < self.tg_time:
            self.px = self.tg_px
            self.trolly.py = self.trolly.tg_py
        if self.tg_time <= simul_clock:
            self.pe_time = self.tg_time
            self.pe_px = self.px = self.tg_px
            self.trolly.pe_py = self.trolly.tg_py
            if self.evt_start: self.evt_start = False
    def update_container_ownership(self, simul_time):
        evt = self.evt_seq[self.target_evt_id]
        wt, oper, c_id = evt.work_type, evt.operation, evt.c_id
        if wt == 'TwistLock' and oper == 'DISCHARGING':
            tg_container = self.target_v.holding_containers.pop(c_id)
            tg_container.px, tg_container.py = 0, 0
            self.holding_containers[c_id] = tg_container
        elif wt == 'TwistUnlock'and oper == 'DISCHARGING':
            tg_container = self.holding_containers.pop(c_id)
            tg_container.px, tg_container.py = self.px, self.target_qb.v_c_pos_info
            self.target_qb.holding_containers[c_id] = tg_container
        elif wt == 'TwistLock' and oper == 'LOADING':
            pos = evt.pos
            qb_id = int(pos[-2:])
            target_qb = QC.QBs[qb_id]
            tg_container = target_qb.holding_containers.pop(c_id)
            tg_container.px, tg_container.py = 0, 0
            self.holding_containers[c_id] = tg_container
        elif wt == 'TwistUnlock' and oper == 'LOADING':
            pos = evt.pos    
            tg_container = self.holding_containers.pop(c_id)
            bay_id, stack_id = int(pos[2:4]), int(pos[5:7]) 
            tg_container.px, tg_container.py = self.target_v.bay_pos_info[bay_id] , self.target_v.stack_pos_info[stack_id]
            self.target_v.holding_containers[c_id] = tg_container
        else:
            assert False
        tg_container.target_evt_id += 1 
        
    def draw(self, gc):
        gc.SetPen(wx.Pen('black', 0.5))
        r, g, b = (0, 0, 0)
        brushclr = wx.Colour(r, g, b)
        paint = wx.Colour(r, g, b, 0)
        gc.SetPen(wx.Pen(brushclr, 1))
        gc.SetBrush(wx.Brush(paint))
        gc.DrawLines([(QC.sx / 2, -QC.sy), (QC.sx / 2, 0)])
        gc.DrawLines([(-QC.sx / 2, -QC.sy), (-QC.sx / 2, 0)])
        gc.DrawLines([(-QC.sx / 2, -container_hs), (QC.sx / 2, 0)])
        gc.DrawLines([(QC.sx / 2, -container_hs), (-QC.sx / 2, 0)])
        gc.DrawLines([(-QC.sx / 2, -container_hs), (QC.sx / 2, -container_hs)])
        gc.DrawLines([(-QC.sx / 2, 0), (QC.sx / 2, 0)])
        
        for i in range(12):
            gc.DrawLines([(-QC.sx / 2, container_hs * 0.5 * i - QC.sy), (QC.sx / 2, container_hs * 0.5 * i - QC.sy)])
        
        old_tr = gc.GetTransform()
        gc.Translate(self.trolly.px, self.trolly.py)
        self.trolly.draw(gc, self.holding_containers)
        gc.SetTransform(old_tr)

class SC(Vehicles):
    Vessels, QBs, TPs, QCs = None, None, None, None
    sx, sy = container_hs * 1.2, container_vs * 1.2
    def __init__(self, veh_id):
        Vehicles.__init__(self)
        self.name = 'SH'
        self.veh_id = veh_id
        self.target_qb, self.target_tp, self.target_qc = None, None, None
        ## ss: sea side, ls: land side 
        self.ss_ls, self.ss_ss, self.ls_ss, self.ls_ls = False, False, False, False
        self.waypoint1_time, self.waypoint2_time, self.waypoint3_time = None, None, None
        self.waypoint1_pos , self.waypoint2_pos, self.waypoint3_pos = (None, None), (None, None), (None, None)
        self.thr_wp1, self.thr_wp2, self.thr_wp3 = None, None, None
        self.lu_px, self.lu_py = -SC.sx / 2, -SC.sy / 2
    
    def calc_sc_pos(self, evt_id, is_tg_evt):
        evt = self.evt_seq[evt_id] 
        pos = evt.pos
        c_id = evt.c_id
        pe_evt_id = evt_id - 1
        pe_evt = None
        if pe_evt_id != -1: pe_evt = self.evt_seq[pe_evt_id] 
        target_qb, target_tp = None, None
        ss_ls, ss_ss, ls_ss, ls_ls = False, False, False, False
        if pos[:3] == 'STS':
            target_qc_id = int(pos[3:6]) 
            for qc in SC.QCs:
                if qc.veh_id == target_qc_id:
                    target_qc = qc
                    break
            else:
                assert False, 'there is not target qc'
            qb_id = int(pos[-1:])
            target_qb = SC.QBs[qb_id]
            px, py = target_qc.px, target_qb.py + target_qb.v_c_pos_info
            if pe_evt and pe_evt.pos[:2] == 'LM':
                oper = evt.operation
                wt = evt.work_type
                if wt == 'TwistUnlock' and oper == 'LOADING':
                    target_qc = None
                    qc_id = int(pos[3:6])
                    for qc in SC.QCs:
                        if qc.veh_id == qc_id:
                            target_qc = qc
                            break
                    cur_qc_evt_id = 0
                    c_qc_evt = target_qc.evt_seq[cur_qc_evt_id]  
                    while c_id != c_qc_evt.c_id or c_qc_evt.dt < evt.dt:
                        cur_qc_evt_id += 1
                        c_qc_evt = target_qc.evt_seq[cur_qc_evt_id]
                    qc_ne_evt = target_qc.evt_seq[cur_qc_evt_id + 1]
                    ne_pos = qc_ne_evt.pos 
                    bay_id, stack_id = int(ne_pos[2:4]), int(ne_pos[5:7])
                    target_v = None
                    v_name, v_voyage_txt, _ = self.target_evt.v_info.split('/')
                    for v in SC.Vessels:
                        if v.name == v_name and v.voyage == int(v_voyage_txt):
                            target_v = v
                            break
                    else:
                        assert False, 'There is not target Vessel'
                            
                    px = target_v.px + target_v.bay_pos_info[bay_id]
                ls_ss = True
            elif pe_evt and pe_evt.pos[:3] == 'STS':
                target_qc = None
                qc_id = int(pos[3:6])
                for qc in SC.QCs:
                    if qc.veh_id == qc_id:
                        target_qc = qc
                        break
                cur_qc_evt_id = 0
                c_qc_evt = target_qc.evt_seq[cur_qc_evt_id]  
                while c_id != c_qc_evt.c_id or c_qc_evt.dt < evt.dt:
                    cur_qc_evt_id += 1
                    c_qc_evt = target_qc.evt_seq[cur_qc_evt_id]
                qc_ne_evt = target_qc.evt_seq[cur_qc_evt_id + 1]
                ne_pos = qc_ne_evt.pos 
                bay_id, stack_id = int(ne_pos[2:4]), int(ne_pos[5:7])
                target_v = None
                v_name, v_voyage_txt, _ = self.target_evt.v_info.split('/')
                for v in SC.Vessels:
                    if v.name == v_name and v.voyage == int(v_voyage_txt):
                        target_v = v
                        break
                else:
                    assert False, 'There is not target Vessel'
                px = target_v.px + target_v.bay_pos_info[bay_id]
                ss_ss = True
            else:
                assert not pe_evt
        elif pos[:2] == 'LM':
            tp_id, stack_id = pos[3:5], int(pos[8:])
            target_tp = SC.TPs[tp_id]
            px, py = target_tp.px + target_tp.stack_pos_info[stack_id], target_tp.py + target_tp.bay_pos_info
            
            if pe_evt and pe_evt.pos[:2] == 'LM':
                ls_ls = True
            elif pe_evt and pe_evt.pos[:3] == 'STS':
                ss_ls = True
            else:
                assert not pe_evt
        else:
            assert False
        if is_tg_evt:
            self.target_qb, self.target_tp = target_qb, target_tp 
            self.ss_ls, self.ss_ss, self.ls_ss, self.ls_ls = ss_ls, ss_ss, ls_ss, ls_ls
            self.tg_container = c_id
        return px, py
    
    def set_evt_data(self, target_evt_id, simul_clock):
        self.target_evt = self.evt_seq[target_evt_id]
        self.tg_time = self.target_evt.dt 
        self.tg_px, self.tg_py = self.calc_sc_pos(target_evt_id, True)
        
        if target_evt_id == 0:
            self.pe_time = self.tg_time - timedelta(seconds=8)
            self.pe_px, self.pe_py = self.px, self.py = self.tg_px - container_hs * 10, self.tg_py
            self.ss_ls = True
        else:
            if self.evt_start:
                pe_evt_id = target_evt_id - 1
                self.pe_time = self.evt_seq[pe_evt_id ].dt
                self.pe_px, self.pe_py = self.calc_sc_pos(pe_evt_id, False) 
            
            time_interval = self.tg_time - self.pe_time
            assert 0 <= time_interval.total_seconds() < 3600 * 24, False
            ti_ts = time_interval.total_seconds()
            
            if self.ss_ls:
                self.waypoint1_time = self.pe_time + timedelta(0, ti_ts * (3 / 10))
                self.waypoint2_time = self.pe_time + timedelta(0, ti_ts * (6 / 10))
                self.waypoint3_time = self.pe_time + timedelta(0, ti_ts * (9 / 10))
                self.wp1_px, self.wp1_py = (self.pe_px + container_hs * 10, self.pe_py)
                self.wp2_px, self.wp2_py = (self.pe_px + container_hs * 10, self.tg_py - container_hs)
                self.wp3_px, self.wp3_py = (self.tg_px, self.tg_py - container_hs)
            elif self.ls_ss:
                self.waypoint1_time = self.pe_time + timedelta(0, ti_ts * (0.1 / 10))
                self.waypoint2_time = self.pe_time + timedelta(0, ti_ts * (4 / 10))
                self.waypoint3_time = self.pe_time + timedelta(0, ti_ts * (9 / 10))
                self.wp1_px, self.wp1_py = (self.pe_px, self.pe_py - container_hs)
                self.wp2_px, self.wp2_py = (self.pe_px - container_hs * 4, self.pe_py - container_hs)
                self.wp3_px, self.wp3_py = (self.pe_px - container_hs * 4, self.tg_py)
            elif self.ls_ls:
                self.waypoint1_time = self.pe_time + timedelta(0, ti_ts * (0.1 / 10))
                self.waypoint2_time = self.pe_time + timedelta(0, ti_ts * (9 / 10))
                self.wp1_px, self.wp1_py = (self.pe_px, self.pe_py - container_hs)
                self.wp2_px, self.wp2_py = (self.tg_px, self.tg_py - container_hs)
            elif self.ss_ss:
                pass
            else:
                assert False
            self.update_pos(simul_clock)
                
        self.thr_wp1 = False
        self.thr_wp2 = False
        self.thr_wp3 = False

    def update_container_ownership(self, simul_clock):
        tg_evt = self.evt_seq[self.target_evt_id]
        wt, oper, c_id, pos = tg_evt.work_type, tg_evt.operation, tg_evt.c_id, tg_evt.pos
        if wt == 'TwistLock' and oper == 'DISCHARGING':
            tg_container = self.target_qb.holding_containers.pop(c_id)
            tg_container.px, tg_container.py = 0, 0
            self.holding_containers[c_id] = tg_container
        elif wt == 'TwistUnlock' and oper == 'DISCHARGING':
            tg_container = self.holding_containers.pop(c_id)
            stack_id = int(pos[8:])
            tg_container.px, tg_container.py = self.target_tp.stack_pos_info[stack_id], self.target_tp.bay_pos_info
            save_c_hs = tg_container.hs 
            tg_container.hs = tg_container.vs
            tg_container.vs = save_c_hs
            self.target_tp.holding_containers[c_id] = tg_container
        elif wt == 'TwistLock' and oper == 'LOADING':
            if pos[:3] == 'STS':
                target_qb = SC.QBs[int(pos[-2:])]
                tg_container = target_qb.holding_containers.pop(c_id)
                tg_container.px, tg_container.py = 0, 0
                self.holding_containers[c_id] = tg_container
            else:
                tp_id, stack_id = pos[3:5], int(pos[8:])
                target_tp = SC.TPs[tp_id]
                tg_container = target_tp.holding_containers.pop(c_id)
                tg_container.px, tg_container.py = 0, 0
                save_c_hs = tg_container.hs 
                tg_container.hs = tg_container.vs
                tg_container.vs = save_c_hs
                self.holding_containers[c_id] = tg_container
        elif wt == 'TwistUnlock' and oper == 'LOADING':
            tg_container = self.holding_containers.pop(c_id)
            qb_id = int(pos[-1:])
            target_qb = SC.QBs[qb_id]
            target_v = None
            c_ne_pos = tg_container.evt_seq[tg_container.target_evt_id + 3].pos
            bay_id = int(c_ne_pos[2:4]) 
            v_name, v_voyage_txt, _ = tg_evt.v_info.split('/')
            for v in SC.Vessels:
                if v.name == v_name and v.voyage == int(v_voyage_txt):
                    target_v = v
                    break
            else:
                assert False, 'There is not target Vessel'
            tg_container.px, tg_container.py = target_v.px + target_v.bay_pos_info[bay_id], target_qb.v_c_pos_info
            target_qb.holding_containers[c_id] = tg_container
        else:
            assert False
        tg_container.target_evt_id += 1   
    
    def update_pos(self, simul_clock):
        if self.target_evt_id == 0:
            if self.tg_container in self.target_qb.holding_containers:
                self.tg_px = self.target_qb.holding_containers[self.tg_container].px
            if self.pe_time <= simul_clock < self.tg_time:
                self.px = self.pe_px + calc_proportional_pos(self.pe_px, self.tg_px, self.pe_time, self.tg_time, simul_clock)
        else:
            if self.ss_ls:
                if self.pe_time <= simul_clock < self.waypoint1_time:
                    self.px = self.pe_px + calc_proportional_pos(self.pe_px, self.wp1_px, self.pe_time, self.waypoint1_time, simul_clock) 
                    self.py = self.pe_py
                elif self.waypoint1_time <= simul_clock < self.waypoint2_time:
                    self.thr_wp1 = True
                    self.px = self.wp1_px  
                    self.py = self.wp1_py + calc_proportional_pos(self.wp1_py, self.wp2_py, self.waypoint1_time, self.waypoint2_time, simul_clock) 
                elif self.waypoint2_time <= simul_clock < self.waypoint3_time:
                    self.thr_wp1 = False
                    self.thr_wp2 = True
                    self.px = self.wp2_px + calc_proportional_pos(self.wp2_px, self.wp3_px, self.waypoint2_time, self.waypoint3_time, simul_clock) 
                    self.py = self.wp2_py
                elif self.waypoint3_time <= simul_clock < self.tg_time:
                    self.thr_wp2 = False
                    self.thr_wp3 = True
                    self.px = self.wp3_px
                    self.py = self.wp3_py + calc_proportional_pos(self.wp3_py, self.tg_py, self.waypoint3_time, self.tg_time, simul_clock) 
            elif self.ls_ss:
                if self.tg_container in self.target_qb.holding_containers:
                    self.tg_px = self.target_qb.holding_containers[self.tg_container].px
                if self.pe_time <= simul_clock < self.waypoint1_time:
                    self.px = self.pe_px
                    self.py = self.pe_py + calc_proportional_pos(self.pe_py, self.wp1_py, self.pe_time, self.waypoint1_time, simul_clock)
                elif self.waypoint1_time <= simul_clock < self.waypoint2_time:
                    self.thr_wp1 = True
                    self.px = self.wp1_px + calc_proportional_pos(self.wp1_px, self.wp2_px, self.waypoint1_time, self.waypoint2_time, simul_clock)
                    self.py = self.wp1_py
                elif self.waypoint2_time <= simul_clock < self.waypoint3_time:
                    self.thr_wp1 = False
                    self.thr_wp2 = True
                    self.px = self.wp2_px
                    self.py = self.wp2_py + calc_proportional_pos(self.wp2_py, self.wp3_py, self.waypoint2_time, self.waypoint3_time, simul_clock) 
                elif self.waypoint3_time <= simul_clock < self.tg_time:
                    self.thr_wp2 = False
                    self.thr_wp3 = True
                    self.px = self.wp3_px + calc_proportional_pos(self.wp3_px, self.tg_px, self.waypoint3_time, self.tg_time, simul_clock) 
                    self.py = self.wp3_py
            elif self.ls_ls:
                if self.pe_time <= simul_clock < self.waypoint1_time:
                    self.px = self.pe_px
                    self.py = self.pe_py + calc_proportional_pos(self.pe_py, self.wp1_py, self.pe_time, self.waypoint1_time, simul_clock)
                elif self.waypoint1_time <= simul_clock < self.waypoint2_time:
                    self.thr_wp1 = True
                    self.px = self.wp1_px + calc_proportional_pos(self.wp1_px, self.wp2_px, self.waypoint1_time, self.waypoint2_time, simul_clock)
                    self.py = self.wp1_py
                elif self.waypoint2_time <= simul_clock < self.tg_time:
                    self.thr_wp1 = False
                    self.thr_wp2 = True
                    self.px = self.wp2_px
                    self.py = self.wp2_py + calc_proportional_pos(self.wp2_py, self.tg_py, self.waypoint2_time, self.tg_time, simul_clock)
            elif self.ss_ss:
                self.px = self.pe_px + calc_proportional_pos(self.pe_px, self.tg_px, self.pe_time, self.tg_time, simul_clock)
        if self.tg_time <= simul_clock:
            self.pe_time = self.tg_time
            self.pe_px, self.pe_py = self.px, self.py = self.tg_px, self.tg_py
            if self.evt_start: self.evt_start = False 
    
    def draw(self, gc):
        if self.ss_ls:
            if self.thr_wp1:
                gc.Rotate(math.pi / 2)
            elif self.thr_wp2:
                gc.Rotate(-math.pi)
            elif self.thr_wp3:
                gc.Rotate(math.pi / 2)
            else:
                gc.Rotate(0)
        elif self.ls_ss:
            if self.thr_wp1:
                gc.Rotate(-math.pi)
            elif self.thr_wp2:
                gc.Rotate(-math.pi / 2)
            elif self.thr_wp3:
                gc.Rotate(0)
            else:
                gc.Rotate(-math.pi / 2)
        elif self.ls_ls:
            if self.thr_wp1:
                gc.Rotate(-math.pi)
            elif self.thr_wp2:
                gc.Rotate(math.pi / 2)    
            else:
                gc.Rotate(-math.pi / 2)
        for c in self.holding_containers.values():
            c.draw(gc)
        tire_d = 5
        gc.SetPen(wx.Pen(wx.Colour(226, 56, 20), 1))
        gc.DrawLines([(self.lu_px, self.lu_py), (self.lu_px + SC.sx, self.lu_py)])
        gc.DrawLines([(self.lu_px, self.lu_py + SC.sy), (self.lu_px + SC.sx, self.lu_py + SC.sy)])
        gc.DrawLines([(self.lu_px, self.lu_py), (self.lu_px, self.lu_py + SC.sy)])
        gc.DrawLines([(self.lu_px + SC.sx, self.lu_py), (self.lu_px + SC.sx, self.lu_py + SC.sy)])
        gc.SetBrush(wx.Brush(wx.Colour(226, 56, 20)))
        gc.DrawLines([(self.lu_px + SC.sx, self.lu_py + 1), (self.lu_px + SC.sx - container_vs * 0.7, self.lu_py + 1), (self.lu_px + SC.sx - container_vs * 0.7, self.lu_py + SC.sy / 2), (self.lu_px + SC.sx, self.lu_py + SC.sy / 2)])
        
class YC(Vehicles):
    TPs, Blocks = None, None
    tro_sx, tro_sy = container_vs * 0.8, container_hs * 0.8
    tro_L_btw_C = container_vs * 4.0
    sy = container_vs * Block.num_of_stacks
    dif_btw_b_tp = container_vs * 0.5
    
    class Trolly(Vehicles):
        def __init__(self):
            Vehicles.__init__(self)
        def draw(self, gc, holding_containers):
            for c in holding_containers.values():
                old_tr = gc.GetTransform()
                gc.Translate(-YC.tro_L_btw_C, 0)
                c.draw(gc)
                gc.SetTransform(old_tr)
            tr, tg, tb = (4, 189, 252)
            t_color = wx.Colour(tr, tg, tb, 200)
            ##draw trolly
            gc.SetPen(wx.Pen(t_color, 0))
            gc.SetBrush(wx.Brush(t_color))
            gc.DrawRectangle(-YC.tro_L_btw_C - YC.tro_sx / 2, -YC.tro_sy / 2, YC.tro_sx, YC.tro_sy)

    def __init__(self, veh_id):
        Vehicles.__init__(self)
        self.name = 'ASC'
        self.veh_id = veh_id
        self.target_tp, self.target_block = None, None
        self.trolly = self.Trolly()
        self.trolly.px, self.trolly.py = container_vs * 4, 0
        #trolly moving start time
        self.tro_ms_time = None
        #trolly operating start time
        self.tro_mf_time = None
    
    def draw(self, gc):
        gc.SetPen(wx.Pen('purple', 0))
        change_b_color(gc, 'purple')
        gc.DrawRectangle(-container_vs * 1.1 - YC.sy / 2, -container_hs * 1.1 / 2, container_vs * 1.1, container_hs * 1.1)
        gc.DrawRectangle(-container_vs * 1.1 - YC.sy / 2 + YC.sy + container_vs * 1.1, -container_hs * 1.1 / 2, container_vs * 1.1, container_hs * 1.1)
        gc.DrawRectangle(-YC.sy / 2, -6, YC.sy, 3)
        gc.DrawRectangle(-YC.sy / 2, 3, YC.sy, 3)
        old_tr = gc.GetTransform()
        gc.Translate(self.trolly.px, self.trolly.py)
        self.trolly.draw(gc, self.holding_containers)
        gc.SetTransform(old_tr)    
    
    def calc_yc_pos(self, evt_id, is_tg_evt):
        evt = self.evt_seq[evt_id]
        pos = evt.pos
        target_tp, target_block = None, None
        stack_id, bay_id = None, None
        if pos[:2] == 'LM':
            tp_id, stack_id = pos[3:5], int(pos[-1:])
            target_tp = YC.TPs[tp_id]
            py = target_tp.py + target_tp.bay_pos_info
        elif pos[:1] == 'A'or pos[:1] == 'B':
            block_id, bay_id, stack_id = pos[:2], int(pos[3:5]), int(pos[6:7])
            target_block = YC.Blocks[block_id]
            py = target_block.py + target_block.bay_pos_info[bay_id]
        else:
            assert False
        if is_tg_evt:
            self.target_tp, self.target_block = target_tp, target_block
            self.stack_id, self.bay_id = stack_id, bay_id
        return py
    
    def calc_tro_pos(self, evt_id):
        evt = self.evt_seq[evt_id]
        pos = evt.pos
        if pos[:2] == 'LM':
            tp_id, stack_id = pos[3:5], int(pos[-1:])
            target_tp = YC.TPs[tp_id]
            px = target_tp.stack_pos_info[stack_id] + YC.dif_btw_b_tp
        elif pos[:1] == 'A'or pos[:1] == 'B':
            block_id, stack_id = pos[:2], int(pos[6:7])
            target_block = YC.Blocks[block_id]
            px = target_block.stack_pos_info[stack_id]
        else:
            assert False
        return px
    
    def set_evt_data(self, target_evt_id, simul_clock):
        self.target_evt = self.evt_seq[target_evt_id]
        self.tg_time, self.tg_container, self.tg_work_type, self.tg_operation = self.target_evt.dt, self.target_evt.c_id, self.target_evt.work_type, self.target_evt.operation
        self.tg_py = self.calc_yc_pos(target_evt_id, True)
        self.trolly.tg_px = self.calc_tro_pos(target_evt_id)
            
        if target_evt_id == 0:
            self.pe_time = self.tg_time - timedelta(seconds=10)
            self.pe_py = self.py = self.tg_py + container_hs * 1.5
            self.trolly.pe_px = self.trolly.px = container_vs * 2
        else:
            if self.evt_start:
                pe_id = target_evt_id - 1
                self.pe_time = self.evt_seq[pe_id].dt
                self.pe_py = self.calc_yc_pos(pe_id, False)
                self.trolly.pe_px = self.trolly.px = self.calc_tro_pos(pe_id)
            self.py = self.pe_py
            self.trolly.px = self.trolly.pe_px
        time_interval = self.tg_time - self.pe_time
        assert 0 <= time_interval.total_seconds() < 3600 * 24, False
        self.tro_ms_time = self.pe_time + timedelta(seconds=time_interval.total_seconds() * (2 / 5))
        self.tro_mf_time = self.pe_time + timedelta(seconds=time_interval.total_seconds() * (4 / 5))
        
        self.update_pos(simul_clock)

    def update_container_ownership(self, simul_clock):
        if self.tg_work_type == 'TwistLock' and self.tg_operation == 'DISCHARGING':
            tg_container = self.target_tp.holding_containers.pop(self.tg_container)
            tg_container.px, tg_container.py = 0, 0
            self.holding_containers[self.tg_container] = tg_container
        elif self.tg_work_type == 'TwistUnlock' and self.tg_operation == 'DISCHARGING':
            tg_container = self.holding_containers.pop(self.tg_container)
            tg_container.px, tg_container.py = self.target_block.stack_pos_info[self.stack_id], self.target_block.bay_pos_info[self.bay_id]
            self.target_block.holding_containers[self.tg_container] = tg_container
        elif self.tg_work_type == 'TwistLock' and self.tg_operation == 'LOADING':
            tg_container = self.target_block.holding_containers.pop(self.tg_container)
            tg_container.px, tg_container.py = 0, 0
            self.holding_containers[self.tg_container] = tg_container
        elif self.tg_work_type == 'TwistUnlock' and self.tg_operation == 'LOADING':
            tg_container = self.holding_containers.pop(self.tg_container)
            tg_container.px, tg_container.py = self.target_tp.stack_pos_info[self.stack_id], self.target_tp.bay_pos_info
            self.target_tp.holding_containers[self.tg_container] = tg_container
        else:
            assert False
        tg_container.target_evt_id += 1
    
    def update_pos(self, simul_clock):
        if self.pe_time <= simul_clock < self.tro_ms_time:
            #straddler moving
            self.py = self.pe_py + calc_proportional_pos(self.pe_py, self.tg_py, self.pe_time, self.tro_ms_time, simul_clock) 
        elif self.tro_ms_time <= simul_clock < self.tro_mf_time:
            self.py = self.tg_py
            #trolly moving
            self.trolly.px = self.trolly.pe_px + calc_proportional_pos(self.trolly.pe_px, self.trolly.tg_px, self.tro_ms_time, self.tro_mf_time, simul_clock) 
        elif self.tro_mf_time <= simul_clock < self.tg_time:
            self.py = self.tg_py
            self.trolly.px = self.trolly.tg_px
        if self.tg_time <= simul_clock:
            self.trolly.px = self.trolly.pe_px = self.trolly.tg_px
            self.pe_time, self.pe_py = self.tg_time, self.tg_py
            if self.evt_start: self.evt_start = False
