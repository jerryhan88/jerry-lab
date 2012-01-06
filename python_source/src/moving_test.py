from __future__ import division
import wx, time #threading
from threading import Timer
class Node:
    def __init__(self, id):
        self.id = id
        self.x = 100
        self.y = 100

#class Timer(threading.Thread):
#    def __init__(self, seconds):
#        self.runTime = seconds

#        threading.Thread.__init__(self)
#    def run(self):
#        counter = self.runTime
#        for sec in range(self.runTime):
#            print counter
#            time.sleep(1.0)
#            counter -=1
#        print 'end'


class Frame(wx.Frame):
    def __init__(self, parent, ID, title, pos, size, style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        f_size_x, f_size_y = size
        self.base_p = wx.Panel(self, -1, pos=(0, 0), size=(f_size_x, f_size_y))
        self.base_p.Bind(wx.EVT_PAINT, self.drawing)
        self.n = Node(0);
        self.runTime = 100

        t = Timer(0, self.refresh_timer)
        t.start()
        
    def refresh_timer(self):
        print 'refresh'
        counter = self.runTime
        for sec in range(self.runTime):
#            print counter
            self.n.x +=1
            self.base_p.Refresh()
            time.sleep(0.1)
#            counter -=1
#        if self.time != 5:
#            self.n.x +=1
#            self.base_p.Refresh()
#        pass
        
    def drawing(self, _):
        dc = wx.PaintDC(self.base_p)
        self.base_p.PrepareDC(dc)
        r, g, b = (255, 0, 0)
        brushclr = wx.Colour(r, g, b, 100)
        dc.SetBrush(wx.Brush(brushclr))
        
        dc.DrawCircle(self.n.x, self.n.y, 30)
        
        dc.EndDrawing()

if __name__ == '__main__':
    app = wx.PySimpleApp()
    mv = Frame(None, -1, 'Main_viewer', pos=(200, 200), size=(300, 300))
    mv.Show(True)
    app.MainLoop()
