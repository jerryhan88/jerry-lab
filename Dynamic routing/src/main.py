from __future__ import division
import wx, time

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Dynamic routing experiment', size=(1024, 768), pos=(243, 80))
        
        ViewPanel(self)
        self.Show(True)        
# 
    def OnCloseWindow(self, event):
        self.Destroy()

class ControlPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.WHITE)
        
class SitDiscPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.WHITE)

class ViewPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.WHITE)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(100)
        self.count = 1
        
        self.st_t = time.time()
    
    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        r, g, b = (255, 0, 0)
        brushclr = wx.Colour(r, g, b, 100)
        dc.SetBrush(wx.Brush(brushclr))
        
        dc.DrawCircle(self.count, self.count, 30)
        
        
        t = time.time()
#         st = time.strftime("%I:%M:%S", t)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        dc.SetFont(wx.Font(30, wx.SWISS, wx.NORMAL, wx.NORMAL))
#         tw, th = dc.GetTextExtent(st)
        dc.DrawText(str(round(t-self.st_t, 2)), 20, 20)
        
        
        dc.EndDrawing()
        
    def OnTimer(self, evt):
        self.count += 1
        self.Refresh()

if __name__ == '__main__':
    app = wx.PySimpleApp()
    win = MainFrame()
    win.Show(True)
    app.MainLoop()
