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
    for i, op_num in enumerate(Gc):
        nn = tnode(tn.C, tn.ns, tn.ms)
        C, ns, ms = nn.C, nn.ns, nn.ms
        print 'selected operation : op', op_num
        target_op = ns[op_num]
#        print target_op
#        print C 
        for j, op_c_num in enumerate(C):
            if op_c_num == op_num:
                C.pop(j)
                break
        else:
            assert False
        except_op_Gc = list(Gc)
        except_op_Gc.pop(i)
        
        target_op.next_by_machine = except_op_Gc
        
        for op_num in except_op_Gc:
            ns[op_num].prev_by_m.append(target_op.num)
          
#        print target_op, ' ', target_op.next_by_machine
        target_op.scheduled = True
        ms[target_op.machine].seq.append(target_op.num)
        calc_es(ns)
        
#        for op in ns[1:-1]:
#            print op, ' ', 'op.next_by_m: ', op.next_by_m
#            print '        es: ', op.es, '    D :', op.duration, '    ef:', op.es + op.duration
        
        beta_ms = set([ns[p_op_num].machine for p_op_num in ns[-1].prev_by_item])
        
        
        run_thm2(beta_ms, ns, ms);
        
        print ''
        
def run_thm2(beta_ms, ns, ms):
    dup_ms = [m.duplicate() for m in ms]
    for m_num in beta_ms:
        beta_m = [op_num for op_num in dup_ms[m_num].assigned_item if not ns[op_num].scheduled]
        es_incre_order = sorted([(ns[op_num].es, op_num) for op_num in beta_m])
#        print dup_ms[m_num], ' ', es_incre_order
        for _, op_num in es_incre_order:
            dup_ms[m_num].seq.append(op_num)
#        print dup_ms[m_num].seq
    dup_ns = [n.duplicate() for n in ns]
    for m in dup_ms[1:]:
#        print m, ' ',
#        unscheduled_items = [op_num for op_num in m.assigned_item if not ns[op_num].scheduled]
        assigned_items = m.assigned_item[:]
#        print unscheduled_items,
        for op_num in m.seq:
            for i, ass_i in enumerate(assigned_items):
                if ass_i == op_num:
                    assigned_items.pop(i)
                    break
            else:
                assert False
            dup_ns[op_num].next_by_m = list(assigned_items) 
            for ass_i in assigned_items:
                if op_num not in dup_ns[ass_i].prev_by_m:  
                    dup_ns[ass_i].prev_by_m.append(op_num)
            
#            print op_num ,
#        print '~~~~'
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    calc_es(dup_ns)
    for op in dup_ns[1:-1]:
        print op, ' ', 'op.next_by_m: ', op.next_by_m
        print '        es: ', op.es, '    D :', op.duration, '    ef:', op.es + op.duration 
    print 'lowBound : ', dup_ns[-1].pf_t 

def calc_es(ns):
    src = ns[0]
    target_n = src
    todo = target_n.next_by_item[:]
    while todo:
        target_op = ns[todo.pop(0)]
        p_ops = target_op.prev_by_item + target_op.prev_by_m
#        print target_op, p_ops
        for p_op in p_ops:
            new_es = ns[p_op].es + ns[p_op].duration 
            if target_op.es < new_es:
                target_op.es = new_es
                target_op.ef = target_op.es + target_op.duration
            for n_op in target_op.next_by_item + target_op.next_by_m:
                if n_op != '*' and n_op not in todo:
                    todo.append(n_op)
#    for op in ns[1:-1]:
#        op.ef = op.es+op.duration
#    for n in ns:
#        print n, ' ', n.es
    # project finish time
    ns[-1].pf_t = 0
    for op_num in ns[-1].prev_by_item:
        new_pf_t = ns[op_num].es + ns[op_num].duration
        if ns[-1].pf_t < new_pf_t:
            ns[-1].pf_t = new_pf_t
            
if __name__ == '__main__':
    run()
