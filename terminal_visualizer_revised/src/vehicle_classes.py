from __future__ import division
from datetime import timedelta
from parameter_function import container_hs, container_vs, calc_proportional_pos, change_b_color
from storage_classes import Block
import wx, math

class Vehicles(object):
    def __init__(self):
        self.veh_id, self.name = None, None
        self.evt_seq, self.target_evt_id, self.evt_end = [], -1, False
        self.start_time, self.start_px, self.start_py = None, None, None
        self.ce_time, self.ce_pos, self.ce_container, self.ce_state, self.ce_px, self.ce_py = None, None, None, None, None, None
        self.px, self.py = None, None
        self.pe_time, self.pe_px, self.pe_py = None, None, None
        self.holding_containers = {}
    def __repr__(self):
        return str(self.name + str(self.veh_id))
    def set_evt_data(self, cur_evt_id):
        pass
    def Update_pos(self, simul_time):
        pass
    def Update_container_ownership(self, simul_time):
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
            gc.DrawRectangle(-QC.tro_sx / 2, -QC.sy - QC.tro_sy / 2, QC.tro_sx, QC.tro_sy)
            
    def __init__(self, veh_id):
        Vehicles.__init__(self)
        self.name = 'STS'
        self.veh_id = veh_id
        self.target_v, self.target_qb = None, None
        self.trolly = self.Trolly()
        #trolly moving start time
        self.tro_ms_time = None
        #trolly moving end time and operating start time
        self.tro_mf_time = None
        self.calc_tro_ori_py = lambda res : res.py - (self.py - QC.sy)
        
    def set_evt_data(self, target_evt_id, simul_clock):
        self.target_evt = self.evt_seq[target_evt_id]
        self.tg_time, self.tg_container, self.tg_work_type = self.target_evt.dt, self.target_evt.c_id, self.target_evt.work_type
        v_name, v_voyage_txt, _ = self.target_evt.v_info.split('/')
        
        if self.target_v == None or self.target_v.name != v_name:    
            for v in QC.Vessels:
                if v.name == v_name and v.voyage == int(v_voyage_txt):
                    self.target_v = v
                    break
            else:
                assert False, 'There is not target Vessel'
        self.px = self.target_v.px + container_hs * 8
        if target_evt_id == 0:
            self.start_time = self.tg_time - timedelta(seconds=10)
            self.trolly.start_px, self.trolly.start_py = self.trolly.px, self.trolly.py = 0 , container_hs * 4
            time_interval = self.tg_time - self.start_time
            assert 0 <= time_interval.total_seconds() < 3600 * 24, False
            self.tro_ms_time = self.start_time + timedelta(seconds=time_interval.total_seconds() * (1 / 5))
            self.tro_mf_time = self.start_time + timedelta(seconds=time_interval.total_seconds() * (4 / 5))
        else:
            self.trolly.py = self.trolly.pe_py
            time_interval = self.ce_time - self.pe_time
            assert 0 <= time_interval.total_seconds() < 3600 * 24, False
            self.tro_ms_time = self.pe_time + timedelta(seconds=time_interval.total_seconds() * (1 / 5))
            self.tro_mf_time = self.pe_time + timedelta(seconds=time_interval.total_seconds() * (4 / 5))
        
        if self.target_evt.work_type == 'TwistLock' and self.target_evt.operation == 'DISCHARGING' or self.target_evt.work_type == 'TwistUnlock' and self.target_evt.operation == 'LOADING':
            temp_stack_id = 4
            self.trolly.ce_py = self.calc_tro_ori_py(self.target_v) + container_hs * temp_stack_id
        elif  self.target_evt.work_type == 'TwistUnlock' and self.target_evt.operation == 'DISCHARGING' or self.target_evt.work_type == 'TwistLock' and self.target_evt.operation == 'LOADING':
            temp_qb_id = 4
            self.target_qb = QC.QBs[temp_qb_id]
            self.trolly.ce_py = self.calc_tro_ori_py(self.target_qb) + self.target_qb.c_pos
            
    def Update_pos(self, simul_time):
        if self.cur_evt_id == 0:
            if self.start_time <= simul_time < self.tro_ms_time:
                pass
                #straddler moving
#                self.px = self.start_px + (self.ce_px - self.start_px) * (simul_time - self.start_time).total_seconds() / (self.tro_ms_time - self.start_time).total_seconds()

            elif self.tro_ms_time <= simul_time < self.tro_mf_time:
                self.px = self.ce_px
                #trolly moving
                self.trolly.py = self.trolly.start_py + (self.trolly.ce_py - self.trolly.start_py) * (simul_time - self.tro_ms_time).total_seconds() / (self.tro_mf_time - self.tro_ms_time).total_seconds()
            elif self.tro_mf_time <= simul_time < self.ce_time:
                self.trolly.py = self.trolly.ce_py
        else:
            if self.pe_time <= simul_time < self.tro_ms_time:
                #straddler moving
                self.px = self.pe_px + (self.ce_px - self.pe_px) * (simul_time - self.pe_time).total_seconds() / (self.tro_ms_time - self.pe_time).total_seconds()
            elif self.tro_ms_time <= simul_time < self.tro_mf_time:
                self.px = self.ce_px
                #trolly moving
                self.trolly.py = self.trolly.pe_py + (self.trolly.ce_py - self.trolly.pe_py) * (simul_time - self.tro_ms_time).total_seconds() / (self.tro_mf_time - self.tro_ms_time).total_seconds()
            elif self.tro_mf_time <= simul_time < self.ce_time:
                self.trolly.py = self.trolly.ce_py
                
        if self.ce_time <= simul_time:
            self.trolly.py = self.trolly.pe_py = self.trolly.ce_py
            self.pe_time, self.pe_px = self.ce_time, self.ce_px
    def Update_container_ownership(self, simul_time):
        pass
        
    def draw(self, gc):
        gc.SetPen(wx.Pen('black', 0.5))
        r, g, b = (0, 0, 0)
        brushclr = wx.Colour(r, g, b, 200)
        paint = wx.Colour(r, g, b, 0)
        gc.SetPen(wx.Pen(brushclr, 1))
        gc.SetBrush(wx.Brush(paint))
        
        gc.DrawRectangle(-QC.sx / 2 - container_hs * 0.1, -QC.sy, QC.sx + container_hs * 0.1, QC.sy)
        
        gc.DrawLines([(-QC.sx / 2, -QC.sy), (-QC.sx / 2, 0)])
        gc.DrawLines([(-QC.sx / 2, -container_hs), (QC.sx / 2, 0)])
        gc.DrawLines([(QC.sx / 2, -container_hs), (-QC.sx / 2, 0)])
        gc.DrawLines([(-QC.sx / 2, -container_hs), (QC.sx / 2, -container_hs)])
        
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
        self.tro_op_time = None
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
                gc.Rotate(0)
                if self.thr_wp2:
                    gc.Rotate(math.pi / 2)
                    if self.thr_wp3:
                        gc.Rotate(math.pi / 2)
            else:
                gc.Rotate(math.pi / 2)
        for c in self.holding_containers.values():
            c.draw(gc)
        gc.SetPen(wx.Pen('black', 0.1))
        change_b_color(gc, 'white')
        gc.DrawRectangle(-SC.sx / 2, -SC.sy / 2, SC.sx, SC.sy)
