'''
Created on 2012. 6. 2.

@author: JerryHan
'''
from __future__ import division
import problem
import sys
from random import seed

class tnode(object):
    next_id = 0
    def __init__(self, C, ns, ms):
        self.id, tnode.next_id = tnode.next_id, tnode.next_id + 1
        self.C = list(C)
        self.ns = [n.duplicate() for n in ns]
        self.ms = [m.duplicate() for m in ms]
        self.Bi = None
        self.LB = None
        self.parent = None
        self.children = []
    
    def __repr__(self):
        return 'tn' + str(self.id) + '  C:' + str(self.C)# + '  Bi:' + str(self.Bi) 
    
    def set_Bi(self, Bi):
        self.Bi = Bi
        self.LB = Bi
        
    def set_parent(self, p):
        self.parent = p
        
    def add_children(self, c):
        self.children.append(c)

class Algorithm(object):
    def __init__(self):
        self.is_algo_end = False
        self.t_s = sys.maxint

    def run(self, ns, ms):
        # INITIALIZE
        alpha = ns[0].next_by_item
        C = alpha[:]
        self.calc_es(ns)
        tn0 = tnode(C, ns, ms)
        tg_n = tn0 
        while not self.is_algo_end:
            self.display_tn(tg_n)
            # Extract Gc from C
            Gc = self.find_Gc(tg_n.C, tg_n.ns)
            if len(Gc) < 1:
                # A solution has been obtained - record its value
                ns = tg_n.ns
                self.calc_es(ns)
                sol_value = ns[-1].pf_t
                tg_n.Bi = sol_value 
                print 'solve'
                print 'tn: ', tg_n, '  Best solution: ', sol_value
                print ''
                if sol_value < self.t_s:
                    self.t_s = sol_value
                tg_n = self.back_tracking(tg_n)
            elif len(Gc) > 1:
                # Compute Bi and branching
                bounds_tn = self.compute_Bi_branching(Gc, tg_n)
                
                # Select MIN Bi operation
                bounds_tn.sort()
                Bj, min_Bi_child_n, selected_op = bounds_tn.pop(0)
                
                # Compare Bj and Best solution 
                if Bj >= self.t_s:
                    tg_n = self.back_tracking(tg_n)
                else:
                    # Set infinite on Bi
                    min_Bi_child_n.set_Bi(sys.maxint)
                    
                    # Update C : add successor operation
                    self.update_C_ET(selected_op, min_Bi_child_n)
                        
                    tg_n = min_Bi_child_n
                         
            elif len(Gc) == 1:
                cn = tnode(tg_n.C, tg_n.ns, tg_n.ms)
                # Connect branch tree
                cn.set_parent(tg_n)
                tg_n.children.append(cn)
                
                selected_op_num = Gc[0]
                C, ns = cn.C, cn.ns
                C.remove(selected_op_num)
                # Update C : add successor operation
                self.update_C_ET(ns[selected_op_num], cn)
                Bi = ns[-1].pf_t
                cn.set_Bi(Bi)
                tg_n = cn
                
                # Display children node
                print cn, cn.LB, '        ',
            else:
                assert False
        
        print 1111111111111
    def update_C_ET(self, selected_op, tg_n):
        ns = tg_n.ns
        if selected_op.next_by_item[0] != ns[-1].num:
            tg_n.C.append(selected_op.next_by_item[0])
        self.calc_es(ns)
             
    def back_tracking(self, cur_tn):
        tn_back_tracked = cur_tn.parent
        if tn_back_tracked.id == 0:
            print 'This is end of algorithms'
            print 'optimal solution: ', self.t_s
            self.is_algo_end = True
        else:
            print 'back tracking ~~', tn_back_tracked
            # Make bounds_tn
            bounds_tn = [] 
            for cn in tn_back_tracked.children:
                # Find selected operation
                selected_op = self.find_selected_op(tn_back_tracked, cn)
                bounds_tn.append((cn.Bi, cn, selected_op))
            #########################################################################################################
            # This part is reused            
            # Select MIN Bi operation
            bounds_tn.sort()
            Bj, min_Bi_child_n, selected_op = bounds_tn.pop(0)
            
            # Compare Bj and Best solution 
            if Bj >= self.t_s:
                self.back_tracking(tn_back_tracked)
            else:
                # Set infinite on Bi
                min_Bi_child_n.set_Bi(sys.maxint)
                # Update C : add successor operation
                print 
                self.update_C_ET(min_Bi_child_n.ns[list(selected_op)[0]], min_Bi_child_n)
                return min_Bi_child_n
            #########################################################################################################
                        
    def compute_Bi_branching(self, Gc, tn):
        # Display children node
        print '    children node :',
        bs = []
        # Branching
        for i, op_num in enumerate(Gc):
            cn = tnode(tn.C, tn.ns, tn.ms)
            # Connect branch tree
            cn.set_parent(tn)
            tn.children.append(cn)
            
            C, ns, ms = cn.C, cn.ns, cn.ms
            target_op = ns[op_num]
            
            for j, op_c_num in enumerate(C):
                if op_c_num == op_num: C.pop(j); break
            else:
                assert False
            
            # For making Graph
            except_op_Gc = list(Gc)
            except_op_Gc.pop(i)
            target_op.next_by_machine = except_op_Gc
            for op_num in except_op_Gc:
                ns[op_num].prev_by_m.append(target_op.num)
            
            # Schedule target operation and update ET 
            target_op.scheduled = True
            ms[target_op.machine].seq.append(target_op.num)
            self.calc_es(ns)
            
            # Compute Bi 
            beta_ms = set([ns[p_op_num].machine for p_op_num in ns[-1].prev_by_item])
            
            # For save data and this action is for make temp graph
            dup_ms = [m.duplicate() for m in ms]
            dup_ns = [n.duplicate() for n in ns]
            # schedule increasing order of ET
            for m_num in beta_ms:
                beta_m = [op_num for op_num in dup_ms[m_num].assigned_item if not ns[op_num].scheduled]
                es_incre_order = sorted([(ns[op_num].es, op_num) for op_num in beta_m])
                for _, op_num in es_incre_order:
                    dup_ms[m_num].seq.append(op_num)
            # Make Graph
            for m in dup_ms[1:]:
                assigned_items = list(m.assigned_item)
                for op_num in m.seq:
                    for i, ass_i in enumerate(assigned_items):
                        if ass_i == op_num: assigned_items.pop(i); break
                    else:
                        assert False, str(m) + ' op_num:' + str(op_num) + ' ass_i: ' + str(ass_i) + '    assign: ' + str(assigned_items) 
                    dup_ns[op_num].next_by_m = list(assigned_items) 
                    for ass_i in assigned_items:
                        if op_num not in dup_ns[ass_i].prev_by_m:  
                            dup_ns[ass_i].prev_by_m.append(op_num)
            # Compute ET of temp Graph
            self.calc_es(dup_ns)
            
            # This is low bound
            bound = dup_ns[-1].pf_t  
            cn.set_Bi(bound)
            
            # Find selected operation for update C
            
            # Keep low bound and tn    
            bs.append((cn.Bi, cn, target_op))
            # Display children node
            print cn, cn.LB, '        ',
        return bs
    
    def find_selected_op(self, p_n, c_n):
        pc = list(p_n.C)
        tc = list(c_n.C)
        s_pc, s_tc = set(pc), set(tc)
        selected_op = s_pc.difference(s_tc)
        return selected_op
    
    def find_Gc(self, C, ns):
        ef_in_cut = [ns[op_num].es + ns[op_num].duration for op_num in C]
        min_ef_id = 0
        for i, ef in enumerate(ef_in_cut):
            if ef < ef_in_cut[min_ef_id]:
                min_ef_id = i
        Gc = [op_num for op_num in C if ns[op_num].machine == ns[C[min_ef_id]].machine]
        return Gc        
        
    def display_tn(self, tn):
        print ''
        print tn
        if tn.parent:
            selected_op = self.find_selected_op(tn.parent, tn)
            print '        chosen_op: ', selected_op
    
    def calc_es(self, ns):
        src = ns[0]
        target_n = src
        # Init TODO
        todo = target_n.next_by_item[:]
        while todo:
            target_op = ns[todo.pop(0)]
            # Find out going edges
            p_ops = target_op.prev_by_item + target_op.prev_by_m
            for p_op in p_ops:
                new_es = ns[p_op].es + ns[p_op].duration 
                if target_op.es < new_es:
                    target_op.es = new_es
                    target_op.ef = target_op.es + target_op.duration
                for n_op in target_op.next_by_item + target_op.next_by_m:
                    if n_op != '*' and n_op not in todo:
                        todo.append(n_op)
        # Calc project finish time
        ns[-1].pf_t = 0
        for op_num in ns[-1].prev_by_item:
            new_pf_t = ns[op_num].es + ns[op_num].duration
            if ns[-1].pf_t < new_pf_t:
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
        algo_engine = Algorithm() 
        algo_engine.run(ns, ms)
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
    algo_engine = Algorithm() 
    algo_engine.run(ns, ms)
#    solve_many_pro()
