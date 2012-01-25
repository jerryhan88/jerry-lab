from __future__ import division
import wx, time
import  wx.lib.anchors as anchors
from datetime import datetime, timedelta
import initializer

frame_milsec = 1000 / 15
container_sx = 20
container_sy = 5

class Node:
    def __init__(self, id):
        self.id = id
        self.x = 20
        self.y = 20

class Input_dialog(wx.Dialog):
    def __init__(self, parent, name, size=(570, 180), pos=(400, 300)):
        wx.Dialog.__init__(self, None, -1, 'Monitoring Input', pos , size)
        wx.StaticText(self, -1, 'Vessel', (15, 10))
        wx.StaticText(self, -1, 'Voyage', (450, 10))
        wx.StaticText(self, -1, 'Date', (15, 50))
        
        v_name = ['HANJIN', 'MAERSK']
        self.v_name_ch = wx.Choice(self, -1, (60, 10), choices=v_name)
        self.v_name_ch.SetSelection(0)
        
        vo_name = ['01', '02', '03', '04', '05', '06', '07']
        self.vo_name_ch = wx.Choice(self, -1, (510, 10), choices=vo_name)
        self.vo_name_ch.SetSelection(0)
        
        y_name1 = ['2005', '2006', '2007', '2008', '2009', '2010', '2011']
        self.y_name1_ch = wx.Choice(self, -1, (60, 50), choices=y_name1)
        self.y_name1_ch.SetSelection(0)
        
        m_name1 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        self.m_name1_ch = wx.Choice(self, -1, (120, 50), choices=m_name1)
        self.m_name1_ch.SetSelection(0)
        
        d_name1 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
        self.d_name1_ch = wx.Choice(self, -1, (165, 50), choices=d_name1)
        self.d_name1_ch.SetSelection(0)
        
        self.t1 = wx.TextCtrl(self, -1, "00", (210, 50), size=(25, -1))
        wx.StaticText(self, -1, ':', (236, 50))
        self.mi1 = wx.TextCtrl(self, -1, "00", (240, 50), size=(25, -1))
        wx.StaticText(self, -1, ':', (266, 50))
        self.s1 = wx.TextCtrl(self, -1, "00", (270, 50), size=(25, -1))
        
        wx.StaticText(self, -1, '-', (305, 50))
        
        y_name2 = ['2005', '2006', '2007', '2008', '2009', '2010', '2011']
        self.y_name2_ch = wx.Choice(self, -1, (320, 50), choices=y_name2)
        self.y_name2_ch.SetSelection(0)
        
        m_name2 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        self.m_name2_ch = wx.Choice(self, -1, (380, 50), choices=m_name2)
        self.m_name2_ch.SetSelection(0)
        
        d_name2 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
        self.d_name2_ch = wx.Choice(self, -1, (425, 50), choices=d_name2)
        self.d_name2_ch.SetSelection(0)
        
        self.t2 = wx.TextCtrl(self, -1, "00", (470, 50), size=(25, -1))
        wx.StaticText(self, -1, ':', (496, 50))
        self.mi2 = wx.TextCtrl(self, -1, "00", (500, 50), size=(25, -1))
        wx.StaticText(self, -1, ':', (526, 50))
        self.s2 = wx.TextCtrl(self, -1, "00", (530, 50), size=(25, -1))
        setting_btn = wx.Button(self, -1, "setting", (480, 90))
        setting_btn.SetConstraints(anchors.LayoutAnchors(setting_btn, False, True, False, False))
        
        self.Bind(wx.EVT_BUTTON, self.setting, setting_btn)
#        self.Bind(wx.EVT_CHOICE, self.EvtChoice_v, self.v_name_ch)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        print self.v_name_ch.GetSelection()
        print self.vo_name_ch.GetString(self.vo_name_ch.GetSelection())
        
        print  self.v_name_ch.GetString(self.v_name_ch.GetSelection())
        
        self.input = None
        
        self.Show(True)
        
#    def EvtChoice_v(self, event):
#        print self.v_name_ch.GetSelection()
#        print self.v_name_ch.GetString(self.v_name_ch.GetSelection())
        
    def OnClose(self, event):
        self.Destroy()
        
    def setting(self, event):
        self.input_v = self.v_name_ch.GetString(self.v_name_ch.GetSelection())
        self.input_vo = self.vo_name_ch.GetString(self.vo_name_ch.GetSelection())
        self.input_y1 = self.y_name1_ch.GetString(self.y_name1_ch.GetSelection())
        self.input_m1 = self.m_name1_ch.GetString(self.m_name1_ch.GetSelection())
        self.input_d1 = self.d_name1_ch.GetString(self.d_name1_ch.GetSelection())
        self.input_t1 = self.t1.GetValue()
        self.input_mi1 = self.mi1.GetValue()
        self.input_s1 = self.s1.GetValue()
        self.input_y2 = self.y_name2_ch.GetString(self.y_name2_ch.GetSelection())
        self.input_m2 = self.m_name2_ch.GetString(self.m_name2_ch.GetSelection())
        self.input_d2 = self.d_name2_ch.GetString(self.d_name2_ch.GetSelection())
        self.input_t2 = self.t2.GetValue()
        self.input_mi2 = self.mi2.GetValue()
        self.input_s2 = self.s2.GetValue()
        
#        for x in [input_v, input_vo, input_y_name1, input_m_name1, input_d_name1, input_t1, input_m1, input_s1, input_y_name2, input_m_name2, input_d_name2, input_t2, input_m2, input_s2]:
#            self.x = self.vo_name_ch.GetString(self.y_name1_ch.SetSelection())
        
#        self.input = self.input_t2.GetValue()
        win = MainFrame(self)
        win.Show(True)
        self.Show(False)

class MainFrame(wx.Frame):
    def __init__(self, input_info):
        self.input_info = input_info
        
        wx.Frame.__init__(self, None, -1, 'Monitoring', size=(1024, 768))
        f_sx, f_sy = self.GetSize()
        self.SetBackgroundColour(wx.Colour(236, 233, 216))
        self.SetAutoLayout(True)
        ###########
        self.start_time = datetime(2011, 1, 20, 16, 20, 30)
        self.end_time = datetime(2011, 1, 20, 16, 20, 30)
        ###########
        self.evts = initializer.run(self.start_time, self.end_time)
        self.cur_time = datetime(2011, 1, 20, 16, 20, 30)
          
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(frame_milsec)
        
        ip_py, ip_sy = 0 , 50
        vp_py, vp_sy = ip_py + ip_sy , 600
        cp_py, cp_sy = vp_py + vp_sy , f_sy - (vp_sy + ip_sy)
        
        Input_View_Panel(self , (0, ip_py), (f_sx, ip_sy), self.input_info)
        self.vp = Viewer_Panel(self, (45, vp_py), (f_sx - 100, vp_sy), self.evts)
        self.cp = Control_Panel(self, (0, cp_py), (f_sx, cp_sy))
        self.Show(True)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        self.saved_time = time.localtime(time.time())
        self.isReverse_play = False
        
    def OnTimer(self, evt):
        saved_sec = self.saved_time[5]
        cur_sec = time.localtime(time.time())[5]
        if abs(saved_sec - cur_sec) >= 1 :
            if not self.isReverse_play:
                self.cur_time += timedelta(seconds=1)
            else:
                self.cur_time -= timedelta(seconds=1)
            self.saved_time = time.localtime(time.time())
        self.vp.OnTimer(evt)
        self.cp.OnTimer(evt)
        
    def OnClose(self, event):
        self.input_info.Destroy()
        self.Destroy()
        
        
class Input_View_Panel(wx.Panel):
    def __init__(self, parent, pos, size, in_d=None):
#        v_name = input_info.GetValue()
        wx.Panel.__init__(self, parent, -1, pos, size)
        self.SetConstraints(anchors.LayoutAnchors(self, True, True, True, False))
        
        v = wx.StaticText(self, -1, 'Vessel', (15, 10))
        v.SetFont(wx.Font(13, wx.SWISS, wx.NORMAL, wx.NORMAL))
        vo = wx.StaticText(self, -1, 'Voyage', (150, 10))
        vo.SetFont(wx.Font(13, wx.SWISS, wx.NORMAL, wx.NORMAL))
        d = wx.StaticText(self, -1, 'Date', (360, 10))
        d.SetFont(wx.Font(13, wx.SWISS, wx.NORMAL, wx.NORMAL))
        v_name = wx.StaticText(self, -1, in_d.input_v, (65, 10), size=(65, -1))
        v_name.SetFont(wx.Font(13, wx.SWISS, wx.NORMAL, wx.NORMAL))
        vo_name = wx.StaticText(self, -1, in_d.input_vo, (215, 10), size=(25, -1))
        vo_name.SetFont(wx.Font(13, wx.SWISS, wx.NORMAL, wx.NORMAL))
        y_name1 = wx.StaticText(self, -1, in_d.input_y1, (390, 10), size=(40, -1))
        m_name1 = wx.StaticText(self, -1, in_d.input_m1, (450, 10), size=(25, -1))
        d_name1 = wx.StaticText(self, -1, in_d.input_d1, (495, 10), size=(25, -1))
        
        t1 = wx.StaticText(self, -1, in_d.input_t1, (540, 10), size=(25, -1))
        c1 = wx.StaticText(self, -1, ':', (564, 10))
        m1 = wx.StaticText(self, -1, in_d.input_mi1, (570, 10), size=(25, -1))
        c2 = wx.StaticText(self, -1, ':', (594, 10))
        s1 = wx.StaticText(self, -1, in_d.input_s1, (600, 10), size=(25, -1))
        l = wx.StaticText(self, -1, '-', (635, 10))        
        y_name2 = wx.StaticText(self, -1, in_d.input_y2, (650, 10), size=(40, -1))
        m_name2 = wx.StaticText(self, -1, in_d.input_m2, (710, 10), size=(25, -1))
        d_name2 = wx.StaticText(self, -1, in_d.input_d2, (755, 10), size=(25, -1))
        t2 = wx.StaticText(self, -1, in_d.input_t2, (800, 10), size=(25, -1))
        c3 = wx.StaticText(self, -1, ':', (824, 10))
        m2 = wx.StaticText(self, -1, in_d.input_mi2, (830, 10), size=(25, -1))
        c4 = wx.StaticText(self, -1, ':', (854, 10))
        s2 = wx.StaticText(self, -1, in_d.input_s2, (860, 10), size=(25, -1))
        
        for x in [v, vo, d, v_name, vo_name, y_name1, m_name1, d_name1, t1, c1, m1, c2, s1, l, y_name2, m_name2, d_name2, t2, c3, m2, c4, s2]:
            x.SetConstraints(anchors.LayoutAnchors(x, False, True, False, False))
        
class Viewer_Panel(wx.Panel):
    def __init__(self, parent, pos, size, Evts):
        vehicles, self.containers = Evts
        self.vessels, self.qcs, self.ycs, self.scs = vehicles
        
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
        
        self.translate_mode = False
        self.translate_x, self.translate_y = 0, 0
        self.scale = 1.0
        
        self.n = Node(0);
        self.InitBuffer()
        
    def OnTimer(self, evt):
        if self.Parent.isReverse_play:
            self.n.x -= 1
        else:
            self.n.x += 1
        self.RefreshGC()
        
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
        gc.Translate(self.translate_x, self.translate_y)
        gc.Scale(self.scale, self.scale)

        c_hour, c_min, c_sec = self.Parent.cur_time.hour, self.Parent.cur_time.minute, self.Parent.cur_time.second
         
        st = '%s : %s : %s' % (c_hour, c_min, c_sec)
        gc.SetFont(wx.Font(30, wx.SWISS, wx.NORMAL, wx.NORMAL))
        gc.DrawText(st, 10, 150)
        
        gc.SetPen(wx.Pen("black", 1))
        r, g, b = (255, 0, 0)
        brushclr = wx.Colour(r, g, b, 100)
        gc.SetBrush(wx.Brush(brushclr))
        gc.DrawRectangle(self.n.x, self.n.y, 100, 100)
        
        #draw Background
        l_sx = self.GetSize()[0]
        l1_py = 100
        l2_py = l1_py + container_sy * 2.5
        
        
        gc.DrawLines([(0, l1_py), (l_sx, l1_py)])
        gc.DrawRectangle(0, l1_py, container_sx, container_sy)
        gc.DrawLines([(0, l2_py), (l_sx, l2_py)])
        

class Control_Panel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, -1, pos, size)
        self.SetConstraints(anchors.LayoutAnchors(self, True, False, True, True))
#        self.SetBackgroundColour(wx.Colour(0, 0, 255))

        self.time_flow = wx.Slider(self, -1, 1, 12.5, 1000, (30, 10), (950, -1), wx.SL_HORIZONTAL)
        self.diplay_time()

        s_img = wx.Image('pic/stop.bmp', wx.BITMAP_TYPE_BMP)
        s_bmp = s_img.Scale(30, 30)
        r_img = wx.Image("pic/reverse.bmp", wx.BITMAP_TYPE_BMP)
        r_bmp = r_img.Scale(30, 30)
        pa_img = wx.Image("pic/pause.bmp", wx.BITMAP_TYPE_BMP)
        pa_bmp = pa_img.Scale(30, 30)
        pl_img = wx.Image("pic/play.bmp", wx.BITMAP_TYPE_BMP)
        pl_bmp = pl_img.Scale(30, 30)
        
        s_btn = wx.BitmapButton(self, -1, wx.BitmapFromImage(s_bmp), (760, 30), (s_bmp.GetWidth() + 2, s_bmp.GetHeight() + 2))
        r_btn = wx.BitmapButton(self, -1, wx.BitmapFromImage(r_bmp), (790, 30), (r_bmp.GetWidth() + 2, r_bmp.GetHeight() + 2))
        pa_btn = wx.BitmapButton(self, -1, wx.BitmapFromImage(pa_bmp), (820, 30), (pa_bmp.GetWidth() + 2, pa_bmp.GetHeight() + 2))
        pl_btn = wx.BitmapButton(self, -1, wx.BitmapFromImage(pl_bmp), (850, 30), (pl_bmp.GetWidth() + 2, pl_bmp.GetHeight() + 2))
        
        self.Bind(wx.EVT_BUTTON, self.time_flow_stop, s_btn)
        self.Bind(wx.EVT_BUTTON, self.time_flow_reverse, r_btn)
        self.Bind(wx.EVT_BUTTON, self.time_flow_pause, pa_btn)
        self.Bind(wx.EVT_BUTTON, self.time_flow_play, pl_btn)
        
        self.dispaly_counter = 0
        self.timer = parent.timer
        self.saved_time = time.localtime(time.time())
        
    def time_flow_stop(self, evt):
        self.time_flow.SetValue(0)
        self.Parent.cur_time = self.Parent.start_time
        self.timer.Stop() 
        
    def time_flow_reverse(self, evt):
        self.Parent.isReverse_play = True
        if not self.timer.IsRunning():
            self.timer.Start(frame_milsec)
        
    def time_flow_pause(self, evt):
        self.timer.Stop()
    
    def time_flow_play(self, evt):
        self.Parent.isReverse_play = False
        self.timer.Start(frame_milsec)

    def OnTimer(self, evt):
        saved_sec = self.saved_time[5]
        cur_sec = time.localtime(time.time())[5]
        if abs(saved_sec - cur_sec) >= 1 :
            self.diplay_time()
            self.saved_time = time.localtime(time.time())
        if self.Parent.isReverse_play:
            self.time_flow.SetValue(self.time_flow.GetValue() - 1)
        else: 
            self.time_flow.SetValue(self.time_flow.GetValue() + 1)
        
    def diplay_time(self):
        c_year, c_month, c_day = self.Parent.cur_time.year, self.Parent.cur_time.month, self.Parent.cur_time.day
        c_hour, c_min, c_sec = self.Parent.cur_time.hour, self.Parent.cur_time.minute, self.Parent.cur_time.second
        st = '%s : %s : %s' % (c_hour, c_min, c_sec)
        self.c_time = wx.StaticText(self, -1, st, (900, 30))
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    id = Input_dialog(None, 'dialog test')
#    app.frame = MainFrame(1)
    app.MainLoop()
#    run()
