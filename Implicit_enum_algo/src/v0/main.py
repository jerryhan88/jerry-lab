'''
Created on 2012. 6. 2.

@author: JerryHan
'''

from __future__ import division
import problem
import sys

class tnode(object):
    next_id = 0
    def __init__(self, C, ns, ms):
        self.id, tnode.next_id = tnode.next_id, tnode.next_id + 1
        self.C = list(C)
        self.ns = [n.duplicate() for n in ns]
        self.ms = [m.duplicate() for m in ms]
    
    def set_lb(self, lb):
        self.lb = lb

def run():
    ns, ms = problem.ex2()
#    ns, ms = problem.ex1()
    
    # step 1
    alpha = ns[0].next_by_item
    C = alpha[:]
    calc_et(ns)
    ns[-1].et = sys.maxint
    BT = [tnode(C, ns, ms)]
    # step 2
    tn0 = BT.pop()
    step_2(tn0, BT)
    
def step_2(tn, BT):
    C0, ns0, ms0 = tn.C, tn.ns, tn.ms
    ef_in_cut = [op.et + op.duration for op in C0]
    min_ef_id = 0
    for i, ef in enumerate(ef_in_cut):
        if ef < ef_in_cut[min_ef_id]:
            min_ef_id = i
    Gc = [op for op in C0 if op.machine == C0[min_ef_id].machine]
    if len(Gc) == 0:
        # go to step 9 
        pass
    elif len(Gc) == 1:
        # go to step 6
        pass
    elif len(Gc) > 1:
        # go to step 3
        # step 3
        bounds = step_3(Gc, tn, BT)
        step_4()
        step_5()
    else:
        assert False

def step_4():
    pass

def step_5():
    pass
    
def step_3(Gc, tn, BT):
    # calc bounds of i in Gc
    for i, op in enumerate(Gc):
        nn = tnode(tn.C, tn.ns, tn.ms)
        C, ns, ms = nn.C, nn.ns, nn.ms
        target_op = ns[op.op_num] 
        for j, op_c in enumerate(C):
            if op_c.op_num == op.op_num:
                C.pop(j)
                break
        else:
            assert False
        except_op_Gc = list(Gc)
        except_op_Gc.pop(i)
        target_op.next_by_machine = except_op_Gc  
        print target_op, ' ', target_op.next_by_machine
        target_op.scheduled = True
        
        
def calc_b():
    pass

def calc_et(ns):
    src = ns[0]
    
    target_n = src
    todo = target_n.next_by_item
#    print todo
    while todo:
        target_n = todo.pop(0)
        prev_n = target_n.prev_by_item        
        new_et = prev_n.et + prev_n.duration
        if target_n.et < new_et:
            target_n.et = new_et
        next_n = target_n.next_by_item
        if next_n.op_num != '*':
            todo.append(next_n)
    
#    for n in ns:
#        print n, ' ', n.et
        
    ns[-1].pf_t = 0
    for n in ns[-1].prev_by_item:
        new_pf_t = n.et + n.duration
        if ns[-1].pf_t < new_pf_t:
            ns[-1].pf_t = new_pf_t
            
#    print ns[-1].pf_t 
            
if __name__ == '__main__':
    run()
