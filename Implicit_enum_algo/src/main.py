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
#    print [ns[x] for x in C]
    calc_es(ns)
    ns[-1].es = sys.maxint
#    print [n.es for n in ns]
    BT = [tnode(C, ns, ms)]
#    # step 2
    tn0 = BT.pop()
    step_2(tn0, BT)
    
def step_2(tn, BT):
    C0, ns0, ms0 = tn.C, tn.ns, tn.ms
    ef_in_cut = [ns0[op_num].es + ns0[op_num].duration for op_num in C0]
    min_ef_id = 0
    for i, ef in enumerate(ef_in_cut):
        if ef < ef_in_cut[min_ef_id]:
            min_ef_id = i
    Gc = [op_num for op_num in C0 if ns0[op_num].machine == ns0[C0[min_ef_id]].machine]
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
        
        beta_m = []
        
def calc_b():
    pass

def calc_es(ns):
    src = ns[0]
    
    target_n = src
    todo = target_n.next_by_item
#    print todo
    
    while todo:
        target_op = ns[todo.pop(0)]
#        print target_op, 
        p_ops = target_op.prev_by_item
#        print p_ops
        for p_op in p_ops:
            new_es = ns[p_op].es + ns[p_op].duration 
            if target_op.es < new_es:
                target_op.es = new_es
            for n_op in target_op.next_by_item:
                if n_op !='*':
                    todo.append(n_op)
#    for n in ns:
#        print n, ' ', n.es
    # project finish time
    ns[-1].pf_t = 0
    for op_num in ns[-1].prev_by_item:
        new_pf_t = ns[op_num].es + ns[op_num].duration
        if ns[-1].pf_t < new_pf_t:
            ns[-1].pf_t = new_pf_t
#    print ns[-1].pf_t 
            
if __name__ == '__main__':
    run()
