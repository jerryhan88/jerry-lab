from __future__ import division
import wx

#standard size of 40ft container
container_sx = 20
container_sy = 5

#lambda function
pyslot = lambda x: (int(x[4:6]), int(x[7:9]), int(x[10:12]))

class Container(object):
    def __init__(self, id):
        self.id = id
        self.moving_seq = []
        self.cur_position = None
        self.cur_index_in_ms = None
        self.px, self.py = None, None
        self.size = None
        self.location = None
        
    def __repr__(self):
        return str(self.id)
    
    def set_position_location(self, px, py, location):
        self.location = location
        bay_id, stack_id, _ = pyslot(self.cur_position)
        if bay_id % 2 == 0:
            self.size = '40ft'   
            self.px, self.py = px + (stack_id - 1) * container_sy, py + (bay_id // 2 - 1) * container_sx 
        else:
            self.size = '20ft'
            if bay_id // 4 == 1:
                self.px, self.py = px + (stack_id - 1) * container_sy, py + (bay_id // 4) * container_sx
            elif bay_id // 4 == 3:
                self.px, self.py = px + (stack_id - 1) * container_sy, py + (bay_id // 4 + 1 / 2) * container_sx
            else:
                assert False
    
    def draw(self, gc):
        if self.location == 'block':
            gc.DrawRectangle(self.px, self.py, container_sy, container_sx)
        elif self.location == 'vessel':
            gc.DrawRectangle(self.px, self.py, container_sx, container_sy)
#        else:
#            assert False

class Block(object):
    def __init__(self, id, px, py):
        self.id = id
        self.px, self.py = px, py
        self.holding_container = []
        self.num_of_bays = 22
        self.num_of_stacks = 8
        
    def draw(self, gc):
        gc.SetPen(wx.Pen("black", 0.5))
        for x in xrange(self.num_of_bays + 1):
            gc.DrawLines([(0, container_sx * x), (container_sy * self.num_of_stacks , container_sx * x)])
        for x in xrange(self.num_of_stacks + 1):
            gc.DrawLines([(container_sy * x, 0), (container_sy * x , container_sx * self.num_of_bays)])

    def set_container_position(self):
        for c in self.holding_container:
            c.set_position_location(self.px, self.py, 'block')
            
class Yard_block(Block):
    def __init__(self):
        self.sea_side_TP# = object of TP
        self.land_side_TP# = object of TP
        self.waiting_sc# = object of SC
        self.qc_buffer# = object of QC_buffer

class Vessel(object):
    def __init__(self, name, voyage, type=0):
        self.name = name
        self.voyage = voyage
        self.type = type
        self.LOA = container_sx * 14
        self.B = container_sy * 10
        self.evt_seq = []
        self.px, self.py = None, None
        self.holding_containers = []
        
    def __repr__(self):
        return self.name + ' : ' + str(self.voyage)
    
    def set_position(self, px, py):
        self.px, self.py = px - self.LOA * 1 / 3 , py - self.B * 1.1
    
    def set_container_position(self):
        for c in self.holding_container:
            c.set_position_location(self.px, self.py, 'block')
    
    def draw(self, gc):
        gc.SetPen(wx.Pen("black", 1))
        brushclr = wx.Colour(255, 255, 255)
        gc.SetBrush(wx.Brush(brushclr))
        #draw vessel surface        
        p0 = (0, container_sy * 2)
        p1 = (container_sx * 1.84 , 0)
        p2 = (container_sx * 11 , 0)
        p3 = (container_sx * 13 , container_sy * 1.25)
        p4 = (self.LOA, self.B / 2) 
        p5 = (container_sx * 13 , self.B - container_sy * 1.25)
        p6 = (container_sx * 11 , self.B)
        p7 = (container_sx * 1.84 , self.B)
        p8 = (0, self.B - container_sy * 2.5) 
        gc.DrawLines([p0, p1, p2, p3, p4, p5, p6, p7, p8, p0])
        
        #draw bays in vessel
        num_of_bay = 9
        b_p0 = container_sx * 2
        gc.SetPen(wx.Pen("black", 0.5))
        for x in xrange(num_of_bay):
            if  x == num_of_bay - 1:
                num_of_stack = 3
                px, py = b_p0 + container_sx * 1.1 * x, container_sy * 1.5
                gc.DrawRectangle(px, py, container_sx, container_sy * 3)
                self.draw_stack(gc, px, py, num_of_stack)
                
                px, py = b_p0 + container_sx * 1.1 * x, self.B / 2 + container_sy * 0.5
                gc.DrawRectangle(px, py, container_sx, container_sy * 3)
                self.draw_stack(gc, px, py, num_of_stack)
            else:
                num_of_stack = 4
                px, py = b_p0 + container_sx * 1.1 * x, container_sy * 0.5
                gc.DrawRectangle(px, py, container_sx, container_sy * 4)
                self.draw_stack(gc, px, py, num_of_stack)
                
                px, py = b_p0 + container_sx * 1.1 * x, self.B / 2 + container_sy * 0.5
                gc.DrawRectangle(px, py, container_sx, container_sy * 4)
                self.draw_stack(gc, px, py, num_of_stack)
                
    def draw_stack(self, gc, px, py, num_of_stack):
        for i in xrange(num_of_stack - 1):
            gc.DrawLines([(px, py + (i + 1) * container_sy), (px + container_sx, py + (i + 1) * container_sy)])
        

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
    def __repr__(self):
        return self.name
    
    def draw(self, gc):
        pass

class Buffer(object):
    def __init__(self):
        self.holding_containers #= [objects of Container]

class TP(Buffer):
    pass

class QC_buffer(Buffer):
    pass
