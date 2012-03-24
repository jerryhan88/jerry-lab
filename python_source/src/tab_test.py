from __future__ import division

import wx

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'test', size=(800, 600))
        base_p = wx.Panel(self, -1)
        r, g, b, a = (100, 200, 200, 100)
        clr = wx.Colour(r, g, b, a )
        
        base_p.SetBackgroundColour(clr)
        sx, sy = self.GetSize()
        base_p.SetSize((sx, sy))
        price_b = wx.Button(base_p, -1, "Price", (50, 50))
        time_b = wx.Button(base_p, -1, "Time", (50, 150))
        
        info_view_p = wx.Panel(base_p, -1, pos=(140, 20), size=(440, 200))
#        wx.StaticText(info_view_p, -1, 'test!!!!', (10, 30))
#        info_view_p.SetBackgroundColour(wx.Colour(0, 255, 0))
        
        self.p_nb = PriceNB(info_view_p)
        self.t_nb = TimeNB(info_view_p)
        
        self.t_nb.Show(False)
        
        
        base_p.Bind(wx.EVT_BUTTON, self.show_p_view, price_b)
        base_p.Bind(wx.EVT_BUTTON, self.show_t_view, time_b)
        
        self.Show(True)
    
    def show_p_view(self, evt):
#        self.p_nb = PriceNB(self.info_view_p)
        self.p_nb.Show(True)
        self.t_nb.Show(False)
        print 'show_p_view'
    
    def show_t_view(self, evt):
        self.p_nb.Show(False)
        self.t_nb.Show(True)
        print 'show_t_view'    

class PriceNB(wx.Notebook):
    def __init__(self, parent):
        sx, sy = parent.GetSize()
        wx.Notebook.__init__(self, parent, -1, size=(sx, sy), style=
                             wx.BK_DEFAULT)
        
        bt = 5
        
        p1 = wx.Panel(self, -1)
        p1.SetBackgroundColour('blue')
        price_b = wx.Button(p1, -1, "Price", (50, 50))
        
        sx, sy = price_b.GetSize()
        px, py = price_b.GetPosition()
        
        b1 = wx.Button(p1, -1, "Button 1", (px + sx + bt, py))
        b2 = wx.Button(p1, -1, "Button 2", (px, py + sy + bt))
        
        
        self.AddPage(p1, "PriceNB p1")
        
        p2 = wx.Panel(self, -1)
        wx.StaticText(p2, -1, 'test!!!!', (10, 30))
        p2.SetBackgroundColour('white')
        self.AddPage(p2, "PriceNB p2")

class TimeNB(wx.Notebook):
    def __init__(self, parent):
        sx, sy = parent.GetSize()
        wx.Notebook.__init__(self, parent, -1, size=(sx, sy), style=
                             wx.BK_DEFAULT)
        p0 = wx.Panel(self, -1)
        p0.SetBackgroundColour('blue')
        txt_ctl = wx.TextCtrl(p0, -1, '', pos=(100, 30), size=(80, 20))
        self.AddPage(p0, "TimeNB p1")
        
        p1 = wx.Panel(self, -1)
        p1.SetBackgroundColour('blue')
        price_b = wx.Button(p1, -1, "Price", (50, 50))
        self.AddPage(p1, "TimeNB p1")
        
        p2 = wx.Panel(self, -1)
        t = wx.StaticText(p2, -1, 'test!!!!', (10, 30))
        t.SetBackgroundColour('red')
        p2.SetBackgroundColour('white')
        self.AddPage(p2, "TimeNB p2")
        

class TestNB(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, -1, size=(21, 21), style=
                             wx.BK_DEFAULT)

        win = self.makeColorPanel(wx.BLUE)
        self.AddPage(win, "Blue")
        
    def makeColorPanel(self, color):
        p = wx.Panel(self, -1)
        p.SetBackgroundColour(color)
        return p

        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    app.frame = MainFrame()
    app.MainLoop()
