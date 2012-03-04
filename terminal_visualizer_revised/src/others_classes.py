from __future__ import division
from datetime import datetime
from parameter_function import container_hs, container_vs, change_b_color, calc_proportional_pos
from random import seed, randrange
from datetime import timedelta
import wx
seed(10)
class Container(object):
    def __init__(self, c_id):
        self.c_id = c_id
        self.evt_seq, self.target_evt_id = [], -1
        self.size = None
        self.hs, self.vs = None, None
        self.px, self.py = None, None
        self.evt_end = False
        self.color = randrange(5)
    def __repr__(self):
        return 'Container ' + str(self.c_id)
    
    def draw(self, gc):
        gc.SetPen(wx.Pen('black', 0))
        if self.color == 0:
            change_b_color(gc, 'orange')
        elif self.color == 1:
            change_b_color(gc, 'red')
        elif self.color == 2:
            change_b_color(gc, 'green')
        elif self.color == 3:
            change_b_color(gc, 'blue')
        elif self.color == 4:
            change_b_color(gc, 'd_orange')
        else:
            assert False, ''
        gc.DrawRectangle(-self.hs / 2, -self.vs / 2, self.hs, self.vs)

class Bitt(object):
    sx, sy = container_hs * 0.26, container_vs * 0.8
    def __init__(self, id, px, py):
        self.id = id
        self.name = 'Bitt'
        self.px, self.py = px, py
    def __repr__(self):
        return self.name + str(self.id)
    def draw(self, gc):
        ## draw Bit
        bitt_clr = wx.Colour(251, 194, 0)
        gc.SetBrush(wx.Brush(bitt_clr))
        gc.SetPen(wx.Pen(bitt_clr, 0))
        gc.DrawRectangle(0, 0.5, Bitt.sx, Bitt.sy)
    
class Evt(object):
    def __init__(self, dt_txt, vehicle, work_type, c_id, operation, v_info, state, pos=None):
        year, month, day, hour, minute, second = dt_txt.split('-') 
        self.dt = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        self.vehicle, self.work_type, self.c_id, self.operation, self.v_info, self.state, self.pos = vehicle, work_type, c_id, operation, v_info, state, pos
    def __repr__(self):
        return str(self.dt) + '_' + self.vehicle + '_' + self.work_type + '_' + str(self.c_id) + '_' + str(self.pos) + '_' + str(self.operation) + '_' + self.v_info + '_' + self.state

class Vessel(object):
    Bitts = None
    LOA = container_hs * 18
    Beam = container_vs * (13 + 4)
    num_of_bay, num_of_stack = 51, 13
    btn_bay = 1.2
    def __init__(self, name, voyage):
        self.name = name
        self.voyage = voyage
        self.evt_seq, self.target_evt_id, self.evt_end = [], -1, False
        self.start_time, self.start_px, self.start_py = None, None, None
        self.end_time, self.end_px, self.end_py = None, None, None
        self.ar_time, self.dp_time, self.anchored_px, self.anchored_py = None, None, None, None
        self.px, self.py = None, None
        self.holding_containers = {}
        self.isVisible = False
        self.bay_pos_info, self.stack_pos_info = {}, {} 
        self.margin_px, self.margin_py = container_hs * 1.2, container_vs * 2
        self.drawing_bays_px = []
        for bay_id in range(Vessel.num_of_bay, 0, -1):
            if bay_id % 4 == 0: px = False
            elif bay_id % 4 == 1: px = self.margin_px + container_hs / 4 * 3 + container_hs * Vessel.btn_bay * ((Vessel.num_of_bay - bay_id) // 4)
            elif bay_id % 4 == 2:
                px = self.margin_px + container_hs / 2 + container_hs * Vessel.btn_bay * ((Vessel.num_of_bay - bay_id) // 4)
                self.drawing_bays_px.append(px)
            elif bay_id % 4 == 3: px = self.margin_px + container_hs / 4 + container_hs * Vessel.btn_bay * ((Vessel.num_of_bay - bay_id) // 4)
            else: assert False
            self.bay_pos_info[bay_id] = px
             
        for x in xrange(self.num_of_stack):
            self.stack_pos_info[x + 1] = x * container_vs + container_vs / 2 + self.margin_py
        
        self.v_d_p = [(0, Vessel.Beam * 0.15),
                      (Vessel.LOA * 0.05, Vessel.Beam * 0.05),
                      (Vessel.LOA * 0.1, 0),
                      (Vessel.LOA * 0.75, 0),
                      (Vessel.LOA * 0.90, Vessel.Beam * 0.02),
                      (Vessel.LOA * 0.95, Vessel.Beam * 0.1),
                      (Vessel.LOA * 0.97, Vessel.Beam * 0.2),
                      (Vessel.LOA, Vessel.Beam * 0.5),
                      (Vessel.LOA * 0.97, Vessel.Beam * 0.8),
                      (Vessel.LOA * 0.95, Vessel.Beam * 0.9),
                      (Vessel.LOA * 0.90, Vessel.Beam * 0.98),
                      (Vessel.LOA * 0.75, Vessel.Beam),
                      (Vessel.LOA * 0.1, Vessel.Beam),
                      (Vessel.LOA * 0.05, Vessel.Beam * 0.95),
                      (0, Vessel.Beam * 0.85),
                      (0, Vessel.Beam * 0.15)]
        mg = 2
        self.hatch = [(self.margin_px - mg, self.margin_py - mg),
                      (self.drawing_bays_px[-1] + container_hs / 2 + mg, self.margin_py - mg),
                      (self.drawing_bays_px[-1] + container_hs / 2 + mg, Vessel.Beam - self.margin_py + mg),
                      (self.margin_px - mg, Vessel.Beam - self.margin_py + mg)]
    def __repr__(self):
        return str(self.name + str(self.voyage))
    
    def set_evt_data(self, target_evt_id, simul_clock):
        if self.evt_end:
            end_evt = self.evt_seq[-1]
            self.end_time = end_evt.dt + timedelta(seconds=15)
            bitt_id = int(end_evt.pos[4:])
            end_evt_px, end_evt_py = Vessel.Bitts[bitt_id].px - Vessel.LOA * 1 / 3, Vessel.Bitts[bitt_id].py - Vessel.Beam * 1.1
            self.end_px, self.end_py = end_evt_px, end_evt_py - container_hs * 2
        else:
            self.set_start_evt_date()    
        self.set_anchor_evt_date()
            
        if self.start_time and simul_clock <= self.start_time:
            self.px, self.py = 0, 0
        elif self.ar_time and self.start_time <= simul_clock < self.ar_time: 
            self.isVisible = True
            self.px = self.start_px
            self.py = self.start_py + calc_proportional_pos(self.start_py, self.anchored_py, self.start_time, self.ar_time, simul_clock)
        elif self.ar_time and self.ar_time <= simul_clock < self.dp_time:
            self.px, self.py = self.anchored_px, self.anchored_py
        elif self.end_time and self.dp_time <= simul_clock < self.end_time:
            self.px = self.anchored_px
            self.py = self.anchored_py + calc_proportional_pos(self.anchored_py, self.end_py, self.dp_time, self.end_time, simul_clock) 
        elif self.end_time and self.end_time <= simul_clock:
            self.isVisible = False
            self.px, self.py = 0, 0
        else:
            assert False
    
    def update_pos(self, simul_clock):
        if self.start_time <= simul_clock < self.ar_time:
            self.isVisible = True
            self.px = self.start_px
            self.py = self.start_py + calc_proportional_pos(self.start_py, self.anchored_py, self.start_time, self.ar_time, simul_clock)
        elif self.ar_time <= simul_clock < self.dp_time:
            self.px, self.py = self.anchored_px, self.anchored_py
        elif self.dp_time <= simul_clock < self.end_time:
            self.px = self.anchored_px
            self.py = self.anchored_py + calc_proportional_pos(self.anchored_py, self.end_py, self.dp_time, self.end_time, simul_clock)
        elif self.end_time:
            self.isVisible = False
            
    def update(self, simul_clock):
        self.update_pos(simul_clock)
        
    def draw(self, gc):
        gc.SetPen(wx.Pen(wx.Colour(65, 51, 128), 2))
        gc.SetBrush(wx.Brush(wx.Colour(45, 189, 45)))
        #draw vessel surface
        if self.isVisible:
#            gc.DrawRectangle(0, 0, Vessel.LOA, Vessel.Beam)
            gc.DrawLines(self.v_d_p)
            gc.SetPen(wx.Pen(wx.Colour(150, 150, 150), 0))
            gc.SetBrush(wx.Brush(wx.Colour(150, 150, 150)))
            gc.DrawLines(self.hatch)
            for x, px in enumerate(self.drawing_bays_px):
                gc.SetPen(wx.Pen(wx.Colour(100, 100, 100), 0.5))
                if x != 4:
                    gc.DrawLines([(px - container_hs / 2, self.margin_py), (px - container_hs / 2, self.margin_py + container_vs * Vessel.num_of_stack)])
                    gc.DrawLines([(px + container_hs / 2, self.margin_py), (px + container_hs / 2, self.margin_py + container_vs * Vessel.num_of_stack)])
                    for s in xrange(Vessel.num_of_stack + 1):
                        gc.DrawLines([(px - container_hs / 2, self.margin_py + s * container_vs), (px + container_hs / 2, self.margin_py + s * container_vs)])
                else:
                    change_b_color(gc, 'white')
                    gc.SetPen(wx.Pen(wx.Colour(200, 200, 200), 1))
                    gc.DrawRectangle(px - container_hs / 2, self.margin_py - container_vs * 1, container_hs, container_vs * Vessel.num_of_stack + container_vs * 2)
                    gc.DrawRectangle(px - container_hs / 2 + container_vs / 2, self.margin_py + container_vs * Vessel.num_of_stack / 4, container_hs / 2, container_vs * Vessel.num_of_stack / 2)
#            p1, p2, p3, p4, p5, p6 = (0, Vessel.Beam * 0.25), (20, 0), (Vessel.LOA - 20, 0), (Vessel.LOA - 10, Vessel.Beam * 0.125), (Vessel.LOA - 5, Vessel.Beam * 0.2), (Vessel.LOA, Vessel.Beam * 0.35)
#            p7, p8, p9 = (Vessel.LOA, Vessel.Beam * 0.65), (Vessel.LOA - 5, Vessel.Beam * 0.8), (Vessel.LOA - 10, Vessel.Beam * 0.875)
#            p10 = (Vessel.LOA - 20, Vessel.Beam-10)
#            gc.DrawLines([p1, p2, p3, p4, p5 , p6
#                          , p7, p8, p9, p10])
##                          , , (20, Vessel.Beam), (0, Vessel.Beam * 0.75), (0, Vessel.Beam * 0.25)])
#            gc.DrawLines([(10, Vessel.Beam * 0.125), (10, Vessel.Beam * 0.875)]) 
            for c in self.holding_containers.values():
                old_tr = gc.GetTransform()
                gc.Translate(c.px, c.py)
                c.draw(gc)
                gc.SetTransform(old_tr)
            
    def set_start_evt_date(self):
        start_evt = self.evt_seq[0]
        self.start_time = start_evt.dt - timedelta(seconds=15)
        bitt_id = int(start_evt.pos[4:])
        start_evt_px, start_evt_py = Vessel.Bitts[bitt_id].px - Vessel.LOA * 1 / 3, Vessel.Bitts[bitt_id].py - Vessel.Beam * 1.1
        self.start_px, self.start_py = start_evt_px, start_evt_py - container_hs * 2
    
    def set_anchor_evt_date(self):
        self.ar_time = self.evt_seq[0].dt
        self.dp_time = self.evt_seq[1].dt
        bitt_id = int(self.evt_seq[0].pos[4:])
        self.anchored_px, self.anchored_py = Vessel.Bitts[bitt_id].px - Vessel.LOA * 1 / 3, Vessel.Bitts[bitt_id].py - Vessel.Beam * 1.1

class Drag_zoom_panel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, -1, pos, size, style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour(wx.WHITE)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        # size and mouse events
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
        self.translate_mode = False
        self.translate_x, self.translate_y = 0, 0
        self.scale = 1.0
#        self.InitBuffer()
        
    def OnSize(self, evt):
        self.InitBuffer()
        evt.Skip()
        
    def OnLeftDown(self, evt):
        self.translate_mode = True
        self.prev_x, self.prev_y = evt.m_x, evt.m_y
        self.CaptureMouse()
        evt.Skip()
        
    def OnMotion(self, evt):
        if self.translate_mode:
            dx, dy = evt.m_x - self.prev_x, evt.m_y - self.prev_y
            self.translate_x += dx
            self.translate_y += dy
            self.prev_x, self.prev_y = evt.m_x, evt.m_y
            self.RefreshGC()
    
    def OnLeftUp(self, evt):
        if self.translate_mode:
            self.translate_mode = False
            self.ReleaseMouse()
            
    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self, self._buffer)
        
    def OnMouseWheel(self, evt):
        zoom_scale = 1.2
        old_scale = self.scale 
        if evt.m_wheelRotation > 0:
            self.scale *= zoom_scale
            self.translate_x = evt.m_x - self.scale / old_scale * (evt.m_x - self.translate_x)
            self.translate_y = evt.m_y - self.scale / old_scale * (evt.m_y - self.translate_y) 
        else:
            self.scale /= zoom_scale
            self.translate_x = evt.m_x - self.scale / old_scale * (evt.m_x - self.translate_x)
            self.translate_y = evt.m_y - self.scale / old_scale * (evt.m_y - self.translate_y)
        self.RefreshGC()
        
    def InitBuffer(self):
        sz = self.GetClientSize()
        sz.width = max(1, sz.width)
        sz.height = max(1, sz.height)
        self._buffer = wx.EmptyBitmap(sz.width, sz.height, 32)
        dc = wx.MemoryDC(self._buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)
        self.Draw(gc)
        
    def RefreshGC(self):
        dc = wx.MemoryDC(self._buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)
        self.Draw(gc)
        self.Refresh(False)
    
    def Draw(self, gc):
        pass
