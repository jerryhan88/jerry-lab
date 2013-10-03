from __future__ import division
from math import sqrt

class Node():
    def __init__(self, _id):
        self.id = _id
        self.px, self.py = None, None

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
    def __init__(self, re_time, _id, sn, dn):
        pass
