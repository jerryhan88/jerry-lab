from __future__ import division
from parameter_function import container_hs, container_vs, l_sx
from parameter_function import pyslot, pvslot
from parameter_function import change_b_color
from datetime import datetime, timedelta
import wx

class Container(object):
    def __init__(self, id):
        self.id = id
        self.moving_seq = []
        self.cur_position = None
        self.cur_index_in_ms = None
        self.hs, self.vs = container_hs , container_vs
        self.size = '40ft'
    def __repr__(self):
        return str(self.id)
    
    def draw(self, gc):
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
        self.holding_containers = []
    def __repr__(self):
        return self.name + str(self.id)

class QC_buffer(Storage):
    def __init__(self, id, px, py):
        Storage.__init__(self)
        self.id = id
        self.name = 'QC Buffer'
        self.px, self.py = px, py
    
    def draw(self, gc):
        gc.SetPen(wx.Pen('black', 0.5))
        gc.DrawLines([(0, 0), (l_sx, 0)])
        gc.DrawLines([(0, container_vs * 2.2), (l_sx, container_vs * 2.2)])
        
#        gc.DrawRectangle(-container_hs / 2, -container_vs / 2, container_vs * 10, container_hs)
        
#        if self.holding_containers:
#            r, g, b = 228, 108, 10
#            bruclr = wx.Colour(r, g, b, 200)
#            gc.SetBrush(wx.Brush(bruclr))
#            gc.DrawRectangle(-container_hs / 2, -container_vs / 2, container_hs, container_vs)

class TP(Storage):
    def __init__(self, id, px, py):
        Storage.__init__(self)
        self.id = id
        self.name = 'TP'
        self.px, self.py = px, py
        self.num_of_stacks = 4
        
#        self.stack_pos = {}
#        for x in xrange(self.num_of_stacks):
#            self.stack_pos[x+1] = {}
             

    def draw(self, gc):
        gc.SetPen(wx.Pen('black', 1))
        gc.DrawLines([(0, 0), (container_vs * self.num_of_stacks , 0)])
        gc.DrawLines([(0, container_hs), (container_vs * self.num_of_stacks , container_hs)])
        for x in xrange(self.num_of_stacks + 1) :
            gc.DrawLines([(container_vs * x, 0), (container_vs * x , container_hs)])

class Block(Storage):
    def __init__(self, id, px, py):
        Storage.__init__(self)
        self.id = id
        self.name = 'Block'
        self.px, self.py = px, py
        
        self.num_of_bays = 45
        self.num_of_stacks = 8
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
            
        for x in xrange(self.num_of_stacks):
            self.stack_pos_info[x + 1] = container_vs * x + container_vs / 2
        
    def draw(self, gc):
        gc.SetPen(wx.Pen("black", 0.5))
        for x in xrange((self.num_of_bays - 1) // 2 + 1):
            gc.DrawLines([(0, container_hs * x), (container_vs * self.num_of_stacks , container_hs * x)])
        for x in xrange(self.num_of_stacks + 1):
            gc.DrawLines([(container_vs * x, 0), (container_vs * x , container_hs * (self.num_of_bays - 1) // 2)])
        change_b_color(gc, 'orange')
        for c in self.holding_containers:
            bay_id, stack_id, _ = pyslot(c.cur_position)
            py = self.bay_pos_info[bay_id]
            px = self.stack_pos_info[stack_id]
            old_tr = gc.GetTransform()
            gc.Translate(px, py)
            c.draw(gc)
            gc.SetTransform(old_tr)

class Vehicles(object):

    def __init__(self):
        self.id = None
        self.name = None
        self.evt_seq = []
        self.cur_evt_id = 0
        self.holding_containers = []
        
        self.ce_px, self.ce_py = None, None
        self.px, self.py = None, None
        self.ne_px, self.ne_py = None, None
    def set_dest_position(self, px, py):
        self.ne_px, self.ne_py = px, py
        
class Vessel(Vehicles):
    def __init__(self, name, voyage):
        Vehicles.__init__(self)
        self.name = name
        self.voyage = voyage
        self.LOA, self.B = container_hs * 14, container_vs * 10
        self.num_of_bay = 35
        self.num_of_stack = 8
        self.bay_pos_info = {}
        self.stack_pos_info = {}
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
    
    def cur_evt_update(self, cur_evt_id, Bitts):
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
        
        self.ar_s_time = self.ce_time - timedelta(0, 15)
        self.dp_e_time = self.ne_time + timedelta(0, 20)
        

    def OnTimer(self, evt, simul_time):
        if self.ar_s_time <= simul_time < self.ce_time:
            self.px = self.ar_s_px
            self.py = self.ar_s_py + (self.ce_py - self.ar_s_py) * (simul_time - self.ar_s_time).seconds / (self.ce_time - self.ar_s_time).seconds
        
        if self.ne_time <= simul_time < self.dp_e_time:
            self.px = self.ar_s_px
            self.py = self.ne_py + (self.ne_py - self.dp_e_py) * (simul_time - self.ne_time).seconds / (self.dp_e_time - self.ne_time).seconds
            
    def draw(self, gc):
        gc.SetPen(wx.Pen("black", 1))
        brushclr = wx.Colour(255, 255, 255)
        gc.SetBrush(wx.Brush(brushclr))
        #draw vessel surface        
        gc.DrawLines(self.v_d_p)
#        gc.DrawRectangle(0,0, self.LOA, self.B)
        gc.SetPen(wx.Pen("black", 0.5))
        
        for x in xrange((self.num_of_bay + 1) // 4):
            bay_ori_px = self.margin_px + container_hs * 1.1 * x
            gc.DrawLines([(bay_ori_px, self.margin_py), (bay_ori_px, self.margin_py + container_vs * self.num_of_stack)])
            gc.DrawLines([(bay_ori_px + container_hs, self.margin_py), (bay_ori_px + container_hs, self.margin_py + container_vs * self.num_of_stack)])
            for s in xrange(self.num_of_stack + 1):
                gc.DrawLines([(bay_ori_px, self.margin_py + s * container_vs), (bay_ori_px + container_hs, self.margin_py + s * container_vs)])
        
        change_b_color(gc, 'orange')
        for c in self.holding_containers:
            bay_id, stack_id, _ = pvslot(c.cur_position)
            px, py = self.bay_pos_info[bay_id] , self.stack_pos_info[stack_id]
            old_tr = gc.GetTransform()
            gc.Translate(px, py)
            c.draw(gc)
            gc.SetTransform(old_tr)
    
class YC(Vehicles):
    class Trolly(Vehicles):
        def __init__(self):
            Vehicles.__init__(self)
        def draw(self, gc):
            tr, tg, tb = (4, 189, 252)
            t_brushclr = wx.Colour(tr, tg, tb, 200)
            ##draw trolly         
            gc.SetPen(wx.Pen(t_brushclr, 0))
            gc.SetBrush(wx.Brush(t_brushclr))
            gc.DrawRectangle(0, 0, container_vs * 1.1, 12)
    def __init__(self, name):
        Vehicles.__init__(self)
        self.id = int(name[-2:])
        self.name = 'YC'
        self.evt_seq = []
        self.cur_evt_id = 0
        self.trolly = self.Trolly()
        self.trolly.px, self.trolly.py = 0, (container_hs * 1.1 * 0.5) - 6
        
        self.isSpreaderMoving = False
        self.isTrollyMoving = False

    def __repr__(self):
        return str(self.name + str(self.id))
    
    def cur_evt_update(self, cur_evt_id, Block):
        if len(self.evt_seq) <= 1: assert False, 'length of evt_seq is smaller than 2'
        self.cur_evt = self.evt_seq[cur_evt_id]
        self.next_evt = self.evt_seq[cur_evt_id + 1]
        
        print self.cur_evt 
        ce_time, ce_pos, ce_container, self.ce_state,  = self.cur_evt
        year, month, day, hour, minute, second = tuple(ce_time.split('-'))
        self.ce_time = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
#        bitt_id = int(ce_pos[-2:])
#        self.ce_px, self.ce_py = Bitts[bitt_id].px - self.LOA * 1 / 3, Bitts[bitt_id].py - self.B * 1.1
        
        ne_time, self.ne_state, ne_pos = self.next_evt
        year, month, day, hour, minute, second = tuple(ne_time.split('-'))
        self.ne_time = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
#        bitt_id = int(ne_pos[-2:])
#        self.ne_px, self.ne_py = Bitts[bitt_id].px - self.LOA * 1 / 3, Bitts[bitt_id].py - self.B * 1.1
        
    def OnTimer(self, evt, simul_time):
        pass
    
    def draw(self, gc):
        yr, yg, yb = (90, 14, 160)
        y_brushclr = wx.Colour(yr, yg, yb, 200)
        gc.SetPen(wx.Pen(y_brushclr, 0))
        gc.SetBrush(wx.Brush(y_brushclr))
        
        gc.DrawRectangle(-container_vs, 0, container_vs * 1.1, container_hs * 1.1)
        gc.DrawRectangle(container_vs * 9 - (container_vs * 1.1), 0, container_vs * 1.1, container_hs * 1.1)
        gc.DrawRectangle(container_vs * 0.1, (container_hs * 1.1 * 0.5) - 6, container_vs * 7.8, 3)
        gc.DrawRectangle(container_vs * 0.1, (container_hs * 1.1 * 0.5) + 3, container_vs * 7.8, 3)
        
        old_tr = gc.GetTransform()
        gc.Translate(self.trolly.px, self.trolly.py)
        self.trolly.draw(gc)
        gc.SetTransform(old_tr)

class QC(Vehicles):
    class Trolly(Vehicles):
        def __init__(self):
            Vehicles.__init__(self)

        def draw(self, gc):
            tr, tg, tb = (4, 189, 252)
            t_brushclr = wx.Colour(tr, tg, tb, 200)
            ##draw trolly         
            gc.SetPen(wx.Pen(t_brushclr, 0))
            gc.SetBrush(wx.Brush(t_brushclr))
            gc.DrawRectangle(0, 0, container_hs * 0.5, container_hs * 0.5)

    def __init__(self, name):
        Vehicles.__init__(self)
        self.id = int(name[-2:])
        self.name = 'QC'
        self.evt_seq = []
        self.cur_evt_id = 0
        self.trolly = self.Trolly()
        self.trolly.px, self.trolly.py = 0, 0
        self.isSpreaderMoving = False
        self.isTrollyMoving = False

    def __repr__(self):
        return str(self.name + str(self.id))
    
    def cur_evt_update(self, cur_evt_id):
        if len(self.evt_seq) <= 1: assert False, 'length of evt_seq is smaller than 2' 
        self.cur_evt = self.evt_seq[cur_evt_id]
        self.next_evt = self.evt_seq[cur_evt_id + 1]
        self.ce_time, ce_pos, self.ce_state = self.cur_evt
        self.ce_px, self.ce_py = ce_pos
        self.ne_time, ne_pos, self.ne_state = self.next_evt
        self.ne_px, self.ne_py = ne_pos
        if self.ce_state[0] == 'S' and self.ne_state[0] == 'S':
            self.isSpreaderMoving = True
            self.isTrollyMoving = False
        elif self.ce_state[0] == 'S' and self.ne_state[0] == 'T':
            self.isSpreaderMoving = False
            self.isTrollyMoving = False    
        elif self.ce_state[0] == 'T' and self.ne_state[0] == 'T':
            self.isSpreaderMoving = False
            self.isTrollyMoving = True
        elif self.ce_state[0] == 'T' and self.ne_state[0] == 'S':
            self.isSpreaderMoving = False
            self.isTrollyMoving = False
        else:
            assert False
            
        if cur_evt_id == 0 : self.px, self.py = self.ce_px, self.ce_py
        
        if self.isSpreaderMoving:
            self.px, self.py = self.ce_px, self.ce_py
        elif self.isTrollyMoving:
            self.trolly.px, self.trolly.py = self.ce_px, self.ce_py
        
    def OnTimer(self, evt, simul_time):
        if self.isSpreaderMoving:
            if self.ce_time < simul_time < self.ne_time: 
                self.px = self.ce_px + (self.ne_px - self.ce_px) * (simul_time - self.ce_time) / (self.ne_time - self.ce_time)
        elif self.isTrollyMoving:
            if self.ce_time < simul_time < self.ne_time:
                self.trolly.py = self.ce_py + (self.ne_py - self.ce_py) * (simul_time - self.ce_time) / (self.ne_time - self.ce_time)
        if self.ne_time <= simul_time:
            self.cur_evt_id += 1
            self.cur_evt_update(self.cur_evt_id)
    
    def draw(self, gc):
        r, g, b = (0, 0, 0)
        brushclr = wx.Colour(r, g, b, 200)
        paint = wx.Colour(r, g, b, 0)
        gc.SetPen(wx.Pen(brushclr, 1))
        gc.SetBrush(wx.Brush(paint))
        
#        gc.DrawRectangle(0,0, container_hs, container_hs)
        
        gc.DrawRectangle(0, 0, container_hs * 0.5, container_hs * 9)
        gc.DrawLines([((container_hs * 0.5 * 0.25), 0), ((container_hs * 0.5 * 0.25) , container_hs * 9)])
        gc.DrawLines([((container_hs * 0.5) , container_hs * 9), ((container_hs * 0.5) - (container_hs * 0.5 * 0.75) , container_hs * 9 - (container_hs * 0.5 * 1.41))])
        gc.DrawRectangle(0, 0, container_hs * 0.5, container_hs * 9)
        gc.DrawLines([((container_hs * 0.5 * 0.25), 0), ((container_hs * 0.5 * 0.25) , container_hs * 9)])
        gc.DrawLines([((container_hs * 0.5) , container_hs * 9), ((container_hs * 0.5) - (container_hs * 0.5 * 0.75) , container_hs * 9 - (container_hs * 0.5 * 1.41))])
        
        gc.DrawLines([((container_hs * 0.5 * 0.25) , container_hs * 9 - (container_hs * 0.5 * 1.41)), (container_hs * 0.5 , container_hs * 9 - (container_hs * 0.5 * 1.41))])
        gc.DrawLines([((container_hs * 0.5) , container_hs * 9 - (container_hs * 0.5 * 1.41)), (container_hs * 0.5 - (container_hs * 0.5 * 0.75) , container_hs * 9)])
        for i in range(9):
            gc.DrawLines([(container_hs * 0.5 * 0.25, container_hs * 0.5 * i), (container_hs * 0.5, container_hs * 0.5 * i)])
            pass
        
        old_tr = gc.GetTransform()
        gc.Translate(self.trolly.px, self.trolly.py)
        self.trolly.draw(gc)
        gc.SetTransform(old_tr)

class SC(object):
    def __init__(self, name):
        self.name = name
        self.evt_seq = []
        self.px, self.py = None, None
        self.start_px, self.start_py = None, None
        self.dest_px, self.dest_py = None, None
        
        self.turn1 = False
        self.turn2 = False 
    
    def __repr__(self):
        return self.name

    def set_position(self, px, py):
        self.px, self.py = px, py

    def set_start_pos(self, px, py):
        self.start_px, self.start_py = int(px), int(py)
        self.set_position(int(px), int(py))

    def set_destination_pos(self, px, py):
        self.dest_px, self.dest_py = int(px), int(py)

    def update(self, evt):
        print 'cur : ' , self.px, self.py
        print 'dest : ', self.dest_px, self.dest_py
        
        if self.px == self.start_px - 50:
            self.turn1 = True
        if self.py == self.dest_py:
            self.turn2 = True
            
        if self.turn1:
            if self.turn2:
                self.set_position(self.px + 1, self.py)
            else :
                self.set_position(self.px, self.py - 1)
        else:
            self.set_position(self.px - 1, self.py)
    
    def draw(self, gc):
        gc.SetPen(wx.Pen("black", 1))
        r, g, b = (255, 255, 255)
        brushclr = wx.Colour(r, g, b, 100)
        gc.SetBrush(wx.Brush(brushclr))
        gc.DrawRectangle(0, 0, container_hs * 1.1, container_vs * 1.1)
