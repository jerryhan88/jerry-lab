from __future__ import division

class Container(object):
    def __init__(self, _id):
        self._id = _id
        self.moving_seq = []
        self.cur_position = None
        self.cur_index_in_ms = None
        
    def __repr__(self):
        return self._id

class Stack(object):
    def __init__(self, id):
        self.id = id
        self.px = None
        self.py = None
        self.stack = []

class Bay(object):
    def __init__(self, id):
        self.id = id
        self.px = None
        self.py = None
        self.stacks = []

class Block(object):
    def __init__(self, id, px, py):
        self.id = id
        self.px = px
        self.py = py
        self.holding_container = []
    
    def draw(self, gc):
#        gc.D
        pass

class Yard_block(Block):
    def __init__(self):
        self.sea_side_TP# = object of TP
        self.land_side_TP# = object of TP
        self.waiting_sc# = object of SC
        self.qc_buffer# = object of QC_buffer
        

class Vessel(object):
    def __init__(self, name, voyage):
        self.name = name
        self.voyage = voyage
        self.evt_seq = []
        self.px, self.py = (0, 0)
        
    def __repr__(self):
        return self.name + ' : ' + str(self.voyage)
#        self.block# = object of Block

class QC(object):
    def __init__(self, name):
        self.name = name
        self.evt_seq = []
        self.px, self.py = (0, 0)
#        self.sequence# = [(vessel, bay, column, time), ]
    def __repr__(self):
        return self.name

class YC(object):
    def __init__(self, name):
        self.name = name
        self.evt_seq = []
        self.px, self.py = (0, 0)
#        self.sequence# = [(bay, column, time), ]
    def __repr__(self):
        return self.name

class SC(object):
    def __init__(self, name):
        self.name = name
        self.evt_seq = []
        self.px, self.py = (0, 0)
#        self.sequence #= [(qc, block, time), ]
    def __repr__(self):
        return self.name

class Buffer(object):
    def __init__(self):
        self.holding_containers #= [objects of Container]

class TP(Buffer):
    pass

class QC_buffer(Buffer):
    pass
