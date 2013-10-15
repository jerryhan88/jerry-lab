from __future__ import division

from math import sqrt
from classes import Node, Edge, Customer, PRT
from util import DragZoomPanel
import wx

REQUEST = []

TIMER_INTERVAL = 100
CLOCK_INCREMENT = 100
CLOCK_INCR_DIFF = sqrt(2)

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Dynamic routing experiment', size=(1024, 768))
        
        self.set_toolbar()

        self.simul_clock = 0
        self.timer = wx.Timer(self)
#         self.timer.Start(TIMER_INTERVAL)
        
        s0 = wx.SplitterWindow(self, style=wx.SP_NOBORDER)
        s1 = wx.SplitterWindow(s0, style=wx.SP_NOBORDER)
        op = OutputPanel(s0)
        s0.SplitHorizontally(s1, op, -200)
        s0.SetMinimumPaneSize(20)
        s0.SetSashGravity(1)
        ip = InputPanel(s1)
        self.vp = ViewPanel(s1, op)
        s1.SplitVertically(ip, self.vp, 250)
        s1.SetMinimumPaneSize(20)
        
        self.Show(True)
        
        self.vp.SetFocus()
        
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
    def set_toolbar(self):
        def load_icon(path):
            bmp = wx.Bitmap(path, wx.BITMAP_TYPE_BMP)
            bmp.SetMaskColour(wx.Color(0, 128, 128))
            return bmp
        tb = self.CreateToolBar()
        b_play = tb.AddSimpleTool(wx.ID_ANY, load_icon('pic/play.bmp'))
        b_pause = tb.AddSimpleTool(wx.ID_ANY, load_icon('pic/pause.bmp'))
        # b_s_up = tb.AddSimpleTool(wx.ID_ANY, load_icon('pic/speed_up.bmp'))
        # b_s_down = tb.AddSimpleTool(wx.ID_ANY, load_icon('pic/speed_down.bmp'))
        self.Bind(wx.EVT_MENU, self.OnPlay, b_play)
        self.Bind(wx.EVT_MENU, self.OnPause, b_pause)
        # self.Bind(wx.EVT_MENU, self.OnSpeedUp, b_s_up)
        # self.Bind(wx.EVT_MENU, self.OnSpeedDown, b_s_down)
        tb.Realize()

    def OnTimer(self, evt):
        self.simul_clock += CLOCK_INCREMENT / 1000
        self.vp.update(self.simul_clock)
        # self.cp.update(self.simul_clock)
    
    def OnPlay(self, _):
        self.timer.Start(TIMER_INTERVAL)

    def OnPause(self, _):
        self.timer.Stop()
        
    def OnSpeedUp(self, _):
        global CLOCK_INCREMENT
        CLOCK_INCREMENT *= CLOCK_INCR_DIFF
        
    def OnSpeedDown(self, _):
        global CLOCK_INCREMENT
        CLOCK_INCREMENT /= CLOCK_INCR_DIFF
        
    def OnClose(self, event):
        self.Destroy()

class ViewPanel(DragZoomPanel):
    def __init__(self, parent, op):
        DragZoomPanel.__init__(self, parent, -1, style=wx.SUNKEN_BORDER)
        self.op = op
        self.SetBackgroundColour(wx.WHITE)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        self.Nodes = []
        self.Edges = []
        self.PRTs = []
        
        sx, sy = 800, 800
        
        self.Nodes.append(Node(sx * 0.1, sy * 0.1))
        self.Nodes.append(Node(sx * 0.4, sy * 0.1))
        self.Nodes.append(Node(sx * 0.75, sy * 0.1))
        self.Nodes.append(Node(sx * 0.1, sy * 0.3))
        self.Nodes.append(Node(sx * 0.4, sy * 0.3))
        self.Nodes.append(Node(sx * 0.75, sy * 0.3))
        self.Nodes.append(Node(sx * 1.0, sy * 0.3))
        self.Nodes.append(Node(sx * 0.1, sy * 0.62))
        self.Nodes.append(Node(sx * 0.4, sy * 0.62))
        self.Nodes.append(Node(sx * 0.75, sy * 0.62))
        self.Nodes.append(Node(sx * 1.0, sy * 0.62))
        
        for i, j in [(1, 0), (1, 2), (3, 4), (5, 4), (5, 6), (8, 7), (8, 9), (10, 9), (0, 3), (4, 1), (2, 5), (7, 3), (4, 8), (9, 5), (6, 10)]:
            self.Edges.append(Edge(self.Nodes[i], self.Nodes[j]))

        self.PRTs.append(PRT())
        self.PRTs[-1].init_position(self.Nodes[4])
        self.PRTs.append(PRT())
        self.PRTs[-1].init_position(self.Nodes[0])
        self.PRTs.append(PRT())
        self.PRTs[-1].init_position(self.Nodes[1])
        self.PRTs.append(PRT())
        self.PRTs[-1].init_position(self.Nodes[8])
    
    def update(self, simul_clock):
        while REQUEST and REQUEST[0][0] <= simul_clock:
            t, c, sn, dn = REQUEST.pop(0)
            self.Nodes[sn].cus_queue.append(Customer(t, c, self.Nodes[sn], self.Nodes[dn]))
            self.op.write(' %s sec, Request of customer %s: N%s -> N%s\n' % (simul_clock, c, sn, dn));
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
            target_n = PRT.find_NearestNode(v, self.Nodes)
            if target_n != None:
                for c in target_n.cus_queue:
                    if c.marked == False:
                        c.marked = True
                        break
                if v.arrived_n != target_n:
                    v.dest_n = target_n
                    v.path_n, v.path_e = PRT.find_SP(v.arrived_n, target_n, self.Nodes)
                    v.state = 1
                    self.op.write(' %s sec, PRT%d is going to N%d\n' % (simul_clock, v.id, target_n.id));
                    
                path_n, path_e = PRT.find_SP(target_n, target_n.cus_queue[0].dn, self.Nodes)
                if v.arrived_n == target_n:
                    v.dest_n = target_n.cus_queue[0].dn
                    v.riding_cus = target_n.cus_queue.pop(0)
                    v.state = 2
                    self.op.write(' %s sec, PRT%d is departing from N%d with %s\n' % (simul_clock, v.id, v.dest_n.id, v.riding_cus.id));
                v.path_n += path_n[1:]  
                v.path_e += path_e
                v.calc_btw_ns(CLOCK_INCREMENT, simul_clock)
                

        for v in self.PRTs:
            if v.arrived_n != v.target_n:
                v.update_pos(CLOCK_INCREMENT, simul_clock, self.op)

        self.RefreshGC()

    def OnDrawDevice(self, gc):
        gc.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        gc.DrawText('%.1f (%.1fX)' % (self.Parent.Parent.Parent.simul_clock, CLOCK_INCREMENT / TIMER_INTERVAL), 5, 3)
        
    def OnDraw(self, gc):
        old_tr = gc.GetTransform()
        
        gc.SetTransform(old_tr)
        for e in self.Edges:
            e.draw(gc)
        
        for n in self.Nodes:
            gc.Translate(n.px, n.py)
            n.draw(gc)
            gc.SetTransform(old_tr)

        for v in self.PRTs:
            gc.SetTransform(old_tr)    
            gc.Translate(v.px, v.py)
            v.draw(gc)

class InputPanel(wx.ListCtrl):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        # self.SetFont(wx.Font(12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT))

        # self.request_view = wx.ListCtrl(self, -1, pos=(2, sy + 4), size=(p_sx - 2, p_sy - sy - 40), style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.InsertColumn(0, 'Customer')
        self.InsertColumn(1, 'Time')
        self.InsertColumn(2, 'From')
        self.InsertColumn(3, 'To')
        
        self.SetColumnWidth(0, 70)
        self.SetColumnWidth(1, 60)
        self.SetColumnWidth(2, 40)
        self.SetColumnWidth(3, 40)
        
        rowCount = 0
        with open('Input', 'r') as fp:
            for line in fp:
                c, t_s, sd = line.split(',')
                t = str(round(float(t_s), 1))
                sn, dn = sd.split('-')
                self.InsertStringItem(rowCount, c)
                self.SetStringItem(rowCount, 1, t)
                self.SetStringItem(rowCount, 2, sn)
                self.SetStringItem(rowCount, 3, dn)
                rowCount += 1
                REQUEST.append((round(float(t_s), 1), c, int(sn), int(dn)))

class OutputPanel(wx.TextCtrl):
    def __init__(self, parent):
        wx.TextCtrl.__init__(self, parent, -1, style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
        self.SetFont(wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT))
        self.SetEditable(False)

if __name__ == '__main__':
    app = wx.PySimpleApp()
    win = MainFrame()
    win.Show(True)
    app.MainLoop()
