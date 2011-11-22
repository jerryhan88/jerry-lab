from __future__ import division

import wx
from random import randrange

class Node:
    def __init__(self, id):
        self.id = id
        self.min_d = None
        self.x = None
        self.y = None
    def __repr__(self):
        return str(self.id)

class Edge:
    def __init__(self, w, prev, next):
        self.w = w
        self.prev = prev
        self.next = next
    def __repr__(self):
        return '('+str(self.prev.id) +'-'+ str(self.next.id)+')'

class Frame(wx.Frame):
    def __init__(self, parent, ID, title, pos, size, style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        self.p = wx.Panel(self, -1, pos=(0, 0), size=(600, 600))
        self.p.Bind(wx.EVT_PAINT, self.drawing)
        self.nodelist = []
        self.edgelist = []
        for i in range(25):
            n = Node(i)
            n.x = (i % 5) * 100 + 70
            n.y = (i // 5) * 100 + 70
            self.nodelist.append(n)
            self.edgelist.append([])
        
        for i in range(len(self.nodelist)) :
            w = randrange(10)
            if i % 5 == 4:
                if i != 24:
                    self.edgelist[i].append(Edge(w, self.nodelist[i], self.nodelist[i + 5]))
            elif i // 5 == 4:
                if i != 24:
                    self.edgelist[i].append(Edge(w, self.nodelist[i], self.nodelist[i + 1]))
            else:
                self.edgelist[i].append(Edge(w, self.nodelist[i], self.nodelist[i + 1]))
                self.edgelist[i].append(Edge(w, self.nodelist[i], self.nodelist[i + 5]))
        
        
        print self.edgelist    
        
    def drawing(self, _):
        dc = wx.PaintDC(self.p)
        self.p.PrepareDC(dc)

        old_pen = dc.GetPen()
        dc.SetPen(wx.Pen(wx.BLACK, 2))

        r, g, b = (236, 233, 216)
        brushclr = wx.Colour(r, g, b, 100)
        dc.SetBrush(wx.Brush(brushclr))

        for n in self.nodelist:
            dc.DrawCircle(n.x, n.y, 30)
            
        
        for es in self.edgelist:
            for e in es:
                prev_n=e.prev
                next_n=e.next
                
                ax = next_n.x - prev_n.x
                ay = next_n.y - prev_n.y
                la = Math.sqrt(ax * ax + ay * ay);
                
                pass
            
#            
#            ax = n1.x - x;
#            ay = n1.y - y;
#    
#            la = Math.sqrt(ax * ax + ay * ay);
#    
#            ux = ax / la;
#            uy = ay / la;
#    
#            sx = x + (int) (ux * 5) - 10;
#            sy = y + (int) (uy * 5) - 10;
#            ex = n1.x - (int) (ux * 5) - 10;
#            ey = n1.y - (int) (uy * 5) - 10;
#    
#            px = -uy;
#            py = ux;
#            g.drawLine(sx, sy, ex, ey);
#            g.drawLine(ex, ey, ex - (int) (ux * 5) + (int) (px * 3), ey
#                    - (int) (uy * 5) + (int) (py * 3));
#            g.drawLine(ex, ey, ex - (int) (ux * 5) - (int) (px * 3), ey
#                    - (int) (uy * 5) - (int) (py * 3));
#                
#                
#            
#            dc.DrawLine()
#        
       

        

        dc.EndDrawing()
    
if __name__ == '__main__':
    app = wx.PySimpleApp()
    mv = Frame(None, -1, 'Main_viewer', pos=(100, 100), size=(600, 600))
    mv.Show(True)
    app.MainLoop()
