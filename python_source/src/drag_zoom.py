from __future__ import division

import wx
import colorsys
from math import cos, sin, radians

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'test', size=(640, 480))
        MyPanel(self)
        self.Show(True)

BASE  = 80.0    # sizes used in shapes drawn below
BASE2 = BASE/2
BASE4 = BASE/4

class MyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.WHITE)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        # size and mouse events
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
        self.translate_mode = False
        self.translate_x, self.translate_y = 0, 0
        self.scale = 1.0
    
    def OnSize(self, evt):
        self.InitBuffer()
        evt.Skip()
    
    def OnLeftDown(self, evt):
        self.translate_mode = True
        self.prev_x, self.prev_y = evt.m_x, evt.m_y
        self.CaptureMouse()
        
    def OnMotion(self, evt):
        if self.translate_mode:
            dx, dy = evt.m_x - self.prev_x, evt.m_y - self.prev_y
            self.translate_x += dx
            self.translate_y += dy
            self.prev_x, self.prev_y = evt.m_x, evt.m_y
            self.RefreshGC()
            
    def OnLeftUp(self, evt):
        self.translate_mode = False
        self.ReleaseMouse()
        
    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self, self._buffer)
    def OnMouseWheel(self, evt):
        # TODO scaling based on mouse position (evt.m_x, evt.m_y)
        if evt.m_wheelRotation > 0:
            self.scale *= 1.2
        else:
            self.scale /= 1.2
        self.RefreshGC()
    def InitBuffer(self):
        sz = self.GetClientSize()
        sz.width = max(1, sz.width)
        sz.height = max(1, sz.height)
        self._buffer = wx.EmptyBitmap(sz.width, sz.height, 32)
        dc = wx.MemoryDC(self._buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)
        self.Draw(gc)
    def RefreshGC(self):
        dc = wx.MemoryDC(self._buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)
        self.Draw(gc)
        self.Refresh(False)
    def Draw(self, gc):
        gc.Translate(self.translate_x, self.translate_y)
        gc.Scale(self.scale, self.scale)
        
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetWeight(wx.BOLD)
        gc.SetFont(font)

        # make a path that contains a circle and some lines, centered at 0,0
        path = gc.CreatePath()
        path.AddCircle(0, 0, BASE2)
        path.MoveToPoint(0, -BASE2)
        path.AddLineToPoint(0, BASE2)
        path.MoveToPoint(-BASE2, 0)
        path.AddLineToPoint(BASE2, 0)
        path.CloseSubpath()
        path.AddRectangle(-BASE4, -BASE4/2, BASE2, BASE4)


        # Now use that path to demonstrate various capbilites of the grpahics context
        gc.PushState()             # save current translation/scale/other state 
        gc.Translate(60, 75)       # reposition the context origin

        gc.SetPen(wx.Pen("navy", 1))
        gc.SetBrush(wx.Brush("pink"))

        # show the difference between stroking, filling and drawing
        for label, PathFunc in [("StrokePath", gc.StrokePath),
                                ("FillPath",   gc.FillPath),
                                ("DrawPath",   gc.DrawPath)]:
            w, h = gc.GetTextExtent(label)
            
            gc.DrawText(label, -w/2, -BASE2-h-4)
            PathFunc(path)
            gc.Translate(2*BASE, 0)

            
        gc.PopState()              # restore saved state
        gc.PushState()             # save it again
        gc.Translate(60, 200)      # offset to the lower part of the window
        
        gc.DrawText("Scale", 0, -BASE2)
        gc.Translate(0, 20)

        # for testing clipping
        #gc.Clip(0, 0, 100, 100)
        #rgn = wx.RegionFromPoints([ (0,0), (75,0), (75,25,), (100, 25),
        #                            (100,100), (0,100), (0,0)  ])
        #gc.ClipRegion(rgn)
        #gc.ResetClip()
        
        gc.SetBrush(wx.Brush(wx.Colour(178,  34,  34, 128)))   # 128 == half transparent
        for cnt in range(8):
            gc.Scale(1.08, 1.08)    # increase scale by 8%
            gc.Translate(5,5)     
            gc.DrawPath(path)


        gc.PopState()              # restore saved state
        gc.PushState()             # save it again
        gc.Translate(400, 200)
        gc.DrawText("Rotate", 0, -BASE2)

        # Move the origin over to the next location
        gc.Translate(0, 75)

        # draw our path again, rotating it about the central point,
        # and changing colors as we go
        for angle in range(0, 360, 30):
            gc.PushState()         # save this new current state so we can 
                                   # pop back to it at the end of the loop
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(float(angle)/360, 1, 1)]
            gc.SetBrush(wx.Brush(wx.Colour(r, g, b, 64)))
            gc.SetPen(wx.Pen(wx.Colour(r, g, b, 128)))
            
            # use translate to artfully reposition each drawn path
            gc.Translate(1.5 * BASE2 * cos(radians(angle)),
                         1.5 * BASE2 * sin(radians(angle)))

            # use Rotate to rotate the path
            gc.Rotate(radians(angle))

            # now draw it
            gc.DrawPath(path)
            gc.PopState()

        gc.PopState()


app = wx.PySimpleApp()
app.frame = MainFrame()
app.MainLoop()
