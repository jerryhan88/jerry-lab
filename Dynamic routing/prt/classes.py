from __future__ import division
from math import sqrt
import wx

class Node():
    _id = 0
    MAXD = 1e400
    def __init__(self, px, py):
        self.id = Node._id
        self.px, self.py = None, None
        self.visited, self.min_d = False, Node.MAXD
        
        self.edges_inward, self.edges_outward = [], []
        self.cus_queue = []
        
        self.set_position(px, py)

        Node._id += 1
        
    def __repr__(self):
        return 'N%d' % self.id
    
    def init_node(self):
        self.visited = False
        self.min_d = Node.MAXD
    
    def set_position(self, px, py):
        self.px, self.py = px, py
        
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
          
class Customer():
    def __init__(self, re_time, _id, sn, dn):
        self.re_time, self.id, self.sn, self.dn = re_time, _id, sn, dn
        self.marked = False
        
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

    def init_position(self, n):
        self.arrived_n = n
        self.set_position(n.px, n.py)
    
    def set_position(self, px, py):
        self.px, self.py = px, py
    
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
    
