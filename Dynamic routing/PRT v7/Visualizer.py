from __future__ import division
from math import sqrt
from util import DragZoomPanel
import wx, Dynamics, Algorithms, Input_gen 

TIMER_INTERVAL = 100
CLOCK_INCREMENT = 100
CLOCK_INCR_DIFF = sqrt(2)

NODE_DIAMETER = 40
CUSTOMER_RADIUS = NODE_DIAMETER / 3
PRT_SIZE = 20

PRT_SPEED = 20
waiting_customers = []
event_queue = []

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Dynamic routing experiment', size=(1024, 768))
        # Every resources are accessible
        self.Nodes, self.Edges = Dynamics.gen_network(*Input_gen.network0())
        self.Customers = Dynamics.gen_customer(self.Nodes)
        self.PRTs = Dynamics.gen_PRT(Input_gen.PRT_pos_ex0(), self.Nodes)
        dispatcher = Algorithms.NN0
#         dispatcher = Algorithms.NN1
#         dispatcher = Algorithms.NN2
#         dispatcher = Algorithms.NN3
#         dispatcher = Algorithms.NN4
#         dispatcher = Algorithms.NN5
        Dynamics.init_dynamics(self.Nodes, self.PRTs, self.Customers, dispatcher)
        
        self.now = 0.0
        self.timer = wx.Timer(self)
        
        self.set_toolbar()
        s0 = wx.SplitterWindow(self, style=wx.SP_NOBORDER)
        s1 = wx.SplitterWindow(s0, style=wx.SP_NOBORDER)
        op = OutputPanel(s0)
        s0.SplitHorizontally(s1, op, -200)
        s0.SetMinimumPaneSize(20)
        s0.SetSashGravity(1)
        ip = InputPanel(s1)
        self.vp = ViewPanel(s1)
        s1.SplitVertically(ip, self.vp, 220)
        s1.SetMinimumPaneSize(20)
        self.Show(True)
        self.vp.SetFocus()
        Dynamics.logger = op.WriteLog
        
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnTimer(self, evt):
        self.now += CLOCK_INCREMENT / 1000
        Dynamics.process_events(self.now)
        
        # Update positions of PRTs
        for prt in self.PRTs:
            if prt.path_e:
                path_travel_distance = (self.now - prt.last_planed_time) * Dynamics.PRT_SPEED
                sum_edges_distance = 0
                edges_counter = 0
                
                prev_n, next_n = None, None
            
                for e in prt.path_e:
                    sum_edges_distance += e.distance
                    edges_counter += 1 
                    if sum_edges_distance >= path_travel_distance:
                        prev_n = e._from
                        next_n = e._to
                
                prev_n_arrival_time = prt.last_planed_time + sum(e.distance for e in prt.path_e[:edges_counter - 1]) / Dynamics.PRT_SPEED  
    
                dx = next_n.px - prev_n.px
                dy = next_n.py - prev_n.py
                cos_theta = dx / sqrt(dx * dx + dy * dy)
                sin_theta = dy / sqrt(dx * dx + dy * dy)
                
                prt.px = prev_n.px + cos_theta * (self.now - prev_n_arrival_time) * Dynamics.PRT_SPEED
                prt.py = prev_n.py + sin_theta * (self.now - prev_n_arrival_time) * Dynamics.PRT_SPEED
            else:
                prt.px, prt.py = prt.arrived_n.px, prt.arrived_n.py 
        
        self.vp.RefreshGC()
                
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
        
    def set_toolbar(self):
        def load_icon(path):
            bmp = wx.Bitmap(path, wx.BITMAP_TYPE_BMP)
            bmp.SetMaskColour(wx.Color(0, 128, 128))
            return bmp
        tb = self.CreateToolBar()
        b_play = tb.AddSimpleTool(wx.ID_ANY, load_icon('pic/play.bmp'))
        b_pause = tb.AddSimpleTool(wx.ID_ANY, load_icon('pic/pause.bmp'))
        b_s_down = tb.AddSimpleTool(wx.ID_ANY, load_icon('pic/speed_down.bmp'))
        b_s_up = tb.AddSimpleTool(wx.ID_ANY, load_icon('pic/speed_up.bmp'))
        self.Bind(wx.EVT_MENU, self.OnPlay, b_play)
        self.Bind(wx.EVT_MENU, self.OnPause, b_pause)
        self.Bind(wx.EVT_MENU, self.OnSpeedDown, b_s_down)
        self.Bind(wx.EVT_MENU, self.OnSpeedUp, b_s_up)
        
        tb.Realize()        

class InputPanel(wx.ListCtrl):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.InsertColumn(0, 'Customer')
        self.InsertColumn(1, 'Time')
        self.InsertColumn(2, 'From')
        self.InsertColumn(3, 'To')
        
        self.SetColumnWidth(0, 65)
        self.SetColumnWidth(1, 45)
        self.SetColumnWidth(2, 43)
        self.SetColumnWidth(3, 43)
        
        rowCount = 0
        with open('Info. Arrivals of customers.txt', 'r') as fp:
            for line in fp:
                arrival_time_str, sd = line.split(',')
                sn, dn = sd.split('-')
                arrival_time = float(arrival_time_str)
                self.InsertStringItem(rowCount, 'C%d' % rowCount)
                self.SetStringItem(rowCount, 1, '%.1f' % arrival_time)
                self.SetStringItem(rowCount, 2, sn)
                self.SetStringItem(rowCount, 3, dn)
                rowCount += 1

class OutputPanel(wx.TextCtrl):
    def __init__(self, parent):
        wx.TextCtrl.__init__(self, parent, -1, style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
        self.SetFont(wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT))
        self.SetEditable(False)
        
    def WriteLog(self, s):
        self.write(' %s\n' % s);

class ViewPanel(DragZoomPanel):
    def __init__(self, parent):
        DragZoomPanel.__init__(self, parent, -1, style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour(wx.WHITE)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
    
    def OnDrawDevice(self, gc):
        gc.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        gc.DrawText('%.1f (%.1fX)' % (self.Parent.Parent.Parent.now, CLOCK_INCREMENT / TIMER_INTERVAL), 5, 3)
    
    def OnDraw(self, gc):
        old_tr = gc.GetTransform()
        
        for n in self.Parent.Parent.Parent.Nodes:
            gc.Translate(n.px, n.py)
            
            gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
            gc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
            gc.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            
            gc.DrawEllipse(-NODE_DIAMETER / 2, -NODE_DIAMETER / 2, NODE_DIAMETER, NODE_DIAMETER)
            gc.DrawText('N%d' % n.id, -7, -7)
#             gc.DrawText('#c: %d' % len(n.cus_queue), -14, NODE_DIAMETER / 2)
            
#             for c in n.cus_queue:
#                 bg_clr = wx.Colour(200, 200, 200)
#                 gc.SetBrush(wx.Brush(bg_clr))
#                 gc.SetPen(wx.Pen(bg_clr, 0.5))
#                 gc.DrawEllipse(-CUSTOMER_RADIUS / 2, -CUSTOMER_RADIUS / 2, CUSTOMER_RADIUS, CUSTOMER_RADIUS)
#                 gc.DrawText(c.id, -7, -7)
            gc.SetTransform(old_tr)
            
        for e in self.Parent.Parent.Parent.Edges:
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
            
        for v in self.Parent.Parent.Parent.PRTs:
            gc.Translate(v.px, v.py)
            
            gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
            gc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
            gc.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            gc.DrawRectangle(-PRT_SIZE / 2, -PRT_SIZE / 2, PRT_SIZE, PRT_SIZE)
            gc.DrawText('PRT%d' % v.id, -PRT_SIZE / 2, -PRT_SIZE / 2 - 10)
            
#             if v.riding_cus:
#                 bg_clr = wx.Colour(200, 200, 200)
#                 gc.SetBrush(wx.Brush(bg_clr))
#                 gc.SetPen(wx.Pen(bg_clr, 0.5))
#                 gc.DrawEllipse(-CUSTOMER_RADIUS / 2, -CUSTOMER_RADIUS / 2, CUSTOMER_RADIUS, CUSTOMER_RADIUS)
#                 gc.DrawText(v.riding_cus.id, -7, -7)
            
            gc.SetTransform(old_tr)
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    win = MainFrame()
    win.Show(True)
    app.MainLoop()

