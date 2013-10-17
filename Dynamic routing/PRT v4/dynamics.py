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
        
    def init_node(self):
        self.visited = False
        self.min_d = Node.MAXD
    
    def __repr__(self):
        return 'N%d' % self.id
    
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
          
class Customer():
    def __init__(self, re_time, _id, sn, dn):
        self.re_time, self.id, self.sn, self.dn = re_time, _id, sn, dn

#         self.marked = False
    
    def __repr__(self):
        return '%s, sn: N%d, en: N%d' % (self.id, self.sn.id, self.dn.id)
        
class PRT():
    _id = 0
    PRT_SPEED = 5
    def __init__(self):
        self.id = PRT._id
        PRT._id += 1
        self.px, self.py = None, None
        self.path_n = []
        self.path_e = []
        self.assigned_customer = None
        self.arrived_n = None
        self.next_n = None
        self.dest_n = None
        # PRT state
        #  S0: Idle, S1: Approaching, S2: Transiting, S3: Parking
        self.state = 0   
        
        
        #------------------------------
#         self.target_n = None
#         
#         self.riding_cus = None
#         
#         self.ETA = 1e400
#         self.sin_theta = 0.0
#         self.cos_theta = 0.0
        
    def __repr__(self):
        return 'PRT%d' % self.id
    
    def set_assi_cus(self, customer):
        self.assigned_customer = customer
         
    def set_position(self, px, py):
        self.px, self.py = px, py
        
    def init_position(self, n):
        self.arrived_n = n
        self.set_position(n.px, n.py)
         
if __name__ == '__main__':
    pass

    
