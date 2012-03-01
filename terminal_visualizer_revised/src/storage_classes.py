from __future__ import division
from parameter_function import container_hs, container_vs, l_sx, change_b_color
import wx
class Storage(object):
    def __init__(self):
        self.id, self.name = None, None
        self.px, self.py = None, None
        self.holding_containers = {}
    def __repr__(self):
        return self.name + str(self.id)
    def draw(self, gc):
        pass
    
class QB(Storage):
    sy = container_vs * 2.2
    h_c_pos_info = sy / 2
    def __init__(self, id, px, py):
        Storage.__init__(self)
        self.name, self.id = 'QC Buffer', id
        self.px, self.py = px, py
    def draw(self, gc):
        gc.SetPen(wx.Pen('black', 0.5))
        gc.DrawLines([(0, 0), (l_sx, 0)])
        gc.DrawLines([(0, QB.sy), (l_sx, QB.sy)])
#        for c in self.holding_containers.values():
#            old_tr = gc.GetTransform()
#            gc.Translate(c.px, c.py)
#            c.draw(gc)
#            gc.SetTransform(old_tr)
class TP(Storage):
    num_of_stacks = 4
    bay_pos_info = container_hs / 2
    stack_pos_info = {}
    for x in xrange(num_of_stacks): stack_pos_info[x + 1] = container_vs / 2 + container_vs * x * 2
    
    def __init__(self, id, px, py):
        Storage.__init__(self)
        self.name, self.id = 'TP', id
        self.px, self.py = px, py
    def draw(self, gc):
        gc.SetPen(wx.Pen('black', 0.2))
        change_b_color(gc, 'white')
        for s_px in TP.stack_pos_info.values() :
            gc.DrawRectangle(s_px - container_vs / 2, 0, container_vs, container_hs)
#        for c in self.holding_containers.values():
#            old_tr = gc.GetTransform()
#            gc.Translate(c.px, c.py)
#            c.draw(gc)
#            gc.SetTransform(old_tr)
class Block(Storage):
    num_of_bays = 45
    num_of_stacks = 8
    bay_pos_info = {}
    stack_pos_info = {}
    for x in xrange(num_of_bays):
        bay_id = x + 1
        if bay_id % 4 == 0: py = container_hs * ((bay_id // 4 - 1) + 1 / 2) + container_hs / 2
        elif bay_id % 4 == 1: py = container_hs * (bay_id // 4) + container_hs / 4
        elif bay_id % 4 == 2: py = container_hs * (bay_id // 4) + container_hs / 2
        elif bay_id % 4 == 3: py = container_hs * ((bay_id // 4) + 1 / 2) + container_hs / 4
        else: assert False
        bay_pos_info[bay_id] = py
    for x in xrange(num_of_stacks):
        stack_pos_info[x + 1] = container_vs * x + container_vs / 2
        
    def __init__(self, id, px, py):
        Storage.__init__(self)
        self.name, self.id = 'Block', id
        self.px, self.py = px, py
    def draw(self, gc):
        gc.SetPen(wx.Pen("black", 0.5))
        for x in xrange((Block.num_of_bays - 1) // 2 + 1):
            gc.DrawLines([(0, container_hs * x), (container_vs * Block.num_of_stacks , container_hs * x)])
        for x in xrange(Block.num_of_stacks + 1):
            gc.DrawLines([(container_vs * x, 0), (container_vs * x , container_hs * (Block.num_of_bays - 1) // 2)])
#        change_b_color(gc, 'orange')
#        
#        for c in self.holding_containers.values():
#            bay_id, stack_id, _ = pyslot(c.moving_seq[c.cur_ms_id][1])
#            py = self.bay_pos_info[bay_id]
#            px = self.stack_pos_info[stack_id]
#            c.px, c.py = px, py
#            old_tr = gc.GetTransform()
#            gc.Translate(c.px, c.py)
#            c.draw(gc)
#            gc.SetTransform(old_tr)
