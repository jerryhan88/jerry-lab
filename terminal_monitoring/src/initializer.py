from __future__ import division

class Container(object):
    def __init__(self):
        self.id

class Stack(object):
    def __init__(self):
        self.stack = [ ]

class Bay(object):
    def __init__(self):
        self.stacks# = [objects of Stack]

class Block(object):
    def __init__(self):
        self.bays# = [objects of Bay]

class Yard_block(Block):
    def __init__(self):
        self.sea_side_TP# = object of TP
        self.land_side_TP# = object of TP
        self.waiting_sc# = object of SC
        self.qc_buffer# = object of QC_buffer

class Vessel(object):
    def __init__(self):
        self.block# = object of Block

class QC(object):
    def __init__(self):
        self.sequence# = [(vessel, bay, column, time), ]

class YC(object):
    def __init__(self):
        self.sequence# = [(bay, column, time), ]

class SC(object):
    def __init__(self):
        self.sequence #= [(qc, block, time), ]

class Buffer(object):
    def __init__(self):
        self.holding_containers #= [objects of Container]

class TP(Buffer):
    pass

class QC_buffer(Buffer):
    pass
#yard = [objects of Yard_block]

