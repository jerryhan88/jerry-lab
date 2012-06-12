'''
Created on 2012. 6. 2.

@author: JerryHan
'''
from __future__ import division
import problem
import sys
from random import seed

Best_sol = sys.maxint
algo_conti = True
class tnode(object):
    next_id = 0
    def __init__(self, C, ns, ms):
        self.id, tnode.next_id = tnode.next_id, tnode.next_id + 1
        self.C = list(C)
        self.ns = [n.duplicate() for n in ns]
        self.ms = [m.duplicate() for m in ms]
        self.Bi = None
        self.parent = None
        self.children = []
    
    def __repr__(self):
        return 'tn' + str(self.id) + '  C:' + str(self.C)# + '  Bi:' + str(self.Bi) 
    
    def set_Bi(self, Bi):
        self.Bi = Bi
        
    def set_parent(self, p):
        self.parent = p
        
    def add_children(self, c):
        self.children.append(c)

def run(ns, ms):
    # problem
#    ns, ms = problem.ex2()
#    print [m.assigned_item for m in ms] 
#    ns, ms = problem.ex1()
    
    # step 1
    alpha = ns[0].next_by_item
    C = alpha[:]
#    print [ns[x] for x in C]
    calc_es(ns)
#    print [n.es for n in ns]
    # step 2
    tn0 = tnode(C, ns, ms)
    
    step_2(tn0)
    
    print 1111111111111
    
def find_Gc(tn):
    C0, ns0 = tn.C, tn.ns
    ef_in_cut = [ns0[op_num].es + ns0[op_num].duration for op_num in C0]
    min_ef_id = 0
    for i, ef in enumerate(ef_in_cut):
        if ef < ef_in_cut[min_ef_id]:
            min_ef_id = i
    Gc = [op_num for op_num in C0 if ns0[op_num].machine == ns0[C0[min_ef_id]].machine]
    return Gc    

def step_2(tn):
    print ''
    print tn
    if tn.parent:
        pc = list(tn.parent.C)
        tc = list(tn.C)
        s_pc, s_tc = set(pc), set(tc)
        chosen_op = s_pc.difference(s_tc)
        print '        chosen_op: ', chosen_op
    ns0 = tn.ns
    calc_es(ns0)
    
    Gc = find_Gc(tn)
    if len(Gc) == 0:
        # go to step 9
        print 'solve', tn
        print ''
        calc_es(ns0)
        
        global Best_sol
        if ns0[-1].pf_t < Best_sol:
            Best_sol = ns0[-1].pf_t
        step_8(tn)
    elif len(Gc) >= 1:
        # go to step 3
        # step 3
        bounds_tn = step_3(Gc, tn)
#        print bounds_tn[0][1].parent.children
        step_4_5_6_7(bounds_tn, tn)
    else:
        assert False

def step_4_5_6_7(bounds_tn, tn):
    global algo_conti
    if algo_conti:
        bounds_tn.sort()
#        print bounds_tn
        Bj, target_n = bounds_tn.pop(0)
    #        print Bj, target_n
        global Best_sol
        if Bj >= Best_sol:
            step_8(tn)
        if algo_conti:
            # step 5
            target_n.set_Bi(sys.maxint)
            # step 6,7
            # these were implemented in step 2 and 3
            step_2(target_n)

def step_8(tn):
    target_tn = tn.parent
    if target_tn.id == 0:
        print 'This is end of algorithms'
        global Best_sol
        print 'optimal solution: ', Best_sol
        global algo_conti
        algo_conti = False
    else:
        print 'back tracking ~~', target_tn
#        print 'target_n: ', target_tn ,'    children: ', target_tn.children 
        bounds_tn = [(cn.Bi, cn) for cn in target_tn.children]
#        print '    bounds_tn: ',bounds_tn 
        step_4_5_6_7(bounds_tn, target_tn)
        
    
def step_3(Gc, tn):
    bs = []
    # calc bounds of i in Gc
    print '    children node :',
    for i, op_num in enumerate(Gc):
        cn = tnode(tn.C, tn.ns, tn.ms)
        print cn,
        cn.set_parent(tn)
        tn.children.append(cn)
        C, ns, ms = cn.C, cn.ns, cn.ms
#        print 'selected operation : op', op_num
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
        bound = run_thm2(beta_ms, ns, ms);
        cn.set_Bi(bound)
        print bound, '        ',
        bs.append((cn.Bi, cn))
        if target_op.next_by_item[0] != ns[-1].num:
            cn.C.append(target_op.next_by_item[0])
#        print ''
    return bs

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
        assigned_items = list(m.assigned_item)
#        print unscheduled_items,
        for op_num in m.seq:
            for i, ass_i in enumerate(assigned_items):
                if ass_i == op_num:
                    assigned_items.pop(i)
                    break
            else:
                print m. seq, '  ', m.assigned_item , assigned_items 
                assert False, str(m) + ' op_num:' + str(op_num) + ' ass_i: ' + str(ass_i) + '    assign: ' + str(assigned_items) 
            dup_ns[op_num].next_by_m = list(assigned_items) 
            for ass_i in assigned_items:
                if op_num not in dup_ns[ass_i].prev_by_m:  
                    dup_ns[ass_i].prev_by_m.append(op_num)
#            print op_num ,
    calc_es(dup_ns)
    return dup_ns[-1].pf_t

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
#    for n in ns:
#        print n, ' ', n.es
    # project finish time
    ns[-1].pf_t = 0
    for op_num in ns[-1].prev_by_item:
        new_pf_t = ns[op_num].es + ns[op_num].duration
        if ns[-1].pf_t < new_pf_t:
#            print 'update: operation', op_num 
            ns[-1].pf_t = new_pf_t

def solve_many_pro():
    count = 95
    while True:
        print ''
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~seed ', count
        if count == 14:
            count += 1
            continue
        seed(count)
#        (num_item, num_machine, io_min, io_max, du_min, du_max):
        ns, ms = problem.gen_pro(5, 4, 2, 5, 2, 6)
        problem.display_graph(ns, ms)
        run(ns, ms)
        tnode.next_id = 0
        global Best_sol
        Best_sol = sys.maxint
        global algo_conti
        algo_conti = True
        
        count += 1
        if count == 96:
            break
if __name__ == '__main__':
    ns, ms = problem.ex2()
    run(ns, ms)
#    solve_many_pro()
