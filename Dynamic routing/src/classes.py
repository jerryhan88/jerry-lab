from __future__ import division
from math import sqrt

class Node():
    min_dis = 10000
    def __init__(self, _id):
        self.id = _id
        self.px, self.py = None, None
        self.visited = False
        self.edges = []

class Edge():
    def __init__(self, _from, _to):
        self._from, self._to = _from, _to
        delX = self._from.px - self._to.px
        delY = self._from.py - self._to.py  
        self.distance = sqrt(delX * delX + delY * delY)
          
class Customer():
    def __init__(self, re_time, _id, sn, dn):
        self.re_time, self.id, self.sn, self.dn = re_time, _id, sn, dn
        self.px, self.py = self.sn.px, self.sn.py        
        
class PRT():
    def __init__(self, _id):
        self.id = _id
        self.px, self.py = None, None
        self.path = []
    def set_position(self, px, py):
        self.px, self.py = px, py
        


def D_algo_run(self, vehicle, sn, en, Nodes, Edges):
    
    
        start = sn
        end = en
        
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
         
if __name__ == '__main__':
    sx, sy = 800, 600
    Nodes = [Node(x) for x in range(8)]
    Nodes[0].px, Nodes[0].py = sx * 0.2, sy * 0.3
    Nodes[1].px, Nodes[1].py = sx * 0.6, sy * 0.2
    Nodes[2].px, Nodes[2].py = sx * 0.1, sy * 0.5
    Nodes[3].px, Nodes[3].py = sx * 0.4, sy * 0.6
    Nodes[4].px, Nodes[4].py = sx * 0.6, sy * 0.45
    Nodes[5].px, Nodes[5].py = sx * 0.85, sy * 0.35
    Nodes[6].px, Nodes[6].py = sx * 0.3, sy * 0.85
    Nodes[7].px, Nodes[7].py = sx * 0.8, sy * 0.65
    
    Edges = []
    Edges.append(Edge(Nodes[0], Nodes[3]))
    Edges.append(Edge(Nodes[1], Nodes[4]))
    Edges.append(Edge(Nodes[2], Nodes[3]))
    Edges.append(Edge(Nodes[3], Nodes[4]))
    Edges.append(Edge(Nodes[3], Nodes[6]))
    Edges.append(Edge(Nodes[4], Nodes[5]))
    Edges.append(Edge(Nodes[4], Nodes[7]))
    
    PRTs = [PRT(0)]
    sn, en = Nodes[5], Nodes[2] 
    D_algo_run(PRTs[-1], sn, en, Nodes, Edges)
    