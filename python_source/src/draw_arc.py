import wx, math

class MyFrame(wx.Frame): 

    def __init__(self, parent): 

        wx.Frame.__init__(self, parent, -1, "Hello wxGraphicsContext",
                          size=(400, 400)) 
        self.Bind(wx.EVT_PAINT, self.OnPaint) 


    def OnPaint(self, event): 

        dc = wx.PaintDC(self) 
        gc = wx.GraphicsContext.Create(dc) 

        path = gc.CreatePath() 
        path.AddArc(50, 100, 40, 0, -math.pi / 2 * 3, False) 

        gc.SetPen(wx.Pen("navy", 1)) 
        gc.SetBrush(wx.Brush("pink")) 

        gc.DrawPath(path) 

app = wx.PySimpleApp() 
frame = MyFrame(None) 
frame.CenterOnScreen() 
frame.Show() 
app.MainLoop() 
