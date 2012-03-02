from __future__ import division
from datetime import datetime
from parameter_function import container_hs, container_vs, change_b_color
from random import seed, randrange
import wx
seed(10)
class Container(object):
    def __init__(self, c_id):
        self.c_id = c_id
        self.evt_seq, self.cur_evt_id = [], 0
        self.size = None
        self.hs, self.vs = None, None
        self.px, self.py = None, None
        self.evt_end = False
        self.color = randrange(4)
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
        change_b_color(gc, 'black')
        gc.SetPen(wx.Pen('black', 0))
        gc.DrawRectangle(0, 0, Bitt.sx, Bitt.sy)
    
class Evt(object):
    def __init__(self, dt_txt, vehicle, work_type, c_id, operation, v_info, state, pos=None):
        year, month, day, hour, minute, second = dt_txt.split('-') 
        self.dt = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        self.vehicle, self.work_type, self.c_id, self.operation, self.v_info, self.state, self.pos = vehicle, work_type, c_id, operation, v_info, state, pos
    def __repr__(self):
        return str(self.dt) + '_' + self.vehicle + '_' + self.work_type + '_' + self.c_id + '_' + self.operation + '_' + self.v_info + '_' + self.state + '_' + str(self.pos)

class Drag_zoom_panel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, -1, pos, size, style=wx.SIMPLE_BORDER)
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
