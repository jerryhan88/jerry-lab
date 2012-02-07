import wx

class TestDialog(wx.Dialog):
    def __init__(self, parent, name, size=(400, 250), pos=(850, 50)):
        wx.Dialog.__init__(self, None, -1, 'Test Dialog', pos , size)
        wx.StaticText(self, -1, name, (70, 50))
        self.input_t = wx.TextCtrl(self, -1, "123", pos=(20, 65), size=(60, 30))
        button = wx.Button(self, -1, "Confirm", (100, 150))
        self.Bind(wx.EVT_BUTTON, self.confirm, button)
        self.input = None
        
        self.Show(True)
        
    def confirm(self, event):
    #    self.Destroy()
        self.input = self.input_t.GetValue() 
        win = MyFrame(None, -1, 'Hello wxPython', (100,100), (200,200), self)
        win.Show(True)
        self.Show(False)
        
class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title, pos=wx.DefaultPosition, size=(1024, 768), td = None):
        wx.Frame.__init__(self, parent, ID, title, pos, size)
        self.p = wx.Panel(self,-1)
        wx.StaticText(self.p, -1, td.input, (10, 30))
        button = wx.Button(self.p, -1, "Confirm", (100, 150))
        self.Bind(wx.EVT_BUTTON, self.confirm, button)
        
    def confirm(self, event):
        td.Destroy()
        self.Destroy()
if __name__ == '__main__':
    app = wx.PySimpleApp()
    td= TestDialog(None, 'dialog test')
    app.MainLoop()
