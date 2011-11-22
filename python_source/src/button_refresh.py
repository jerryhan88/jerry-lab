import wx

class MyFrame(wx.Frame): #@UndefinedVariable
    def __init__(self, parent, ID, title, pos=wx.DefaultPosition, size=(1024, 768), style=wx.DEFAULT_FRAME_STYLE): #@UndefinedVariable
        wx.Frame.__init__(self, parent, ID, title, pos, size, style) #@UndefinedVariable
        self.p = wx.Panel(self,-1)#@UndefinedVariable
        b = wx.Button(self.p, -1, "Press^^", (100,100))#@UndefinedVariable
        wx.StaticText(self.p, -1, 'Studnent ID', (10, 30))#@UndefinedVariable
        self.s_id_typed= wx.TextCtrl(self.p, -1, 'type stuID', pos=(100, 30), size=(80, 20))#@UndefinedVariable
#        self.s_id = eval(s_id_typed.GetValue()) 
        
        self.p.Bind(wx.EVT_BUTTON, self.print_hello, b)#@UndefinedVariable
        self.s_name_show = None


    def print_hello(self, evt):
        s_id = self.s_id_typed.GetValue()
        if self.s_name_show == None:
            self.s_name_show = wx.StaticText(self.p, -1, s_id, (10, 50))#@UndefinedVariable
        else:
            #self.s_name_show.Destroy()
            self.s_name_show = wx.StaticText(self.p, -1, s_id, (10, 50))#@UndefinedVariable
            
        print 'hello'   
        print s_id
        
        

if __name__ == '__main__':
    app = wx.PySimpleApp() #@UndefinedVariable
    win = MyFrame(None, -1, 'Hello wxPython', (100,100), (200,200))#@UndefinedVariable
    win.Show(True)
    app.MainLoop()




