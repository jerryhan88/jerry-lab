import wx

def print_hello(evt):
    print 'hello'

app = wx.PySimpleApp()

win = wx.Frame(None, -1, 'Hello wxPython', (100,100), (200,200))
p = wx.Panel(win,-1)
b = wx.Button(p, -1, "Press^^", (100,50), (100,10))

p.Bind(wx.EVT_BUTTON, print_hello, b)

win.Show(True)

app.MainLoop()
