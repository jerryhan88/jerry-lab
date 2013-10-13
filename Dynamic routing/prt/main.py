from __future__ import division
from classes import Node, Edge, Customer, PRT
from math import sqrt
import wx
from NN_algo import NN_algo

NODE_DIAMETER = 40
CUSTOMER_RADIUS = NODE_DIAMETER / 3
PRT_SIZE = 20

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
        self.op = OutputPanel(self, (f_sx - op_sx, 0), (op_sx, op_sy))
         
        vp_sx, vp_sy = f_sx - ip_sx - op_sx, f_sy * 0.89  
        self.vp = ViewPanel(self, (ip_px + ip_sx, ip_py), (vp_sx, vp_sy), self.op)
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
    def __init__(self, parent, pos, size, output_panel):
        wx.Panel.__init__(self, parent, -1, pos, size, style=wx.SUNKEN_BORDER)
        
        self.log_view = output_panel.log_view
        
        self.SetBackgroundColour(wx.WHITE)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Nodes = []
        self.Edges = []
        self.PRTs = []
        self.considered_cus = []
        self.NodeByNodeDistance_matrix = None
        
        sx, sy = self.GetSize()
        self.Nodes.append(Node(sx * 0.2, sy * 0.3))
        self.Nodes.append(Node(sx * 0.6, sy * 0.2))
        self.Nodes.append(Node(sx * 0.1, sy * 0.5))
        self.Nodes.append(Node(sx * 0.4, sy * 0.6))
        self.Nodes.append(Node(sx * 0.6, sy * 0.45))
        self.Nodes.append(Node(sx * 0.85, sy * 0.35))
        self.Nodes.append(Node(sx * 0.3, sy * 0.85))
        self.Nodes.append(Node(sx * 0.8, sy * 0.65))
        
        for i, j in [(0, 3), (0, 2), (0, 4), (1, 4), (1, 5), (2, 3), (3, 4), (3, 6), (4, 5), (4, 7), (5, 7), (6, 7)]:
            self.Edges.append(Edge(self.Nodes[i], self.Nodes[j]))
        
        for e in self.Edges[:]:
            e.gen_biDir(self.Edges)
        
        self.nn_algo = NN_algo(self.Nodes)
        
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
            cus = Customer(t, c, self.Nodes[sn], self.Nodes[dn])
            self.considered_cus.append(cus)
            self.Nodes[sn].cus_queue.append(cus)
            self.log_view.write('-------------------------------------------------------\n');
            self.log_view.write(' %s sec,    %s: N%s -> N%s \n' % (simul_clock, c, sn, dn));
        
#         if self.considered_cus:
            
        
        for v in [x for x in self.PRTs if x.state == 0]:
            target_n = self.nn_algo.find_NearestNode(v, self.Nodes)
            if target_n != None:
                for c in target_n.cus_queue:
                    if c.marked == False:
                        c.marked = True
                        break
                if v.arrived_n != target_n:
                    v.dest_n = target_n
                    v.path_n, v.path_e = self.nn_algo.find_SP(v.arrived_n, target_n, self.Nodes)
                    v.state = 1
                path_n, path_e = self.nn_algo.find_SP(target_n, target_n.cus_queue[0].dn, self.Nodes)
                if v.arrived_n == target_n:
                    v.dest_n = target_n.cus_queue[0].dn
                    v.riding_cus = target_n.cus_queue.pop(0)
                    v.state = 2
                v.path_n += path_n[1:]  
                v.path_e += path_e
                v.calc_btw_ns(CLOCK_INCREMENT, simul_clock)

        for v in self.PRTs:
            if v.arrived_n != v.target_n:
                v.update_pos(CLOCK_INCREMENT, simul_clock)
        self.RefreshGC()
        
    def Draw(self, gc):   
        old_tr = gc.GetTransform()
            
        for n in self.Nodes:
            gc.Translate(n.px, n.py)
            
            gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
            gc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
            gc.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            
            gc.DrawEllipse(-NODE_DIAMETER / 2, -NODE_DIAMETER / 2, NODE_DIAMETER, NODE_DIAMETER)
            gc.DrawText('N%d' % n.id, -7, -7)
            gc.DrawText('#c: %d' % len(n.cus_queue), -14, NODE_DIAMETER / 2)
            
            for c in n.cus_queue:
                bg_clr = wx.Colour(200, 200, 200)
                gc.SetBrush(wx.Brush(bg_clr))
                gc.SetPen(wx.Pen(bg_clr, 0.5))
                gc.DrawEllipse(-CUSTOMER_RADIUS / 2, -CUSTOMER_RADIUS / 2, CUSTOMER_RADIUS, CUSTOMER_RADIUS)
                gc.DrawText(c.id, -7, -7)
            
            gc.SetTransform(old_tr)
            
        for e in self.Edges[:len(self.Edges) // 2]:
            ax = e._to.px - e._from.px;
            ay = e._to.py - e._from.py;
            
            la = sqrt(ax * ax + ay * ay);
            ux = ax / la;
            uy = ay / la;
             
            sx = e._from.px + ux * NODE_DIAMETER / 2
            sy = e._from.py + uy * NODE_DIAMETER / 2
            ex = e._to.px - ux * NODE_DIAMETER / 2
            ey = e._to.py - uy * NODE_DIAMETER / 2
            
            
            px = -uy;
            py = ux;
                        
            gc.DrawLines([(sx, sy), (ex, ey)])
            gc.DrawLines([(ex, ey), (ex - int((ux * 5)) + int(px * 3), ey
                        - int(uy * 5) + int(py * 3))])
            
            gc.DrawLines([(ex, ey), (ex - int(ux * 5) - int(px * 3), ey
                        - int(uy * 5) - int(py * 3))])            
            
            gc.DrawText('%d' % int(round(e.distance, 1)), (e._from.px + e._to.px) / 2, (e._from.py + e._to.py) / 2)

        for v in self.PRTs:
            gc.Translate(v.px, v.py)
            
            gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
            gc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
            gc.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            gc.DrawRectangle(-PRT_SIZE / 2, -PRT_SIZE / 2, PRT_SIZE, PRT_SIZE)
            gc.DrawText('PRT%d' % v.id, -PRT_SIZE / 2, -PRT_SIZE / 2 - 10)
            
            if v.riding_cus:
                bg_clr = wx.Colour(200, 200, 200)
                gc.SetBrush(wx.Brush(bg_clr))
                gc.SetPen(wx.Pen(bg_clr, 0.5))
                gc.DrawEllipse(-CUSTOMER_RADIUS / 2, -CUSTOMER_RADIUS / 2, CUSTOMER_RADIUS, CUSTOMER_RADIUS)
                gc.DrawText(v.riding_cus.id, -7, -7)
            
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
        
        self.log_view = wx.TextCtrl(self, -1, "", pos=(2, sy + 4), size=(p_sx - 2, p_sy - sy - 40), style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
        self.log_view.SetEditable(False)
        self.log_view.SetBackgroundColour(wx.WHITE)

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
