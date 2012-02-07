from __future__ import division

#from datetime import datetime, timedelta
#from parameter_function import container_hs, container_vs, frame_milsec

import wx, time


frame = 15.0


class Vehicles(object):
    def __init__(self, id):
        self.id = id
        self.evt_seq = []
        self.px, self.py = None, None
        self.dest_px, self.dest_py = None, None
        self.moving_speed = None
        
    def set_position(self, px, py):
        self.px, self.py = px, py
        
    def set_dest_position(self, px, py):
        self.dest_px, self.dest_py = px, py
        
class SC(Vehicles):
    def __init__(self, id):
        Vehicles.__init__(self, id)
        self.direction = None
#        self.isVisualize = False
        
    def __repr__(self):
        return 'SC' + str(self.id) + self.evt_seq  
    
    def cur_evt_init(self):
        self.cur_evt = self.evt_seq[0]
        self.next_evt = self.evt_seq[1]
        self.moving_speed = self.calc_moving_speed()
        self.direction = 'EAST'
        ce_time, ce_pos, ce_state = self.cur_evt
        self.px, self.py = ce_pos
        ne_time, ne_pos, ne_state = self.next_evt
        self.dest_px, self.dest_py = ne_pos

    def draw(self, gc):
        gc.DrawRectangle(0, 0, 10, 10)
#        st = 'SC' + str(self.id)
#        gc.DrawText(st, -5, -5)
    
    def OnTimer(self, evt, simul_time):
        ce_time, ce_pos, ce_state = self.cur_evt
        ne_time, ne_pos, ne_state = self.next_evt
        if ce_time < simul_time < ne_time:
            self.px += self.moving_speed
            if  self.px >= self.dest_px:
                self.px = self.dest_px
                self.py += self.moving_speed
    
    def calc_moving_speed(self):
        ce_time, ce_pos, ce_state = self.cur_evt
        ce_px, ce_py = ce_pos
        ne_time, ne_pos, ne_state = self.next_evt
        ne_px, ne_py = ne_pos
        travel_dist = abs(ce_px - ne_px) + abs(ce_py - ne_py)
        
        travel_time = ne_time - ce_time
        print travel_dist, travel_time, travel_dist / travel_time / frame 
        return (travel_dist / travel_time) / frame# +0.03
     
        
#        v1.evt_seq = [(3, (100, 200), 'AR',), (10, (100, 200), 'DP')]
    
class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'test', size=(1024, 768))
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
        self.cur_time = 0
        self.saved_time = time.localtime(time.time())
        self.vessels, self.qcs, self.ycs, self.scs = self.make_vehicle()
    
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
        saved_sec = self.saved_time[5]
        cur_sec = time.localtime(time.time())[5]
        
        for v in self.vessels, self.qcs, self.ycs, self.scs:
            for x in v:
                x.OnTimer(evt, self.cur_time)
                
        if abs(saved_sec - cur_sec) >= 1 :
            self.cur_time += 1
            self.saved_time = time.localtime(time.time())
        
            
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
        brushclr = wx.Colour(255, 255, 255)
        gc.SetBrush(wx.Brush(brushclr))
#        gc.DrawText(str(self.cur_time), 800, 600)
        gc.DrawText(str(self.cur_time), 100, 100)
        gc.DrawRectangle(100, 200, 10, 10)
        gc.DrawRectangle(120, 220, 10, 10)
        old_tr = gc.GetTransform()
        for v in self.vessels, self.qcs, self.ycs, self.scs:
            for x in v:
                gc.Translate(x.px, x.py)
                x.draw(gc)
                gc.SetTransform(old_tr)
    
    def make_vehicle(self):
        vessels = []
        qcs = []
        ycs = []
        scs = []
        
        sc1 = SC(1)
        sc1.evt_seq = [(2.0, (100.0, 200.0), 'go',), (20.0, (120.0, 220.0), 'stop')]
        sc1.cur_evt_init()
        scs.append(sc1)
        
#        v2 = SC(2)
#        v2.evt_seq = [(0, (100, 500), 'AR',), (10, (100, 500), 'DP')]
#        vessels.append(v2)
        
#        q1 = QC()
        return (vessels, qcs, ycs, scs)
if __name__ == '__main__':
    app = wx.PySimpleApp()
    app.frame = MainFrame()
    app.MainLoop()
#    v = Vessel(1)
#    print v.px, v.py 
