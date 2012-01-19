from __future__ import division
#from initisalizer import run 
import wx, time

class Node:
    def __init__(self, id):
        self.id = id
        self.x = 20
        self.y = 20

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'test', size=(1024, 768))
        sw = wx.SplitterWindow(self, -1, size =(1024,768))
        sty = wx.BORDER_STATIC 
    
        ip_win = wx.Window(sw, style = wx.BORDER_NONE )
        ip_win.SetBackgroundColour("pink")
        wx.StaticText(ip_win, -1, "input_win", (5,5))
    
        p2 = wx.Window(sw, style = sty)
#        p2.SetBackgroundColour("sky blue")
#        wx.StaticText(p2, -1, "Panel Two", (5,5))

        sw.SetMinimumPaneSize(20)
        sw.SplitHorizontally(ip_win, p2, 50)
        
        sw2 = wx.SplitterWindow(p2, -1, size = (100,100))
        
        p3 = wx.Window(sw2)
        p3.SetBackgroundColour("pink")
        wx.StaticText(p3, -1, "Panel One", (5,5))
    
        p4 = wx.Window(sw2)
        
        sw2.SetMinimumPaneSize(20)
        sw2.SplitVertically(p3, p4, -100)
        
#        f_sx, f_sy = self.GetSize()
#        ip_py, ip_sy = 0 , 50
#        vp_py, vp_sy = ip_py + ip_sy , 600
#        cp_py, cp_sy = vp_py + vp_sy , f_sy - (vp_sy + ip_sy) 
#        
#        Input_Panel(self , (0, ip_py), (f_sx, ip_sy))
#        bvp = wx.Panel(self, -1, (0, vp_py), (f_sx, vp_sy))
#        Viewer_Panel(bvp, (45, 8), (f_sx - 100, vp_sy - 20))
#        Control_Panel(self, (0, cp_py), (f_sx, cp_sy))
        
        self.Show(True)

class Input_Panel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, -1, pos, size)
        self.SetBackgroundColour(wx.Colour(255, 0, 0))
        wx.StaticText(self, -1, 'Vessel', (15, 10))
        
        v_name = ['HANJIN', 'MAERSK']
        self.sc_ch = wx.Choice(self, -1, (100, 10), choices=v_name)
        
        self.input_sh = wx.TextCtrl(self, -1, '00', pos=(200, 10))
        
        b = wx.Button(self, -1, "setting", (300, 10))
        
class Viewer_Panel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, -1, pos, size)
        self.SetBackgroundColour(wx.WHITE)
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
        self.timer.Start(1000)
        self.n = Node(0);
        
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
        self.n.x += 1
        self.RefreshGC()
            
    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self, self._buffer)
        
    def OnMouseWheel(self, evt):
        # TODO scaling based on mouse position (evt.m_x, evt.m_y)
        zoom_scale = 1.2
        old_scale = self.scale 
        if evt.m_wheelRotation > 0:
            self.scale *= zoom_scale
            self.translate_x = evt.m_x - self.scale/old_scale *(evt.m_x - self.translate_x)
            self.translate_y = evt.m_y - self.scale/old_scale *(evt.m_y - self.translate_y) 
            
#            self.translate_x -= evt.m_x * (zoom_scale - 1)
#            self.translate_y -= evt.m_y * (zoom_scale - 1)
        else:
            self.scale /= zoom_scale
            self.translate_x = evt.m_x - self.scale/old_scale *(evt.m_x - self.translate_x)
            self.translate_y = evt.m_y - self.scale/old_scale *(evt.m_y - self.translate_y)
#            self.translate_x += evt.m_x * (zoom_scale - 1)
#            self.translate_y += evt.m_y * (zoom_scale - 1)
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
        
        t = time.localtime(time.time())
        st = time.strftime("%I:%M:%S", t)
#        gc.Clear()
        gc.SetFont(wx.Font(30, wx.SWISS, wx.NORMAL, wx.NORMAL))
        gc.DrawText(st, 10, 150)
        
        gc.SetPen(wx.Pen("black", 1))
#        gc.DrawRectangle(10,10,100,100)
        r, g, b = (255, 0, 0)
        brushclr = wx.Colour(r, g, b, 100)
        gc.SetBrush(wx.Brush(brushclr))
        gc.DrawRectangle(self.n.x, self.n.y, 100, 100)
        
        
        

class Control_Panel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, -1, pos, size)
#        self.SetBackgroundColour(wx.Colour(0, 0, 255))
        
        slider = wx.Slider(self, -1, 1, 12.5, 100, (30, 10), (250, -1), wx.SL_HORIZONTAL)
        
        s_b = wx.Button(self, -1, "stop", (300, 10))
        pu_b = wx.Button(self, -1, "stop", (350, 10))
        r_b = wx.Button(self, -1, "reverse", (400, 10))
        pl_b = wx.Button(self, -1, "play", (450, 10))
        
#        slider.Bind(wx.EVT_SCROLL_CHANGED, self.onChanged)

#    def onChanged(self, evt):
#        self.log.write('changed: %d' % evt.EventObject.GetValue())
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    app.frame = MainFrame()
    app.MainLoop()
#    run()
