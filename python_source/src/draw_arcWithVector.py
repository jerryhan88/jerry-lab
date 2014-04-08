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

class Node:
    def __init__(self, px, py):
        self.id = id
        self.px = px
        self.py = py

def rotateP(c, p, ang):
    P = np.matrix(p).reshape(len(p), 1)
    C = np.matrix(c).reshape(len(c), 1)
    rotationM = np.matrix([
                           [cos(ang), sin(ang)],
                           [-sin(ang), cos(ang)]
                           ])
    m = np.add((np.dot(rotationM, np.subtract(P, C))), C).reshape(-1,)
    return np.array(m).flatten().tolist()
    
def calc_curvP(C, theta, w, l1, l2, r):
    pass
    
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
        theta = 0.5
        l = 100
        r = 30
        alpha = 1.2
        vRadi = calc_angle((1, 0), (0, 1))
        hRadi = calc_angle((1, 0), (-1, 0))
        print vRadi, hRadi 
        c1, c2 = 400, 200
        C = Node(c1, c2)
        P2 = Node(*calc_point((C.px , C.py), (cos(hRadi + theta), sin(hRadi + theta)), l))
        P2_ = Node(*calc_point((C.px , C.py), (cos(theta), sin(theta)), l))
        O2 = Node(*calc_point((P2.px , P2.py), (cos(vRadi + theta), sin(vRadi + theta)), r))
        O2_ = Node(*calc_point((P2_.px , P2_.py), (cos(vRadi + theta), sin(vRadi + theta)), r))
        O1 = Node(*calc_point((O2.px , O2.py), (-cos(theta + (alpha + vRadi)), -sin(theta + (alpha + vRadi))), 2 * r))
        O1_ = Node(*calc_point((O2_.px , O2_.py), (cos(theta + ((hRadi - alpha) + vRadi)), sin(theta + ((hRadi - alpha) + vRadi))), 2 * r))
        P1 = Node(*calc_point((O1.px , O1.py), (cos(theta + vRadi), sin(theta + vRadi)), r))
        P1_ = Node(*calc_point((O1_.px , O1_.py), (cos(theta + vRadi), sin(theta + vRadi)), r))
        self.nodes.append(C)
        self.nodes.append(P2)
        self.nodes.append(P2_)
        self.nodes.append(O2)
        self.nodes.append(O2_)
        self.nodes.append(O1)
        self.nodes.append(O1_)
        self.nodes.append(P1)
        self.nodes.append(P1_)
        
        for i in range(1, 5):
            self.nodes.append(
                              Node(*rotateP((O2.px, O2.py),
                                            (P2.px, P2.py),
                                            i * -0.25
                                            )),
                              )
            
        for i in range(1, 5):
            self.nodes.append(
                              Node(*rotateP((O2_.px, O2_.py),
                                            (P2_.px, P2_.py),
                                            i * 0.25
                                            )),
                              )
            
        for i in range(1, 5):
            self.nodes.append(
                              Node(*rotateP((O1.px, O1.py),
                                            (P1.px, P1.py),
                                            i * -0.25
                                            )),
                              )
        for i in range(1, 5):
            self.nodes.append(
                              Node(*rotateP((O1_.px, O1_.py),
                                            (P1_.px, P1_.py),
                                            i * 0.25
                                            )),
                              )

        aP = Node(300, 20)
        bP = Node(300, 110)
        O = Node(450, 80)
        r = 20
        
        aV = calc_vec((O.px, O.py), (aP.px, aP.py))
        bV = calc_vec((O.px, O.py), (bP.px, bP.py))
        theta = calc_angle(aV, bV)
        x = r / sin(theta / 2)
        p = r / tan(theta / 2)
        P1 = Node(*calc_point((O.px , O.py), aV, p))
        P2 = Node(*calc_point((O.px , O.py), bV, p))
        
#         print calc_point((O.px , O.py), aV, p)
#         assert False
        
        C = Node(*calc_point((O.px , O.py), addVec(aV, bV), x))
        
        self.nodes.append(aP)
        self.nodes.append(bP)
        self.nodes.append(O)
        self.nodes.append(P1)
        self.nodes.append(P2)
        self.nodes.append(C)
        for i in range(1, 10):
            self.nodes.append(
                              Node(*rotateP((C.px, C.py),
                                            (P1.px, P1.py),
                                            i * -0.25
                                            )),
                              )
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
    
    
