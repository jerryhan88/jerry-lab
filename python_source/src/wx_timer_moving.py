from __future__ import division
import wx, time #threading
from threading import Timer
class Node:
    def __init__(self, id):
        self.id = id
        self.x = 100
        self.y = 100
#        self.seq = [(0,100,'stop'),(10,100,'go'), (20,200,'stop'),]

class Frame(wx.Frame):
    def __init__(self, parent, ID, title, pos, size, style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        f_size_x, f_size_y = size
        self.base_p = wx.Panel(self, -1, pos=(0, 0), size=(f_size_x, f_size_y))
        self.base_p.Bind(wx.EVT_PAINT, self.OnPaint)
        self.timer = wx.Timer(self.base_p)
        self.base_p.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(1000)
        self.n = Node(0);
        
    def Draw(self, dc):
        t = time.localtime(time.time())
        st = time.strftime("%I:%M:%S", t)
        dc.Clear()
        dc.SetFont(wx.Font(30, wx.SWISS, wx.NORMAL, wx.NORMAL))
        dc.DrawText(st, 10, 200)

        r, g, b = (255, 0, 0)
        brushclr = wx.Colour(r, g, b, 100)
        dc.SetBrush(wx.Brush(brushclr))
        dc.DrawCircle(self.n.x, self.n.y, 30)
        
    def OnTimer(self, evt):
        self.n.x += 1
        dc = wx.BufferedDC(wx.ClientDC(self.base_p))
        self.Draw(dc)
        self.base_p.Refresh()

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self.base_p)
        self.Draw(dc)

if __name__ == '__main__':
    app = wx.PySimpleApp()
    mv = Frame(None, -1, 'Main_viewer', pos=(200, 200), size=(300, 300))
    mv.Show(True)
    app.MainLoop()
