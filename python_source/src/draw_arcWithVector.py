from __future__ import division
import wx, time

from math import sqrt, acos, cos, sin, tan
import numpy as np

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

def rotateP(c, p, ang):
    P = np.matrix(p).reshape(len(p), 1)
    C = np.matrix(c).reshape(len(c), 1)
    rotationM = np.matrix([
                           [cos(ang), sin(ang)],
                           [-sin(ang), cos(ang)]
                           ])
    m = np.add((np.dot(rotationM, np.subtract(P, C))), C).reshape(-1,)
    return np.array(m).flatten().tolist()

def calc_dcPos(C, theta, alpha, l, r, n1, n2):
    points = []
    P2, P2_ = calc_point(C, (cos(hRadi + theta), sin(hRadi + theta)), l), calc_point(C, (cos(theta), sin(theta)), l)
    O2, O2_ = calc_point(P2, (cos(vRadi + theta), sin(vRadi + theta)), r), calc_point(P2_, (cos(vRadi + theta), sin(vRadi + theta)), r)
    O1, O1_ = calc_point(O2, (-cos(theta + (alpha + vRadi)), -sin(theta + (alpha + vRadi))), 2 * r), calc_point(O2_, (cos(theta + ((hRadi - alpha) + vRadi)), sin(theta + ((hRadi - alpha) + vRadi))), 2 * r)
    P1, P1_ = calc_point(O1, (cos(theta + vRadi), sin(theta + vRadi)), r), calc_point(O1_, (cos(theta + vRadi), sin(theta + vRadi)), r)
    vO2O1, vO2_O1_ = calc_vec(O2, O1), calc_vec(O2_, O1_)
    vO1O2, vO1_O2_ = calc_vec(O1, O2), calc_vec(O1_, O2_) 
    CP, CP_ = calc_point(O1, vO1O2, r), calc_point(O1_, vO1_O2_, r)
    uA2, uA2_ = calc_angle(calc_vec(O2, P2), vO2O1) / (n2 + 1), calc_angle(calc_vec(O2_, P2_), vO2_O1_) / (n2 + 1) 
    uA1, uA1_ = calc_angle(calc_vec(O1, P1), vO1O2) / (n1 + 1), calc_angle(calc_vec(O1_, P1_), vO1_O2_) / (n1 + 1)  
    
    points.append(P2)
    for i in range(n2): points.append(rotateP(O2, P2, (i + 1) * -uA2))
    points.append(CP)
    for i in list(reversed(range(n1))): points.append(rotateP(O1, P1, (i + 1) * -uA1))
    points.append(P1)
     
    points.append(P1_)
    for i in range(n1): points.append(rotateP(O1_, P1_, (i + 1) * uA1_))
    points.append(CP_)          
    for i in list(reversed(range(n2))): points.append(rotateP(O2_, P2_, (i + 1) * uA2_))
    points.append(P2_)
    return points

def calc_cPos(sP, eP, O, r, n):
    points = []
    aV, bV = calc_vec(O, sP), calc_vec(O, eP)
    theta = calc_angle(aV, bV)
    x, p = r / sin(theta / 2), r / tan(theta / 2) 
    P1, P2 = calc_point(O, aV, p), calc_point(O, bV, p)
    C = calc_point(O, addVec(aV, bV), x)
    uA = calc_angle(calc_vec(C, P1), calc_vec(C, P2)) / (n + 1)
    
    points.append(P1)
    for i in range(n):
        points.append(rotateP(C, P1, (i + 1) * uA))
    points.append(P2)
    
    return points      

class Node:
    def __init__(self, px, py):
        self.id = id
        self.px = px
        self.py = py
  
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
        self.timer.Start(1000)
        self.n = Node(0, 10)
        c1, c2 = 100, 100
        self.nodes = [
                      Node(c1, c2),
                      Node(c1 + 50, c2),
                     ]
        
        for i in range(1, 20):
            self.nodes.append(
                              Node(*rotateP((self.nodes[0].px, self.nodes[0].py),
                                            (self.nodes[1].px, self.nodes[1].py),
                                            (-i) * 0.25
                                            )),
                              )
        
        C, theta, alpha, l, r = (400, 200), 0.5, 1.2, 100, 30 
        
        for px, py in calc_dcPos(C, theta, alpha, l, r, 10, 10):
            self.nodes.append(Node(px, py))
            
        sP, eP, O, r, n = (300, 20), (300, 110), (450, 80), 20, 15
        for px, py in calc_cPos(sP, eP, O, r, n):
            self.nodes.append(Node(px, py))
            
        P1, P2 = (190, 220), (220, 310)
        V1 = calc_vec(P1, P2)
        M1 = tuple(sum(arg) / 2 for arg in zip(P1, P2))
        k = 50
        print cos(theta + vRadi), sin(theta + vRadi)
        theta = calc_angle((1, 0), V1)
        C = calc_point(M1, (cos(theta + vRadi), sin(theta + vRadi)), k) 
        for px, py in [P1, P2, C]:
            self.nodes.append(Node(px, py))
        
        sP, eP, O, r, n = P1, P2, C, 20, 2
        for px, py in calc_cPos(sP, eP, O, r, n):
            self.nodes.append(Node(px, py))
        
    def OnTimer(self, evt):
        self.n.px += 1
        self.RefreshGC()
            
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
            
    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self, self._buffer)
        
    def OnMouseWheel(self, evt):
        # TODO scaling based on mouse position (evt.m_x, evt.m_y)
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
        gc.SetFont(wx.Font(30, wx.SWISS, wx.NORMAL, wx.NORMAL))
        gc.DrawText(st, 10, 150)
        
        gc.SetPen(wx.Pen("black", 1))
        r, g, b = (255, 0, 0)
        brushclr = wx.Colour(r, g, b, 100)
        gc.SetBrush(wx.Brush(brushclr))
        gc.DrawRectangle(self.n.px, self.n.py, 20, 20)
        
        for n in self.nodes:
            gc.DrawEllipse(n.px, n.py, 5, 5)
        gc.DrawRectangle(self.nodes[2].px, self.nodes[2].py, 20, 20)
class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'test', size=(600, 400))
        MyPanel(self)
        self.Show(True)
        
if __name__ == '__main__':
#     p1 = (1, 2)
#     p2 = (2, 3)
#     v1 = (1, 2)
#     v2 = (2, 3)
#     v3 = calc_vec(p1, p2)
#     v4 = (2, 2)
#     print calc_unitVec(v3)
#     print innPro(v1, v2) 
#     
#     print norm(v1), norm(v3) 
#     
#     print calc_angle(v1, v2)
#     print calc_angle(v4, (1, 0))
#     assert False
    app = wx.PySimpleApp()
    app.frame = MainFrame()
    app.MainLoop()
    
    
