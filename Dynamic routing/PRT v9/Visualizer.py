from __future__ import division
from math import sqrt
from util import DragZoomPanel
import wx, Dynamics, Algorithms, Network
from Dynamics import ST_IDLE, ST_APPROACHING, ST_TRANSITING, ST_PARKING, STATION
  

TIMER_INTERVAL = 100
CLOCK_INCREMENT = 100
CLOCK_INCR_DIFF = sqrt(2)

STATION_DIAMETER = 30
JUNCTION_DIAMETER = STATION_DIAMETER / 4
CUSTOMER_RADIUS = STATION_DIAMETER / 3
PRT_SIZE = STATION_DIAMETER / 5

waiting_customers = []
event_queue = []

TITLE = 'PRT Simulator'

class MainFrame(wx.Frame):
    def __init__(self):
#         wx.Frame.__init__(self, None, -1, TITLE, size=(1024, 768), pos=(20, 20))
        wx.Frame.__init__(self, None, -1, TITLE, size=(1920, 960), pos=(0, 0))
        # Every resources are accessible
        self.Nodes, self.Edges = Dynamics.Network1()
#         gen_Network(*Network.network0())
        
        
        self.Customers = Dynamics.gen_Customer(2.5, 2000, self.Nodes)
        self.NumOfTotalCustomer = len(self.Customers)
        self.PRTs = Dynamics.gen_PRT(10, self.Nodes)
        
        self.idlePRT_in_node = {}
        for n in self.Nodes:
            if n.nodeType == STATION:
                self.idlePRT_in_node[n.id] = []
        
        self.waiting_customers_in_node = {}
        for n in self.Nodes:
            if n.nodeType == STATION:
                self.waiting_customers_in_node[n.id] = []
        
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
        
        self.idlePRT_in_node = {}
        for n in self.Nodes:
            if n.nodeType == STATION:
                self.idlePRT_in_node[n.id] = []
        
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
                self.idlePRT_in_node[prt.arrived_n.id].append(prt.id)
        
        self.waiting_customers_in_node = {}
        for n in self.Nodes:
            if n.nodeType == STATION:
                self.waiting_customers_in_node[n.id] = []
        
        for c in Dynamics.waiting_customers:
            self.waiting_customers_in_node[c.sn.id].append(c.id) 
        self.vp.RefreshGC()
        
        
        self.onTimer_counter += 1
        
        if self.onTimer_counter == 10:
            self.onTimer_counter = 0
            self.mp.update_stat(self.now)
                
    def OnPlay(self, _):
        self.timer.Start(TIMER_INTERVAL)

    def OnPause(self, _):
        self.timer.Stop()
        self.mp.update_stat(self.now)
        
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
        self.show_distance = wx.CheckBox(tb, -1, "Show distance", pos=(265, 5))
        self.Bind(wx.EVT_MENU, self.OnPlay, b_play)
        self.Bind(wx.EVT_MENU, self.OnPause, b_pause)
        self.Bind(wx.EVT_MENU, self.OnSpeedDown, b_s_down)
        self.Bind(wx.EVT_MENU, self.OnSpeedUp, b_s_up)
        
        tb.Realize()


StaticInfo, NumOfStations, NumOfPRTs, TotalCustomer, AboutCustomer, CustomerArrivals, WaitingCustomers, PickedUpCustomers, ServicedCustomers, WaitingTime, WTTotal, WTAverage, WTMaximum, FlowTime, FTTotal, FTAverage, TravelDistance, TDTotal, TDAverage, EmptyTravelDistance, ETDTotal, ETDAverage, StateDuration, Idle, Approaching, Transiting, Parking = range(27)
 

measure_name = ['T.TravelDist', 'T.TravelDist', 'T.E.TravelDist', 'A.WaitTime', 'A.FlowTime']

class MeasurePanel(wx.ListCtrl):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.InsertColumn(0, 'Title')
        self.InsertColumn(1, 'Value', wx.LIST_FORMAT_RIGHT)

        self.SetColumnWidth(0, 90)
        self.SetColumnWidth(1, 90)
        bg_clr = wx.Colour(220, 220, 220)
        self.InsertStringItem(StaticInfo, 'Static informations')
        self.SetStringItem(StaticInfo, 1, '   ')
        self.SetItemBackgroundColour(StaticInfo, bg_clr)
        self.InsertStringItem(NumOfStations, 'Stations')
        self.SetStringItem(NumOfStations, 1, '%d' % len([n for n in self.Parent.Parent.Parent.Nodes if n.nodeType == Dynamics.STATION]))
            
        self.InsertStringItem(NumOfPRTs, 'PRTs')
        self.SetStringItem(NumOfPRTs, 1, '%d' % len(self.Parent.Parent.Parent.PRTs))
         
        self.InsertStringItem(TotalCustomer, 'T. Customers')
        self.SetStringItem(TotalCustomer, 1, '%d' % self.Parent.Parent.Parent.NumOfTotalCustomer)
         
        self.InsertStringItem(AboutCustomer, 'About Cusomer')
        self.SetStringItem(AboutCustomer, 1, '   ')
        self.SetItemBackgroundColour(AboutCustomer, bg_clr)
        self.InsertStringItem(CustomerArrivals, 'C. Arrivals')
        self.SetStringItem(CustomerArrivals, 1, '%d' % Dynamics.NumOfCustomerArrivals)
        self.InsertStringItem(WaitingCustomers, 'Waiting Customers')
        self.SetStringItem(WaitingCustomers, 1, '%d' % len(Dynamics.waiting_customers))
        self.InsertStringItem(PickedUpCustomers, 'PickedUp Customers')
        self.SetStringItem(PickedUpCustomers, 1, '%d' % Dynamics.NumOfPickedUpCustomer)
        self.InsertStringItem(ServicedCustomers, 'Serviced Customers')
        self.SetStringItem(ServicedCustomers, 1, '%d' % Dynamics.NumOfServicedCustomer)
         
        self.InsertStringItem(WaitingTime, 'Waiting Time')
        self.SetStringItem(WaitingTime, 1, '   ')
        self.SetItemBackgroundColour(WaitingTime, bg_clr)
        self.InsertStringItem(WTTotal, 'Total')
        self.SetStringItem(WTTotal, 1, '%.1f' % Dynamics.Total_customers_waiting_time)
        self.InsertStringItem(WTAverage, 'Average')
        self.SetStringItem(WTAverage, 1, '%.1f' % 0.0)
        self.InsertStringItem(WTMaximum, 'Maximum')
        self.SetStringItem(WTMaximum, 1, '%.1f' % Dynamics.MaxCustomerWaitingTime)
         
        self.InsertStringItem(FlowTime, 'Flow Time')
        self.SetStringItem(FlowTime, 1, '   ')
        self.SetItemBackgroundColour(FlowTime, bg_clr)
        self.InsertStringItem(FTTotal, 'Total')
        self.SetStringItem(FTTotal, 1, '%.1f' % Dynamics.Total_customers_flow_time)
        self.InsertStringItem(FTAverage, 'Average')
        self.SetStringItem(FTAverage, 1, '%.1f' % 0.0)
         
        self.InsertStringItem(TravelDistance, 'Travel Distance')
        self.SetStringItem(TravelDistance, 1, '   ')
        self.SetItemBackgroundColour(TravelDistance, bg_clr)
        self.InsertStringItem(TDTotal, 'Total')
        self.SetStringItem(TDTotal, 1, '%.1f' % Dynamics.Total_travel_distance)
        self.InsertStringItem(TDAverage, 'Average')
        self.SetStringItem(TDAverage, 1, '%.1f' % 0.0)
         
        self.InsertStringItem(EmptyTravelDistance, 'E. T. Distance')
        self.SetStringItem(EmptyTravelDistance, 1, '   ')
        self.SetItemBackgroundColour(EmptyTravelDistance, bg_clr)
        self.InsertStringItem(ETDTotal, 'Total')
        self.SetStringItem(ETDTotal, 1, '%.1f' % Dynamics.Total_empty_travel_distance)
        self.InsertStringItem(ETDAverage, 'Average')
        self.SetStringItem(ETDAverage, 1, '%.1f' % 0.0)
         
        self.InsertStringItem(StateDuration, 'State Duration')
        self.SetStringItem(StateDuration, 1, '   ')
        self.SetItemBackgroundColour(StateDuration, bg_clr)
        self.InsertStringItem(Idle, 'Idle')
        self.SetStringItem(Idle, 1, '%.1f' % Dynamics.IdleState_time)
        self.InsertStringItem(Approaching, 'Approaching')
        self.SetStringItem(Approaching, 1, '%.1f' % Dynamics.ApproachingState_time)
        self.InsertStringItem(Transiting, 'Transiting')
        self.SetStringItem(Transiting, 1, '%.1f' % Dynamics.TransitingState_time)
        self.InsertStringItem(Parking, 'Parking')
        self.SetStringItem(Parking, 1, '%.1f' % Dynamics.ParkingState_time)
                
    def update_stat(self, cur_time):
        self.SetStringItem(CustomerArrivals, 1, '%d' % Dynamics.NumOfCustomerArrivals)
        self.SetStringItem(WaitingCustomers, 1, '%d' % len(Dynamics.waiting_customers))
        self.SetStringItem(PickedUpCustomers, 1, '%d' % Dynamics.NumOfPickedUpCustomer)
        self.SetStringItem(ServicedCustomers, 1, '%d' % Dynamics.NumOfServicedCustomer)
        
        self.SetStringItem(WTTotal, 1, '%.1f' % Dynamics.Total_customers_waiting_time)
        if cur_time != 0:
            self.SetStringItem(WTAverage, 1, '%.1f' % (Dynamics.Total_customers_waiting_time / cur_time))
        self.SetStringItem(WTMaximum, 1, '%.1f' % Dynamics.MaxCustomerWaitingTime)
        
        self.SetStringItem(FTTotal, 1, '%.1f' % Dynamics.Total_customers_flow_time)
        self.SetStringItem(TDTotal, 1, '%.1f' % Dynamics.Total_travel_distance)
        if Dynamics.NumOfServicedCustomer != 0:
            self.SetStringItem(FTAverage, 1, '%.1f' % (Dynamics.Total_customers_flow_time / Dynamics.NumOfServicedCustomer))
            self.SetStringItem(TDAverage, 1, '%.1f' % (Dynamics.Total_travel_distance / Dynamics.NumOfServicedCustomer))
        
        self.SetStringItem(ETDTotal, 1, '%.1f' % Dynamics.Total_empty_travel_distance)
        if Dynamics.NumOfPickedUpCustomer != 0:
            self.SetStringItem(ETDAverage, 1, '%.1f' % (Dynamics.Total_empty_travel_distance / Dynamics.NumOfPickedUpCustomer))
        
        self.SetStringItem(Idle, 1, '%.1f' % Dynamics.IdleState_time)
        self.SetStringItem(Approaching, 1, '%.1f' % Dynamics.ApproachingState_time)
        self.SetStringItem(Transiting, 1, '%.1f' % Dynamics.TransitingState_time)
        self.SetStringItem(Parking, 1, '%.1f' % Dynamics.ParkingState_time)
        
        self.Refresh()
            
class InputPanel(wx.ListCtrl):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.InsertColumn(0, 'Customer')
        self.InsertColumn(1, 'Time', wx.LIST_FORMAT_RIGHT)
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
        self.EnsureVisible(customer.id)
        
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
        from Dynamics import STATION, JUNCTION, DOT
        global STATION, JUNCTION, DOT
    
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
            gc.Translate(n.px, n.py)
            if n.nodeType == STATION:
                gc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
                gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
                gc.DrawEllipse(-STATION_DIAMETER / 2, -STATION_DIAMETER / 2, STATION_DIAMETER, STATION_DIAMETER)
                gc.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                if len(n.id) > 1:
                    gc.DrawText('%s' % n.id, -7, -8)
                else:
                    gc.DrawText('%s' % n.id, -3, -8)
            elif n.nodeType == JUNCTION:
                gc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
                gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 0.01))
                gc.DrawEllipse(-JUNCTION_DIAMETER / 2, -JUNCTION_DIAMETER / 2, JUNCTION_DIAMETER, JUNCTION_DIAMETER)
            else:
                assert n.nodeType == DOT
            gc.SetTransform(old_tr)
            
        for n_id, waiting_c_in_node in self.Parent.Parent.Parent.Parent.waiting_customers_in_node.iteritems():
            if waiting_c_in_node:
                waiting_c_str = '[' + ':'.join(('C%d' % c_id) for c_id in waiting_c_in_node) + ']'
                gc.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                gc.DrawText(waiting_c_str, Dynamics.findNode(n_id).px + STATION_DIAMETER / 2, Dynamics.findNode(n_id).py - STATION_DIAMETER / 2 - 5)
        
        for n_id, idlePRT_in_node in self.Parent.Parent.Parent.Parent.idlePRT_in_node.iteritems():
            if idlePRT_in_node:
                PRTs_str = '(' + ':'.join(('PRT%d' % prt_id) for prt_id in idlePRT_in_node) + ')'
                gc.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                gc.DrawText(PRTs_str, Dynamics.findNode(n_id).px + STATION_DIAMETER / 2, Dynamics.findNode(n_id).py + STATION_DIAMETER / 2 - 5)
        
        for e in self.Parent.Parent.Parent.Parent.Edges:
            prev_n, next_n = e._from, e._to
            
            ax, ay = next_n.px - prev_n.px, next_n.py - prev_n.py
            la = sqrt(ax * ax + ay * ay)
            ux, uy = ax / la, ay / la
            px, py = -uy, ux
            if prev_n.nodeType == STATION and next_n.nodeType == JUNCTION:
                sx = prev_n.px + ux * STATION_DIAMETER / 2
                sy = prev_n.py + uy * STATION_DIAMETER / 2
                ex = next_n.px - ux * JUNCTION_DIAMETER / 2
                ey = next_n.py - uy * JUNCTION_DIAMETER / 2
                gc.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                gc.DrawLines([(ex, ey), (ex - int((ux * 5)) + int(px * 3), ey - int(uy * 5) + int(py * 3))])
                gc.DrawLines([(ex, ey), (ex - int(ux * 5) - int(px * 3), ey - int(uy * 5) - int(py * 3))])  
            elif prev_n.nodeType == JUNCTION and next_n.nodeType == STATION:
                sx = prev_n.px + ux * JUNCTION_DIAMETER / 2
                sy = prev_n.py + uy * JUNCTION_DIAMETER / 2
                ex = next_n.px - ux * STATION_DIAMETER / 2
                ey = next_n.py - uy * STATION_DIAMETER / 2
                gc.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                gc.DrawLines([(ex, ey), (ex - int((ux * 5)) + int(px * 3), ey - int(uy * 5) + int(py * 3))])
                gc.DrawLines([(ex, ey), (ex - int(ux * 5) - int(px * 3), ey - int(uy * 5) - int(py * 3))])
            elif prev_n.nodeType == JUNCTION and next_n.nodeType == JUNCTION:
                sx = prev_n.px + ux * JUNCTION_DIAMETER / 2
                sy = prev_n.py + uy * JUNCTION_DIAMETER / 2
                ex = next_n.px - ux * JUNCTION_DIAMETER / 2
                ey = next_n.py - uy * JUNCTION_DIAMETER / 2
                gc.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                gc.DrawLines([(ex, ey), (ex - int((ux * 5)) + int(px * 3), ey - int(uy * 5) + int(py * 3))])
                gc.DrawLines([(ex, ey), (ex - int(ux * 5) - int(px * 3), ey - int(uy * 5) - int(py * 3))])
            elif prev_n.nodeType == DOT and next_n.nodeType == JUNCTION:
                sx = prev_n.px
                sy = prev_n.py
                ex = next_n.px - ux * JUNCTION_DIAMETER / 2
                ey = next_n.py - uy * JUNCTION_DIAMETER / 2
                gc.SetFont(wx.Font(5, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                gc.DrawLines([(ex, ey), (ex - int((ux * 5)) + int(px * 3), ey - int(uy * 5) + int(py * 3))])
                gc.DrawLines([(ex, ey), (ex - int(ux * 5) - int(px * 3), ey - int(uy * 5) - int(py * 3))])
            elif prev_n.nodeType == JUNCTION and next_n.nodeType == DOT :
                sx = prev_n.px + ux * JUNCTION_DIAMETER / 2
                sy = prev_n.py + uy * JUNCTION_DIAMETER / 2
                ex = next_n.px
                ey = next_n.py
                gc.SetFont(wx.Font(5, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            elif prev_n.nodeType == DOT and next_n.nodeType == DOT :
                sx = prev_n.px
                sy = prev_n.py
                ex = next_n.px
                ey = next_n.py
                gc.DrawLines([(sx, sy), (ex, ey)])
                gc.SetFont(wx.Font(5, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
#                 gc.DrawText('%d' % int(round(e.distance, 1)), (prev_n.px + next_n.px) / 2, (prev_n.py + next_n.py) / 2)
                continue
            else:
                assert False 
            gc.DrawLines([(sx, sy), (ex, ey)])
            
            if self.Parent.Parent.Parent.Parent.show_distance.GetValue():
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

            if v.state != ST_IDLE:
                gc.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                gc.DrawEllipse(-PRT_SIZE / 2, -PRT_SIZE / 2, PRT_SIZE, PRT_SIZE)
                
                if v.assigned_customer:
                    gc.DrawText('PRT%d-C%d' % (v.id, v.assigned_customer.id), -PRT_SIZE / 2, -PRT_SIZE / 2 - 12)
                elif v.transporting_customer:
                    gc.DrawText('PRT%d(C%d)' % (v.id, v.transporting_customer.id), -PRT_SIZE / 2, -PRT_SIZE / 2 - 12)
                else:
                    assert not v.assigned_customer and not v.transporting_customer 
                    gc.DrawText('PRT%d' % v.id, -PRT_SIZE / 2, -PRT_SIZE / 2 - 12)
            
            gc.SetTransform(old_tr)
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    win = MainFrame()
    win.Show(True)
    app.MainLoop()

