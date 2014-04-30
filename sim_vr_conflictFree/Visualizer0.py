from __future__ import division
from util import DragZoomPanel
from math import sqrt, acos
import wx

TIMER_INTERVAL = 100
CLOCK_INCREMENT = 200
CLOCK_INCR_DIFF = sqrt(2)
TITLE = 'PRT Simulator'

STATION_DIAMETER = 50
PRT_SIZE = 15

addVec = lambda v1, v2: tuple(v1[i] + v2[i] for i in range(len(v1)))
subVec = lambda v1, v2: tuple(v1[i] - v2[i] for i in range(len(v1)))
# scalMul = lambda v1, k: tuple(k * v1[i] for i in range(len(v1))) 
innPro = lambda v1, v2: sum(p * q for p, q in zip(v1, v2))
norm = lambda v1: sqrt(sum(i ** 2 for i in v1))
calc_vec = lambda p1, p2: tuple(p2[i] - p1[i] for i in range(len(p1)))
calc_unitVec = lambda v1: tuple(v1[i] / norm(v1)for i in range(len(v1)))
calc_angle = lambda v1, v2: acos(innPro(v1, v2) / (norm(v1) * norm(v2)))
calc_point = lambda p1, v1, l: tuple(p1[i] + l * v1[i] / norm(v1)  for i in range(len(v1)))

vRadi = calc_angle((1, 0), (0, 1))
hRadi = calc_angle((1, 0), (-1, 0))

class MainFrame(wx.Frame):
    def __init__(self, Network, PRTs):
        wx.Frame.__init__(self, None, -1, TITLE, size=(1024, 768), pos=(20, 20))
        self.Nodes, self.Edges = Network
        self.PRTs = PRTs 
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
        
        for p in self.PRTs:
            if p.cur_scheIndex == -1: continue
            cur_sche = p.schedules[p.cur_scheIndex]
            cur_inT, cur_outT = cur_sche[0][0], cur_sche[0][1]
            cN, cE = cur_sche[1], cur_sche[2]
            cP = (cN.px, cN.py)
            travelT = self.now - (cur_inT + cur_outT) / 2
            if p.cur_scheIndex + 1 != len(p.schedules):
                next_sche = p.schedules[p.cur_scheIndex + 1]
                next_inT, next_outT = next_sche[0][0], next_sche[0][1]
                nN, nE = next_sche[1], next_sche[2]
                nP = (nN.px, nN.py)
                v1 = calc_vec(cP, nP)
                l = norm(v1) * (travelT / cE.net_trackTime)
                
            if p.cur_scheIndex == 0:
                if self.now < (cur_inT + cur_outT) / 2:
                    p.px, p.py = p.arrived_n.px, p.arrived_n.py
                else:
                    p.px, p.py = calc_point(cP, v1, l)
            elif p.cur_scheIndex != 0 and p.cur_scheIndex + 1 != len(p.schedules):
                p.px, p.py = calc_point(cP, v1, l)
            
            if (next_inT + next_outT) / 2 <= self.now:
                p.n_arrT = (next_inT + next_outT) / 2 
                p.cur_scheIndex += 1
                if p.cur_scheIndex ==  len(p.schedules)-1:
                    p.px, p.py = nN.px, nN.py
                    p.cur_scheIndex = -1
                
        
        self.vp.RefreshGC()
        
    def OnSpeedUp(self, _):
        global CLOCK_INCREMENT
        CLOCK_INCREMENT *= CLOCK_INCR_DIFF
        self.vp.RefreshGC()
        
    def OnSpeedDown(self, _):
        global CLOCK_INCREMENT
        CLOCK_INCREMENT /= CLOCK_INCR_DIFF
        self.vp.RefreshGC()
        
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
        for n in self.Parent.Nodes:
            gc.Translate(n.px, n.py)
            gc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
            gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
            gc.DrawRectangle(-STATION_DIAMETER / 2, -STATION_DIAMETER / 2, STATION_DIAMETER, STATION_DIAMETER)
            gc.DrawText('%s' % n.id, -14, 5)
            
            gc.SetTransform(old_tr)
            
        for e in self.Parent.Edges:
            prev_n, next_n = e._from, e._to
            ax, ay = next_n.px - prev_n.px, next_n.py - prev_n.py
            la = sqrt(ax * ax + ay * ay)
            assert la != 0 
            ux, uy = ax / la, ay / la
            px, py = -uy, ux
            sx = prev_n.px + ux * STATION_DIAMETER / 2
            sy = prev_n.py + uy * STATION_DIAMETER / 2
            ex = next_n.px - ux * STATION_DIAMETER / 2
            ey = next_n.py - uy * STATION_DIAMETER / 2
            gc.DrawLines([(sx, sy), (ex, ey)])
            
            px, py = (sx + ex) / 2, (sy + ey) / 2
            
            gc.DrawText('(%s)_%d' % (e.id, e.net_trackTime - 4), px - 14, py + 5)
        
        for p in self.Parent.PRTs:
            gc.Translate(p.px, p.py)
            gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
            
            gc.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            gc.DrawEllipse(-PRT_SIZE / 2, -PRT_SIZE / 2, PRT_SIZE, PRT_SIZE)
            gc.DrawText('PRT%s' % p.id, -PRT_SIZE / 2, -PRT_SIZE / 2 - 12)
            gc.SetTransform(old_tr)     

if __name__ == '__main__':
    app = wx.App(False)
    win = MainFrame()
    win.Show(True)
    app.MainLoop()
