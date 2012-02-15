from __future__ import division
import wx

class Vessel:
    pass

class QC:
    pass

class AYC:
    pass

class SC:
    pass

class Frame(wx.Frame):
    def __init__(self, parent, ID, title, pos, size, style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        self.p = wx.Panel(self, -1, pos=(0, 0), size=(1000, 1000))
        self.p.Bind(wx.EVT_PAINT, self.drawing)

    def drawing(self, _):
        dc =wx.PaintDC(self.p)
        self.p.PrepareDC(dc)

        old_pen = dc.GetPen()
        dc.SetPen(wx.Pen(wx.BLACK, 2))

        r, g, b = (236, 233, 216)
        brushclr = wx.Colour(r, g, b, 100)
        dc.SetBrush(wx.Brush(brushclr))
        
        #monitor
        dc.DrawLine(670, 0, 670, 600)
        dc.DrawLine(0, 85, 670, 85)
        dc.DrawLine(0, 600, 670, 600)
        
        #vessel drawing
        dc.DrawRectangle(70, 30, 200, 50)
        dc.DrawRectangle(400, 30, 200, 50)

        #QC drawing
        dc.DrawRectangle(100, 20, 30, 150)
        dc.DrawRectangle(150, 20, 30, 150)
        dc.DrawRectangle(200, 20, 30, 150)
        dc.DrawRectangle(430, 20, 30, 150)
        dc.DrawRectangle(480, 20, 30, 150)
        dc.DrawRectangle(530, 20, 30, 150)
        
        #yard drawing
        dc.DrawRectangle(20, 300, 60, 200)
        dc.DrawRectangle(160, 300, 60, 200)
        dc.DrawRectangle(300, 300, 60, 200)
        dc.DrawRectangle(440, 300, 60, 200)
        dc.DrawRectangle(580, 300, 60, 200)
        
        #AYC drawing
        dc.DrawRectangle(5, 320, 90, 25)
        dc.DrawRectangle(5, 400, 90, 25)

        dc.DrawRectangle(145, 320, 90, 25)
        dc.DrawRectangle(145, 400, 90, 25)

        dc.DrawRectangle(285, 320, 90, 25)
        dc.DrawRectangle(285, 400, 90, 25)

        dc.DrawRectangle(425, 320, 90, 25)
        dc.DrawRectangle(425, 400, 90, 25)

        dc.DrawRectangle(565, 320, 90, 25)
        dc.DrawRectangle(565, 400, 90, 25)

        dc.EndDrawing()
       
if __name__ == '__main__':
    app = wx.PySimpleApp()
    mv = Frame(None, -1, 'Main_viewer', pos=(100, 100), size=(1000, 1000))
    mv.Show(True)
    app.MainLoop()
