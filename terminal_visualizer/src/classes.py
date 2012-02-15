from __future__ import division
from parameter_function import container_hs, container_vs
from parameter_function import pyslot, pvslot
from parameter_function import change_b_color
import wx

class Container(object):
    def __init__(self, id):
        self.id = id
        self.moving_seq = []
        self.cur_position = None
        self.cur_index_in_ms = None
        self.hs, self.vs = container_hs , container_vs
        self.size = '40ft'
        self.location = None
        
    def __repr__(self):
        return str(self.id)

class Storage(object):
    def __init__(self, id):
        self.id = id
        self.name = None
        self.px, self.py = None, None
        self.holding_containers = []


class TP(Storage):
    def __init__(self, id):
        Storage.__init__(self, id)
        self.name = 'TP'

class Block(object):
    def __init__(self, id):
        self.id = id
        self.px, self.py = None, None
        self.holding_containers = []
        self.num_of_bays = 45
        self.num_of_stacks = 8
        self.bay_pos_info = {}
        for x in xrange(self.num_of_bays):
            bay_id = x + 1
            if bay_id % 4 == 0:
                py = container_hs * ((bay_id // 4 - 1) + 1 / 2)
            elif bay_id % 4 == 1:
                py = container_hs * (bay_id // 4)
            elif bay_id % 4 == 2:
                py = container_hs * (bay_id // 4)
            elif bay_id % 4 == 3:
                py = container_hs * ((bay_id // 4) + 1 / 2)
            else:
                assert False
            self.bay_pos_info[bay_id] = (0, py)
    def set_position(self, px, py):
        self.px, self.py = px , py
        
    def draw(self, gc):
        gc.SetPen(wx.Pen("black", 0.5))
        for x in xrange((self.num_of_bays - 1) // 2 + 1):
            gc.DrawLines([(0, container_hs * x), (container_vs * self.num_of_stacks , container_hs * x)])
        for x in xrange(self.num_of_stacks + 1):
            gc.DrawLines([(container_vs * x, 0), (container_vs * x , container_hs * self.num_of_bays)])
        
        change_b_color(gc, 'orange')
        for c in self.holding_containers:
            bay_id, stack_id, _ = pyslot(c.cur_position)
            bay_px, bay_py = self.bay_pos_info[bay_id]
            px, py = bay_px + (stack_id - 1) * container_vs, bay_py
            gc.DrawRectangle(px, py, c.hs, c.vs)

#class TP(object):
#    def __init__(self, id, px, py):
#        self.id = id
#        self.px, self.py = px, py
#        self.holding_containers = []
#        self.num_of_stack = 4
#    
#    def draw(self, gc):
#        gc.SetPen(wx.Pen("black", 0.1))
#        for x in xrange(self.num_of_stack + 1):
#            gc.DrawLines([((2 + x) * container_vs, 0), ((2 + x) * container_vs, container_hs)])
#        gc.DrawLines([(2 * container_vs, 0), ((2 + 4) * container_vs , 0)])
#        gc.DrawLines([(2 * container_vs, container_hs), ((2 + 4) * container_vs , container_hs)])


class Vessel(object):
    def __init__(self, name, voyage, type=0): 
        self.name = name
        self.voyage = voyage
        self.type = type
        self.LOA, self.B = container_hs * 14, container_vs * 10
        self.num_of_bay_drawn = 9
        
        self.evt_seq = []
        self.px, self.py = None, None
        self.holding_containers = []
        self.bay_pos_info = {}
        
        margin_px = container_hs * 2
        for x in xrange(self.num_of_bay_drawn):
            if  x == self.num_of_bay_drawn - 1:
                margin_py = 1.8
            else:
                margin_py = 0.8
            self.bay_pos_info[(self.num_of_bay_drawn - (x + 1)) * 4 + 1] = (margin_px + container_hs * 1.1 * x + container_hs / 2, container_vs * margin_py)
            self.bay_pos_info[(self.num_of_bay_drawn - (x + 1)) * 4 + 2] = (margin_px + container_hs * 1.1 * x, container_vs * margin_py)
            self.bay_pos_info[(self.num_of_bay_drawn - (x + 1)) * 4 + 3] = (margin_px + container_hs * 1.1 * x, container_vs * margin_py)
        self.even_num_bay_pos = [(k, v[0], v[1]) for k, v in self.bay_pos_info.items() if k % 2 == 0 ]
        
        self.v_d_p = [(0, container_vs * 2), (container_hs * 1.84 , 0), (container_hs * 11 , 0),
                      (container_hs * 13 , container_vs * 1.25), (self.LOA, self.B / 2) , (container_hs * 13 , self.B - container_vs * 1.25),
                      (container_hs * 11 , self.B), (container_hs * 1.84 , self.B), (0, self.B - container_vs * 2.5),
                       (0, container_vs * 2)]
        
    def __repr__(self):
        return self.name + ' : ' + str(self.voyage)
    
    def set_position(self, px, py):
        self.px, self.py = px - self.LOA * 1 / 3 , py - self.B * 1.1
    
    def draw(self, gc):
        gc.SetPen(wx.Pen("black", 1))
        brushclr = wx.Colour(255, 255, 255)
        gc.SetBrush(wx.Brush(brushclr))
        #draw vessel surface        
        gc.DrawLines(self.v_d_p)
        gc.SetPen(wx.Pen("black", 0.5))
        for k, px, py in self.even_num_bay_pos:
            if k == 2:
                num_of_stack = 6
            else:
                num_of_stack = 8
            for x in xrange(num_of_stack + 1):
                #draw stack and bay
                gc.DrawLines([(px, py + x * container_vs), (px + container_hs, py + x * container_vs)])
                gc.DrawLines([(px, py), (px, py + num_of_stack * container_vs)])
                gc.DrawLines([(px + container_hs, py), (px + container_hs, py + num_of_stack * container_vs)])
        
        change_b_color(gc, 'orange')
        for c in self.holding_containers:
            bay_id, stack_id, _ = pvslot(c.cur_position)
            bay_px, bay_py = self.bay_pos_info[bay_id]
            px, py = bay_px, bay_py + (stack_id - 1) * container_vs
            gc.DrawRectangle(px, py, c.hs, c.vs)

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
        gc.DrawRectangle(container_vs * 9 -(container_vs*1.1), 0, container_vs * 1.1, container_hs * 1.1)
        gc.DrawRectangle(container_vs*0.1, (container_hs*1.1*0.5)-6, container_vs * 7.8, 3 )
        gc.DrawRectangle(container_vs*0.1, (container_hs*1.1*0.5)+3, container_vs * 7.8, 3)
        
        ##2nd yc
        gc.DrawRectangle(-container_vs, 50, container_vs * 1.1, container_hs * 1.1)
        gc.DrawRectangle(container_vs * 9 -(container_vs*1.1), 50, container_vs * 1.1, container_hs * 1.1)
        gc.DrawRectangle(container_vs*0.1, (container_hs*1.1*0.5)-6+50, container_vs * 7.8, 3 )
        gc.DrawRectangle(container_vs*0.1, (container_hs*1.1*0.5)+3+50, container_vs * 7.8, 3)

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

class Buffer(object):
    def __init__(self):
        self.holding_containers #= [objects of Container]

class QC_buffer(Buffer):
    pass
