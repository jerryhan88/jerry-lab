from util import DragZoomPanel
import wx, Dynamics
from math import sqrt

STATION_DIAMETER = 40
JUNCTION_DIAMETER = STATION_DIAMETER / 3
DOT_DIAMETER = STATION_DIAMETER / 20

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Shortest Path test', size=(1024, 768), pos=(20, 20))
        vp = ViewPanel(self)
        
class ViewPanel(DragZoomPanel):
    def __init__(self, parent):
        DragZoomPanel.__init__(self, parent, -1, style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour(wx.WHITE)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        from Dynamics import STATION, JUNCTION, DOT
        global STATION, JUNCTION, DOT
        
        self.Nodes, self.Edges = Dynamics.Network1()
        self.Show(True)
        path_n, path_e = find_SP(Dynamics.findNode('5E'), Dynamics.findNode('14'), self.Nodes) 
        
    def OnDrawDevice(self, gc):
        pass
    
    def OnDraw(self, gc):
        old_tr = gc.GetTransform()
        
        for n in self.Nodes:
            gc.Translate(n.px, n.py)
            
            if n.visited:
                gc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
            else:
                gc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
            if n.nodeType == STATION:
                gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
                gc.DrawEllipse(-STATION_DIAMETER / 2, -STATION_DIAMETER / 2, STATION_DIAMETER, STATION_DIAMETER)
                gc.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                if len(n.id) > 1:
                    gc.DrawText('%s' % n.id, -7, -8)
                else:
                    gc.DrawText('%s' % n.id, -3, -8)
            elif n.nodeType == JUNCTION:
                gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 0.01))
                gc.DrawEllipse(-JUNCTION_DIAMETER / 2, -JUNCTION_DIAMETER / 2, JUNCTION_DIAMETER, JUNCTION_DIAMETER)
            else:
                assert n.nodeType == DOT
                gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 0.01))
                gc.DrawEllipse(-DOT_DIAMETER / 2, -DOT_DIAMETER / 2, DOT_DIAMETER, DOT_DIAMETER)
            gc.SetTransform(old_tr)
            
        for e in self.Edges:
            prev_n, next_n = e._from, e._to
            
            ax, ay = next_n.px - prev_n.px, next_n.py - prev_n.py
            la = sqrt(ax * ax + ay * ay)
            ux, uy = ax / la, ay / la
            px, py = -uy, ux
            if prev_n.nodeType == STATION and next_n.nodeType == JUNCTION:
                sx = prev_n.px + ux * STATION_DIAMETER / 2
                sy = prev_n.py + uy * STATION_DIAMETER / 2
                ex = next_n.px - ux * JUNCTION_DIAMETER / 2
                ey = next_n.py - uy * JUNCTION_DIAMETER / 2
                gc.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))  
            elif prev_n.nodeType == JUNCTION and next_n.nodeType == STATION:
                sx = prev_n.px + ux * JUNCTION_DIAMETER / 2
                sy = prev_n.py + uy * JUNCTION_DIAMETER / 2
                ex = next_n.px - ux * STATION_DIAMETER / 2
                ey = next_n.py - uy * STATION_DIAMETER / 2
                gc.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            elif prev_n.nodeType == JUNCTION and next_n.nodeType == JUNCTION:
                sx = prev_n.px + ux * JUNCTION_DIAMETER / 2
                sy = prev_n.py + uy * JUNCTION_DIAMETER / 2
                ex = next_n.px - ux * JUNCTION_DIAMETER / 2
                ey = next_n.py - uy * JUNCTION_DIAMETER / 2
                gc.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            elif prev_n.nodeType == DOT and next_n.nodeType == JUNCTION:
                sx = prev_n.px + ux * DOT_DIAMETER / 2
                sy = prev_n.py + uy * DOT_DIAMETER / 2
                ex = next_n.px - ux * JUNCTION_DIAMETER / 2
                ey = next_n.py - uy * JUNCTION_DIAMETER / 2
                gc.SetFont(wx.Font(5, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            elif prev_n.nodeType == JUNCTION and next_n.nodeType == DOT :
                sx = prev_n.px + ux * JUNCTION_DIAMETER / 2
                sy = prev_n.py + uy * JUNCTION_DIAMETER / 2
                ex = next_n.px - ux * DOT_DIAMETER / 2
                ey = next_n.py - uy * DOT_DIAMETER / 2
                gc.SetFont(wx.Font(5, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            elif prev_n.nodeType == DOT and next_n.nodeType == DOT :
                sx = prev_n.px + ux * DOT_DIAMETER / 2
                sy = prev_n.py + uy * DOT_DIAMETER / 2
                ex = next_n.px - ux * DOT_DIAMETER / 2
                ey = next_n.py - uy * DOT_DIAMETER / 2
                gc.DrawLines([(sx, sy), (ex, ey)])
                gc.SetFont(wx.Font(5, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                gc.DrawText('%d' % int(round(e.distance, 1)), (prev_n.px + next_n.px) / 2, (prev_n.py + next_n.py) / 2)
                continue
            else:
                assert False 
            
            gc.DrawLines([(ex, ey), (ex - int((ux * 5)) + int(px * 3), ey - int(uy * 5) + int(py * 3))])
            gc.DrawLines([(ex, ey), (ex - int(ux * 5) - int(px * 3), ey - int(uy * 5) - int(py * 3))])
            gc.DrawLines([(sx, sy), (ex, ey)])
            
            gc.DrawText('%d' % int(round(e.distance, 1)), (prev_n.px + next_n.px) / 2, (prev_n.py + next_n.py) / 2)
        
def find_SP(sn, en, Nodes):
    # Initialize node state for adapting Dijkstra algorithm
    for n in Nodes:
        n.init_node()
    
    # Update minimum distance
    sn.min_d = 0
    sn.visited = True
    todo = [sn]
    while todo:
        n = todo.pop()
        if not n.visited:
            for e in n.edges_inward:
                if not e._from.visited:
                    break
            else:
                n.visited = True
        for e in n.edges_outward:
            consi_n = e._to
            dist = n.min_d + e.distance
            if consi_n.min_d >= dist:
                consi_n.min_d = dist
                if not consi_n.visited and consi_n not in todo:
                    todo.append(consi_n)
                
    # Find Path
    path_n = []
    path_e = []
    consi_n = en
    while consi_n:
        path_n.append(consi_n)
        for e in consi_n.edges_inward:
            if e._from.min_d + e.distance == consi_n.min_d:
                consi_n = e._from
                path_e.append(e)
                break 
        else:
            consi_n = None
    path_n.reverse()
    path_e.reverse()
    
    print sn, en
    
    print path_n

    assert sn == path_n[0]
    assert en == path_n[-1] 
    
    return path_n, path_e

if __name__ == '__main__':
    app = wx.PySimpleApp()
    win = MainFrame()
    win.Show(True)
    app.MainLoop()
