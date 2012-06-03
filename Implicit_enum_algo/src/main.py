'''
Created on 2012. 6. 2.

@author: JerryHan
'''

from __future__ import division
import problem
import sys

class tnode(object):
    '''
    tree node
      C: list of jobs in cut
      CO = [o0, o1, ..., o_i, ...]: node of job i, which is in cut
      YS, TS: job sequence of yc and truck
      nat: # of trucks available for planning
      nft: # of trucks free (not restricted) for planning
    '''
    next_id = 0
    def __init__(self, C, ns, ms):
        self.id, tnode.next_id = tnode.next_id, tnode.next_id + 1
        self.C = C
        self.ns = [n.duplicate() for n in ns]
        self.ms = [m.duplicate() for m in ms]

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
    C0, ns0, ms0 = tn0.C, tn0.ns, tn0.ms
    step_2(C0)
    
def step_2(cut):
    ef_in_cut = [op.et + op.duration for op in cut]
    min_ef_id = 0
    for i, ef in enumerate(ef_in_cut):
        if ef < ef_in_cut[min_ef_id]:
            min_ef_id = i
    Gc = [op for op in cut if op.machine == cut[min_ef_id].machine]
    if len(Gc) == 0:
        # go to step 9 
        pass
    elif len(Gc) == 1:
        # go to step 6
        pass
    elif len(Gc) > 1:
        # go to step 3
        # step 3
        step_3(Gc)
    else:
        assert False
    
def step_3(Gc):
    # calc bounds of i in Gc
    bounds = []
    for i, op in enumerate(Gc):
        ect_op_in_Gc = Gc[:]
        ect_op_in_Gc.pop(i)
        op.next_by_machine = ect_op_in_Gc 
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
