from __future__ import division
import wx, math

def lead_cmp(e1, e2):
    l1, l2 = e1[2], e2[2]
    if l1 < l2:
        return -1;
    elif l1 == l2:
        return 0;
    elif l1 > l2:
        return 1;  

class Unit(object):
    def __init__(self, px, py):
        self.px = px
        self.py = py
        self.prev = []
        self.next = []

class Work(Unit):
    def __init__(self, w_name, px, py, candidates):
        Unit.__init__(self, px, py)
        self.name = w_name
        self.candidates = candidates
        self.candidates.sort(lead_cmp)
        self.cur_selected_candi = self.candidates[0][0]
        self.pi = self.calc_pi(self.candidates)
#        print self.candidates
#        print self.pi 
    def calc_pi(self, candi):
        ratio = []
        for i, c in enumerate(candi[:-1]):
            c_cost, c_lead = c[1], c[2]
            c_n_cost, c_n_lead = candi[i + 1][1], candi[i + 1][2]
            delta_cost = c_cost - c_n_cost
            delta_lead = c_n_lead - c_lead  
            ratio.append(delta_cost / delta_lead)
        return sum(ratio) / len(candi)

class My_frame(wx.Frame):
    def __init__(self, parent, ID, title, pos, size):
        wx.Frame.__init__(self, parent, ID, title, pos, size)
        sx, sy = self.GetSize()
        center_py = sy / 2 - 100
        btw_col = 90
        btw_row = 70
        self.u_size = 30
        u0 = Unit(btw_col, center_py)
        w1 = Work('w1', u0.px + btw_col, center_py + btw_row, [('A1', 5, 2), ('B1', 3, 4)])
        w2 = Work('w2', w1.px, center_py - btw_row, [('A2' , 3, 5), ('B2' , 2, 6)])
        w3 = Work('w3', w1.px + btw_col, w1.py, [('A3', 7, 4), ('B3' , 10, 2), ('C3', 3, 10)])
        w4 = Work('w4', w3.px + btw_col, w3.py + btw_row, [('A4', 5, 2), ('B4' , 3, 6)])
        w5 = Work('w5', w4.px, w3.py - btw_row, [('A5' , 2, 4), ('B5' , 5, 2), ('C5', 8, 1)])
        w6 = Work('w6', w4.px, w2.py, [('A6' , 4, 7), ('B6' , 3, 5), ('C6', 6, 2)])
        w7 = Work('w7', w6.px + btw_col, w5.py, [('A7', 4, 6), ('B7' , 6, 4)])
        u8 = Unit(w7.px + btw_col, w7.py)
        
        self.units = [u0, u8]
        self.works = [w1, w2, w3, w4, w5, w6, w7]
        
        path1 = [u0, w1, w3, w4, w7, u8]
        path2 = [u0, w1, w3, w5, w7, u8]
        path3 = [u0, w2, w6, u8]
        
        for p in [path1, path2, path3]:
            for i, u in enumerate(p):
                if i == 0:
                    u.next.append(p[i + 1]) 
                elif i == len(p) - 1:
                    u.prev.append(p[i - 1])
                else:
                    u.next.append(p[i + 1])
                    u.prev.append(p[i - 1])
        
        self.p = wx.Panel(self, -1)
        self.p.Bind(wx.EVT_PAINT, self.onPaint)
    
    def onPaint(self, _):
        dc = wx.PaintDC(self.p)
        self.p.PrepareDC(dc)
        dc.SetPen(wx.Pen('black', 0.5))

        for w in self.works:
            dc.DrawRectangle(w.px, w.py, self.u_size, self.u_size)
            dc.DrawText(w.name, w.px, w.py - 15)
            dc.DrawText(w.cur_selected_candi, w.px + 5, w.py + 5)
            for n_w in w.next:
                self.drawArrow(dc, w.px + self.u_size, w.py + self.u_size / 2, n_w.px, n_w.py + self.u_size / 2)
        
        for u in self.units:
            dc.DrawCircle(u.px + self.u_size / 2, u.py + self.u_size / 2, self.u_size / 2)
            for n_u in u.next:
                self.drawArrow(dc, u.px + self.u_size, u.py + self.u_size / 2, n_u.px, n_u.py + self.u_size / 2) 
            
        dc.EndDrawing()
    
    def drawArrow(self, dc, sx, sy, ex, ey):
        ax = ex - sx;
        ay = ey - sy;
        la = math.sqrt(ax * ax + ay * ay);
        ux = ax / la;
        uy = ay / la;
        px = -uy;
        py = ux;
        dc.DrawLine(sx, sy, ex, ey)
        dc.DrawLine(ex, ey, ex - int((ux * 5)) + int(px * 3), ey
                - int(uy * 5) + int(py * 3));
        dc.DrawLine(ex, ey, ex - int(ux * 5) - int(px * 3), ey
                - int(uy * 5) - int(py * 3));

if __name__ == '__main__':
    app = wx.PySimpleApp()
    mv = My_frame(None, -1, 'POCUS', pos=(100, 50), size=(800, 600))
    mv.Show(True)
    app.MainLoop()
    
