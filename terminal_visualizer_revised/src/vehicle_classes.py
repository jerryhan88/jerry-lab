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
        self.start_time, self.start_px, self.start_py = None, None, None
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
    
    def update(self, simul_clock):
        self.update_pos(simul_clock)
        if self.tg_time <= simul_clock:
            self.update_container_ownership(simul_clock)
            self.target_evt_id += 1
            self.set_evt_data(self.target_evt_id, simul_clock)
    def calc_tro_ori_py(self, res):
        if isinstance(res, Vessel): py = res.anchored_py
        elif isinstance(res, QB): py = res.py
        else: assert False
        return py - (self.py - QC.sy) 
    
    def set_evt_data(self, target_evt_id, simul_clock):
        print target_evt_id, self.holding_containers, simul_clock,self.evt_seq[target_evt_id]
        for v in self.holding_containers.values():
            print v.target_evt_id, v.evt_seq
        self.target_evt = self.evt_seq[target_evt_id]
        self.tg_time, self.tg_container, self.tg_work_type, tg_pos, self.tg_operation = self.target_evt.dt, self.target_evt.c_id, self.target_evt.work_type, self.target_evt.pos, self.target_evt.operation
        v_name, v_voyage_txt, _ = self.target_evt.v_info.split('/')
        if self.target_v == None or self.target_v.name != v_name:    
            for v in QC.Vessels:
                if v.name == v_name and v.voyage == int(v_voyage_txt):
                    self.target_v = v
                    break
            else:
                assert False, 'There is not target Vessel'
        if tg_pos[:2] == 'SB':
            bay_id = int(tg_pos[2:4]) 
            self.tg_px = self.target_v.px + self.target_v.bay_pos_info[bay_id]
        elif tg_pos[7:-2] == 'Lane':
            pe_evt = self.evt_seq[target_evt_id - 1]
            bay_id = int(pe_evt.pos[2:4]) 
            self.tg_px = self.target_v.px + self.target_v.bay_pos_info[bay_id]
        
        if self.evt_start:
            if target_evt_id == 0:
                self.start_time = self.tg_time - timedelta(seconds=5)
            else:
                self.start_time = self.evt_seq[target_evt_id-1].dt
            self.start_px = self.px = self.tg_px
            self.trolly.start_px, self.trolly.start_py = self.trolly.px, self.trolly.py = 0 , container_hs*4
            time_interval = self.tg_time - self.start_time
            assert 0 <= time_interval.total_seconds() < 3600 * 24, False
            self.tro_ms_time = self.start_time + timedelta(seconds=time_interval.total_seconds() * (1 / 5))
            self.tro_mf_time = self.start_time + timedelta(seconds=time_interval.total_seconds() * (4 / 5))
        else:
            self.trolly.py = self.trolly.pe_py
            self.px = self.pe_px
            time_interval = self.tg_time - self.pe_time
            assert 0 <= time_interval.total_seconds() < 3600 * 24, False
            self.tro_ms_time = self.pe_time + timedelta(seconds=time_interval.total_seconds() * (1 / 5))
            self.tro_mf_time = self.pe_time + timedelta(seconds=time_interval.total_seconds() * (4 / 5))
        
        if self.tg_work_type == 'TwistLock' and self.tg_operation == 'DISCHARGING' or self.tg_work_type == 'TwistUnlock' and self.tg_operation == 'LOADING':
            stack_id = int(tg_pos[5:7])
            self.trolly.tg_py = self.calc_tro_ori_py(self.target_v) + self.target_v.stack_pos_info[stack_id]
        elif  self.tg_work_type == 'TwistUnlock' and self.tg_operation == 'DISCHARGING' or self.tg_work_type == 'TwistLock' and self.tg_operation == 'LOADING':
            qb_id = int(tg_pos[-2:])
            self.target_qb = QC.QBs[qb_id]
            self.trolly.tg_py = self.calc_tro_ori_py(self.target_qb) + self.target_qb.v_c_pos_info
                
    def update_pos(self, simul_clock):
        if self.evt_start:
            if self.start_time <= simul_clock < self.tro_ms_time:
                #straddler moving
                self.px = self.start_px + calc_proportional_pos(self.start_px, self.tg_px, self.start_time, self.tro_ms_time, simul_clock)
            elif self.tro_ms_time <= simul_clock < self.tro_mf_time:
                self.px = self.tg_px
                #trolly moving
                self.trolly.py = self.trolly.start_py + calc_proportional_pos(self.trolly.start_py, self.trolly.tg_py, self.tro_ms_time, self.tro_mf_time, simul_clock)
            elif self.tro_mf_time <= simul_clock < self.tg_time:
                self.trolly.py = self.trolly.tg_py
        else:
            if self.pe_time <= simul_clock < self.tro_ms_time:
                #straddler moving
                self.px = self.pe_px + calc_proportional_pos(self.pe_px, self.tg_px, self.pe_time, self.tro_ms_time, simul_clock)
            elif self.tro_ms_time <= simul_clock < self.tro_mf_time:
                self.px = self.tg_px
                #trolly moving
                self.trolly.py = self.trolly.pe_py + calc_proportional_pos(self.trolly.pe_py, self.trolly.tg_py, self.tro_ms_time, self.tro_mf_time, simul_clock)
            elif self.tro_mf_time <= simul_clock < self.tg_time:
                self.trolly.py = self.trolly.tg_py
        if self.tg_time <= simul_clock:
            self.pe_time, self.trolly.pe_py, self.pe_px = self.tg_time, self.trolly.tg_py, self.tg_px
            if self.evt_start: self.evt_start = False
    def update_container_ownership(self, simul_time):
        if self.tg_work_type == 'TwistLock' and self.tg_operation == 'DISCHARGING':
            tg_container = self.target_v.holding_containers.pop(self.tg_container)
            tg_container.px, tg_container.py = 0, 0
            self.holding_containers[self.tg_container] = tg_container
        elif self.tg_work_type == 'TwistUnlock'and self.tg_operation == 'DISCHARGING':
            tg_container = self.holding_containers.pop(self.tg_container)
            tg_container.px, tg_container.py = self.px, self.target_qb.v_c_pos_info
            self.target_qb.holding_containers[self.tg_container] = tg_container
        else:
            assert False
        
        tg_container.target_evt_id += 1 
        
#        if self.tg_work_type == 'TwistLock' and self.target_evt.operation == 'DISCHARGING':
#            tg_container = self.target_v.holding_containers.pop(self.tg_container)
#            tg_container.px, tg_container.py = 0, 0
#            self.holding_containers[self.tg_container] = tg_container
#        if self.tg_work_type == 'TwistLock' and self.target_evt.operation == 'LOADING':
#            print 'self.tg_work_type == TwistLock and self.target_evt.operation == LOADING:'
#            tg_container = self.target_qb.holding_containers.pop(self.tg_container)
#            tg_container.px, tg_container.py = 0, 0
#            self.target_v.holding_containers[self.tg_container] = tg_container
#        elif self.tg_work_type == 'TwistUnlock'and self.target_evt.operation == 'DISCHARGING':
#            tg_container = self.holding_containers.pop(self.tg_container)
#            tg_container.px, tg_container.py = self.px, self.target_qb.v_c_pos_info
#            self.target_qb.holding_containers[self.tg_container] = tg_container
#        elif self.tg_work_type == 'TwistUnlock'and self.target_evt.operation == 'LOADING':
#            tg_container = self.holding_containers.pop(self.tg_container)
#            tg_c_pos = tg_container.evt_seq[tg_container.target_evt_id].pos
#            print 2343242343333333333333333333333333333333333333333333333333333333333333 
#            pass
#        else:
#            assert False    
            
            
               
        
    def draw(self, gc):
        gc.SetPen(wx.Pen('black', 0.5))
        r, g, b = (0, 0, 0)
        brushclr = wx.Colour(r, g, b)
        paint = wx.Colour(r, g, b, 0)
        gc.SetPen(wx.Pen(brushclr, 1))
        gc.SetBrush(wx.Brush(paint))
        
#        gc.DrawRectangle(-QC.sx / 2 - container_hs * 0.1, -QC.sy, QC.sx + container_hs * 0.1, QC.sy)
        
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

    def update(self, simul_clock):
        self.update_pos(simul_clock)
        if self.tg_time <= simul_clock:
            self.update_container_ownership(simul_clock)
            self.target_evt_id += 1
            if self.target_evt_id == len(self.evt_seq):self.evt_end = True
            if not self.evt_end:
                self.set_evt_data(self.target_evt_id, simul_clock)
            
    def set_evt_data(self, target_evt_id, simul_clock):
        self.target_evt = self.evt_seq[target_evt_id]
        self.tg_time, self.tg_container, self.tg_work_type, tg_pos, self.tg_operation = self.target_evt.dt, self.target_evt.c_id, self.target_evt.work_type, self.target_evt.pos, self.target_evt.operation
        if tg_pos[:2] == 'LM':
            tp_id, self.stack_id = tg_pos[3:5], int(tg_pos[-1:])
            self.target_tp = YC.TPs[tp_id]
            self.tg_py = self.target_tp.py + self.target_tp.bay_pos_info
        elif tg_pos[:1] == 'A'or tg_pos[:1] == 'B':
            block_id, self.bay_id, self.stack_id = tg_pos[:2], int(tg_pos[3:5]), int(tg_pos[6:7])
            self.target_block = YC.Blocks[block_id]
            self.tg_py = self.target_block.py + self.target_block.bay_pos_info[self.bay_id]
        else:
            assert False
        if target_evt_id == 0:
            self.start_time = self.tg_time - timedelta(seconds=10)
            self.start_py = self.py = self.tg_py + container_hs * 1.5
            time_interval = self.tg_time - self.start_time
            assert 0 <= time_interval.total_seconds() < 3600 * 24, False
            self.tro_ms_time = self.start_time + timedelta(seconds=time_interval.total_seconds() * (2 / 5))
            self.tro_mf_time = self.start_time + timedelta(seconds=time_interval.total_seconds() * (3 / 5))
            self.trolly.start_px, self.trolly.start_py = self.trolly.px, self.trolly.py = 0, 0
        else:
            self.py = self.pe_py
            time_interval = self.tg_time - self.pe_time
            assert 0 <= time_interval.total_seconds() < 3600 * 24, False
            self.tro_ms_time = self.pe_time + timedelta(seconds=time_interval.total_seconds() * (2 / 5))
            self.tro_mf_time = self.pe_time + timedelta(seconds=time_interval.total_seconds() * (4 / 5))
            self.trolly.px, self.trolly.py = self.trolly.pe_px, self.trolly.pe_py
            
        if tg_pos[:2] == 'LM': 
            self.trolly.tg_px, self.trolly.tg_py = self.target_tp.stack_pos_info[self.stack_id] + YC.dif_btw_b_tp, self.trolly.py
        elif tg_pos[:1] == 'A'or tg_pos[:1] == 'B':
            self.trolly.tg_px, self.trolly.tg_py = self.target_block.stack_pos_info[self.stack_id], self.trolly.py
        else:
            assert False

    def update_container_ownership(self, simul_clock):
#        pass
        if self.tg_work_type == 'TwistLock' and self.tg_operation == 'DISCHARGING':
            tg_container = self.target_tp.holding_containers.pop(self.tg_container)
            tg_container.px, tg_container.py = 0, 0
            if self.tg_container == 'HJCU6126555':
                print 'HJCU6126555'
            self.holding_containers[self.tg_container] = tg_container
        elif self.tg_work_type == 'TwistUnlock' and self.tg_operation == 'DISCHARGING':
            if self.tg_container == 'HJCU6126555':
                print 'HJCU6126555~~~~'
#            print self.tg_container, self, self.target_evt
            tg_container = self.holding_containers.pop(self.tg_container)
            tg_container.px, tg_container.py = self.target_block.stack_pos_info[self.stack_id], self.target_block.bay_pos_info[self.bay_id]
            self.target_block.holding_containers[self.tg_container] = tg_container
        elif self.tg_work_type == 'TwistLock' and self.tg_operation == 'LOADING':
            tg_container = self.target_block.holding_containers.pop(self.tg_container)
            tg_container.px, tg_container.py = 0, 0
            self.holding_containers[self.tg_container] = tg_container
            print 11111111111
            print self, self.target_evt
        elif self.tg_work_type == 'TwistUnlock' and self.tg_operation == 'LOADING':
            tg_container = self.holding_containers.pop(self.tg_container)
            tg_container.px, tg_container.py = self.target_tp.stack_pos_info[self.stack_id], self.target_tp.bay_pos_info
            self.target_tp.holding_containers[self.tg_container] = tg_container
            print 2222222222222
            print self, self.target_evt
        else:
            assert False
        tg_container.target_evt_id += 1     
#            
#            stack_id = int(tg_container.evt_seq[tg_container.target_evt_id].pos[8:])
#            tg_container.px, tg_container.py = self.target_tp.stack_pos_info[stack_id], self.target_tp.bay_pos_info
#            save_c_hs = tg_container.hs 
#            tg_container.hs = tg_container.vs
#            tg_container.vs = save_c_hs
#            self.target_tp.holding_containers[self.tg_container] = tg_container
#        tg_container.target_evt_id += 1
#        if self.tg_work_type == 'TwistLock':
#            tg_container = self.target_qb.holding_containers.pop(self.tg_container)
#            tg_container.px, tg_container.py = 0, 0
#            self.holding_containers[self.tg_container] = tg_container
#        elif self.tg_work_type == 'TwistUnlock':
#            tg_container = self.holding_containers.pop(self.tg_container)
#            stack_id = int(tg_container.evt_seq[tg_container.target_evt_id].pos[8:])
#            tg_container.px, tg_container.py = self.target_tp.stack_pos_info[stack_id], self.target_tp.bay_pos_info
#            save_c_hs = tg_container.hs 
#            tg_container.hs = tg_container.vs
#            tg_container.vs = save_c_hs
#            self.target_tp.holding_containers[self.tg_container] = tg_container
#        tg_container.target_evt_id += 1   
    
    def update_pos(self, simul_clock):
        if self.target_evt_id == 0:
            if self.start_time <= simul_clock < self.tro_ms_time:
                #straddler moving
                self.py = self.start_py + calc_proportional_pos(self.start_py, self.tg_py, self.start_time, self.tro_ms_time, simul_clock)
            elif self.tro_ms_time <= simul_clock < self.tro_mf_time:
                self.py = self.tg_py
                #trolly moving
                self.trolly.px = self.trolly.start_px + calc_proportional_pos(self.trolly.start_px, self.trolly.tg_px, self.tro_ms_time, self.tro_mf_time, simul_clock) 
                self.trolly.py = self.trolly.start_py
            elif self.tro_mf_time <= simul_clock < self.tg_time:
                self.trolly.px, self.trolly.py = self.trolly.tg_px, self.trolly.tg_py
        else:
            if self.pe_time <= simul_clock < self.tro_ms_time:
                #straddler moving
                self.py = self.pe_py + calc_proportional_pos(self.pe_py, self.tg_py, self.start_time, self.tro_ms_time, simul_clock) 
            elif self.tro_ms_time <= simul_clock < self.tro_mf_time:
                self.py = self.tg_py
                #trolly moving
                self.trolly.px = self.trolly.pe_px + calc_proportional_pos(self.trolly.pe_px, self.trolly.tg_px, self.tro_ms_time, self.tro_mf_time, simul_clock) 
                self.trolly.py = self.trolly.pe_py
            elif self.tro_mf_time <= simul_clock < self.tg_time:
                self.trolly.px, self.trolly.py = self.trolly.tg_px, self.trolly.tg_py
        
        if self.tg_time <= simul_clock:
            self.trolly.px, self.trolly.py = self.trolly.pe_px, self.trolly.pe_py = self.trolly.tg_px, self.trolly.tg_py
            self.pe_time, self.pe_py = self.tg_time, self.tg_py

class SC(Vehicles):
    QBs, TPs, QCs = None, None, None
    sx, sy = container_hs * 1.2, container_vs * 1.2
    def __init__(self, veh_id):
        Vehicles.__init__(self)
        self.name = 'SH'
        self.veh_id = veh_id
        self.target_qb, self.target_tp, self.target_qc = None, None, None
        ## ss: sea side, ls: land side 
        self.is_ss_to_ls = True
        self.waypoint1_time, self.waypoint2_time, self.waypoint3_time = None, None, None
        self.waypoint1_pos , self.waypoint2_pos, self.waypoint3_pos = (None, None), (None, None), (None, None)
        self.thr_wp1, self.thr_wp2, self.thr_wp3 = None, None, None
        
        self.lu_px, self.lu_py = -SC.sx / 2, -SC.sy / 2
    
    def update(self, simul_clock):
        self.update_pos(simul_clock)
        if self.tg_time <= simul_clock:
            self.update_container_ownership(simul_clock)
            self.target_evt_id += 1
            self.set_evt_data(self.target_evt_id, simul_clock)
            
    def set_evt_data(self, target_evt_id, simul_clock):
#        if target_evt_id == len(self.evt_seq) - 1:
#            self.evt_end = True
        self.target_evt = self.evt_seq[target_evt_id]
        self.tg_time, self.tg_container, tg_pos, self.tg_work_type = self.target_evt.dt, self.target_evt.c_id, self.target_evt.pos, self.target_evt.work_type
        if tg_pos[:3] == 'STS':
            target_qc_id = int(tg_pos[3:6]) 
            for qc in SC.QCs:
                if qc.veh_id == target_qc_id:
                    self.target_qc = qc
                    break
            else:
                assert False, 'there is not target qc'
            qb_id = int(tg_pos[-1:])
            self.target_qb = SC.QBs[qb_id]
            self.tg_px, self.tg_py = self.target_qc.px, self.target_qb.py + self.target_qb.v_c_pos_info
            self.is_ss_to_ls = False
        elif tg_pos[:2] == 'LM':
            tp_id, stack_id = tg_pos[3:5], int(tg_pos[8:])
            self.target_tp = SC.TPs[tp_id]
            self.tg_px, self.tg_py = self.target_tp.px + self.target_tp.stack_pos_info[stack_id], self.target_tp.py + self.target_tp.bay_pos_info
            self.is_ss_to_ls = True
        
        if target_evt_id == 0:
            self.start_time = self.tg_time - timedelta(seconds=8)
            self.start_px, self.start_py = self.px, self.py = self.tg_px - container_hs * 10, self.tg_py
            self.is_ss_to_ls = True
        else:
            self.px = self.pe_px
            time_interval = self.tg_time - self.pe_time
            assert 0 <= time_interval.total_seconds() < 3600 * 24, False
            ti_ts = time_interval.total_seconds()
            if self.is_ss_to_ls:
                self.waypoint1_time = self.pe_time + timedelta(0, ti_ts * (3 / 10))
                self.waypoint2_time = self.pe_time + timedelta(0, ti_ts * (6 / 10))
                self.waypoint3_time = self.pe_time + timedelta(0, ti_ts * (9 / 10))
                
                self.wp1_px, self.wp1_py = (self.pe_px + container_hs * 10, self.pe_py)
                self.wp2_px, self.wp2_py = (self.pe_px + container_hs * 10, self.tg_py - container_hs)
                self.wp3_px, self.wp3_py = (self.tg_px, self.tg_py - container_hs)
            else:
                self.waypoint1_time = self.pe_time + timedelta(0, ti_ts * (0.1 / 10))
                self.waypoint2_time = self.pe_time + timedelta(0, ti_ts * (4 / 10))
                self.waypoint3_time = self.pe_time + timedelta(0, ti_ts * (9 / 10))
                
                self.wp1_px, self.wp1_py = (self.pe_px, self.pe_py - container_hs)
                self.wp2_px, self.wp2_py = (self.pe_px - container_hs * 4, self.pe_py - container_hs)
                self.wp3_px, self.wp3_py = (self.pe_px - container_hs * 4, self.tg_py)
        self.thr_wp1 = False
        self.thr_wp2 = False
        self.thr_wp3 = False

    def update_container_ownership(self, simul_clock):
        if self.tg_work_type == 'TwistLock':
            tg_container = self.target_qb.holding_containers.pop(self.tg_container)
            tg_container.px, tg_container.py = 0, 0
            self.holding_containers[self.tg_container] = tg_container
        elif self.tg_work_type == 'TwistUnlock':
            tg_container = self.holding_containers.pop(self.tg_container)
            stack_id = int(tg_container.evt_seq[tg_container.target_evt_id].pos[8:])
            tg_container.px, tg_container.py = self.target_tp.stack_pos_info[stack_id], self.target_tp.bay_pos_info
            save_c_hs = tg_container.hs 
            tg_container.hs = tg_container.vs
            tg_container.vs = save_c_hs
            self.target_tp.holding_containers[self.tg_container] = tg_container
        tg_container.target_evt_id += 1   
    
    def update_pos(self, simul_clock):
        if self.tg_container in self.target_qb.holding_containers:
            self.tg_px = self.target_qb.holding_containers[self.tg_container].px
            
        if self.target_evt_id == 0:
            if self.start_time <= simul_clock < self.tg_time:
                self.px = self.start_px + calc_proportional_pos(self.start_px, self.tg_px, self.start_time, self.tg_time, simul_clock)
        else:
            if self.is_ss_to_ls:
                if self.pe_time <= simul_clock < self.waypoint1_time:
                    self.px = self.pe_px + calc_proportional_pos(self.pe_px, self.wp1_px, self.pe_time, self.waypoint1_time, simul_clock) 
                    self.py = self.pe_py
                elif self.waypoint1_time <= simul_clock < self.waypoint2_time:
                    self.thr_wp1 = True
                    self.px = self.wp1_px  
                    self.py = self.wp1_py + calc_proportional_pos(self.wp1_py, self.wp2_py, self.waypoint1_time, self.waypoint2_time, simul_clock) 
                elif self.waypoint2_time <= simul_clock < self.waypoint3_time:
                    self.thr_wp2 = True
                    self.px = self.wp2_px + calc_proportional_pos(self.wp2_px, self.wp3_px, self.waypoint2_time, self.waypoint3_time, simul_clock) 
                    self.py = self.wp2_py
                elif self.waypoint3_time <= simul_clock < self.tg_time:
                    self.thr_wp3 = True
                    self.px = self.wp3_px
                    self.py = self.wp3_py + calc_proportional_pos(self.wp3_py, self.tg_py, self.waypoint3_time, self.tg_time, simul_clock) 
            else:
                if self.pe_time <= simul_clock < self.waypoint1_time:
                    self.px = self.pe_px
                    self.py = self.pe_py + calc_proportional_pos(self.pe_py, self.wp1_py, self.pe_time, self.waypoint1_time, simul_clock)
                elif self.waypoint1_time <= simul_clock < self.waypoint2_time:
                    self.thr_wp1 = True
                    self.px = self.wp1_px + calc_proportional_pos(self.wp1_px, self.wp2_px, self.waypoint1_time, self.waypoint2_time, simul_clock)
                    self.py = self.wp1_py
                elif self.waypoint2_time <= simul_clock < self.waypoint3_time:
                    self.thr_wp2 = True
                    self.px = self.wp2_px
                    self.py = self.wp2_py + calc_proportional_pos(self.wp2_py, self.wp3_py, self.waypoint2_time, self.waypoint3_time, simul_clock) 
                elif self.waypoint3_time <= simul_clock < self.tg_time:
                    self.thr_wp3 = True
                    self.px = self.wp3_px + calc_proportional_pos(self.wp3_px, self.tg_px, self.waypoint3_time, self.tg_time, simul_clock) 
                    self.py = self.wp3_py
        
        if self.tg_time <= simul_clock:
            self.pe_time, self.pe_px , self.pe_py = self.tg_time, self.tg_px, self.tg_py 
    def draw(self, gc):
        if self.is_ss_to_ls:
            if self.thr_wp1:
                gc.Rotate(math.pi / 2)
                if self.thr_wp2:
                    gc.Rotate(math.pi / 2)
                    if self.thr_wp3:
                        gc.Rotate(-math.pi / 2)
            else:
                gc.Rotate(0)
        else:
            if self.thr_wp1:
                gc.Rotate(-math.pi)
                if self.thr_wp2:
                    gc.Rotate(math.pi / 2)
                    if self.thr_wp3:
                        gc.Rotate(math.pi / 2)
            else:
                gc.Rotate(-math.pi / 2)
        for c in self.holding_containers.values():
            c.draw(gc)
        tire_d = 5
        gc.SetPen(wx.Pen(wx.Colour(226, 56, 20), 1))
#        gc.DrawCircles([(self.lu_px,self.lu_px+tire_d), (self.lu_py-tire_d,self.lu_py+SC.sy+tire_d)])
        gc.DrawLines([(self.lu_px, self.lu_py), (self.lu_px + SC.sx, self.lu_py)])
        gc.DrawLines([(self.lu_px, self.lu_py + SC.sy), (self.lu_px + SC.sx, self.lu_py + SC.sy)])
        gc.DrawLines([(self.lu_px, self.lu_py), (self.lu_px, self.lu_py + SC.sy)])
        gc.DrawLines([(self.lu_px + SC.sx, self.lu_py), (self.lu_px + SC.sx, self.lu_py + SC.sy)])
#        gc.DrawLines([(self.lu_px+tire_d*0.2,self.lu_py),(self.lu_px,self.lu_py+tire_d*0.5),(self.lu_px + SC.sx*0.5-tire_d*0.2,self.lu_py)])
        gc.SetBrush(wx.Brush(wx.Colour(226, 56, 20)))
        
        gc.DrawLines([(self.lu_px + SC.sx, self.lu_py + 1), (self.lu_px + SC.sx - container_vs * 0.7, self.lu_py + 1), (self.lu_px + SC.sx - container_vs * 0.7, self.lu_py + SC.sy / 2), (self.lu_px + SC.sx, self.lu_py + SC.sy / 2)])
#        gc.DrawLines([(self.lu_px + SC.sx + container_vs, self.lu_py + SC.sy / 2), (self.lu_px + SC.sx + container_vs, self.lu_py + SC.sy / 2)])
        
#        gc.DrawRectangle(-SC.sx / 2, -SC.sy / 2, SC.sx, SC.sy)
        
