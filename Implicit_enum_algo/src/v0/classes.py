'''
Created on 2012. 6. 2.

@author: JerryHan
'''

from __future__ import division
#from sys import maxint

class Operation(object):
    def __init__(self, op_num, duration, machine, item):
        self.op_num = op_num
        self.duration = duration
        self.machine = machine
        self.item_num = item
        self.next_by_item = None
        self.prev_by_item = None
        self.next_by_m = []
        self.prev_by_m = []
        self.et = 0
        self.ef = 0
        self.scheduled = False
    
    def __repr__(self):
        return 'op' + str(self.op_num)
    
    def duplicate(self):
        d_op = Operation(self.op_num, self.duration, self.machine, self.item_num)
        d_op.next_by_item = self.next_by_item
        d_op.prev_by_item = self.prev_by_item
        d_op.next_by_m = list(self.next_by_m)
        d_op.prev_by_m = list(self.prev_by_m)
        d_op.et = self.et
        d_op.ef = self.ef
        return d_op
        
    def set_next_by_item(self, op):
        self.next_by_item = op
    
    def set_prev_by_item(self, op):
        self.prev_by_item = op
    
    def set_next_by_machine(self, op):
        self.next_by_m = op

class Machine(object):
    def __init__(self, m_num):
        self.m_num = m_num
        self.assigned_item = []
        self.seq = []
        
    def __repr__(self):
        return 'm' + str(self.m_num)
    
    def duplicate(self):
        d_m = Machine(self.m_num)
        d_m.seq = list(self.seq)
        return d_m
