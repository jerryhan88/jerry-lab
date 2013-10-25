from __future__ import division
from math import sqrt
from util import DragZoomPanel
import wx

TIMER_INTERVAL = 100
CLOCK_INCREMENT = 100
CLOCK_INCR_DIFF = sqrt(2)

NODE_DIAMETER = 40
CUSTOMER_RADIUS = NODE_DIAMETER / 3
PRT_SIZE = 20



class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Dynamic routing experiment', size=(1024, 768))
        
        self.set_toolbar()
        self.simul_clock = 0
        self.timer = wx.Timer(self)
        
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
        
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnTimer(self, evt):
        self.simul_clock += CLOCK_INCREMENT / 1000
#         self.vp.update(self.simul_clock)
                
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

class ViewPanel(DragZoomPanel):
    def __init__(self, parent):
        DragZoomPanel.__init__(self, parent, -1, style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour(wx.WHITE)
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    win = MainFrame()
    win.Show(True)
    app.MainLoop()

