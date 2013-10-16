from __future__ import division
from classes import Node, Edge, Customer, PRT
import wx
REQUEST = []
TIMER_INTERVAL = 100
CLOCK_INCREMENT = 100

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Dynamic routing experiment', size=(1024, 768), pos=(243, 80))
        
        self.simul_clock = 0
        self.timer = wx.Timer(self)
        self.timer.Start(TIMER_INTERVAL)
        
        f_sx, f_sy = self.GetSize()
        
        ip_sx, ip_sy = f_sx * 0.2, f_sy
        ip = InputPanel(self, (0, 0), (ip_sx, ip_sy))
        ip_px, ip_py = ip.GetPosition()
        
        op_sx, op_sy = f_sx / 4, f_sy
        OutputPanel(self, (f_sx - op_sx, 0), (op_sx, op_sy))
         
        vp_sx, vp_sy = f_sx - ip_sx - op_sx, f_sy * 0.89  
        self.vp = ViewPanel(self, (ip_px + ip_sx, ip_py), (vp_sx, vp_sy))
        self.cp = ControlPanel(self, (ip_px + ip_sx, ip_py + vp_sy), (vp_sx, f_sy - vp_sy))
         
        self.Show(True)
         
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
    def OnTimer(self, evt):
        self.simul_clock += CLOCK_INCREMENT / 1000
        self.vp.update(self.simul_clock)
        self.cp.update(self.simul_clock)
        
    def OnClose(self, event):
        self.Destroy()

class ViewPanel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, -1, pos, size, style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour(wx.WHITE)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Nodes = []
        self.Edges = []
        self.PRTs = []
        
        sx, sy = self.GetSize()
        self.Nodes.append(Node(sx * 0.2, sy * 0.3))
        self.Nodes.append(Node(sx * 0.6, sy * 0.2))
        self.Nodes.append(Node(sx * 0.1, sy * 0.5))
        self.Nodes.append(Node(sx * 0.4, sy * 0.6))
        self.Nodes.append(Node(sx * 0.6, sy * 0.45))
        self.Nodes.append(Node(sx * 0.85, sy * 0.35))
        self.Nodes.append(Node(sx * 0.3, sy * 0.85))
        self.Nodes.append(Node(sx * 0.8, sy * 0.65))
        
        self.Edges.append(Edge(self.Nodes[0], self.Nodes[3]))
        self.Edges.append(Edge(self.Nodes[0], self.Nodes[2]))
        self.Edges.append(Edge(self.Nodes[0], self.Nodes[4]))
        self.Edges.append(Edge(self.Nodes[1], self.Nodes[4]))
        self.Edges.append(Edge(self.Nodes[1], self.Nodes[5]))
        self.Edges.append(Edge(self.Nodes[2], self.Nodes[3]))
        self.Edges.append(Edge(self.Nodes[3], self.Nodes[4]))
        self.Edges.append(Edge(self.Nodes[3], self.Nodes[6]))
        self.Edges.append(Edge(self.Nodes[4], self.Nodes[5]))
        self.Edges.append(Edge(self.Nodes[4], self.Nodes[7]))
        self.Edges.append(Edge(self.Nodes[5], self.Nodes[7]))
        self.Edges.append(Edge(self.Nodes[6], self.Nodes[7]))
        
        for e in self.Edges[:]:
            e.gen_biDir(self.Edges)

        self.PRTs.append(PRT())
        self.PRTs[-1].init_position(self.Nodes[4])
        self.PRTs.append(PRT())
        self.PRTs[-1].init_position(self.Nodes[0])
        self.PRTs.append(PRT())
        self.PRTs[-1].init_position(self.Nodes[6])

        self.InitBuffer()
    
    def update(self, simul_clock):
        while REQUEST and REQUEST[0][0] <= simul_clock:
            t, c, sn, dn = REQUEST.pop(0)
            self.Nodes[sn].cus_queue.append(Customer(t, c, self.Nodes[sn], self.Nodes[dn]))
#            Next time NN implement            
#             v = PRT.find_NN(self.PRTs, self.Nodes)
#             if v.state == 0 and v.arrived_n != self.Nodes[sn]:
#                 v.path_n, v.path_e = PRT.find_SP(v.arrived_n, self.Nodes[sn], self.Nodes)
#                 v.calc_btw_ns(CLOCK_INCREMENT, simul_clock)
#                 v.dest_n = self.Nodes[sn]
#                 path_n, path_e = PRT.find_SP(self.Nodes[sn], self.Nodes[dn], self.Nodes)
#                 v.path_n += path_n[1:]  
#                 v.path_e += path_e
#                 v.state = 2
        
        for v in [x for x in self.PRTs if x.state == 0]:
            print 11
            target_n = PRT.find_NearestNode(v, self.Nodes)
            print 
            if v.arrived_n != target_n:
                v.path_n, v.path_e = PRT.find_SP(v.arrived_n, self.Nodes[sn], self.Nodes)
                v.calc_btw_ns(CLOCK_INCREMENT, simul_clock)
                v.dest_n = self.Nodes[sn]
                path_n, path_e = PRT.find_SP(self.Nodes[sn], self.Nodes[dn], self.Nodes)
                v.path_n += path_n[1:]  
                v.path_e += path_e
                v.state = 1
        
        for v in self.PRTs:
            if v.arrived_n != v.target_n:
                v.update_pos(CLOCK_INCREMENT, simul_clock)
        self.RefreshGC()
        
    def Draw(self, gc):   
        old_tr = gc.GetTransform()
            
        for n in self.Nodes:
            gc.Translate(n.px, n.py)
            n.draw(gc)
            gc.SetTransform(old_tr)
            
        for e in self.Edges[:len(self.Edges) // 2]:
            e.draw(gc)

        for v in self.PRTs:
            gc.Translate(v.px, v.py)
            v.draw(gc)
            gc.SetTransform(old_tr)    
            
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
    
    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self, self._buffer)

class InputPanel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, -1, pos, size)
        self.SetBackgroundColour(wx.WHITE)
        p_sx, p_sy = self.GetSize()
        re_st = wx.StaticText(self, -1, 'Requests of customers', (2, 2))
        re_st.SetFont(wx.Font(12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT))
        sx, sy = re_st.GetSize()
        
        self.request_view = wx.ListCtrl(self, -1, pos=(2, sy + 4), size=(p_sx - 2, p_sy - sy - 40), style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.request_view.InsertColumn(0, 'Customer')
        self.request_view.InsertColumn(1, 'Time')
        self.request_view.InsertColumn(2, 'From')
        self.request_view.InsertColumn(3, 'To')
        
        self.request_view.SetColumnWidth(0, p_sx / 3)
        self.request_view.SetColumnWidth(1, p_sx / 4)
        self.request_view.SetColumnWidth(2, p_sx / 4.5)
        self.request_view.SetColumnWidth(3, p_sx / 4.5)
        
        rowCount = 0
        with open('Input', 'r') as input:
            for line in input:
                c, t_s, sd = line.split(',')
                t = str(round(float(t_s), 1))
                sn, dn = sd.split('-')
                self.request_view.InsertStringItem(rowCount, c)
                self.request_view.SetStringItem(rowCount, 1, t)
                self.request_view.SetStringItem(rowCount, 2, sn)
                self.request_view.SetStringItem(rowCount, 3, dn)
                rowCount += 1
                REQUEST.append((round(float(t_s), 1), c, int(sn), int(dn)))

class OutputPanel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, -1, pos, size)
        self.SetBackgroundColour(wx.WHITE)
        p_sx, p_sy = self.GetSize()
        re_st = wx.StaticText(self, -1, 'Operation of PRTs', (2, 2))
        re_st.SetFont(wx.Font(12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT))
        sx, sy = re_st.GetSize()
        
        self.request_view = wx.TextCtrl(self, -1, "", pos=(2, sy + 4), size=(p_sx - 2, p_sy - sy - 40), style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
        self.request_view.SetEditable(False)
        self.request_view.SetBackgroundColour(wx.WHITE)

class ControlPanel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, -1, pos, size)    
        sx, sy = self.GetSize()
        wx.StaticBox(self, -1, "", pos=(5, 0), size=(sx - 10, sy - 43))
        
        pa_img, pl_img = wx.Image("pic/pause.bmp", wx.BITMAP_TYPE_BMP), wx.Image("pic/play.bmp", wx.BITMAP_TYPE_BMP) 
        pa_bmp, pl_bmp = pa_img.Scale(26, 26), pl_img.Scale(26, 26)
        
        self.simul_st = wx.StaticText(self, -1, str(0), (250, 10))
        self.simul_st.SetFont(wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT))
        
        px = 430
        py = 9
        bt = 30
        
        pl_btn = wx.BitmapButton(self, -1, wx.BitmapFromImage(pl_bmp), (px + bt * 2, py), (pl_bmp.GetWidth() + 2, pl_bmp.GetHeight() + 2))
        pa_btn = wx.BitmapButton(self, -1, wx.BitmapFromImage(pa_bmp), (px + bt * 3, py), (pa_bmp.GetWidth() + 2, pl_bmp.GetHeight() + 2))
        
        self.Bind(wx.EVT_BUTTON, self.play, pl_btn)
        self.Bind(wx.EVT_BUTTON, self.pause, pa_btn)
    
    def update(self, simul_clock):
        self.simul_st.SetLabel(str(round(simul_clock, 2)))
        
    def play(self, evt):
        self.Parent.timer.Start(TIMER_INTERVAL)
        
    def pause(self, evt):
        self.Parent.timer.Stop()

if __name__ == '__main__':
    app = wx.PySimpleApp()
    win = MainFrame()
    win.Show(True)
    app.MainLoop()
