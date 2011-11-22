import wx
from random import randrange

class Main_viewer(wx.Frame):
    def __init__(self, parent, ID, title, pos, size, style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        self.p = wx.Panel(self, -1, pos=(0, 0), size=(810, 730))
        self.p.Bind(wx.EVT_PAINT, self.OnViewPaint_yard)
        
    def OnViewPaint_yard(self, _):
        dc = wx.PaintDC(self.p)
        self.p.PrepareDC(dc)
        
        r, g, b = (200, 200, 200)
        brushclr = wx.Colour(r, g, b, 128)
        dc.SetBrush(wx.Brush(brushclr))
        
        old_pen = dc.GetPen()
        dc.SetPen(wx.Pen(wx.BLUE, 3))
        
        dc.DrawRectangle(10, 10, 100, 100)
        
        dc.SetFont(wx.Font(7, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        dc.SetTextForeground(brushclr)
              
        
        dc.DrawText('123', 200, 150)
               
        
        dc.SetPen(old_pen)
        
        old_pen = dc.GetPen()
        dc.SetPen(wx.Pen(wx.BLACK, 6))
        dc.DrawLine(110,110, 210,210)
        
        dc.SetPen(old_pen)
        dc.EndDrawing()
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    mv = Main_viewer(None, -1, 'Main_viewer', pos=(30, 30), size=(600, 500))
    mv.Show(True)
    app.MainLoop()
