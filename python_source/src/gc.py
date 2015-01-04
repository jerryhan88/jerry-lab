from __future__ import division
import wx, time

class Node:
    def __init__(self, _id, x, y):
        self.id = _id
        self.x, self.y = x, y
        

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'test', size=(640, 480))
        MyPanel(self)
        self.Show(True)

class MyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.WHITE)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.GP = None
    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        gc.SetPen(wx.BLACK_PEN)
        gc.SetBrush(wx.BLUE_BRUSH)
        gc.DrawRectangle(100, 100, 100, 100)
        if self.GP == None:
            gpath1 = gc.CreatePath()
            gpath1.MoveToPoint(0, 0)
            gpath1.AddLineToPoint(0, 100)
            gpath1.AddLineToPoint(100, 100)
            gpath1.AddLineToPoint(-50, 0)
            gpath1.CloseSubpath()
            gpath2 = gc.CreatePath()
            gpath2.MoveToPoint(150, 0)
            gpath2.AddLineToPoint(200, 0)
            gpath2.AddLineToPoint(200, 50)
            gpath2.CloseSubpath()
            self.GP = [gpath1, gpath2]
        #
        gc.Translate(300, 100)
        gc.SetBrush(wx.RED_BRUSH)
        gc.DrawPath(self.GP[0])
        gc.Translate(0, 0)
        gc.SetBrush(wx.GREEN_BRUSH)
        gc.DrawPath(self.GP[1])

if __name__ == '__main__':
    app = wx.App(False)
    app.frame = MainFrame()
    app.MainLoop()
