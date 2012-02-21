from __future__ import division
from parameter_function import container_hs, container_vs, l_sx
from parameter_function import pyslot, pvslot
from parameter_function import change_b_color
from datetime import datetime
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
        gc.DrawRectangle(self.hs / 2, self.vs / 2, self.hs, self.vs)
    
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
            if bay_id % 4 == 0:
                py = container_hs * ((bay_id // 4 - 1) + 1 / 2) + container_hs / 2
            elif bay_id % 4 == 1:
                py = container_hs * (bay_id // 4) + container_hs / 4
            elif bay_id % 4 == 2:
                py = container_hs * (bay_id // 4) + container_hs / 2
            elif bay_id % 4 == 3:
                py = container_hs * ((bay_id // 4) + 1 / 2) + container_hs / 4
            else:
                assert False
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
        self.sf_ori_px, self.sf_ori_py = None, None  
        
        self.v_d_p = [(0, container_vs * 2), (container_hs * 1.84 , 0), (container_hs * 11 , 0),
                      (container_hs * 13 , container_vs * 1.25), (self.LOA, self.B / 2) , (container_hs * 13 , self.B - container_vs * 1.25),
                      (container_hs * 11 , self.B), (container_hs * 1.84 , self.B), (0, self.B - container_vs * 2.5),
                       (0, container_vs * 2)]
        
        self.margin_px = container_hs * 2
        for x in xrange(self.num_of_bay):
            self.bay_pos_info[(self.num_of_bay_drawn - (x + 1)) * 4 + 1] = self.margin_px + container_hs / 4 + container_hs * 1.1 * x 
            self.bay_pos_info[(self.num_of_bay_drawn - (x + 1)) * 4 + 2] = self.margin_px + container_hs * 1.1 * x + container_hs / 2
            self.bay_pos_info[(self.num_of_bay_drawn - (x + 1)) * 4 + 3] = self.margin_px - container_hs / 4 + container_hs * 1.1 * x
             
        self.margin_py = container_vs * 1.0
        for x in xrange(self.num_of_stack):
            self.stack_pos_info[x + 1] = x * container_vs + container_vs / 2
#            self.stack_pos_info[x + 1] = self.margin_py + x * container_vs + container_vs / 2 
        
    def __repr__(self):
        return self.name + ' : ' + str(self.voyage)
    
    def cur_evt_update(self, cur_evt_id, Bitts):
        if len(self.evt_seq) <= 1: assert False, 'length of evt_seq is smaller than 2'
        self.cur_evt = self.evt_seq[cur_evt_id]
        self.next_evt = self.evt_seq[cur_evt_id + 1]
        ce_time, self.ce_state, ce_pos = self.cur_evt
        year, month, day, hour, minute, second = tuple(ce_time.split('-'))
        self.ce_time = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        bitt_id = int(ce_pos[-2:])
        self.ce_px, self.ce_py = Bitts[bitt_id].px - self.LOA * 1 / 3, Bitts[bitt_id].py - self.B * 1.1
        
        if cur_evt_id == 0 :
            self.sf_ori_px, self.sf_ori_py = self.px, self.py = self.ce_px, self.ce_py# - container_hs * 2 
        
        ne_time, self.ne_state, ne_pos = self.next_evt
        year, month, day, hour, minute, second = tuple(ne_time.split('-'))
        self.ne_time = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        
        bitt_id = int(ne_pos[-2:])
        self.ne_px, self.ne_py = Bitts[bitt_id].px - self.LOA * 1 / 3, Bitts[bitt_id].py - self.B * 1.1
    
    def draw(self, gc):
        gc.SetPen(wx.Pen("black", 1))
        brushclr = wx.Colour(255, 255, 255)
        gc.SetBrush(wx.Brush(brushclr))
        #draw vessel surface        
        gc.DrawLines(self.v_d_p)
#        gc.DrawRectangle(0,0, self.LOA, self.B)
        gc.SetPen(wx.Pen("black", 0.5))
        
#        for b in xrange((self.num_of_bay-1)//2):
#            gc.DrawLines([(0, container_hs * x), (container_vs * self.num_of_stacks , container_hs * x)])




#            px = self.bay_pos_info[bay_id] - container_hs / 2
##            px = self.margin_px + container_hs * b
#            py = self.margin_py
#            for s in xrange(self.num_of_stack + 1):
#                gc.DrawLines([(px, py + s * container_vs), (px + container_hs, py + s * container_vs)])
#            gc.DrawLines([(px, py), (px, py + self.num_of_stack * container_vs)])
#            gc.DrawLines([(px + container_hs, py), (px + container_hs, py + self.num_of_stack * container_vs)])
        
#        change_b_color(gc, 'orange')
#        for c in self.holding_containers:
#            bay_id, stack_id, _ = pvslot(c.cur_position)
#            px, py = self.bay_pos_info[bay_id] , self.stack_pos_info[stack_id]
#            old_tr = gc.GetTransform()
#            gc.Translate(px, py)
#            c.draw(gc)
#            gc.SetTransform(old_tr)

class QC(object):
    def __init__(self, name):
        self.name = name
        self.evt_seq = []
        self.px, self.py = None, None

    def __repr__(self):
        return self.name
    
    def draw(self, gc):
        pass

class YC(object):
    def __init__(self, name):
        self.name = name
        self.evt_seq = []
        self.px, self.py = None, None
    def __repr__(self):
        return self.name

    def set_position(self, px, py):
        self.px, self.py = px, py

    def set_destination_pos(self, px, py):
        self.dest_px, self.dest_py = int(px), int(py)
 
    def draw(self, gc):
        r, g, b = (90, 14, 160)
        brushclr = wx.Colour(r, g, b, 200)
        gc.SetPen(wx.Pen(brushclr, 0))
        gc.SetBrush(wx.Brush(brushclr))
        
        ##1st yc
        gc.DrawRectangle(-container_vs, 0, container_vs * 1.1, container_hs * 1.1)
        gc.DrawRectangle(container_vs * 9 - (container_vs * 1.1), 0, container_vs * 1.1, container_hs * 1.1)
        gc.DrawRectangle(container_vs * 0.1, (container_hs * 1.1 * 0.5) - 6, container_vs * 7.8, 3)
        gc.DrawRectangle(container_vs * 0.1, (container_hs * 1.1 * 0.5) + 3, container_vs * 7.8, 3)
        
        ##2nd yc
        gc.DrawRectangle(-container_vs, 50, container_vs * 1.1, container_hs * 1.1)
        gc.DrawRectangle(container_vs * 9 - (container_vs * 1.1), 50, container_vs * 1.1, container_hs * 1.1)
        gc.DrawRectangle(container_vs * 0.1, (container_hs * 1.1 * 0.5) - 6 + 50, container_vs * 7.8, 3)
        gc.DrawRectangle(container_vs * 0.1, (container_hs * 1.1 * 0.5) + 3 + 50, container_vs * 7.8, 3)

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
        r, g, b = (255, 0, 0)
        brushclr = wx.Colour(r, g, b, 100)
        gc.SetBrush(wx.Brush(brushclr))
        gc.DrawRectangle(0, 0, container_hs * 1.1, container_vs * 1.1)
