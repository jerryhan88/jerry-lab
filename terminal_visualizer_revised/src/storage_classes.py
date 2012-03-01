from __future__ import division
from parameter_function import container_hs, container_vs

class Storage(object):
    def __init__(self):
        self.id, self.name = None, None
        self.px, self.py = None, None
        self.holding_containers = {}
    def __repr__(self):
        return self.name + str(self.id)
    
class QB(Storage):
    sy = container_vs * 2.2
    h_c_pos_info = sy / 2
    def __init__(self, id, px, py):
        Storage.__init__(self)
        self.name, self.id = 'QC Buffer', id
        self.px, self.py = px, py
        
class TP(Storage):
    num_of_stacks = 4
    bay_pos_info = container_hs / 2
    stack_pos_info = {}
    for x in xrange(num_of_stacks): stack_pos_info[x + 1] = container_vs / 2 + container_vs * x
    
    def __init__(self, id, px, py):
        Storage.__init__(self)
        self.name, self.id = 'TP', id
        self.px, self.py = px, py

class Block(Storage):
    num_of_bays = 45
    num_of_stacks = 8
    bay_pos_info = {}
    stack_pos_info = {}
    for x in xrange(num_of_bays):
        bay_id = x + 1
        if bay_id % 4 == 0: py = container_hs * ((bay_id // 4 - 1) + 1 / 2) + container_hs / 2
        elif bay_id % 4 == 1: py = container_hs * (bay_id // 4) + container_hs / 4
        elif bay_id % 4 == 2: py = container_hs * (bay_id // 4) + container_hs / 2
        elif bay_id % 4 == 3: py = container_hs * ((bay_id // 4) + 1 / 2) + container_hs / 4
        else: assert False
        bay_pos_info[bay_id] = py
    for x in xrange(num_of_stacks):
        stack_pos_info[x + 1] = container_vs * x + container_vs / 2
        
    def __init__(self, id, px, py):
        Storage.__init__(self)
        self.name, self.id = 'Block', id
        self.px, self.py = px, py
