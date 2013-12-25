from __future__ import division
from math import sqrt, pi
from util import DragZoomPanel
import wx, Dynamics, Algorithms
from Dynamics import ST_IDLE, ST_APPROACHING, ST_SETTING, ST_TRANSITING, ST_PARKING, STATION, TRANSFER
from time import time
  

TIMER_INTERVAL = 100
CLOCK_INCREMENT = 100
CLOCK_INCR_DIFF = sqrt(2)

STAT_UPDATE_INTERVAL = 1.0  # sec

STATION_DIAMETER = 30
JUNCTION_DIAMETER = STATION_DIAMETER / 4
CUSTOMER_RADIUS = STATION_DIAMETER / 3
PRT_SIZE = STATION_DIAMETER / 5

waiting_customers = []
event_queue = []

LOG_TO_OUTPUT = True


TITLE = 'PRT Simulator'

class CustomerWaitingTime_chart(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, '', pos=(150, 150) , size=(1024, 768))
        self.SetTitle('Customer waiting time chart' + ' - ' + self.Parent.dispatcher.__name__)
        self.cp = ChartPanel(self) 
        self.SetBackgroundColour(wx.Colour(236, 233, 216))
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Show(True)
        
    def OnClose(self, event):
        self.Show(False)

class ChartPanel(DragZoomPanel):
    def __init__(self, parent):
        DragZoomPanel.__init__(self, parent, -1, style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour(wx.WHITE)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.lastTime = Dynamics.Customers[-1].arriving_time + 600.0
        self.NumOfTotalCustomer = len(Dynamics.Customers)
        
        
    def OnDrawDevice(self, gc):
        pass
    
    def OnDraw(self, gc):
        sx, sy = self.GetSize()
        ori_px, ori_py = sx * 0.1, sy * (1 - 0.2)
        len_sx, len_sy = sx * 0.8, sy * 0.6
        gc.DrawLines([(ori_px, ori_py), (ori_px + len_sx, ori_py)])
        gc.DrawLines([(ori_px + len_sx, ori_py), (ori_px + len_sx - 3, ori_py - 3)])
        gc.DrawLines([(ori_px + len_sx, ori_py), (ori_px + len_sx - 3, ori_py + 3)])
        gc.DrawLines([(ori_px, ori_py), (ori_px, ori_py - len_sy)])
        gc.DrawLines([(ori_px, ori_py - len_sy), (ori_px - 3, ori_py - len_sy + 3)])
        gc.DrawLines([(ori_px, ori_py - len_sy), (ori_px + 3, ori_py - len_sy + 3)])
        
        xUnit = len_sx / (self.lastTime)
        yUnit = len_sy / (self.NumOfTotalCustomer / 10)
        
#         gc.SetFont(wx.Font(5, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
#         gc.DrawText('%d' % self.NumOfTotalCustomer, ori_px + len_sx, ori_py - len_sy )
        gc.SetFont(wx.Font(5, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        TTI = 10
        for i in range(TTI):
            t = (i + 1) * (self.lastTime / TTI)
            h = int(t // 3600)
            m = int(t // 60) % 60
            s = t % 60
            gc.DrawText('%02d:%02d:%04.1f' % (h, m, s), ori_px + t * xUnit, ori_py + 10)
        
        last_px, last_py = ori_px, ori_py
        CCS, NWC = 0.0, 0
        gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 0.5))
        for i, args in enumerate(Dynamics.WaitingCustomerChanges):
            CCS, NWC = args 
            if i == 0:
                gc.DrawLines([(ori_px, ori_py), (ori_px + CCS * xUnit, ori_py)])
            else:
                gc.DrawLines([(ori_px + Dynamics.WaitingCustomerChanges[i - 1][0] * xUnit, ori_py - Dynamics.WaitingCustomerChanges[i - 1][1] * yUnit), (ori_px + Dynamics.WaitingCustomerChanges[i - 1][0] * xUnit, ori_py - NWC * yUnit)])
                gc.DrawLines([(ori_px + Dynamics.WaitingCustomerChanges[i - 1][0] * xUnit, ori_py - NWC * yUnit), (ori_px + CCS * xUnit, ori_py - NWC * yUnit)])
        
        CT, TWT = 0.0, 0.0
        gc.SetPen(wx.Pen(wx.Colour(255, 0, 0), 0.5)) 
        for i, args in enumerate(Dynamics.WaitingTimeChanges):
            CT, TWT = args
            AWT = TWT / CT 
            if i == 0:
                gc.DrawLines([(ori_px, ori_py), (ori_px + CT * xUnit, ori_py - AWT * yUnit)])
            else:
                gc.DrawLines([(ori_px + Dynamics.WaitingTimeChanges[i - 1][0] * xUnit, ori_py - (Dynamics.WaitingTimeChanges[i - 1][1] / Dynamics.WaitingTimeChanges[i - 1][0]) * yUnit), (ori_px + CT * xUnit, ori_py - AWT * yUnit)])

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, TITLE, size=(1024, 768), pos=(20, 20))
#         wx.Frame.__init__(self, None, -1, TITLE, size=(1920, 960), pos=(0, 0))
        # Every resources are accessible
#         self.Nodes, self.Edges = Dynamics.Network1()
        self.Nodes, self.Edges = Dynamics.Network2()
        self.Customers = Dynamics.gen_Customer(4.2, 5000, 0.3, self.Nodes)
        self.NumOfTotalCustomer = len(self.Customers)
        self.PRTs = Dynamics.gen_PRT(50, self.Nodes)
        
        Algorithms.init_algorithms(self.Nodes)
        
        self.idlePRT_in_node = {}
        for n in self.Nodes:
            if n.nodeType == TRANSFER or n.nodeType == STATION:
                self.idlePRT_in_node[n.id] = []
        
        self.waiting_customers_in_node = {}
        for n in self.Nodes:
            if n.nodeType == TRANSFER or n.nodeType == STATION:
                self.waiting_customers_in_node[n.id] = []
        
        self.now = 0.0
        self.timer = wx.Timer(self)
        
        self.set_toolbar()
        
        s0 = wx.SplitterWindow(self, style=wx.SP_NOBORDER)
        s1 = wx.SplitterWindow(s0, style=wx.SP_NOBORDER)
        s2 = wx.SplitterWindow(s1, style=wx.SP_NOBORDER)
        
        ip = InputPanel(s0)
        s0.SplitVertically(ip, s1, 250)
        s0.SetMinimumPaneSize(20)
        
        self.mp = MeasurePanel(s1)
        
        s1.SplitVertically(s2, self.mp, -210)
        s1.SetSashGravity(1)
        
        self.vp = ViewPanel(s2)
        lp = LogPanel(s2)
        s2.SplitHorizontally(self.vp, lp, -200)
        s2.SetSashGravity(1)
        
        if LOG_TO_OUTPUT:
            Dynamics.logger = lp.WriteLog

        Algorithms.on_notify_assignmentment_point = self.pause_clock_ressignement_point 
         
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        Dynamics.on_notify_customer_arrival = ip.on_notify_customer_arrival

        self.Show(True)
        
#         self.dispatcher = self.select_dispatcher()
        
        self.dispatcher = Algorithms.NN1 
        
        if self.dispatcher == None:
            return
        
        Dynamics.init_dynamics(self.Nodes, self.PRTs, self.Customers, self.dispatcher)
        
        self.SetTitle(TITLE + ' - ' + self.dispatcher.__name__)
        self.vp.SetFocus()
        
#         self.CWTC = CustomerWaitingTime_chart(self)
        
        ##############################
        
        self.next_stat_update_time = time() + STAT_UPDATE_INTERVAL

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
    def OnClose(self, event):
#         self.CWTC.Destroy()
        self.Destroy()
    
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
            if n.nodeType == TRANSFER or n.nodeType == STATION:
                self.idlePRT_in_node[n.id] = []
        
        # Update positions of PRTs
        for prt in self.PRTs:
            if prt.state == Dynamics.ST_SETTING:
                prt.px, prt.py = prt.arrived_n.px, prt.arrived_n.py
                
            elif prt.path_e:
                path_travel_time = self.now - prt.last_planed_time
                edges_counter = 0
                prev_n, next_n = None, None
                sum_travel_time = 0.0
                for e in prt.path_e:
                    sum_travel_time += e.distance / min(Dynamics.PRT_SPEED, e.maxSpeed) 
                    edges_counter += 1 
                    if sum_travel_time >= path_travel_time:
                        prev_n = e._from
                        next_n = e._to
                        break
                prev_n_arrival_time = prt.last_planed_time + sum(e.distance / min(Dynamics.PRT_SPEED, e.maxSpeed) for e in prt.path_e[:edges_counter - 1])
                
                if next_n:
                    dx = next_n.px - prev_n.px
                    dy = next_n.py - prev_n.py
                    cos_theta = dx / sqrt(dx * dx + dy * dy)
                    sin_theta = dy / sqrt(dx * dx + dy * dy)
                    
                    prt.px = prev_n.px + cos_theta * (self.now - prev_n_arrival_time) * min(Dynamics.PRT_SPEED, prt.path_e[edges_counter - 1].maxSpeed)
                    prt.py = prev_n.py + sin_theta * (self.now - prev_n_arrival_time) * min(Dynamics.PRT_SPEED, prt.path_e[edges_counter - 1].maxSpeed)
                else:
                    prt.px = prt.path_n[-1].px
                    prt.py = prt.path_n[-1].py
                
            else:
                assert prt.state == Dynamics.ST_IDLE 
                prt.px, prt.py = prt.arrived_n.px, prt.arrived_n.py
                self.idlePRT_in_node[prt.arrived_n.id].append(prt.id)
        
        self.waiting_customers_in_node = {}
        for n in self.Nodes:
            if n.nodeType == TRANSFER or n.nodeType == STATION:
                self.waiting_customers_in_node[n.id] = []
        
        for c in Dynamics.waiting_customers:
            self.waiting_customers_in_node[c.sn.id].append(c.id) 
        self.vp.RefreshGC()
#         self.CWTC.cp.RefreshGC()
        
        if self.next_stat_update_time < time():
            self.next_stat_update_time = time() + STAT_UPDATE_INTERVAL
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


StaticInfo, NumOfStations, NumOfPRTs, TotalCustomer, AboutCustomer, CustomerArrivals, WaitingCustomers, PickedUpCustomers, ServicedCustomers, WaitingTime, WTTotal, WTAverage, WTMaximum, FlowTime, FTTotal, FTAverage, TravelDistance, TDTotal, TDAverage, EmptyTravelDistance, ETDTotal, ETDAverage, StateDuration, Idle, Approaching, Setting, Transiting, Parking = range(28)
 

measure_name = ['T.TravelDist', 'T.TravelDist', 'T.E.TravelDist', 'A.WaitTime', 'A.FlowTime']

class MeasurePanel(wx.ListCtrl):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.InsertColumn(0, 'Title')
        self.InsertColumn(1, 'Value', wx.LIST_FORMAT_RIGHT)

        self.SetColumnWidth(0, 90)
        self.SetColumnWidth(1, 110)
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
         
        self.InsertStringItem(AboutCustomer, 'Customer')
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
        self.InsertStringItem(Setting, 'Setting')
        self.SetStringItem(Setting, 1, '%.1f' % Dynamics.ApproachingState_time)
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
        
        total_tive_flow = cur_time * len(Dynamics.PRTs)
        self.SetStringItem(Idle, 1, '%.1f(%.1f%s)' % (Dynamics.IdleState_time, Dynamics.IdleState_time / total_tive_flow * 100, '%'))
        self.SetStringItem(Approaching, 1, '%.1f(%.1f%s)' % (Dynamics.ApproachingState_time, Dynamics.ApproachingState_time / total_tive_flow * 100, '%'))
        self.SetStringItem(Setting, 1, '%.1f(%.1f%s)' % (Dynamics.SettingState_time, Dynamics.SettingState_time / total_tive_flow * 100, '%'))
        self.SetStringItem(Transiting, 1, '%.1f(%.1f%s)' % (Dynamics.TransitingState_time, Dynamics.TransitingState_time / total_tive_flow * 100, '%'))
        self.SetStringItem(Parking, 1, '%.1f(%.1f%s)' % (Dynamics.ParkingState_time, Dynamics.ParkingState_time / total_tive_flow * 100, '%'))
        
        self.Refresh()
            
class InputPanel(wx.ListCtrl):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.InsertColumn(0, 'Customer', wx.LIST_FORMAT_CENTER)
        self.InsertColumn(1, 'Time', wx.LIST_FORMAT_CENTER)
        self.InsertColumn(2, 'From', wx.LIST_FORMAT_CENTER)
        self.InsertColumn(3, 'To', wx.LIST_FORMAT_CENTER)
        
        self.SetColumnWidth(0, 65)
        self.SetColumnWidth(1, 80)
        self.SetColumnWidth(2, 43)
        self.SetColumnWidth(3, 43)
        
        rowCount = 0
        with open('Info. Arrivals of customers.txt', 'r') as fp:
            for line in fp:
                arrival_time_str, sd = line.split(',')
                sn, dn = sd.split('-')
                arrival_time = float(arrival_time_str)
                self.InsertStringItem(rowCount, 'C%d' % rowCount)
                h = int(arrival_time // 3600)
                m = int(arrival_time // 60) % 60
                s = arrival_time % 60
                self.SetStringItem(rowCount, 1, '%02d:%02d:%04.1f' % (h, m, s))
                self.SetStringItem(rowCount, 2, sn)
                self.SetStringItem(rowCount, 3, dn)
                rowCount += 1
                
    def on_notify_customer_arrival(self, customer):
        if customer.id != 0:
            self.SetItemBackgroundColour(customer.id - 1, wx.Colour(255, 255, 255))
        self.SetItemBackgroundColour(customer.id, wx.Colour(200, 200, 200))
#         self.EnsureVisible(customer.id)
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
        
        h = int(self.Parent.Parent.Parent.Parent.now // 3600)
        m = int(self.Parent.Parent.Parent.Parent.now // 60) % 60
        s = self.Parent.Parent.Parent.Parent.now % 60
        
        gc.DrawText('%02d:%02d:%04.1f (%.1fX)' % (h, m, s, CLOCK_INCREMENT / TIMER_INTERVAL), 5, 3)
    
    def OnDraw(self, gc):
        old_tr = gc.GetTransform()
        
        for n in self.Parent.Parent.Parent.Parent.Nodes:
            gc.Translate(n.px, n.py)
            if n.nodeType == TRANSFER or n.nodeType == STATION:
                gc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
                gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
                gc.DrawEllipse(-STATION_DIAMETER / 2, -STATION_DIAMETER / 2, STATION_DIAMETER, STATION_DIAMETER)
                gc.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
#                 if n.settingPRTs:
                PRTs_str = 'S #%d {' % len(n.settingPRTs) + ':'.join(('PRT%d(C%d)' % (prt.id, prt.transporting_customer.id)) for prt in n.settingPRTs) + '}'
                gc.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                gc.DrawText(PRTs_str, STATION_DIAMETER / 2 - 2, 22)
                
                PRTs_str = 'SW #%d {' % len(n.setupWaitingPRTs) + ':'.join(('PRT%d' % (prt.id)) for prt in n.setupWaitingPRTs) + '}'
                
                notEnterPRTs = []
                notLeavePRTs = []
                for prt in n.setupWaitingPRTs:
                    if prt.state == ST_TRANSITING:
                        notEnterPRTs.append(prt)
                    else:
                        assert prt.state == ST_IDLE or prt.state == ST_APPROACHING
                        notLeavePRTs.append(prt)
                        
                PRTs_str = 'XE #%d {' % len(notEnterPRTs) + ':'.join(('PRT%d(C%d)' % (prt.id, prt.transporting_customer.id)) for prt in notEnterPRTs) + '}'
                gc.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                gc.DrawText(PRTs_str, STATION_DIAMETER / 2 - 8, 32)
                
                PRTs_str = 'XL #%d {' % len(notLeavePRTs) + ':'.join(('PRT%d' % (prt.id)) for prt in notLeavePRTs) + '}'
                gc.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                gc.DrawText(PRTs_str, STATION_DIAMETER / 2 - 8, 42)
                
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
                waiting_c_str = 'C #%d [' % len(waiting_c_in_node) + ':'.join(('C%d' % c_id) for c_id in waiting_c_in_node) + ']'
                gc.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                gc.DrawText(waiting_c_str, Dynamics.findNode(n_id).px + STATION_DIAMETER / 2, Dynamics.findNode(n_id).py - STATION_DIAMETER / 2 - 9)
        
        for n_id, idlePRT_in_node in self.Parent.Parent.Parent.Parent.idlePRT_in_node.iteritems():
            if idlePRT_in_node:
                PRTs_str = 'I #%d (' % len(idlePRT_in_node) + ':'.join(('PRT%d' % prt_id) for prt_id in idlePRT_in_node) + ')'
                gc.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                gc.DrawText(PRTs_str, Dynamics.findNode(n_id).px + STATION_DIAMETER / 2, Dynamics.findNode(n_id).py + STATION_DIAMETER / 2 - 5)
        
        for e in self.Parent.Parent.Parent.Parent.Edges:
            prev_n, next_n = e._from, e._to
            
            ax, ay = next_n.px - prev_n.px, next_n.py - prev_n.py
            la = sqrt(ax * ax + ay * ay)
            ux, uy = ax / la, ay / la
            px, py = -uy, ux
            
            if (prev_n.nodeType == TRANSFER or prev_n.nodeType == STATION) and next_n.nodeType == JUNCTION:
                sx = prev_n.px + ux * STATION_DIAMETER / 2
                sy = prev_n.py + uy * STATION_DIAMETER / 2
                ex = next_n.px - ux * JUNCTION_DIAMETER / 2
                ey = next_n.py - uy * JUNCTION_DIAMETER / 2
                gc.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                gc.DrawLines([(ex, ey), (ex - int((ux * 5)) + int(px * 3), ey - int(uy * 5) + int(py * 3))])
                gc.DrawLines([(ex, ey), (ex - int(ux * 5) - int(px * 3), ey - int(uy * 5) - int(py * 3))])  
            elif prev_n.nodeType == JUNCTION and (next_n.nodeType == TRANSFER or next_n.nodeType == STATION):
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
#                 gc.DrawLines([(sx, sy), (ex, ey)])
                gc.SetFont(wx.Font(5, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
#                 continue
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
            elif v.state == ST_SETTING:
                # APPROACHING PRT's color is LIGHT_GREEN
                gc.SetBrush(wx.Brush(wx.Colour(181, 230, 29)))    
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

