import wx
app = wx.PySimpleApp()
mv = wx.Frame(None, -1, 'ListCtrl test', (100,100),(600,400))
p = wx.Panel(mv, -1)

##lc = wx.ListCtrl(p, -1, (10, 80), (560, 130), style=wx.LC_LIST)

lc = wx.ListCtrl(p, -1, (10, 80), (560, 130), style=wx.LC_REPORT | wx.SUNKEN_BORDER)
##lc = wx.ListCtrl(p, -1, (10, 80), (560, 130))
lc.InsertColumn(0,'Student ID')

mv.Show(True)
app.MainLoop()
