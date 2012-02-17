from __future__ import division
import wx, time
from datetime import datetime, timedelta
import math
container_hs = 20
container_vs = 5
frame = 15.0

containers = {}
TPs = {}
QBs = {}
SCs = {}

class Container(object):
    def __init__(self, id):
        self.id = id
        self.moving_seq = []
        self.cur_index_in_ms = 0
        
        self.hs, self.vs = container_hs , container_vs
        self.size = '40ft'
        
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

    def draw(self, gc):
        r, g, b = (0, 0, 0)
        penclr = wx.Colour(r, g, b)
        r, g, b = (255, 255, 255)
        bruclr = wx.Colour(r, g, b, 200)
        gc.SetPen(wx.Pen(penclr, 1))
        gc.SetBrush(wx.Brush(bruclr))
        gc.DrawRectangle(0, 0, container_vs * 4, container_hs)
        
class QC_buffer(Storage):
    def __init__(self, id):
        Storage.__init__(self, id)
        self.name = 'QC Buffer'
    
    def draw(self, gc):
        r, g, b = (0, 0, 0)
        penclr = wx.Colour(r, g, b)
        r, g, b = (255, 255, 255)
        bruclr = wx.Colour(r, g, b, 200)
        gc.SetPen(wx.Pen(penclr, 1))
        gc.SetBrush(wx.Brush(bruclr))
        gc.DrawRectangle(0, 0, container_vs * 10, container_hs)
        
        if self.holding_containers:
            r, g, b = 228, 108, 10
            bruclr = wx.Colour(r, g, b, 200)
            gc.SetBrush(wx.Brush(bruclr))
            gc.DrawRectangle(0, 0, container_hs, container_vs)

class Vehicles(object):
    def __init__(self, id):
        self.id = id
        self.name = None
        self.evt_seq = []
        self.cur_evt_id = 0
        self.holding_contaners = []
        
        self.ce_px, self.ce_py = None, None
        self.px, self.py = None, None
        self.ne_px, self.ne_py = None, None

    def set_position(self, px, py):
        self.px, self.py = px, py
        
    def set_dest_position(self, px, py):
        self.ne_px, self.ne_py = px, py

class SC(Vehicles):
    def __init__(self, id):
        Vehicles.__init__(self, id)
        self.name = 'SC'
        
    def __repr__(self):
        return self.name + str(self.id)

    def cur_evt_update(self, cur_evt_id):
        if len(self.evt_seq) <= 1: assert False, 'length of evt_seq is smaller than 2' 
        self.cur_evt = self.evt_seq[cur_evt_id]
        self.next_evt = self.evt_seq[cur_evt_id + 1]
        
        global containers
        ce_time, ce_pos, ce_container, self.ce_state = self.cur_evt
        year, month, day, hour, minute, second = tuple(ce_time.split('-'))
        self.ce_time = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        if ce_pos[:2] == 'QB':
            self.ce_px, self.ce_py = QBs[int(ce_pos[2:])].px, QBs[int(ce_pos[2:])].py 
        elif ce_pos[:2] == 'TP':
            self.ce_px, self.ce_py = TPs[int(ce_pos[2:])].px, TPs[int(ce_pos[2:])].py
        else:
            assert False
#        self.ce_c = containers[int(ce_container[1:])]
        
        ne_time, ne_pos, ne_container, self.ne_state = self.next_evt
        year, month, day, hour, minute, second = tuple(ne_time.split('-'))
        self.ne_time = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        if ne_pos[:2] == 'QB':
            self.ne_px, self.ne_py = QBs[int(ne_pos[2:])].px, QBs[int(ne_pos[2:])].py 
        elif ne_pos[:2] == 'TP':
            self.ne_px, self.ne_py = TPs[int(ne_pos[2:])].px, TPs[int(ne_pos[2:])].py
        else:
            assert False
    def OnTimer(self, evt, simul_time):
        if self.ce_time < simul_time < self.ne_time:
            self.px = self.ce_px + (self.ne_px - self.ce_px) * (simul_time - self.ce_time).seconds / (self.ne_time - self.ce_time).seconds
            self.py = self.ce_py
        
        if self.ne_time <= simul_time:
            self.cur_evt_id += 1
            self.cur_evt_update(self.cur_evt_id)
        
    def draw(self, gc):
        gc.Rotate(math.pi)
        gc.DrawRectangle(0, 0, container_hs, container_vs)
    
class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'test', size=(800, 600))
        MyPanel(self)
        self.Show(True)

class MyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
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
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(1000 / frame)
        
        self.simul_clock = datetime(2011, 8, 23, 10, 9, 50)
        self.saved_time = time.time()
        
        self.containers = self.make_container()
        self.tps, self.qbs = self.make_storage()
        self.vessels, self.qcs, self.ycs, self.scs = self.make_vehicle()
        
    def make_container(self):
        c1 = Container(2)
        c2 = Container(7)
        
        global containers
        for c in [c1, c2]:
            containers[c.id] = c
    
    def make_storage(self):
        qb1 = QC_buffer(1)
        qb1.px, qb1.py = 300, 200
        qb2 = QC_buffer(2)
        qb2.px, qb2.py = 300, 250
        
        global containers, TPs, QBs
        qb1.holding_containers = [containers[2]]
        qb2.holding_containers = [containers[7]]
        
        QBs[qb1.id] = qb1
        QBs[qb2.id] = qb2
        
        tp = TP(1)
        tp.px, tp.py = 100, 350
        
        TPs[tp.id] = tp
        
        return ([tp], [qb1, qb2])

    def make_vehicle(self):
        vessels = []
        qcs = []
        ycs = []
        scs = []
        #SC
        sc1 = SC(2)
        sc1.evt_seq = [('2011-08-23-10-09-50', 'QB01', 'C02', 'TL'),
                       ('2011-08-23-10-10-30', 'TP01', 'C02', 'TU'),
                       ('2011-08-23-10-37-00', 'QB02', 'C07', 'TL'),
                       ('2011-08-23-10-38-40', 'TP01', 'C07', 'TU')
                       ]
        sc1.cur_evt_update(sc1.cur_evt_id)
        scs.append(sc1)
        
        return (vessels, qcs, ycs, scs)
    
    def OnSize(self, evt):
        self.InitBuffer()
        evt.Skip()
        
    def OnLeftDown(self, evt):
        self.translate_mode = True
        self.prev_x, self.prev_y = evt.m_x, evt.m_y
        self.CaptureMouse()
        
    def OnMotion(self, evt):
        if self.translate_mode:
            dx, dy = evt.m_x - self.prev_x, evt.m_y - self.prev_y
            self.translate_x += dx
            self.translate_y += dy
            self.prev_x, self.prev_y = evt.m_x, evt.m_y
            self.RefreshGC()
    
    def OnLeftUp(self, evt):
        self.translate_mode = False
        self.ReleaseMouse()
    
    def OnTimer(self, evt):
        cur_time = time.time()
        
        for v in self.vessels, self.qcs, self.ycs, self.scs:
            for x in v:
                x.OnTimer(evt, self.simul_clock)
        self.simul_clock += timedelta(seconds=cur_time - self.saved_time)
        
        self.saved_time = cur_time
        self.RefreshGC()
            
    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self, self._buffer)
        
    def OnMouseWheel(self, evt):
        # TODO scaling based on mouse position (evt.m_x, evt.m_y)
        zoom_scale = 1.2
        if evt.m_wheelRotation > 0:
            self.scale *= zoom_scale
            self.translate_x -= evt.m_x * (zoom_scale - 1)
            self.translate_y -= evt.m_y * (zoom_scale - 1)
        else:
            self.scale /= zoom_scale
            self.translate_x += evt.m_x * (zoom_scale - 1)
            self.translate_y += evt.m_y * (zoom_scale - 1)
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
        gc.Translate(self.translate_x, self.translate_y)
        gc.Scale(self.scale, self.scale)
        #show time
        gc.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL))
        gc.SetPen(wx.Pen("black", 1))
        gc.DrawText(self.simul_clock.ctime(), 100, 100)

        old_tr = gc.GetTransform()
        for v in self.tps, self.qbs, self.vessels, self.qcs, self.ycs, self.scs:
            for x in v:
                gc.Translate(x.px, x.py)
                x.draw(gc)
                gc.SetTransform(old_tr)
    
if __name__ == '__main__':
    app = wx.PySimpleApp()
    app.frame = MainFrame()
    app.MainLoop()
