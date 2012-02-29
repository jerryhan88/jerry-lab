from __future__ import division
from parameter_function import container_hs, container_vs, l_sx
from parameter_function import pyslot, pvslot
from parameter_function import change_b_color
from datetime import datetime, timedelta
from random import random, seed
import math
import wx

seed(10)
class Container(object):
    def __init__(self, id):
        self.id = id
        self.moving_seq = []
        self.cur_position = None
        self.cur_ms_id = 0
        self.hs, self.vs = container_hs , container_vs
        self.size = '40ft'
        self.px, self.py = None, None
        
    def __repr__(self):
        return str(self.id)
    
    def draw(self, gc):
        gc.SetPen(wx.Pen('black', 0))
        change_b_color(gc, 'orange')
        gc.DrawRectangle(-self.hs / 2, -self.vs / 2, self.hs, self.vs)
    
class Bitt(object):
    def __init__(self, id, px, py):
        self.id = id
        self.name = 'Bitt'
        self.px, self.py = px, py
    def __repr__(self):
        return self.name + str(self.id)
    def draw(self, gc):
        ## draw Bit
        change_b_color(gc, 'black')
        gc.SetPen(wx.Pen("white", 0))
        bit_sx, bit_sy = container_hs * 0.26, container_vs * 0.8
        gc.DrawRectangle(0, 0, bit_sx, bit_sy)

class Storage(object):
    def __init__(self):
        self.id = None
        self.name = None
        self.px, self.py = None, None
        self.holding_containers = {}
    def __repr__(self):
        return self.name + str(self.id)

class QC_buffer(Storage):
    def __init__(self, id, px, py):
        Storage.__init__(self)
        self.id = id
        self.name = 'QC Buffer'
        self.px, self.py = px, py
        self.sy = container_vs * 2.2
        self.c_pos = self.sy / 2 
    
    def draw(self, gc):
        gc.SetPen(wx.Pen('black', 0.5))
        gc.DrawLines([(0, 0), (l_sx, 0)])
        gc.DrawLines([(0, self.sy), (l_sx, self.sy)])
        
        for c in self.holding_containers.values():
            old_tr = gc.GetTransform()
            gc.Translate(c.px, c.py)
            c.draw(gc)
            gc.SetTransform(old_tr)

class TP(Storage):
    num_of_stacks = 4
    def __init__(self, id, px, py):
        Storage.__init__(self)
        self.id = id
        self.name = 'TP'
        self.px, self.py = px, py
        TP.num_of_stacks = 4
        self.bay_pos_info = container_hs / 2
        self.stack_pos = {}
        for x in xrange(TP.num_of_stacks):
            self.stack_pos[x + 1] = container_vs / 2 + container_vs * x 

    def draw(self, gc):
        gc.SetPen(wx.Pen('black', 0.2))
        gc.DrawLines([(0, 0), (container_vs * TP.num_of_stacks , 0)])
        gc.DrawLines([(0, container_hs), (container_vs * TP.num_of_stacks , container_hs)])
        for x in xrange(TP.num_of_stacks + 1) :
            gc.DrawLines([(container_vs * x, 0), (container_vs * x , container_hs)])
        
        for c in self.holding_containers.values():
            old_tr = gc.GetTransform()
            gc.Translate(c.px, c.py)
            c.draw(gc)
            gc.SetTransform(old_tr)    
            

class Block(Storage):
    num_of_stacks = 8
    def __init__(self, id, px, py):
        Storage.__init__(self)
        self.id = id
        self.name = 'Block'
        self.px, self.py = px, py
        
        self.num_of_bays = 45
        self.bay_pos_info = {}
        self.stack_pos_info = {}
        
        for x in xrange(self.num_of_bays):
            bay_id = x + 1
            if bay_id % 4 == 0: py = container_hs * ((bay_id // 4 - 1) + 1 / 2) + container_hs / 2
            elif bay_id % 4 == 1: py = container_hs * (bay_id // 4) + container_hs / 4
            elif bay_id % 4 == 2: py = container_hs * (bay_id // 4) + container_hs / 2
            elif bay_id % 4 == 3: py = container_hs * ((bay_id // 4) + 1 / 2) + container_hs / 4
            else: assert False
            self.bay_pos_info[bay_id] = py
            
        for x in xrange(Block.num_of_stacks):
            self.stack_pos_info[x + 1] = container_vs * x + container_vs / 2
        
    def draw(self, gc):
        gc.SetPen(wx.Pen("black", 0.5))
        for x in xrange((self.num_of_bays - 1) // 2 + 1):
            gc.DrawLines([(0, container_hs * x), (container_vs * self.num_of_stacks , container_hs * x)])
        for x in xrange(self.num_of_stacks + 1):
            gc.DrawLines([(container_vs * x, 0), (container_vs * x , container_hs * (self.num_of_bays - 1) // 2)])
        change_b_color(gc, 'orange')
        
        for c in self.holding_containers.values():
            bay_id, stack_id, _ = pyslot(c.moving_seq[c.cur_ms_id][1])
            py = self.bay_pos_info[bay_id]
            px = self.stack_pos_info[stack_id]
            c.px, c.py = px, py
            old_tr = gc.GetTransform()
            gc.Translate(c.px, c.py)
            c.draw(gc)
            gc.SetTransform(old_tr)

class Vehicles(object):
    def __init__(self):
        self.id = None
        self.name = None
        self.evt_seq = []
        self.cur_evt_id = 0
        self.holding_containers = {}
        
        self.pe_time = None
        self.pe_px, self.pe_py = None, None
        
        self.ce_px, self.ce_py = None, None
        self.px, self.py = None, None
        
    def set_dest_position(self, px, py):
        self.ne_px, self.ne_py = px, py
        
class Vessel(Vehicles):
    def __init__(self, name, voyage):
        Vehicles.__init__(self)
        self.name = name
        self.voyage = voyage
        self.LOA, self.B = container_hs * 14, container_vs * 10
        self.num_of_bay, self.num_of_stack = 35, 8
        self.bay_pos_info, self.stack_pos_info = {}, {}
        self.ar_s_px, self.ar_s_py = None, None
        self.dp_e_px, self.dp_e_py = None, None
        self.ar_s_time = None
        self.dp_e_time = None    
        
        self.v_d_p = [(0, container_vs * 2), (container_hs * 1.84 , 0), (container_hs * 11 , 0),
                      (container_hs * 13 , container_vs * 1.25), (self.LOA, self.B / 2) , (container_hs * 13 , self.B - container_vs * 1.25),
                      (container_hs * 11 , self.B), (container_hs * 1.84 , self.B), (0, self.B - container_vs * 2.5),
                       (0, container_vs * 2)]
        
        self.margin_px = container_hs * 2
        for bay_id in range(self.num_of_bay, 0, -1):
            if bay_id % 4 == 0: px = False
            elif bay_id % 4 == 1: px = self.margin_px + container_hs / 4 * 3 + container_hs * 1.1 * ((self.num_of_bay - bay_id) // 4)
            elif bay_id % 4 == 2: px = self.margin_px + container_hs / 2 + container_hs * 1.1 * ((self.num_of_bay - bay_id) // 4)
            elif bay_id % 4 == 3: px = self.margin_px + container_hs / 4 + container_hs * 1.1 * ((self.num_of_bay - bay_id) // 4)
            else: assert False
            self.bay_pos_info[bay_id] = px
             
        self.margin_py = container_vs * 1.0
        for x in xrange(self.num_of_stack):
            self.stack_pos_info[x + 1] = x * container_vs + container_vs / 2 + self.margin_py
        
    def __repr__(self):
        return self.name + str(self.voyage)
    
    def cur_evt_update(self, cur_evt_id, Bitts, simul_clock):
        if len(self.evt_seq) <= 1: assert False, 'length of evt_seq is smaller than 2'
        self.cur_evt = self.evt_seq[cur_evt_id]
        self.next_evt = self.evt_seq[cur_evt_id + 1]
        ce_time, self.ce_state, ce_pos = self.cur_evt
        year, month, day, hour, minute, second = tuple(ce_time.split('-'))
        self.ce_time = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        bitt_id = int(ce_pos[-2:])
        self.ce_px, self.ce_py = Bitts[bitt_id].px - self.LOA * 1 / 3, Bitts[bitt_id].py - self.B * 1.1
        
        ne_time, self.ne_state, ne_pos = self.next_evt
        year, month, day, hour, minute, second = tuple(ne_time.split('-'))
        self.ne_time = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        bitt_id = int(ne_pos[-2:])
        self.ne_px, self.ne_py = Bitts[bitt_id].px - self.LOA * 1 / 3, Bitts[bitt_id].py - self.B * 1.1
        self.ar_s_px, self.ar_s_py = self.dp_e_px, self.dp_e_py = self.px, self.py = self.ce_px, self.ce_py - container_hs * 2
        
        if self.ce_time <= simul_clock <= self.ne_time:
            self.px, self.py = self.ce_px, self.ce_py
        self.ar_s_time = self.ce_time - timedelta(0, 15)
        self.dp_e_time = self.ne_time + timedelta(0, 20)

    def OnTimer(self, evt, simul_time):
        if self.ar_s_time <= simul_time < self.ce_time:
            self.px = self.ar_s_px
            self.py = self.ar_s_py + (self.ce_py - self.ar_s_py) * (simul_time - self.ar_s_time).total_seconds() / (self.ce_time - self.ar_s_time).total_seconds()
        elif self.ce_time <= simul_time < self.ne_time:
            self.px = self.ne_px
            self.py = self.ne_py
        if self.ne_time <= simul_time < self.dp_e_time:
            self.px = self.ar_s_px
            self.py = self.ne_py + (self.ne_py - self.dp_e_py) * (simul_time - self.ne_time).seconds / (self.dp_e_time - self.ne_time).seconds
            
    def draw(self, gc):
        gc.SetPen(wx.Pen("black", 1))
        brushclr = wx.Colour(255, 255, 255)
        gc.SetBrush(wx.Brush(brushclr))
        #draw vessel surface        
        gc.DrawLines(self.v_d_p)
        gc.SetPen(wx.Pen("black", 0.5))
        
        for x in xrange((self.num_of_bay + 1) // 4):
            bay_ori_px = self.margin_px + container_hs * 1.1 * x
            gc.DrawLines([(bay_ori_px, self.margin_py), (bay_ori_px, self.margin_py + container_vs * self.num_of_stack)])
            gc.DrawLines([(bay_ori_px + container_hs, self.margin_py), (bay_ori_px + container_hs, self.margin_py + container_vs * self.num_of_stack)])
            for s in xrange(self.num_of_stack + 1):
                gc.DrawLines([(bay_ori_px, self.margin_py + s * container_vs), (bay_ori_px + container_hs, self.margin_py + s * container_vs)])
                
        for c in self.holding_containers.values():
            bay_id, stack_id, _ = pvslot(c.cur_position)
            px, py = self.bay_pos_info[bay_id] , self.stack_pos_info[stack_id]
            old_tr = gc.GetTransform()
            gc.Translate(px, py)
            c.draw(gc)
            gc.SetTransform(old_tr)

class QC(Vehicles):
    QBs = None
    sx, sy = container_hs * 0.6 , container_hs * 10 
    tro_sx, tro_sy = container_hs * 0.5, container_vs * 0.8 
    class Trolly(Vehicles):
        def __init__(self):
            Vehicles.__init__(self)
            self.start_px, self.start_py = None, None
        def draw(self, gc, holding_containers):
            tr, tg, tb = (4, 189, 252)
            t_brushclr = wx.Colour(tr, tg, tb, 200)
            
            for c in holding_containers.values():
                old_tr = gc.GetTransform()
                gc.Translate(0, -QC.sy)
                c.draw(gc)
                gc.SetTransform(old_tr)
                
            ##draw trolly         
            gc.SetPen(wx.Pen(t_brushclr, 0))
            gc.SetBrush(wx.Brush(t_brushclr))
            gc.DrawRectangle(-QC.tro_sx / 2, -QC.sy - QC.tro_sy / 2, QC.tro_sx, QC.tro_sy)
                
    def __init__(self, name):
        Vehicles.__init__(self)
        self.id = int(name[-2:])
        self.name = 'QC'
        self.evt_seq = []
        self.cur_evt_id = 0
        self.trolly = self.Trolly()
        
        self.target_v, self.target_qb = None, None
        self.start_time = None
        self.start_px, self.start_py = None, None
        #trolly moving start time
        self.tro_ms_time = None
        #trolly operating start time
        self.tro_mf_time = None

    def __repr__(self):
        return str(self.name + str(self.id))
    
    def cur_evt_update(self, cur_evt_id, Vessels=None, QBs=None):
        if len(self.evt_seq) <= 1: assert False, 'length of evt_seq is smaller than 2'
        self.cur_evt = self.evt_seq[cur_evt_id]
        ce_time, v_name, v_voyage, ce_pos, self.ce_container, self.ce_state, = self.cur_evt
        year, month, day, hour, minute, second = tuple(ce_time.split('-'))
        self.ce_time = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        
        if cur_evt_id == 0:
            QC.QBs = QBs
            last_QB_id = 0
            for qb_id in QC.QBs.keys():
                if qb_id > last_QB_id : last_QB_id = qb_id
            self.py = QC.QBs[last_QB_id].py + QC.QBs[last_QB_id].sy
        
        if self.target_v == None or self.target_v.name != v_name:    
            for v in Vessels:
                if v.name == v_name and v.voyage == v_voyage:
                    self.target_v = v
                    break
            else:
                assert False, 'There is not target Vessel'
             
        if ce_pos[:2] == 'SB':
            bay_id = int(ce_pos[2:4])    
            self.ce_px = self.target_v.px + self.target_v.bay_pos_info[bay_id]        
        else:
            # is there any container which is loaded before unloading containers from vessel?
            pass
        if cur_evt_id == 0:
            self.start_time = self.ce_time - timedelta(0, 10)
            self.start_px = self.px = self.ce_px + container_hs * 2 * random()
            self.trolly.start_px, self.trolly.start_py = self.trolly.px, self.trolly.py = 0 , container_hs * 8 * random()
            time_interval = self.ce_time - self.start_time
            assert 0 <= time_interval.total_seconds() < 3600 * 24, False
            self.tro_ms_time = self.start_time + timedelta(0, time_interval.total_seconds() * (1 / 5))
            self.tro_mf_time = self.start_time + timedelta(0, time_interval.total_seconds() * (4 / 5))
        else:
            self.px = self.pe_px
            self.trolly.py = self.trolly.pe_py
            time_interval = self.ce_time - self.pe_time
            assert 0 <= time_interval.total_seconds() < 3600 * 24, False
            self.tro_ms_time = self.pe_time + timedelta(0, time_interval.total_seconds() * (1 / 5))
            self.tro_mf_time = self.pe_time + timedelta(0, time_interval.total_seconds() * (4 / 5))
        
        if ce_pos[:2] == 'SB':
            stack_id = int(ce_pos[5:7])
            self.trolly.ce_py = self.calc_tro_ori_py(self.target_v) + self.target_v.stack_pos_info[stack_id]
        else:
            qb_id = int(ce_pos[10:])
            self.target_qb = QC.QBs[qb_id]
            self.trolly.ce_py = self.calc_tro_ori_py(self.target_qb) + self.target_qb.c_pos
        
    def calc_tro_ori_py(self, res):
        py = res.py - (self.py - QC.sy)
        return py
    
    def OnTimer(self, evt, simul_time):
        if self.cur_evt_id == 0:
            if self.start_time <= simul_time < self.tro_ms_time:
                #straddler moving
                self.px = self.start_px + (self.ce_px - self.start_px) * (simul_time - self.start_time).total_seconds() / (self.tro_ms_time - self.start_time).total_seconds()
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
            if self.ce_state == 'TL':
                ce_c_id = int(self.ce_container[1:3])
                ce_container = self.target_v.holding_containers.pop(ce_c_id)
                ce_container.px, ce_container.py = 0, 0
                self.holding_containers[int(ce_container.id[1:3])] = ce_container
            else: #self.ce_state == 'TU':
                ce_c_id = int(self.ce_container[1:3])
                ce_container = self.holding_containers.pop(ce_c_id)
                ce_container.px, ce_container.py = self.px, self.target_qb.c_pos
                self.target_qb.holding_containers[int(ce_container.id[1:3])] = ce_container
            print ce_container.id ,ce_container.cur_ms_id , ce_container.moving_seq[ce_container.cur_ms_id] 
            ce_container.cur_ms_id +=1
            self.cur_evt_id += 1
            self.cur_evt_update(self.cur_evt_id)
    
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
    dif_btw_b_tp_stack = abs(Block.num_of_stacks - TP.num_of_stacks)
    TPs, Blocks = None, None
    tro_sx, tro_sy = container_vs * 0.8, container_hs * 0.8
    tro_L_btw_C = container_vs * 4.0
    width = container_vs * Block.num_of_stacks
    class Trolly(Vehicles):
        def __init__(self):
            Vehicles.__init__(self)
            self.start_px, self.start_py = None, None
        def draw(self, gc, holding_containers):
            tr, tg, tb = (4, 189, 252)
            t_brushclr = wx.Colour(tr, tg, tb, 200)
            
            for c in holding_containers.values():
                old_tr = gc.GetTransform()
                gc.Translate(-YC.tro_L_btw_C, 0)
                c.draw(gc)
                gc.SetTransform(old_tr)
            
            ##draw trolly
            gc.SetPen(wx.Pen(t_brushclr, 0))
            gc.SetBrush(wx.Brush(t_brushclr))
            gc.DrawRectangle(-YC.tro_L_btw_C - YC.tro_sx / 2, -YC.tro_sy / 2, YC.tro_sx, YC.tro_sy)
    def __init__(self, name):
        Vehicles.__init__(self)
        self.id = int(name[-2:])
        self.name = 'YC'
        self.evt_seq = []
        self.cur_evt_id = 0
        self.trolly = self.Trolly()
        
        self.start_time = None
        self.start_px, self.start_py = None, None
        #trolly moving start time
        self.tro_ms_time = None
        #trolly operating start time
        self.tro_op_time = None
        
        self.target_tp, self.target_block = None, None

    def __repr__(self):
        return str(self.name + str(self.id))
    
    def cur_evt_update(self, cur_evt_id, TPs=None, Blocks=None):
        if len(self.evt_seq) <= 1: assert False, 'length of evt_seq is smaller than 2'
        if cur_evt_id == 0:
            YC.TPs, YC.Blocks = TPs, Blocks
            self.px = YC.Blocks[(self.id + 1) // 2].px + +YC.width / 2 
        
        self.cur_evt = self.evt_seq[cur_evt_id]
        
        ce_time, self.ce_pos, self.ce_container, self.ce_state, = self.cur_evt
        year, month, day, hour, minute, second = tuple(ce_time.split('-'))
        self.ce_time = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        if self.ce_pos[4:6] == 'TP':
            block_id, tp_stack_id = int(self.ce_pos[1:3]), int(self.ce_pos[6:])
            tp_id = block_id
            self.target_block = YC.Blocks[block_id]
            self.target_tp = YC.TPs[tp_id]
            self.ce_py = self.target_tp.py + self.target_tp.bay_pos_info
        else:
            #moving point is in block
            block_id, bay_id, stack_id, _ = int(self.ce_pos[1:3]), int(self.ce_pos[4:6]), int(self.ce_pos[7:9]), int(self.ce_pos[10:])
            self.target_block = YC.Blocks[block_id]
            self.ce_py = self.target_block.py + self.target_block.bay_pos_info[bay_id]
        
        #for moving trolly
        if cur_evt_id == 0:
            self.start_time = self.ce_time - timedelta(0, 10)
            self.start_py = self.py = self.ce_py + container_hs * 1.5
            time_interval = self.ce_time - self.start_time
            assert 0 <= time_interval.total_seconds() < 3600 * 24, False
            self.tro_ms_time = self.start_time + timedelta(0, time_interval.total_seconds() * (2 / 5))
            self.tro_op_time = self.start_time + timedelta(0, time_interval.total_seconds() * (3 / 5))
            self.trolly.start_px, self.trolly.start_py = self.trolly.px, self.trolly.py = container_vs * 8 * random(), 0
        else:
            self.py = self.pe_py
            time_interval = self.ce_time - self.pe_time
            assert 0 <= time_interval.total_seconds() < 3600 * 24, False
            self.tro_ms_time = self.pe_time + timedelta(0, time_interval.total_seconds() * (2 / 5))
            self.tro_op_time = self.pe_time + timedelta(0, time_interval.total_seconds() * (4 / 5))
            self.trolly.px, self.trolly.py = self.trolly.pe_px, self.trolly.pe_py
            
        if self.ce_pos[4:6] == 'TP': 
            self.trolly.ce_px, self.trolly.ce_py = self.target_tp.stack_pos[tp_stack_id] + container_vs * YC.dif_btw_b_tp_stack / 2, self.trolly.py
        else:
            self.trolly.ce_px, self.trolly.ce_py = self.target_block.stack_pos_info[stack_id], self.trolly.py
        
    def OnTimer(self, evt, simul_time):
        if self.cur_evt_id == 0:
            if self.start_time <= simul_time < self.tro_ms_time:
                #straddler moving
                self.py = self.start_py + (self.ce_py - self.start_py) * (simul_time - self.start_time).total_seconds() / (self.tro_ms_time - self.start_time).total_seconds()
            elif self.tro_ms_time <= simul_time < self.tro_op_time:
                self.py = self.ce_py
                #trolly moving
                self.trolly.px = self.trolly.start_px + (self.trolly.ce_px - self.trolly.start_px) * (simul_time - self.tro_ms_time).total_seconds() / (self.tro_op_time - self.tro_ms_time).total_seconds()
                self.trolly.py = self.trolly.start_py
            elif self.tro_op_time <= simul_time < self.ce_time:
                self.trolly.px, self.trolly.py = self.trolly.ce_px, self.trolly.ce_py
        else:
            if self.pe_time <= simul_time < self.tro_ms_time:
                #straddler moving
                self.py = self.pe_py + (self.ce_py - self.pe_py) * (simul_time - self.pe_time).total_seconds() / (self.tro_ms_time - self.pe_time).total_seconds()
            elif self.tro_ms_time <= simul_time < self.tro_op_time:
                self.py = self.ce_py
                #trolly moving
                self.trolly.px = self.trolly.pe_px + (self.trolly.ce_px - self.trolly.pe_px) * (simul_time - self.tro_ms_time).total_seconds() / (self.tro_op_time - self.tro_ms_time).total_seconds()
                self.trolly.py = self.trolly.pe_py
            elif self.tro_op_time <= simul_time < self.ce_time:
                self.trolly.px, self.trolly.py = self.trolly.ce_px, self.trolly.ce_py
                
        if self.ce_time <= simul_time:
            self.trolly.px, self.trolly.py = self.trolly.pe_px, self.trolly.pe_py = self.trolly.ce_px, self.trolly.ce_py
            self.pe_time, self.pe_py = self.ce_time, self.ce_py
            
            
            if self.ce_state == 'TL':
                ce_c_id = int(self.ce_container[1:3])
                ce_container = self.target_tp.holding_containers.pop(ce_c_id)
                ce_container.px, ce_container.py = 0, 0
                self.holding_containers[int(ce_container.id[1:3])] = ce_container
#                print 'TL  id %d  -  c_id %d ' % (self.id, ce_c_id),
#                print ' -  holding ', self.holding_containers
                print ce_container.id ,ce_container.cur_ms_id , ce_container.moving_seq[ce_container.cur_ms_id]
                ce_container.cur_ms_id +=1
            else: #self.ce_state == 'TU':
                ce_c_id = int(self.ce_container[1:3])
#                print 'TU  id %d  -  c_id %d ' % (self.id, ce_c_id),
#                print ' -  holding ', self.holding_containers
                ce_container = self.holding_containers.pop(ce_c_id)
#                bay_id, stack_id = int(self.ce_pos[4:6]), int(self.ce_pos[7:9])
#                ce_container.px, ce_container.py =self.target_block.bay_pos_info[bay_id],self.target_block.stack_pos_info[stack_id]  
                self.target_block.holding_containers[int(ce_container.id[1:3])] = ce_container
                
            self.cur_evt_id += 1
            self.cur_evt_update(self.cur_evt_id)
            
    def draw(self, gc):
        gc.SetPen(wx.Pen('purple', 0))
        change_b_color(gc, 'purple')
        gc.DrawRectangle(-container_vs * 1.1 - container_vs * 7.8 / 2, -container_hs * 1.1 / 2, container_vs * 1.1, container_hs * 1.1)
        gc.DrawRectangle(-container_vs * 1.1 - container_vs * 7.8 / 2 + container_vs * 7.8 + container_vs * 1.1, -container_hs * 1.1 / 2, container_vs * 1.1, container_hs * 1.1)
        gc.DrawRectangle(-container_vs * 7.8 / 2, -6, container_vs * 7.8, 3)
        gc.DrawRectangle(-container_vs * 7.8 / 2, 3, container_vs * 7.8, 3)
        
        old_tr = gc.GetTransform()
        gc.Translate(self.trolly.px, self.trolly.py)
        self.trolly.draw(gc, self.holding_containers)
        gc.SetTransform(old_tr)

class SC(Vehicles):
    QBs, TPs, QCs = None, None, None
    sx, sy = container_hs * 1.2, container_vs * 1.2
    def __init__(self, name):
        Vehicles.__init__(self)
        self.id = int(name[-2:])
        self.name = 'SC'
        self.evt_seq = []
        self.cur_evt_id = 0
        
        self.target_qb, self.target_tp, self.target_qc = None, None, None
        self.start_time = None
        self.start_px, self.start_py = None, None
        
        ## ss: sea side, ls: land side 
        self.is_ss_to_ls = True
        self.waypoint1_time = None
        self.waypoint2_time = None
        self.waypoint3_time = None
        
        self.waypoint1_pos = (None, None)
        self.waypoint2_pos = (None, None)
        self.waypoint3_pos = (None, None)
        
        self.thr_wp1 = None
        self.thr_wp2 = None
        self.thr_wp3 = None
        
        self.px, self.py = 0, 0
    
    def __repr__(self):
        return str(self.name + str(self.id))
    
    def cur_evt_update(self, cur_evt_id, QBs=None, TPs=None, QCs=None):
        if len(self.evt_seq) <= 1: assert False, 'length of evt_seq is smaller than 2'
        
        if cur_evt_id == 0: SC.QBs, SC.TPs, SC.QCs = QBs, TPs, QCs
        self.cur_evt = self.evt_seq[cur_evt_id]
        ce_time, ce_pos, self.ce_container, self.ce_state, = self.cur_evt
        year, month, day, hour, minute, second = tuple(ce_time.split('-'))
        self.ce_time = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        
        if ce_pos[:1] == 'S':
            target_qc_id = int(ce_pos[3:5]) 
            for qc in SC.QCs:
                if qc.id == target_qc_id:
                    self.target_qc = qc
                    break
            else:
                assert False, 'there is not target qc'
            qb_id = int(ce_pos[10:])
            self.target_qb = SC.QBs[qb_id]
            self.ce_px, self.ce_py = self.target_qc.px, self.target_qb.py + self.target_qb.c_pos
            self.is_ss_to_ls = False 
        else: #ce_pos[:1] == 'B':
            tp_id, self.stack_id = int(ce_pos[1:3]), int(ce_pos[6:])
            self.target_tp = SC.TPs[tp_id]
            self.ce_px, self.ce_py = self.target_tp.px + self.target_tp.stack_pos[self.stack_id], SC.TPs[tp_id].py + SC.TPs[tp_id].bay_pos_info
            self.is_ss_to_ls = True
        
        if cur_evt_id == 0:
            self.start_time = self.ce_time - timedelta(0, 8)
            self.start_px, self.start_py = self.px, self.py = self.ce_px - container_hs * 10, self.ce_py
            self.is_ss_to_ls = True
        else:
            self.px = self.pe_px
            time_interval = self.ce_time - self.pe_time
            assert 0 <= time_interval.total_seconds() < 3600 * 24, False
            ti_ts = time_interval.total_seconds()
            if self.is_ss_to_ls:
                self.waypoint1_time = self.pe_time + timedelta(0, ti_ts * (3 / 10))
                self.waypoint2_time = self.pe_time + timedelta(0, ti_ts * (6 / 10))
                self.waypoint3_time = self.pe_time + timedelta(0, ti_ts * (9 / 10))
                
                self.wp1_px, self.wp1_py = (self.pe_px + container_hs * 10, self.pe_py)
                self.wp2_px, self.wp2_py = (self.pe_px + container_hs * 10, self.ce_py - container_hs)
                self.wp3_px, self.wp3_py = (self.ce_px, self.ce_py - container_hs)
            else:
                self.waypoint1_time = self.pe_time + timedelta(0, ti_ts * (0.1 / 10))
                self.waypoint2_time = self.pe_time + timedelta(0, ti_ts * (4 / 10))
                self.waypoint3_time = self.pe_time + timedelta(0, ti_ts * (9 / 10))
                
                self.wp1_px, self.wp1_py = (self.pe_px, self.pe_py - container_hs)
                self.wp2_px, self.wp2_py = (self.pe_px - container_hs * 4, self.pe_py - container_hs)
                self.wp3_px, self.wp3_py = (self.pe_px - container_hs * 4, self.ce_py)
            
            self.thr_wp1 = False
            self.thr_wp2 = False
            self.thr_wp3 = False
        
    def OnTimer(self, evt, simul_time):
        if int(self.ce_container[1:]) in self.target_qb.holding_containers:
            ce_c_id = int(self.ce_container[1:])
            self.ce_px = self.target_qb.holding_containers[ce_c_id].px
        if self.cur_evt_id == 0:
            if self.start_time <= simul_time < self.ce_time:
                self.px = self.start_px + (self.ce_px - self.start_px) * (simul_time - self.start_time).total_seconds() / (self.ce_time - self.start_time).total_seconds()
        else:
            if self.is_ss_to_ls:
                if self.pe_time <= simul_time < self.waypoint1_time:
                    self.px = self.pe_px + (self.wp1_px - self.pe_px) * (simul_time - self.pe_time).total_seconds() / (self.waypoint1_time - self.pe_time).total_seconds()
                    self.py = self.pe_py
                elif self.waypoint1_time <= simul_time < self.waypoint2_time:
                    self.thr_wp1 = True
                    self.px = self.wp1_px  
                    self.py = self.wp1_py + (self.wp2_py - self.wp1_py) * (simul_time - self.waypoint1_time).total_seconds() / (self.waypoint2_time - self.waypoint1_time).total_seconds()
                elif self.waypoint2_time <= simul_time < self.waypoint3_time:
                    self.thr_wp2 = True
                    self.px = self.wp2_px + (self.wp3_px - self.wp2_px) * (simul_time - self.waypoint2_time).total_seconds() / (self.waypoint3_time - self.waypoint2_time).total_seconds()
                    self.py = self.wp2_py
                elif self.waypoint3_time <= simul_time < self.ce_time:
                    self.thr_wp3 = True
                    self.px = self.wp3_px
                    self.py = self.wp3_py + (self.ce_py - self.wp3_py) * (simul_time - self.waypoint3_time).total_seconds() / (self.ce_time - self.waypoint3_time).total_seconds()
            else:
                if self.pe_time <= simul_time < self.waypoint1_time:
                    self.px = self.pe_px
                    self.py = self.pe_py + (self.wp1_py - self.pe_py) * (simul_time - self.pe_time).total_seconds() / (self.waypoint1_time - self.pe_time).total_seconds()
                elif self.waypoint1_time <= simul_time < self.waypoint2_time:
                    self.thr_wp1 = True
                    self.px = self.wp1_px + (self.wp2_px - self.wp1_px) * (simul_time - self.waypoint1_time).total_seconds() / (self.waypoint2_time - self.waypoint1_time).total_seconds()
                    self.py = self.wp1_py
                elif self.waypoint2_time <= simul_time < self.waypoint3_time:
                    self.thr_wp2 = True
                    self.px = self.wp2_px
                    self.py = self.wp2_py + (self.wp3_py - self.wp2_py) * (simul_time - self.waypoint2_time).total_seconds() / (self.waypoint3_time - self.waypoint2_time).total_seconds()
                elif self.waypoint3_time <= simul_time < self.ce_time:
                    self.thr_wp3 = True
                    self.px = self.wp3_px + (self.ce_px - self.wp3_px) * (simul_time - self.waypoint3_time).total_seconds() / (self.ce_time - self.waypoint3_time).total_seconds()
                    self.py = self.wp3_py

        if  self.ce_time <= simul_time:
            self.pe_time = self.ce_time
            self.pe_px, self.pe_py = self.px, self.py = self.ce_px, self.ce_py
            
            if self.ce_state == 'TL':
                ce_c_id = int(self.ce_container[1:3])
                ce_container = self.target_qb.holding_containers.pop(ce_c_id)
                ce_container.px, ce_container.py = 0, 0
                self.holding_containers[int(ce_container.id[1:3])] = ce_container
            else: #self.ce_state == 'TU':
                ce_c_id = int(self.ce_container[1:3])
                ce_container = self.holding_containers.pop(ce_c_id)
                ce_container.px, ce_container.py = self.target_tp.stack_pos[self.stack_id], self.target_tp.bay_pos_info
                save_c_hs = ce_container.hs 
                ce_container.hs = ce_container.vs
                ce_container.vs = save_c_hs
                self.target_tp.holding_containers[int(ce_container.id[1:3])] = ce_container
            print ce_container.id ,ce_container.cur_ms_id , ce_container.moving_seq[ce_container.cur_ms_id]
            ce_container.cur_ms_id +=1    
            self.cur_evt_id += 1
            self.cur_evt_update(self.cur_evt_id)
                
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
            
        gc.SetPen(wx.Pen("black", 0.1))
        r, g, b = (255, 255, 255)
        brushclr = wx.Colour(r, g, b, 100)
        gc.SetBrush(wx.Brush(brushclr))
        gc.DrawRectangle(-SC.sx / 2, -SC.sy / 2, SC.sx, SC.sy)
