from __future__ import division
import wx, time
import  wx.lib.anchors as anchors

class Node:
    def __init__(self, id):
        self.id = id
        self.x = 20
        self.y = 20

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'test', size=(1024, 768))
        f_sx, f_sy = self.GetSize()
        self.SetBackgroundColour(wx.Colour(236, 233, 216))
        self.SetAutoLayout(True)

        ip_py, ip_sy = 0 , 50
        vp_py, vp_sy = ip_py + ip_sy , 600
        cp_py, cp_sy = vp_py + vp_sy , f_sy - (vp_sy + ip_sy)
        
        Input_Panel(self , (0, ip_py), (f_sx, ip_sy))
        Viewer_Panel(self, (45, vp_py), (f_sx - 100, vp_sy))
        Control_Panel(self, (0, cp_py), (f_sx, cp_sy))

        self.Show(True)
        

class Input_Panel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, -1, pos, size)
        self.SetConstraints(anchors.LayoutAnchors(self, True, True, True, False))
#        self.SetBackgroundColour(wx.Colour(255, 0, 0))


#======================Input=======================================
#        wx.StaticText(self, -1, 'Vessel', (15, 10))
#        wx.StaticText(self, -1, 'Voyage', (150, 10))
#        wx.StaticText(self, -1, 'Date', (360, 10))
#        
#        v_name = ['HANJIN', 'MAERSK']
#        self.sc_ch = wx.Choice(self, -1, (60, 10), choices=v_name)
#        
#        vo_name = ['01', '02', '03', '04', '05', '06', '07']
#        self.sc_ch = wx.Choice(self, -1, (200, 10), choices=vo_name)
#        
#        y_name1 = ['2005', '2006', '2007', '2008', '2009', '2010', '2011']
#        self.sc_ch = wx.Choice(self, -1, (390, 10), choices=y_name1)
#        
#        m_name1 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
#        self.sc_ch = wx.Choice(self, -1, (450, 10), choices=m_name1)
#        
#        d_name1 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
#        self.sc_ch = wx.Choice(self, -1, (495, 10), choices=d_name1)
#        
#        wx.TextCtrl(self, -1, "00", (540, 10), size=(25, -1))
#        wx.StaticText(self, -1, ':', (566, 10))
#        wx.TextCtrl(self, -1, "00", (570, 10), size=(25, -1))
#        wx.StaticText(self, -1, ':', (596, 10))
#        wx.TextCtrl(self, -1, "00", (600, 10), size=(25, -1))
#        
#        wx.StaticText(self, -1, '-', (635, 10))
#    
#        y_name2 = ['2005', '2006', '2007', '2008', '2009', '2010', '2011']
#        self.sc_ch = wx.Choice(self, -1, (650, 10), choices=y_name2)
#        
#        m_name2 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
#        self.sc_ch = wx.Choice(self, -1, (710, 10), choices=m_name2)
#        
#        d_name2 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
#        self.sc_ch = wx.Choice(self, -1, (755, 10), choices=d_name2)
#        
#        wx.TextCtrl(self, -1, "00", (800, 10), size=(25, -1))
#        wx.StaticText(self, -1, ':', (826, 10))
#        wx.TextCtrl(self, -1, "00", (830, 10), size=(25, -1))
#        wx.StaticText(self, -1, ':', (856, 10))
#        wx.TextCtrl(self, -1, "00", (860, 10), size=(25, -1))
#        
# #        self.input_sh = wx.TextCtrl(self, -1, '00', pos=(200, 10))
# #        
#        b = wx.Button(self, -1, "setting", (900, 10))
#===============================================================================
        
        v = wx.StaticText(self, -1, 'Vessel', (15, 10))
        v.SetConstraints(anchors.LayoutAnchors(v, False, True, False, False))
        
        vo = wx.StaticText(self, -1, 'Voyage', (150, 10))
        vo.SetConstraints(anchors.LayoutAnchors(vo, False, True, False, False))
        
        d = wx.StaticText(self, -1, 'Date', (360, 10))
        d.SetConstraints(anchors.LayoutAnchors(d, False, True, False, False))
        
        v_name = wx.StaticText(self, -1, "HANJIN", (60, 10), size=(65, -1))
        
        vo_name = wx.StaticText(self, -1, "01", (200, 10), size=(25, -1))
                
        y_name1 = wx.StaticText(self, -1, "2011", (390, 10), size=(40, -1))
        m_name1 = wx.StaticText(self, -1, "11", (450, 10), size=(25, -1))
        d_name1 = wx.StaticText(self, -1, "07", (495, 10), size=(25, -1))
        
        
        wx.StaticText(self, -1, "00", (540, 10), size=(25, -1))
        wx.StaticText(self, -1, ':', (564, 10))
        wx.StaticText(self, -1, "00", (570, 10), size=(25, -1))
        wx.StaticText(self, -1, ':', (594, 10))
        wx.StaticText(self, -1, "00", (600, 10), size=(25, -1))
        
        wx.StaticText(self, -1, '-', (635, 10))
    
        y_name2 = wx.StaticText(self, -1, "2011", (650, 10), size=(40, -1))
        m_name2 = wx.StaticText(self, -1, "11", (710, 10), size=(25, -1))
        d_name2 = wx.StaticText(self, -1, "07", (755, 10), size=(25, -1))
        
        
        wx.StaticText(self, -1, "00", (800, 10), size=(25, -1))
        wx.StaticText(self, -1, ':', (824, 10))
        wx.StaticText(self, -1, "00", (830, 10), size=(25, -1))
        wx.StaticText(self, -1, ':', (854, 10))
        wx.StaticText(self, -1, "00", (860, 10), size=(25, -1))
        
 #        self.input_sh = wx.TextCtrl(self, -1, '00', pos=(200, 10))
 #        
        b = wx.Button(self, -1, "setting", (900, 10))
class Viewer_Panel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, -1, pos, size, style=wx.SIMPLE_BORDER)
        self.SetConstraints(anchors.LayoutAnchors(self, True, True, True, True))
        self.SetBackgroundColour(wx.WHITE)
        self.SetBackgroundColour(wx.WHITE)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        # size and mouse events
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
        
#        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        
        self.translate_mode = False
        self.translate_x, self.translate_y = 0, 0
        self.scale = 1.0
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(1000)
        self.n = Node(0);
        
        self.InitBuffer()
        
#    def OnKeyDown(self, evt):
#        print 11
        
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
    
    def OnTimer(self, evt):
        self.n.x += 1
        self.RefreshGC()
            
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
        self.SetConstraints(anchors.LayoutAnchors(self, True, False, True, True))
#        self.SetBackgroundColour(wx.Colour(0, 0, 255))
        self.time_flow = wx.Slider(self, -1, 1, 12.5, 100, (30, 10), (250, -1), wx.SL_HORIZONTAL)
        self.diplay_time()

        s_img = wx.Image('pic/stop.bmp', wx.BITMAP_TYPE_BMP)
        s_bmp = s_img.Scale(20,20)
        s_button = wx.BitmapButton(self, -1, wx.BitmapFromImage(s_bmp), (300, 10), (s_bmp.GetWidth() + 2, s_bmp.GetHeight() + 2))
        self.Bind(wx.EVT_BUTTON, self.test, s_button)
        
        r_img = wx.Bitmap("pic/reverse.bmp", wx.BITMAP_TYPE_BMP)
        r_bmp = r_img.Scale(20,20)
        r_button = wx.BitmapButton(self, -1, wx.BitmapFromImage(r_bmp), (350, 10),(r_bmp.GetWidth()+2, r_bmp.GetHeight()+2))
        
        pa_img = wx.Bitmap("pic/pause.bmp", wx.BITMAP_TYPE_BMP)
        pa_bmp = pa_img.Scale(20,20)
        pa_button = wx.BitmapButton(self, -1, wx.BitmapFromImage(pa_bmp), (350, 10),(pa_bmp.GetWidth()+2, pa_bmp.GetHeight()+2))
        
        pl_img = wx.Bitmap("pic/play.bmp", wx.BITMAP_TYPE_BMP)
        pl_bmp = pl_img.Scale(20,20)
        pl_button = wx.BitmapButton(self, -1, wx.BitmapFromImage(pl_bmp), (350, 10),(pl_bmp.GetWidth()+2, pl_bmp.GetHeight()+2))
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(1000)
        
    def test(self, e):
        print 1

    def OnTimer(self, evt):
        self.diplay_time()
        self.time_flow.SetValue(self.time_flow.GetValue() + 1)
        
    def diplay_time(self):
        t = time.localtime(time.time())
        st = time.strftime("%I:%M:%S", t)
        self.c_time = wx.StaticText(self, -1, st, (600, 20))
        
        
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    app.frame = MainFrame()
    app.MainLoop()
#    run()
