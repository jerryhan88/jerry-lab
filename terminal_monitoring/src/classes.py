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
        return str(self.id) + ' : ' + self.cur_position
    
#    def set_position_location(self, location, sb_pos_info):
##    def set_position_location(self, px, py, location, sb_pos_info = None):
#        self.location = location
#        if self.location == 'block': 
#            bay_id, stack_id, _ = pyslot(self.cur_position)
            # TODO  arrange container's position
            #   make bay and stack pos dic in Block
####            if bay_id % 4 == 0:
####                self.size = '40ft'
####                self.px, self.py = px + (stack_id - 1) * container_vs, py + (bay_id // 4 - 1 + 1 / 2) * container_hs
####                pass
####            elif bay_id % 2 == 0:
####                self.size = '40ft'   
####                self.px, self.py = px + (stack_id - 1) * container_vs, py + (bay_id // 2 - 1) * container_hs 
####            else:
####                self.size = '20ft'
####                self.px, self.py = px + (stack_id - 1) * container_vs, py + (bay_id // 2) * container_hs / 2
#        elif self.location == 'vessel':
#            bay_id, stack_id, _ = pvslot(self.cur_position)
#            if bay_id % 2 == 0:
##                self.px, self.py = px + (stack_id - 1) * container_vs, py + (bay_id // 2 - 1) * container_hs
#            else:
#                self.size = '20ft'
#            bay_px, bay_py = sb_pos_info[bay_id]
#            self.px, self.py = bay_px, bay_py + (stack_id - 1) * container_vs   
    
#    def draw(self, gc):
#        if self.location == 'block':
#            if self.size == '40ft':
#                gc.DrawRectangle(self.px, self.py, container_vs, container_hs)
#            elif self.size == '20ft':
#                gc.DrawRectangle(self.px, self.py, container_vs, container_hs / 2)
#            else:
#                assert False
#        elif self.location == 'vessel':
#            if self.size == '40ft':
#                gc.DrawRectangle(self.px, self.py, container_hs, container_vs)
#            elif self.size == '20ft':
#                gc.DrawRectangle(self.px, self.py, container_hs / 2, container_vs)    
#        else:
#            assert False

class Block(object):
    def __init__(self, id):
        self.id = id
        self.px, self.py = None, None
        self.holding_containers = []
        self.num_of_bays = 45
        self.num_of_stacks = 8
        self.bay_pos_info = {}
        ######################################## TODO
        #############error
        for x in xrange(self.num_of_bays):
            self.bay_pos_info[x * 4 + 1] = (0, container_hs * x)
            self.bay_pos_info[x * 4 + 2] = (0, container_hs * x)
            self.bay_pos_info[x * 4 + 3] = (0, container_hs * (x + 1 / 2))
    
    def set_position(self, px, py):
        self.px, self.py = px , py
        
    def draw(self, gc):
        gc.SetPen(wx.Pen("black", 0.5))
        for x in xrange((self.num_of_bays - 1) // 2 + 1):
            gc.DrawLines([(0, container_hs * x), (container_vs * self.num_of_stacks , container_hs * x)])
        for x in xrange(self.num_of_stacks + 1):
            gc.DrawLines([(container_vs * x, 0), (container_vs * x , container_hs * self.num_of_bays)])
        
        change_b_color(gc, 'orange')
        for c in self.holding_containers[:]:
            bay_id, stack_id, _ = pyslot(c.cur_position)
            print bay_id 
            bay_px, bay_py = self.bay_pos_info[bay_id]
            px, py = bay_px + (stack_id - 1) * container_vs, bay_py
            gc.DrawRectangle(px, py, c.hs, c.vs)

class TP(object):
    def __init__(self, id, px, py):
        self.id = id
        self.px, self.py = px, py
        self.holding_containers = []
        self.num_of_stack = 4
    
    def draw(self, gc):
        gc.SetPen(wx.Pen("black", 0.1))
        for x in xrange(self.num_of_stack + 1):
            gc.DrawLines([((2 + x) * container_vs, 0), ((2 + x) * container_vs, container_hs)])
        gc.DrawLines([(2 * container_vs, 0), ((2 + 4) * container_vs , 0)])
        gc.DrawLines([(2 * container_vs, container_hs), ((2 + 4) * container_vs , container_hs)])


class Vessel(object):
    def __init__(self, name, voyage, type=0):
        self.name = name
        self.voyage = voyage
        self.type = type
        self.LOA, self.B = container_hs * 14, container_vs * 10
        self.num_of_bay = 9
        
        self.evt_seq = []
        self.px, self.py = None, None
        self.holding_containers = []
        self.bay_pos_info = {}
        
        margin_px = container_hs * 2
        for x in xrange(self.num_of_bay):
            if  x == self.num_of_bay - 1:
                margin_py = 1.8
            else:
                margin_py = 0.8
            self.bay_pos_info[(self.num_of_bay - (x + 1)) * 4 + 1] = (margin_px + container_hs * 1.1 * x + container_hs / 2, container_vs * margin_py)
            self.bay_pos_info[(self.num_of_bay - (x + 1)) * 4 + 2] = (margin_px + container_hs * 1.1 * x, container_vs * margin_py)
            self.bay_pos_info[(self.num_of_bay - (x + 1)) * 4 + 3] = (margin_px + container_hs * 1.1 * x, container_vs * margin_py)
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
        for c in self.holding_containers[:]:
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
    
    def draw(self, gc):
        pass

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
        pass
class Buffer(object):
    def __init__(self):
        self.holding_containers #= [objects of Container]

class QC_buffer(Buffer):
    pass
