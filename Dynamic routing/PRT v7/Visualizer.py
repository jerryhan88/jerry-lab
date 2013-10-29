from __future__ import division
from math import sqrt
from util import DragZoomPanel
import wx, Dynamics, Algorithms, Input_gen
from Dynamics import ST_IDLE, ST_APPROACHING, ST_TRANSITING, ST_PARKING
  

TIMER_INTERVAL = 100
CLOCK_INCREMENT = 100
CLOCK_INCR_DIFF = sqrt(2)

NODE_DIAMETER = 40
CUSTOMER_RADIUS = NODE_DIAMETER / 3
PRT_SIZE = 20

waiting_customers = []
event_queue = []

TITLE = 'PRT Simulator'

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, TITLE, size=(1024, 768), pos=(20, 20))
#         wx.Frame.__init__(self, None, -1, TITLE, size=(1920, 960), pos=(0, 0))
        # Every resources are accessible
        self.Nodes, self.Edges = Dynamics.gen_network(*Input_gen.network0())
        self.Customers = Dynamics.gen_customer(self.Nodes)
        self.PRTs = Dynamics.gen_PRT(Input_gen.PRT_pos_ex0(), self.Nodes)
        
        self.waiting_customers_in_node = [[] for _ in range(len(self.Nodes))]
        
        self.now = 0.0
        self.timer = wx.Timer(self)
        
        self.set_toolbar()
        
        s0 = wx.SplitterWindow(self, style=wx.SP_NOBORDER)
        s1 = wx.SplitterWindow(s0, style=wx.SP_NOBORDER)
        s2 = wx.SplitterWindow(s1, style=wx.SP_NOBORDER)
        
        ip = InputPanel(s0)
        s0.SplitVertically(ip, s1, 220)
        s0.SetMinimumPaneSize(20)
        
        self.mp = MeasurePanel(s1)
        
        s1.SplitVertically(s2, self.mp, -200)
        s1.SetSashGravity(1)
        
        self.vp = ViewPanel(s2)
        lp = LogPanel(s2)
        s2.SplitHorizontally(self.vp, lp, -200)
        s2.SetSashGravity(1)
        
        Dynamics.logger = lp.WriteLog

        Algorithms.on_notify_assignmentment_point = self.pause_clock_ressignement_point 
         
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        Dynamics.on_notify_customer_arrival = ip.on_notify_customer_arrival

        self.Show(True)
        
        dispatcher = self.select_dispatcher()
        if dispatcher == None:
            return
        
        Dynamics.init_dynamics(self.Nodes, self.PRTs, self.Customers, dispatcher)
        
        self.SetTitle(TITLE + ' - ' + dispatcher.__name__)
        
        self.vp.SetFocus()
        self.onTimer_counter = 0

    def select_dispatcher(self):
        AD = Algorithms.get_all_dispatchers()
        dlg = wx.SingleChoiceDialog(self, 'Select dispatcher:', 'Dispatcher Selection', sorted(AD), wx.CHOICEDLG_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            dispatcher = AD[dlg.GetStringSelection()]
            dlg.Destroy()
            
            self.timer.Start(TIMER_INTERVAL)
            
            return dispatcher
        else:
            self.Close()
    
    def pause_clock_ressignement_point(self, _):
        if self.check_reassign.GetValue():
            self.timer.Stop()
    
    def OnTimer(self, evt):
        self.now += CLOCK_INCREMENT / 1000
        if not Dynamics.process_events(self.now):
            self.OnPause(None)
        
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
                        break
                
                prev_n_arrival_time = prt.last_planed_time + sum(e.distance for e in prt.path_e[:edges_counter - 1]) / Dynamics.PRT_SPEED  
                
                dx = next_n.px - prev_n.px
                dy = next_n.py - prev_n.py
                cos_theta = dx / sqrt(dx * dx + dy * dy)
                sin_theta = dy / sqrt(dx * dx + dy * dy)
                
                prt.px = prev_n.px + cos_theta * (self.now - prev_n_arrival_time) * Dynamics.PRT_SPEED
                prt.py = prev_n.py + sin_theta * (self.now - prev_n_arrival_time) * Dynamics.PRT_SPEED
            else:
                prt.px, prt.py = prt.arrived_n.px, prt.arrived_n.py 
        
        self.waiting_customers_in_node = [[] for _ in range(len(self.Nodes))]
        for c in Dynamics.waiting_customers:
            self.waiting_customers_in_node[c.sn.id].append(c.id) 
        
        self.vp.RefreshGC()
        
        self.onTimer_counter += 1
        
        if self.onTimer_counter == 10:
            self.onTimer_counter = 0
            self.mp.update_stat()
                
    def OnPlay(self, _):
        self.timer.Start(TIMER_INTERVAL)

    def OnPause(self, _):
        self.timer.Stop()
        self.mp.update_stat()
        
    def OnSpeedUp(self, _):
        global CLOCK_INCREMENT
        CLOCK_INCREMENT *= CLOCK_INCR_DIFF
        self.vp.RefreshGC()
        
    def OnSpeedDown(self, _):
        global CLOCK_INCREMENT
        CLOCK_INCREMENT /= CLOCK_INCR_DIFF
        self.vp.RefreshGC()
        
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
        
        self.check_reassign = wx.CheckBox(tb, -1, "Check reassignment point", pos=(100, 5))
        self.Bind(wx.EVT_MENU, self.OnPlay, b_play)
        self.Bind(wx.EVT_MENU, self.OnPause, b_pause)
        self.Bind(wx.EVT_MENU, self.OnSpeedDown, b_s_down)
        self.Bind(wx.EVT_MENU, self.OnSpeedUp, b_s_up)
        
        tb.Realize()


measure_name = ['T.TravelDist', 'T.TravelDist', 'T.E.TravelDist', 'A.WaitTime', 'A.FlowTime']

class MeasurePanel(wx.ListCtrl):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.InsertColumn(0, 'Measure')
        self.InsertColumn(1, 'Value', wx.LIST_FORMAT_RIGHT)

        self.SetColumnWidth(0, 80)
        self.SetColumnWidth(1, 110)
        
        for i, mn in enumerate(measure_name):
            self.InsertStringItem(i, 'T.TravelDist')
            self.SetStringItem(i, 1, '%.1f' % 0.0)
        
        self.PRTs = self.Parent.Parent.Parent.PRTs
                
    def update_stat(self):
        
        TTD = 0.0
        ETD = 0.0
        TWT = 0.0
        numOfPickedUp_customer = 0
        TFT = 0.0
        numOfServiced_customer = 0
        
        for prt in self.PRTs:
            TTD += prt.total_travel_distance
            ETD += prt.empty_travel_distance
            TWT += prt.customers_waiting_time
            TFT += prt.customers_flow_time
            
            numOfPickedUp_customer += prt.numOfPickedUp_customer
            numOfServiced_customer += prt.numOfServiced_customer
        
        self.SetStringItem(0, 1, '%.1f' % TTD)
        self.SetStringItem(1, 1, '%.1f' % ETD)
        if numOfPickedUp_customer != 0:
            self.SetStringItem(2, 1, '%.1f' % (TWT / numOfPickedUp_customer))
        if numOfServiced_customer != 0:    
            self.SetStringItem(3, 1, '%.1f' % (TFT / numOfServiced_customer))
        
        self.Refresh()
            
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
                
    def on_notify_customer_arrival(self, customer):
        if customer.id != 0:
            self.SetItemBackgroundColour(customer.id - 1, wx.Colour(255, 255, 255))
        self.SetItemBackgroundColour(customer.id, wx.Colour(200, 200, 200))
        
        self.Refresh()

class LogPanel(wx.TextCtrl):
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
    
    def OnMouseWheel(self, e):
        if e.ControlDown():
            win.OnSpeedUp(None) if e.m_wheelRotation > 0 else win.OnSpeedDown(None)
        else:
            DragZoomPanel.OnMouseWheel(self, e)
        # self.set_scale(self.scale * (self.scale_inc if e.m_wheelRotation > 0 else (1 / self.scale_inc)), e.m_x, e.m_y)
        # self.RefreshGC()

    def OnDrawDevice(self, gc):
        gc.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        gc.DrawText('%.1f (%.1fX)' % (self.Parent.Parent.Parent.Parent.now, CLOCK_INCREMENT / TIMER_INTERVAL), 5, 3)
    
    def OnDraw(self, gc):
        old_tr = gc.GetTransform()
        
        for n in self.Parent.Parent.Parent.Parent.Nodes:
            if not n.isStation:
                continue
            gc.Translate(n.px, n.py)
            
            gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
            gc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
            gc.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            
            gc.DrawEllipse(-NODE_DIAMETER / 2, -NODE_DIAMETER / 2, NODE_DIAMETER, NODE_DIAMETER)
            if n.isStation:
                gc.DrawText('N%d' % n.id, -7, -7)
            gc.SetTransform(old_tr)
            
        for i, waiting_c_in_node in enumerate(self.Parent.Parent.Parent.Parent.waiting_customers_in_node):
            if waiting_c_in_node:
                waiting_c_str = '[' + ':'.join(('C%d' % c_id) for c_id in waiting_c_in_node) + ']'
                gc.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                gc.DrawText(waiting_c_str, self.Parent.Parent.Parent.Parent.Nodes[i].px + NODE_DIAMETER / 2, self.Parent.Parent.Parent.Parent.Nodes[i].py - NODE_DIAMETER / 2)
        
        for e in self.Parent.Parent.Parent.Parent.Edges:
            prev_n, next_n = e._from, e._to
            
            if prev_n.isStation and not next_n.isStation:
                ax = next_n.px - prev_n.px
                ay = next_n.py - prev_n.py
                
                la = sqrt(ax * ax + ay * ay)
                ux = ax / la
                uy = ay / la
                 
                sx = prev_n.px + ux * NODE_DIAMETER / 2
                sy = prev_n.py + uy * NODE_DIAMETER / 2
                ex = next_n.px
                ey = next_n.py
                            
                gc.DrawLines([(sx, sy), (ex, ey)])
                gc.SetFont(wx.Font(5, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                gc.DrawText('%d' % int(round(e.distance, 1)), (prev_n.px + next_n.px) / 2, (prev_n.py + next_n.py) / 2)
                
            elif not prev_n.isStation and not next_n.isStation:
                sx = prev_n.px
                sy = prev_n.py
                ex = next_n.px
                ey = next_n.py
                gc.DrawLines([(sx, sy), (ex, ey)])
                gc.SetFont(wx.Font(5, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                gc.DrawText('%d' % int(round(e.distance, 1)), (prev_n.px + next_n.px) / 2, (prev_n.py + next_n.py) / 2)
                    
            elif not prev_n.isStation and next_n.isStation:
                ax = next_n.px - prev_n.px
                ay = next_n.py - prev_n.py
                
                la = sqrt(ax * ax + ay * ay)
                ux = ax / la
                uy = ay / la
                
                sx = prev_n.px
                sy = prev_n.py
                ex = next_n.px - ux * NODE_DIAMETER / 2
                ey = next_n.py - uy * NODE_DIAMETER / 2
                
                px = -uy
                py = ux
                            
                gc.DrawLines([(sx, sy), (ex, ey)])
                gc.DrawLines([(ex, ey), (ex - int((ux * 5)) + int(px * 3), ey
                            - int(uy * 5) + int(py * 3))])
                
                gc.DrawLines([(ex, ey), (ex - int(ux * 5) - int(px * 3), ey
                            - int(uy * 5) - int(py * 3))])
                gc.SetFont(wx.Font(5, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                gc.DrawText('%d' % int(round(e.distance, 1)), (prev_n.px + next_n.px) / 2, (prev_n.py + next_n.py) / 2)
            
            if prev_n.isStation and next_n.isStation: 
                ax = next_n.px - prev_n.px
                ay = next_n.py - prev_n.py
                
                la = sqrt(ax * ax + ay * ay)
                ux = ax / la
                uy = ay / la
                 
                sx = prev_n.px + ux * NODE_DIAMETER / 2
                sy = prev_n.py + uy * NODE_DIAMETER / 2
                ex = next_n.px - ux * NODE_DIAMETER / 2
                ey = next_n.py - uy * NODE_DIAMETER / 2
                
                px = -uy
                py = ux
                            
                gc.DrawLines([(sx, sy), (ex, ey)])
                gc.DrawLines([(ex, ey), (ex - int((ux * 5)) + int(px * 3), ey
                            - int(uy * 5) + int(py * 3))])
                
                gc.DrawLines([(ex, ey), (ex - int(ux * 5) - int(px * 3), ey
                            - int(uy * 5) - int(py * 3))])           
                
                gc.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                gc.DrawText('%d' % int(round(e.distance, 1)), (prev_n.px + next_n.px) / 2, (prev_n.py + next_n.py) / 2)
            
        for v in self.Parent.Parent.Parent.Parent.PRTs:
            gc.Translate(v.px, v.py)
            
            gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
            if v.state == ST_IDLE:
                # IDLE PRT's color is GRAY
                gc.SetBrush(wx.Brush(wx.Colour(200, 200, 200)))
            elif v.state == ST_APPROACHING:
                # APPROACHING PRT's color is WHITE
                gc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
            elif v.state == ST_TRANSITING:
                # TRANSITING PRT's color is PINK
                gc.SetBrush(wx.Brush(wx.Colour(255, 193, 193))) 
            else:
                assert v.state == ST_PARKING
                # PARKING PRT's color is YELLOW
                gc.SetBrush(wx.Brush(wx.Colour(255, 242, 0)))
            
            gc.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            gc.DrawRectangle(-PRT_SIZE / 2, -PRT_SIZE / 2, PRT_SIZE, PRT_SIZE)
            gc.DrawText('PRT%d' % v.id, -PRT_SIZE / 2, -PRT_SIZE / 2 - 10)
            
            if v.assigned_customer:
                assert v.state == ST_APPROACHING
                gc.DrawText('C%d' % v.assigned_customer.id, -7, -7)                

            if v.transporting_customer:
                bg_clr = wx.Colour(255, 255, 0)
                gc.SetBrush(wx.Brush(bg_clr))
                gc.SetPen(wx.Pen(bg_clr, 0.5))
                gc.DrawEllipse(-CUSTOMER_RADIUS / 2, -CUSTOMER_RADIUS / 2, CUSTOMER_RADIUS, CUSTOMER_RADIUS)
                gc.DrawText('C%d' % v.transporting_customer.id, -7, -7)
            
            gc.SetTransform(old_tr)
            
    
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    win = MainFrame()
    win.Show(True)
    app.MainLoop()

