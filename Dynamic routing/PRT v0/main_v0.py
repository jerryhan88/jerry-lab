from __future__ import division
from time import time
from input_gen import N
from classes import Node, Edge, Customer, PRT
import wx

milsec = 100
REQUEST = []

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Dynamic routing experiment', size=(1024, 768), pos=(243, 80))
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        
        self.timer.Start(milsec)
        self.st_t = time()
        self.simul_clock = 0
        
        f_sx, f_sy = self.GetSize()
        
        ip_sx, ip_sy = f_sx * 0.16, f_sy
        ip = InputPanel(self, (0, 0), (ip_sx, ip_sy))
        ip_px, ip_py = ip.GetPosition()
        
        op_sx, op_sy = f_sx / 4, f_sy
        op = OutputPanel(self, (f_sx - op_sx, 0), (op_sx, op_sy))
        
        vp_sx, vp_sy = f_sx - ip_sx - op_sx, f_sy * 0.9  
        
        self.vp = ViewPanel(self, (ip_px + ip_sx, ip_py), (vp_sx, vp_sy))
        self.cp = ControlPanel(self, (ip_px + ip_sx, ip_py + vp_sy), (vp_sx, f_sy - vp_sy))
        
        self.Show(True)
        
    def OnTimer(self, evt):
        self.vp.update(self.simul_clock)
        self.cp.update(self.simul_clock)
        self.simul_clock += milsec / 1000 
    def OnCloseWindow(self, event):
        self.Destroy()

class ViewPanel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, -1, pos, size)
        self.SetBackgroundColour(wx.WHITE)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
        sx, sy = self.GetSize()
        self.n_radius = 25
        self.Nodes = [Node(x) for x in range(N)]
        self.Nodes[0].px, self.Nodes[0].py = sx * 0.2, sy * 0.3
        self.Nodes[1].px, self.Nodes[1].py = sx * 0.6, sy * 0.2
        self.Nodes[2].px, self.Nodes[2].py = sx * 0.1, sy * 0.5
        self.Nodes[3].px, self.Nodes[3].py = sx * 0.4, sy * 0.6
        self.Nodes[4].px, self.Nodes[4].py = sx * 0.6, sy * 0.45
        self.Nodes[5].px, self.Nodes[5].py = sx * 0.85, sy * 0.35
        self.Nodes[6].px, self.Nodes[6].py = sx * 0.3, sy * 0.85
        self.Nodes[7].px, self.Nodes[7].py = sx * 0.8, sy * 0.65
        
        self.Edges = []
        self.Edges.append(Edge(self.Nodes[0], self.Nodes[3]))
        self.Edges.append(Edge(self.Nodes[1], self.Nodes[4]))
        self.Edges.append(Edge(self.Nodes[2], self.Nodes[3]))
        self.Edges.append(Edge(self.Nodes[3], self.Nodes[4]))
        self.Edges.append(Edge(self.Nodes[3], self.Nodes[6]))
        self.Edges.append(Edge(self.Nodes[4], self.Nodes[5]))
        self.Edges.append(Edge(self.Nodes[4], self.Nodes[7]))
        
        self.on_requests = []
        self.c_radius = 10
        
        self.PRTs = []
        self.PRTs.append(PRT(0, self.Nodes[4].px, self.Nodes[4].py))
        self.PRTs.append(PRT(1, self.Nodes[0].px, self.Nodes[0].py))
        self.PRTs.append(PRT(2, self.Nodes[6].px, self.Nodes[6].py))
        self.PRT_size = 20
    
    def update(self, simul_clock):
        self.Refresh()
        if REQUEST and REQUEST[0][0] <= simul_clock:
            t, c, sn, dn = REQUEST.pop(0)
            self.on_requests.append(Customer(t, c, self.Nodes[sn], self.Nodes[dn]))
    
    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        
        dc.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        for e in self.Edges:
            dc.DrawLine(e._from.px, e._from.py, e._to.px, e._to.py)
            dc.DrawText('%d' % int(round(e.distance, 1)), (e._from.px + e._to.px) / 2, (e._from.py + e._to.py) / 2)
        
        for n in self.Nodes:
            dc.DrawCircle(n.px, n.py, self.n_radius)
            dc.DrawText('N%d' % n.id, n.px - 7, n.py - 7)
            
        old_font = dc.GetFont()
        dc.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        for v in self.PRTs:
            dc.DrawRectangle(v.px - self.PRT_size / 2, v.py - self.PRT_size / 2, self.PRT_size, self.PRT_size)
            dc.DrawText('PRT%d' % v.id, v.px - self.PRT_size / 2, v.py - self.PRT_size / 2)    
            
        r, g, b = (200, 200, 200)
        brushclr = wx.Colour(r, g, b, 100)
        dc.SetBrush(wx.Brush(brushclr))
        
        for r in self.on_requests:
            dc.DrawCircle(r.px, r.py, self.c_radius)
            dc.DrawText(r.id, r.px - 7, r.py - 7)
        
        dc.SetFont(old_font)
        
        dc.EndDrawing()

class InputPanel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, -1, pos, size)
        self.SetBackgroundColour(wx.WHITE)
        p_sx, p_sy = self.GetSize()
        re_st = wx.StaticText(self, -1, 'Requests of customers', (2, 0))
        sx, sy = re_st.GetSize()
        
        self.request_view = wx.TextCtrl(self, -1, "", pos=(2, sy), size=(p_sx - 2, p_sy - sy - 40), style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
        self.request_view.SetEditable(False)
        self.request_view.SetBackgroundColour(wx.WHITE)
        
        with open('Input', 'r') as input:
            for line in input:
                c, t_s, sd = line.split(',')
                t = str(round(float(t_s), 1))
                sn, dn = sd.split('-')
                self.request_view.write('---------------------------------\n');
                self.request_view.write('%s sec, %s: N%s -> N%s ' % (t, c, sn, dn));
                self.request_view.write('\n');
                REQUEST.append((round(float(t_s), 1), c, int(sn), int(dn)))

class OutputPanel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, -1, pos, size)
        self.SetBackgroundColour(wx.RED)

class ControlPanel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, -1, pos, size)    
        self.SetBackgroundColour((0, 255, 255))
        
        self.simul_st = wx.StaticText(self, -1, str(0), (0, 0))
        
        pa_img, pl_img = wx.Image("pic/pause.bmp", wx.BITMAP_TYPE_BMP), wx.Image("pic/play.bmp", wx.BITMAP_TYPE_BMP) 
        pa_bmp, pl_bmp = pa_img.Scale(30, 30), pl_img.Scale(30, 30)
        px = 100
        py = 5
        bt = 30
        
        pl_btn = wx.BitmapButton(self, -1, wx.BitmapFromImage(pl_bmp), (px + bt * 2, py), (pl_bmp.GetWidth() + 2, pl_bmp.GetHeight() + 2))
        pa_btn = wx.BitmapButton(self, -1, wx.BitmapFromImage(pa_bmp), (px + bt * 3, py), (pa_bmp.GetWidth() + 2, pl_bmp.GetHeight() + 2))
        
        self.Bind(wx.EVT_BUTTON, self.play, pl_btn)
        self.Bind(wx.EVT_BUTTON, self.pause, pa_btn)
    
    def update(self, simul_clock):
        self.simul_st.SetLabel(str(round(simul_clock, 2)))
        
    def play(self, evt):
        self.Parent.timer.Start(milsec)
        
    def pause(self, evt):
        self.Parent.timer.Stop()

if __name__ == '__main__':
    app = wx.PySimpleApp()
    win = MainFrame()
    win.Show(True)
    app.MainLoop()
