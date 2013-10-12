from __future__ import division
from math import sqrt
import wx

NODE_DIAMETER = 40
CUSTOMER_RADIUS = NODE_DIAMETER / 3
PRT_SIZE = 20

class Node():
    _id = 0
    MAXD = 10000
    def __init__(self, px, py):
        self.id = Node._id
        self.px, self.py = None, None
        
        self.edges_inward = []
        self.edges_outward = []
        
        self.set_position(px, py)
        self.visited = False
        self.min_d = None
        
        self.cus_queue = []

        Node._id += 1
        
    def __repr__(self):
        return 'N%d' % self.id
    
    def set_position(self, px, py):
        self.px, self.py = px, py
    
    def draw(self, gc):
        gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
        gc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
        gc.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        
        gc.DrawEllipse(-NODE_DIAMETER / 2, -NODE_DIAMETER / 2, NODE_DIAMETER, NODE_DIAMETER)
        gc.DrawText('N%d' % self.id, -7, -7)
        gc.DrawText('#c: %d' % len(self.cus_queue), -14, NODE_DIAMETER / 2)
        
        for c in self.cus_queue:
            c.draw(gc) 
        
class Edge():
    _id = 0
    def __init__(self, _from, _to):
        self.id = Edge._id
        Edge._id += 1
        self._from, self._to = _from, _to
        delX = self._from.px - self._to.px
        delY = self._from.py - self._to.py
        self.distance = sqrt(delX * delX + delY * delY)
        
        self._from.edges_outward.append(self)
        self._to.edges_inward.append(self)
        
    def __repr__(self):
        return 'Edge %d, N%d -> N%d' % (self.id, self._from.id, self._to.id)
    
    def gen_biDir(self, Edges):
        Edges.append(Edge(self._to, self._from))
    
    def draw(self, gc):
        ax = self._to.px - self._from.px;
        ay = self._to.py - self._from.py;
        
        la = sqrt(ax * ax + ay * ay);
        ux = ax / la;
        uy = ay / la;
         
        sx = self._from.px + ux * NODE_DIAMETER / 2
        sy = self._from.py + uy * NODE_DIAMETER / 2
        ex = self._to.px - ux * NODE_DIAMETER / 2
        ey = self._to.py - uy * NODE_DIAMETER / 2
         
        gc.DrawLines([(sx, sy), (ex, ey)])
        gc.DrawText('%d' % int(round(self.distance, 1)), (self._from.px + self._to.px) / 2, (self._from.py + self._to.py) / 2)
          
class Customer():
    def __init__(self, re_time, _id, sn, dn):
        self.re_time, self.id, self.sn, self.dn = re_time, _id, sn, dn
        self.marked = False
                
    def draw(self, gc):
        bg_clr = wx.Colour(200, 200, 200)
        gc.SetBrush(wx.Brush(bg_clr))
        gc.SetPen(wx.Pen(bg_clr, 0.5))
        gc.DrawEllipse(-CUSTOMER_RADIUS / 2, -CUSTOMER_RADIUS / 2, CUSTOMER_RADIUS, CUSTOMER_RADIUS)
        gc.DrawText(self.id, -7, -7)    
        
class PRT():
    _id = 0
    PRT_SPEED = 5
    def __init__(self):
        self.id = PRT._id
        PRT._id += 1
        self.px, self.py = None, None
        self.path_n = []
        self.path_e = []
        self.arrived_n = None
        self.target_n = None
        self.dest_n = None
        self.riding_cus = None
        
        self.ETA = 1e400
        self.sin_theta = 0.0
        self.cos_theta = 0.0
        # PRT state
        #  0: idle, 1: approaching, 2: transit
        self.state = 0   
        
    def __repr__(self):
        return 'PRT%d' % self.id

    def set_position(self, px, py):
        self.px, self.py = px, py
        
    def draw(self, gc):
        gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
        gc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
        gc.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        gc.DrawRectangle(-PRT_SIZE / 2, -PRT_SIZE / 2, PRT_SIZE, PRT_SIZE)
        gc.DrawText('PRT%d' % self.id, -PRT_SIZE / 2, -PRT_SIZE / 2 - 10)
        
        if self.riding_cus:
            self.riding_cus.draw(gc)
    
    @classmethod
    def find_NN(self, PRTs, Nodes):
        best_v = None
        for v in PRTs:
            if v.state == 0:
                best_v = v
                break
        else:
            return None
        return best_v
    
    @classmethod
    def find_NearestNode(self, v, Nodes):
        candi_nodes = [n for n in Nodes if any(c for c in n.cus_queue if c.marked == False)]
        if not candi_nodes:
            return None
        target_n = None
        nearest_distance = 1e400
        for n in candi_nodes:
            v.path_n, v.path_e = PRT.find_SP(v.arrived_n, n, Nodes)
            distance = sum([e.distance for e in v.path_e])
            if distance < nearest_distance:
                target_n = n
        return target_n
            
    def calc_btw_ns(self, TIMER_MILSEC, simul_clock):
        if len(self.path_n) > 1:
            self.target_n = self.path_n[1]
            self.ETA = simul_clock + self.path_e[0].distance / (PRT.PRT_SPEED / (TIMER_MILSEC / 1000))
            dx = self.target_n.px - self.arrived_n.px
            dy = self.target_n.py - self.arrived_n.py  
            self.cos_theta = dx / sqrt(dx * dx + dy * dy)
            self.sin_theta = dy / sqrt(dx * dx + dy * dy)
        else:
            self.target_n = self.arrived_n

    def update_pos(self, TIMER_MILSEC, simul_clock):
        if self.ETA <= simul_clock:
            self.set_position(self.target_n.px, self.target_n.py)
            self.arrived_n = self.target_n
            self.path_n.pop(0)
            self.path_e.pop(0)
            self.calc_btw_ns(TIMER_MILSEC, simul_clock)
            if self.arrived_n == self.dest_n:
                if self.state == 1:
                    self.riding_cus = self.dest_n.cus_queue.pop(0)
                    self.dest_n = self.riding_cus.dn
                    self.state = 2
                else:
                    assert self.state == 2
                    self.riding_cus = None
                    self.state = 0
        else:
            self.px += PRT.PRT_SPEED * self.cos_theta
            self.py += PRT.PRT_SPEED * self.sin_theta  
    
    def init_position(self, n):
        self.arrived_n = n
        self.set_position(n.px, n.py)
    
    @classmethod
    def find_SP(self, sn, en, Nodes):
    #     init
        for n in Nodes:
            n.visited = False
            n.min_d = Node.MAXD
            
        sn.min_d = 0
        todo = [sn]
        
        while todo:
            n = todo.pop(0)
            n.visited = True
            for e in n.edges_outward:
                consi_n = e._to
                dist = n.min_d + e.distance
                if consi_n.min_d >= dist:
                    consi_n.min_d = dist
                if not consi_n.visited and not [x for x in todo if consi_n.id == x.id]:
                    todo.append(consi_n)
        path_n = []
        path_e = []
        path_n.append(en)
        consi_n = en
        while consi_n:
            for e in consi_n.edges_inward:
                if e._from.min_d + e.distance == consi_n.min_d:
                    consi_n = e._from
                    path_e.append(e)
                    break 
            else:
                consi_n = None
                break
            path_n.append(consi_n)
        path_n.reverse()
        path_e.reverse()

        return path_n, path_e 

def t_D_algo_run(vehicle, sn, en, Nodes):
#     init
    for n in Nodes:
        n.visited = False
        n.min_d = Node.MAXD
        
    sn.min_d = 0
    todo = [sn]
    
    while todo:
        n = todo.pop(0)
        n.visited = True
        
        for e in n.edges_outward:
            target_n = e._to
            dist = n.min_d + e.distance
            
            if target_n.min_d >= dist:
                target_n.min_d = dist
            if not target_n.visited and not [x for x in todo if target_n.id == x.id]:
                todo.append(target_n)
    
    vehicle.path.append(en)
    target_n = en
    while target_n:
        for e in target_n.edges_inward:
            if e._from.min_d + e.distance == target_n.min_d:
                target_n = e._from
                break 
        else:
            target_n = None
            break
        vehicle.path.append(target_n)
    vehicle.path.reverse()
    return  vehicle.path   
         
if __name__ == '__main__':
    sx, sy = 800, 600
    Nodes = []
    Nodes.append(Node(sx * 0.2, sy * 0.3))
    Nodes.append(Node(sx * 0.6, sy * 0.2))
    Nodes.append(Node(sx * 0.1, sy * 0.5))
    Nodes.append(Node(sx * 0.4, sy * 0.6))
    Nodes.append(Node(sx * 0.6, sy * 0.45))
    Nodes.append(Node(sx * 0.85, sy * 0.35))
    Nodes.append(Node(sx * 0.3, sy * 0.85))
    Nodes.append(Node(sx * 0.8, sy * 0.65))
    
    Edges = []
    Edges.append(Edge(Nodes[0], Nodes[3]))
    Edges.append(Edge(Nodes[0], Nodes[3]))
    Edges.append(Edge(Nodes[1], Nodes[4]))
    Edges.append(Edge(Nodes[2], Nodes[3]))
    Edges.append(Edge(Nodes[3], Nodes[4]))
    Edges.append(Edge(Nodes[3], Nodes[6]))
    Edges.append(Edge(Nodes[4], Nodes[5]))
    Edges.append(Edge(Nodes[4], Nodes[7]))

    Edges.append(Edge(Nodes[0], Nodes[3]))
    Edges.append(Edge(Nodes[0], Nodes[2]))
    Edges.append(Edge(Nodes[0], Nodes[4]))
    Edges.append(Edge(Nodes[1], Nodes[4]))
    Edges.append(Edge(Nodes[1], Nodes[5]))
    Edges.append(Edge(Nodes[2], Nodes[3]))
    Edges.append(Edge(Nodes[3], Nodes[4]))
    Edges.append(Edge(Nodes[3], Nodes[6]))
    Edges.append(Edge(Nodes[4], Nodes[5]))
    Edges.append(Edge(Nodes[4], Nodes[7]))
    Edges.append(Edge(Nodes[5], Nodes[7]))
    Edges.append(Edge(Nodes[6], Nodes[7]))
    
    for e in Edges[:]:
        e.gen_biDir(Edges)
    
    prt = PRT()
    prt.find_SP(Nodes[4], Nodes[0], Nodes)
#     t_D_algo_run(prt, Nodes[4], Nodes[0], Nodes)
    
    print prt.path
    
    
#     PRTs = [PRT(0)]
#     sn, en = Nodes[5], Nodes[2] 
#     D_algo_run(PRTs[-1], sn, en, Nodes, Edges)
    
