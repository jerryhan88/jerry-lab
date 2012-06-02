'''
Created on 2012. 6. 2.

@author: JerryHan
'''

from __future__ import division

class Node(object):
    def __init__(self, op_num, duration, machine, item):
        self.op_num = op_num
        self.duration = duration
        self.machine = machine
        self.item_num = item
        self.next_by_item = None
        self.next_by_m = None
        self.et = None
    
    def __repr__(self):
        return 'op' + str(self.op_num)
        
    def set_next_by_item(self, op):
        self.next_by_item = op
        
class Machine(object):
    def __init__(self, m_num):
        self.m_num = m_num
        self.assigned_item = []
        self.seq = []
        
    def __repr__(self):
        return 'm' + str(self.m_num)
