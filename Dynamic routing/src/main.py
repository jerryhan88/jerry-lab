from __future__ import division
from time import time
import wx

milsec = 100

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Dynamic routing experiment', size=(1024, 768), pos=(243, 80))
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        
        self.timer.Start(milsec)
        self.st_t = time()
        self.simul_clock = 0
        
        f_sx, f_sy = self.GetSize()
        
        ip_sx, ip_sy = f_sx / 7, f_sy
        ip = InputPanel(self, (0, 0), (ip_sx, ip_sy))
        ip_px, ip_py = ip.GetPosition()
        
        op_sx, op_sy = f_sx / 4, f_sy
        op = OutputPanel(self, (f_sx - op_sx, 0), (op_sx, op_sy))
        
        vp_sx, vp_sy = f_sx - ip_sx - op_sx, f_sy * 0.9  
        
        self.vp = ViewPanel(self, (ip_px + ip_sx, ip_py), (vp_sx, vp_sy))
        self.cp = ControlPanel(self, (ip_px + ip_sx, ip_py + vp_sy), (vp_sx, f_sy - vp_sy))
        
        
        
        self.Show(True)
        
    def OnTimer(self, evt):
        self.simul_clock += milsec/1000   
        self.vp.Refresh()
        self.cp.update(self.simul_clock)  
# 
    def OnCloseWindow(self, event):
        self.Destroy()

class InputPanel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, -1, pos, size)
        self.SetBackgroundColour(wx.BLUE)

class OutputPanel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, -1, pos, size)
        self.SetBackgroundColour(wx.RED)

class ControlPanel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, -1, pos, size)    
        self.SetBackgroundColour((0, 255, 255))
        
        self.simul_st= wx.StaticText(self, -1, str(0), (0, 0))
        
        pa_img, pl_img = wx.Image("pic/pause.bmp", wx.BITMAP_TYPE_BMP), wx.Image("pic/play.bmp", wx.BITMAP_TYPE_BMP) 
        pa_bmp, pl_bmp = pa_img.Scale(30, 30), pl_img.Scale(30, 30)
        px = 100
        py = 5
        bt = 30
        
        pl_btn = wx.BitmapButton(self, -1, wx.BitmapFromImage(pl_bmp), (px + bt * 2, py), (pl_bmp.GetWidth() + 2, pl_bmp.GetHeight() + 2))
        pa_btn = wx.BitmapButton(self, -1, wx.BitmapFromImage(pa_bmp), (px + bt * 3, py), (pa_bmp.GetWidth() + 2, pl_bmp.GetHeight() + 2))
        
        self.Bind(wx.EVT_BUTTON, self.play, pl_btn)
        self.Bind(wx.EVT_BUTTON, self.pause, pa_btn)
#         self.Bind(wx.EVT_BUTTON, self.time_flow_pause, pa_btn)
        
    
    def update(self, simul_clock):
        self.simul_st.SetLabel(str(round(simul_clock,2)))
        
    def play(self, evt):
        self.Parent.timer.Start(milsec)
        print 11
        
    def pause(self, evt):
        self.Parent.timer.Stop()
        print 12

class ViewPanel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, -1, pos, size)
        self.SetBackgroundColour(wx.WHITE)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
    
    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        r, g, b = (255, 0, 0)
        brushclr = wx.Colour(r, g, b, 100)
        dc.SetBrush(wx.Brush(brushclr))
        
        dc.DrawCircle(100, 100, 30)
        
#         t = time.time()
#         dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
#         dc.Clear()
#         dc.SetFont(wx.Font(30, wx.SWISS, wx.NORMAL, wx.NORMAL))
#         dc.DrawText(str(round(t - self.st_t, 2)), 20, 20)
        
        dc.EndDrawing()

if __name__ == '__main__':
    app = wx.PySimpleApp()
    win = MainFrame()
    win.Show(True)
    app.MainLoop()
