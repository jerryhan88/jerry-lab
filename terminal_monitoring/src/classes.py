from __future__ import division
import wx

#standard size of 40ft container
container_sx = 20
container_sy = 5

#lambda function
pyslot = lambda x: (int(x[4:6]), int(x[7:9]), int(x[10:12]))
pvslot = lambda x: (int(x[2:4]), int(x[5:7]), int(x[8:10]))

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
    
    def set_position_location(self, px, py, location, sb_pos_info = None):
        self.location = location
        if self.location == 'block': 
            bay_id, stack_id, _ = pyslot(self.cur_position)
            # TODO  arrange container's position
            if bay_id % 4 == 0:
                self.size = '40ft'
                self.px, self.py = px + (stack_id - 1) * container_sy, py + (bay_id // 4 - 1 + 1 / 2) * container_sx
                pass
            elif bay_id % 2 == 0:
                self.size = '40ft'   
                self.px, self.py = px + (stack_id - 1) * container_sy, py + (bay_id // 2 - 1) * container_sx 
            else:
                self.size = '20ft'
                self.px, self.py = px + (stack_id - 1) * container_sy, py + (bay_id // 2) * container_sx / 2
        elif self.location == 'vessel':
            bay_id, stack_id, _ = pvslot(self.cur_position)
            if bay_id % 2 == 0:
                self.size = '40ft'
                self.px, self.py = px + (stack_id - 1) * container_sy, py + (bay_id // 2 - 1) * container_sx  
            else:
                self.size = '20ft'
#                self.px, self.py = 
    
    def draw(self, gc):
        if self.location == 'block':
            if self.size == '40ft':
                gc.DrawRectangle(self.px, self.py, container_sy, container_sx)
            elif self.size == '20ft':
                gc.DrawRectangle(self.px, self.py, container_sy, container_sx / 2)
            else:
                assert False
#        elif self.location == 'vessel':
#            gc.DrawRectangle(self.px, self.py, container_sx, container_sy)
#        else:
#            assert False

class Block(object):
    def __init__(self, id, px, py):
        self.id = id
        self.px, self.py = px, py
        self.holding_containers = []
        # 
        self.num_of_bays = 22
        self.num_of_stacks = 8
        
    def draw(self, gc):
        gc.SetPen(wx.Pen("black", 0.5))
        for x in xrange(self.num_of_bays * 2 + 1):
            gc.DrawLines([(0, container_sx * x / 2), (container_sy * self.num_of_stacks , container_sx * x / 2)])
        for x in xrange(self.num_of_stacks + 1):
            gc.DrawLines([(container_sy * x, 0), (container_sy * x , container_sx * self.num_of_bays)])

    def set_container_position(self):
        for c in self.holding_containers:
            c.set_position_location(self.px, self.py, 'block')

class TP(object):
    def __init__(self, id, px, py):
        self.id = id
        self.px, self.py = px, py
        self.holding_containers = []
        self.num_of_stack = 4
    
    def draw(self, gc):
        gc.SetPen(wx.Pen("black", 0.1))
        for x in xrange(self.num_of_stack + 1):
            gc.DrawLines([((2 + x) * container_sy, 0), ((2 + x) * container_sy, container_sx)])
        gc.DrawLines([(2 * container_sy, 0), ((2 + 4) * container_sy , 0)])
        gc.DrawLines([(2 * container_sy, container_sx), ((2 + 4) * container_sy , container_sx)])

class Vessel(object):
    def __init__(self, name, voyage, type=0):
        self.name = name
        self.voyage = voyage
        self.type = type
        self.LOA = container_sx * 14
        self.B = container_sy * 10
        self.evt_seq = []
        self.num_of_bay = 9
        self.px, self.py = None, None
        self.holding_containers = []
        self.bay_pos_info = {}
        
        p0 = (0, container_sy * 2)
        p1 = (container_sx * 1.84 , 0)
        p2 = (container_sx * 11 , 0)
        p3 = (container_sx * 13 , container_sy * 1.25)
        p4 = (self.LOA, self.B / 2) 
        p5 = (container_sx * 13 , self.B - container_sy * 1.25)
        p6 = (container_sx * 11 , self.B)
        p7 = (container_sx * 1.84 , self.B)
        p8 = (0, self.B - container_sy * 2.5)
        self.v_d_p = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p0]
        
    def __repr__(self):
        return self.name + ' : ' + str(self.voyage)
    
    def set_position(self, px, py):
        self.px, self.py = px - self.LOA * 1 / 3 , py - self.B * 1.1
        b_p0 = container_sx * 2
        for x in xrange(self.num_of_bay):
            if  x == self.num_of_bay - 1:
                self.bay_pos_info[(self.num_of_bay - (x + 1)) * 4 + 2] = (b_p0 + container_sx * 1.1 * x, container_sy * 1.8)
            else:
                self.bay_pos_info[(self.num_of_bay - (x + 1)) * 4 + 2] = (b_p0 + container_sx * 1.1 * x, container_sy * 0.8)

    def set_container_position(self):
        for c in self.holding_containers:
            c.set_position_location(self.px, self.py, 'vessel')
    
    def draw(self, gc):
        gc.SetPen(wx.Pen("black", 1))
        brushclr = wx.Colour(255, 255, 255)
        gc.SetBrush(wx.Brush(brushclr))
        #draw vessel surface        
        gc.DrawLines(self.v_d_p)
        
        gc.SetPen(wx.Pen("black", 0.5))
        for k, v in self.bay_pos_info.items():
            px, py = v
            if k == 2:
                num_of_stack = 6
            else:
                num_of_stack = 8
            for x in xrange(num_of_stack // 2 + 1):
                #draw stack and bay
                gc.DrawLines([(px, py + x * container_sy), (px + container_sx, py + x * container_sy)])
                gc.DrawLines([(px, py + (x + num_of_stack / 2 + 0.5) * container_sy), (px + container_sx, py + (x + num_of_stack / 2 + 0.5) * container_sy)])
                
                gc.DrawLines([(px, py), (px, py + num_of_stack / 2 * container_sy)])
                gc.DrawLines([(px, py + (num_of_stack / 2 + 0.5) * container_sy), (px, py + (num_of_stack + 0.5) * container_sy)])
                
                gc.DrawLines([(px + container_sx, py), (px + container_sx, py + num_of_stack / 2 * container_sy)])
                gc.DrawLines([(px + container_sx, py + (num_of_stack / 2 + 0.5) * container_sy), (px + container_sx, py + (num_of_stack + 0.5) * container_sy)])

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
#        self.num_of_bays = 22
#        self.num_of_stacks = 8
    def __repr__(self):
        return self.name
    
    def draw(self, gc):
#        gc.SetPen(wx.Pen("black", 0.5))
#        gc.DrawRectangle(0, 0, container_sy*self.num_of_stacks, container_sx)
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
        gc.DrawRectangle(0, 0, container_sx * 1.1, container_sy * 1.1)
        pass
class Buffer(object):
    def __init__(self):
        self.holding_containers #= [objects of Container]

class QC_buffer(Buffer):
    pass
