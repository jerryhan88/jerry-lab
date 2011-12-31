from __future__ import division

import wx
from random import randrange, seed
from math import sqrt

class Node:
    def __init__(self, id):
        self.id = id
        self.min_d = 10000
        self.visited = False
        self.color = 0
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
        return '(' + str(self.prev.id) + '-' + str(self.next.id) + ')'

class Person:
    def __init__(self, name, start_n, end_n):
        self.name = name
        self.start_n = start_n
        self.end_n = end_n
        self.path = []

class Frame(wx.Frame):
    def __init__(self, parent, ID, title, pos, size, style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        f_size_x, f_size_y = size
        self.base_p = wx.Panel(self, -1, pos=(0, 0), size=(f_size_x, f_size_y))
        
        self.base_p.Bind(wx.EVT_PAINT, self.drawing)
        self.nodelist = []
        self.edgelist = []
        for i in range(25):
            n = Node(i)
            n.x = (i % 5) * 100 + 70
            n.y = (i // 5) * 100 + 70
            n.prev_ns = []
            n.next_ns = []
            self.nodelist.append(n)
            self.edgelist.append([])
        
        for i in range(len(self.nodelist)) :
            w = randrange(10)
            if i == 24:
                pass
            elif i % 5 == 4:
                self.edgelist[i].append(Edge(w, self.nodelist[i], self.nodelist[i + 5]))
            elif i // 5 == 4:
                self.edgelist[i].append(Edge(w, self.nodelist[i], self.nodelist[i + 1]))
            else:
                self.edgelist[i].append(Edge(w, self.nodelist[i], self.nodelist[i + 1]))
                w = randrange(10)
                self.edgelist[i].append(Edge(w, self.nodelist[i], self.nodelist[i + 5]))

        
        for es in self.edgelist:
            for e in es:
                prev_n = e.prev
                next_n = e.next
                prev_n.next_ns.append(next_n)
                next_n.prev_ns.append(prev_n)

        wx.StaticText(self.base_p, -1, 'User', (60, f_size_y - 90))
        self.user_n = wx.TextCtrl(self.base_p, -1, 'Jerry', pos=(55, f_size_y - 67), size=(50, 20))
        
        
        tem_x = 70
        wx.StaticText(self.base_p, -1, 'Choice Two nodes, start and end', (60 + tem_x, f_size_y - 90))
        wx.StaticText(self.base_p, -1, 'Start', (60 + tem_x, f_size_y - 65))
        self.start_n = wx.TextCtrl(self.base_p, -1, '0', pos=(95 + tem_x, f_size_y - 67), size=(25, 20))
        
        wx.StaticText(self.base_p, -1, 'End', (200 + tem_x, f_size_y - 65))
        self.end_n = wx.TextCtrl(self.base_p, -1, '24', pos=(230 + tem_x, f_size_y - 67), size=(25, 20))

        
        s_btn = wx.Button(self.base_p, -1, "solve", pos=(f_size_x - 100, f_size_y - 80), size=(60, 30))
        
        self.base_p.Bind(wx.EVT_BUTTON, self.start_D_algo, s_btn)
        
    def start_D_algo(self, _):
        for n in self.nodelist:
            n.color = 0
            n.min_d = 100
            n.visited = False
        name = self.user_n.GetValue()
        start_n = self.start_n.GetValue()
        end_n = self.end_n.GetValue()
        ps = Person(name, self.nodelist[int(start_n)], self.nodelist[int(end_n)])
        
        path = self.D_algo_run(ps)
        
        for i, n in enumerate(path):
            if i == 0:
                n.color = 1
            elif i==len(path)-1:
                n.color = 2
            else:
                n.color = 3
        
        print path
        self.base_p.Refresh()
        
    def D_algo_run(self, ps):
        start = ps.start_n
        end = ps.end_n
        
        start.min_d = 0
        todo = [start]
        
        while todo:
            n = todo.pop(0)
            n.visited = True
            
            for e in self.edgelist[n.id]:
                target_n = e.next
                
                dist = n.min_d + e.w
                
                if target_n.min_d >= dist:
                    target_n.min_d = dist
                if not target_n.visited and not [x for x in todo if target_n.id == x.id]:
                    todo.append(target_n)
        
        ps.path.append(end)
        target_n = end
        while target_n:
            for prev_n in target_n.prev_ns:
                w = [e.w for e in self.edgelist[prev_n.id] if e.next == target_n]
                if prev_n.min_d + w[0] == target_n.min_d:
                    target_n = prev_n
                    break
            else:
                target_n = None
                break
            ps.path.append(target_n)
        ps.path.reverse()
        return  ps.path
        
    def drawing(self, _):
        dc = wx.PaintDC(self.base_p)
        self.base_p.PrepareDC(dc)

        old_pen = dc.GetPen()
        dc.SetPen(wx.Pen(wx.BLACK, 2))

        r, g, b = (236, 233, 216)
        

        for n in self.nodelist:
            if n.color ==1:
                r, g, b = (255, 0, 0)
            elif n.color ==2:
                r, g, b = (0, 255, 0)
            elif n.color ==3:
                r, g, b = (0, 0, 255)
            else:
                r, g, b = (236, 233, 216)    
            brushclr = wx.Colour(r, g, b, 100)
            dc.SetBrush(wx.Brush(brushclr))
            dc.DrawCircle(n.x, n.y, 30)
            dc.DrawText(str(n.id), n.x - 7, n.y - 7)
        
        for es in self.edgelist:
            for e in es:
                prev_n = e.prev
                next_n = e.next
                
                ax = next_n.x - prev_n.x
                ay = next_n.y - prev_n.y
                la = sqrt(ax * ax + ay * ay);
                ux = ax / la;
                uy = ay / la;

                sx = prev_n.x + (int) (ux * 30);
                sy = prev_n.y + (int) (uy * 30);
                ex = next_n.x - (int) (ux * 30);
                ey = next_n.y - (int) (uy * 30);

                px = -uy;
                py = ux;
                
                dc.DrawLine(sx, sy, ex, ey);
                dc.DrawLine(ex, ey, ex - (int) (ux * 5) + (int) (px * 3), ey
                        - (int) (uy * 5) + (int) (py * 3));
                dc.DrawLine(ex, ey, ex - (int) (ux * 5) - (int) (px * 3), ey
                        - (int) (uy * 5) - (int) (py * 3));
                
                dc.DrawText(str(e.w), sx, sy)
                    
#            dc.DrawLine()
        

        dc.EndDrawing()
    
if __name__ == '__main__':
    seed(0)
    app = wx.PySimpleApp()
    mv = Frame(None, -1, 'Main_viewer', pos=(100, 100), size=(600, 600))
    mv.Show(True)
    app.MainLoop()
