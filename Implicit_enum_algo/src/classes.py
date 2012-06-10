'''
Created on 2012. 6. 2.

@author: JerryHan
'''

from __future__ import division
#from sys import maxint

class Operation(object):
    def __init__(self, num, duration, machine, item):
        self.num = num
        self.duration = duration
        self.machine = machine
        self.item = item
        self.next_by_item = []
        self.prev_by_item = []
        self.next_by_m = []
        self.prev_by_m = []
        self.es = 0
        self.ef = 0
        self.scheduled = False
    
    def __repr__(self):
        return 'op' + str(self.num)
    
    def duplicate(self):
        d_op = Operation(self.num, self.duration, self.machine, self.item)
        d_op.next_by_item = list(self.next_by_item)
        d_op.prev_by_item = list(self.prev_by_item)
        d_op.next_by_m = list(self.next_by_m)
        d_op.prev_by_m = list(self.prev_by_m)
        d_op.es = self.es
        d_op.ef = self.ef
        return d_op

class Machine(object):
    def __init__(self, num):
        self.num = num
        self.assigned_item = []
        self.seq = []
        
    def __repr__(self):
        return 'm' + str(self.num)
    
    def duplicate(self):
        d_m = Machine(self.num)
        d_m.seq = list(self.seq)
        return d_m
