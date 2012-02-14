from __future__ import division
import wx, time

container_hs = 20
container_vs = 5
frame = 15.0

class Vehicles(object):
    def __init__(self, id):
        self.id = id
        self.evt_seq = []
        self.ce_px, self.ce_py = None, None
        self.px, self.py = None, None
        self.ne_px, self.ne_py = None, None

    def set_position(self, px, py):
        self.px, self.py = px, py
        
    def set_dest_position(self, px, py):
        self.ne_px, self.ne_py = px, py

class YC(Vehicles):
    class Trolly(Vehicles):
        def __init__(self, id):
            Vehicles.__init__(self, id)
            
        def cur_evt_init(self):
            pass
        
        def OnTimer(self, evt, simul_time):
            self.t_px = self.t_ce_px + (self.t_ne_px - self.t_ce_px) * (simul_time - self.t_ce_time) / (self.t_ne_time - self.t_ce_time)
            
        def draw(self, gc):
            tr, tg, tb = (4, 189, 252)
            t_brushclr = wx.Colour(tr, tg, tb, 200)
            ##draw lines
            r, g, b = (0, 0, 0)
            brushclr = wx.Colour(r, g, b, 100)
            gc.SetPen(wx.Pen(brushclr, 1))
            gc.SetBrush(wx.Brush(brushclr))
            gc.DrawLines([(0, -30), (0, 30)])
            gc.DrawLines([(15, -30), (15, 30)])
            
            ##draw trolly         
            gc.SetPen(wx.Pen(t_brushclr, 0))
            gc.SetBrush(wx.Brush(t_brushclr))
            gc.DrawRectangle(0, 0, container_vs * 1.1, 12)
            
            
            
    def __init__(self, id):
        Vehicles.__init__(self, id)
        self.id = id
        self.evt_seq = []
        self.trolly = self.Trolly(1)
        self.trolly.px, self.trolly.py = container_vs, (container_hs * 1.1 * 0.5) - 6

    def __repr__(self):
        return self.id
    
    def cur_evt_init(self):
        self.cur_evt = self.evt_seq[0]
        self.next_evt = self.evt_seq[1]
        ce_time, ce_pos, ce_state = self.cur_evt
        self.ce_px, self.ce_py = ce_pos
        self.px, self.py = self.ce_px, self.ce_py
        self.ce_time = ce_time
        ne_time, ne_pos, ne_state = self.next_evt
        self.ne_px, self.ne_py = ne_pos
        self.ne_time = ne_time
        ##trolly
        self.t_cur_evt=self.evt_seq[2]
        self.t_next_evt=self.evt_seq[3]
        t_ce_time, t_ce_pos, t_ce_state = self.t_cur_evt
        self.t_ce_px, self.t_ce_py = t_ce_pos
        self.t_px, self.t_py = self.t_ce_px, self.t_ce_py
        self.t_ce_time = t_ce_time
        t_ne_time, t_ne_pos, t_ne_state = self.t_next_evt
        self.t_ne_px, self.t_ne_py = t_ne_pos
        self.t_ne_time = t_ne_time
        
    def OnTimer(self, evt, simul_time):
        if self.ce_time < simul_time < self.ne_time: 
            self.py = self.ce_py + (self.ne_py - self.ce_py) * (simul_time - self.ce_time) / (self.ne_time - self.ce_time)
        
        elif self.t_ce_time < simul_time < self.t_ne_time:
            self.trolly.OnTimer(evt, simul_time)
        
    
    def draw(self, gc):
        yr, yg, yb = (90, 14, 160)
        y_brushclr = wx.Colour(yr, yg, yb, 200)
        gc.SetPen(wx.Pen(y_brushclr, 0))
        gc.SetBrush(wx.Brush(y_brushclr))
        
        gc.DrawRectangle(-container_vs, 0, container_vs * 1.1, container_hs * 1.1)
        gc.DrawRectangle(container_vs * 9 - (container_vs * 1.1), 0, container_vs * 1.1, container_hs * 1.1)
        gc.DrawRectangle(container_vs * 0.1, (container_hs * 1.1 * 0.5) - 6, container_vs * 7.8, 3)
        gc.DrawRectangle(container_vs * 0.1, (container_hs * 1.1 * 0.5) + 3, container_vs * 7.8, 3)
        old_tr = gc.GetTransform()
        gc.Translate(self.trolly.px, self.trolly.py)
        self.trolly.draw(gc)
        gc.SetTransform(old_tr)

class SC(Vehicles):
    def __init__(self, id):
        Vehicles.__init__(self, id)
        self.direction = None
        
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
        brushclr = wx.Colour(255, 255, 255)
        gc.SetBrush(wx.Brush(brushclr))
        gc.DrawRectangle(0, 0, 10, 10)
    
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
        
        self.simul_clock = 0
        self.saved_time = time.time()
        
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
        cur_time = time.time()
        for v in self.vessels, self.qcs, self.ycs, self.scs:
            for x in v:
                x.OnTimer(evt, self.simul_clock)
        #        if abs(saved_sec - cur_sec) >= 1 :
        self.simul_clock += abs(cur_time - self.saved_time) * 0.8
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
        
        gc.DrawText(str(self.simul_clock), 100, 100)
        gc.DrawRectangle(100, 200, 10, 10)
        gc.DrawRectangle(120, 220, 10, 10)
        
        ##Lines
        r, g, b = (0, 0, 0)
        brushclr = wx.Colour(r, g, b, 100)
        gc.SetPen(wx.Pen(brushclr, 1))
        gc.SetBrush(wx.Brush(brushclr))
        
        gc.DrawLines([(200.0, 200.0), (400.0, 200.0)])
        gc.DrawLines([(200.0, 220.0), (400.0, 220.0)])
        
        
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
        #spreader moving
        #trolly moving
        yc1 = YC(1)
        yc1.evt_seq = [(1.0, (300.0, 200.0), 'S_go',), (10.0, (300.0, 220.0), 'S_stop'),
                       (11.0, (0.0, 0.0), 'T_go',), (13.0, (15.0, 0.0), 'T_stop'),
                       (14.0, (300.0, 220.0), 'S_go',), (17.0, (300.0, 200.0), 'S_stop')
                       ]
        yc1.cur_evt_init()
        ycs.append(yc1)
        return (vessels, qcs, ycs, scs)
    
if __name__ == '__main__':
    app = wx.PySimpleApp()
    app.frame = MainFrame()
    app.MainLoop()
