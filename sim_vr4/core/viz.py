from __future__ import division

from lib.dz_panel import DragZoomPanel

'''
    print l31.length
    print l31.points
    print l31.seg_break_distance
    from bisect import bisect
    u = 0
    while u < l31.length:
        i = bisect(l31.seg_break_distance, u)
        print u, i, l31.points[i], l31.points[i + 1]
        u += 12.1
'''


class MainFrame(wx.Frame):
    def __init__(self, L):
        wx.Frame.__init__(self, None, -1, TITLE, size=(1024, 768), pos=(20, 20))
        self.L = L         
         
        self.now = 0.0
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(TIMER_INTERVAL)
        self.vp = ViewPanel(self)
        self.Show(True)
        
    def OnClose(self, event):
        self.Destroy()

    def OnTimer(self, evt):
        self.now += CLOCK_INCREMENT / 1000
        

class ViewPanel(DragZoomPanel):
    def __init__(self, parent):
        DragZoomPanel.__init__(self, parent, -1, style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour(wx.WHITE)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
    def OnMouseWheel(self, e):
        if e.ControlDown():
            self.Parent.OnSpeedUp(None) if e.WheelRotation > 0 else self.Parent.OnSpeedDown(None)
        else:
            DragZoomPanel.OnMouseWheel(self, e)

    def OnDrawDevice(self, gc):
        gc.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        
        h = int(self.Parent.now // 3600)
        m = int(self.Parent.now // 60) % 60
        s = self.Parent.now % 60
        
        gc.DrawText('%02d:%02d:%04.1f (%.1fX)' % (h, m, s, CLOCK_INCREMENT / TIMER_INTERVAL), 5, 3)
    
    def OnDraw(self, gc):
        old_tr = gc.GetTransform()
        for n in self.Parent.L:
            gc.Translate(n.px, n.py)

        
if __name__ == '__main__':
    pass
