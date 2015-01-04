from __future__ import division
import wx, time
from dz_panel import DragZoomPanel

class Node:
    def __init__(self, _id, x, y):
        self.id = _id
        self.x, self.y = x, y

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'test', size=(300, 300))
        MyPanel(self)
        self.Show(True)

class MyPanel(DragZoomPanel):
    def __init__(self, parent):
        DragZoomPanel.__init__(self, parent, -1, style=wx.SUNKEN_BORDER)
        
        self.SetBackgroundColour(wx.WHITE)
        
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        self.nodes = [
                      Node(0, 20, 20),
                      Node(0, 20.01, 20.09),
                      ]
        #
    # Zoom or play speed control event.
    #  
    def OnMouseWheel(self, e):
        if e.ControlDown():
            ''' Speed control. '''
            main_frame = self.sim_frame.Parent
            if e.GetWheelRotation() > 0:
                main_frame.OnSpeedUp(None)
            else:
                main_frame.OnSpeedDown(None)
        else:
            ''' Zoom control. '''
            DragZoomPanel.OnMouseWheel(self, e)
    #
    # Represent simulator's time.
    #
    def OnDrawDevice(self, gc):
        gc.DrawText('test', 5, 3)
    #
    # Draw objects.
    #
    def OnDraw(self, gc):
#         
        
        for i, n in enumerate(self.nodes):
            if i ==0:
                gc.SetPen(wx.Pen("black", 0))
                r, g, b = (255, 0, 0)
            else:
                gc.SetPen(wx.Pen("yellow", 0))
                r, g, b = (0, 255, 0)
            brushclr = wx.Colour(r, g, b, 100)
            gc.SetBrush(wx.Brush(brushclr))
            gc.DrawRectangle(n.x, n.y, 100, 100)

if __name__ == '__main__':
    app = wx.PySimpleApp()
    app.frame = MainFrame()
    app.MainLoop()
