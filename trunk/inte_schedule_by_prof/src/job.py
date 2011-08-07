from itertools import *

class O(object):
    '''
    Operation
    next_by_op is not changed
    next_by_res and prev are repeatedly cleared and reassigned
    '''
    def __repr__(self):
        return str(self.j) + ':' + str(self.type)
    def set_prev_by_res(self, prev):
        self.prev_by_res = prev
        prev.ne
        xt_by_res = self

class O1(O):
    'Operation type 1'
    def __init__(self, job):
        self.j = job
        self.type = 1
    def remove_and_update_t(self):
        if self.prev_by_res == None:
            next_t = self.t + self.pt
            if self.next_by_op.t < next_t:
                self.next_by_op.t = next_t
            self.next_by_op.prev_by_op1 = None
            return True
        return False
    def removable(self):
        return self.prev_by_res == None

class O2(O):
    'Operation type 2'
    def __init__(self, job):
        self.j = job
        self.type = 2
    def remove_and_update_t(self):
        if self.prev_by_res == None:
            next_t = self.t + self.pt
            if self.next_by_op.t < next_t:
                self.next_by_op.t = next_t
            self.next_by_op.prev_by_op2 = None
            return True
        return False
    def removable(self):
        return self.prev_by_res == None
    
class O3(O):
    'Operation type 3'
    def __init__(self, prev1, prev2, job):
        prev1.next_by_op = self
        prev2.next_by_op = self
        self.j = job
        self.type = 3
    def remove_and_update_t(self):
        if self.prev_by_op1 == None and self.prev_by_op2 == None:
            next_t = self.t + self.pt
            if self.next_by_op.t < next_t:
                self.next_by_op.t = next_t
            self.next_by_op.prev_by_op = None
            if self.next_by_res:
                if self.next_by_res.t < self.t:
                    self.next_by_res.t = self.t
                self.next_by_res.prev_by_res = None
            return True
        return False
    def removable(self):
        return self.prev_by_op1 == None and self.prev_by_op2 == None
    
class O4(O):
    'Operation type 4'
    def __init__(self, prev, job):
        prev.next_by_op = self
        self.j = job
        self.type = 4
    def remove_and_update_t(self):
        if self.prev_by_op == None and self.prev_by_res == None:
            next_t = self.t + self.pt
            if self.next_by_op.t < next_t:
                self.next_by_op.t = next_t
            self.next_by_op.prev_by_op = None
            if self.next_by_res:
                if self.next_by_res.t < self.t:
                    self.next_by_res.t = self.t
                self.next_by_res.prev_by_res = None
            return True
        return False
    def removable(self):
        return self.prev_by_op == None and self.prev_by_res == None
    
class O5(O):
    'Operation type 5'
    def __init__(self, prev, job):
        prev.next_by_op = self
        self.j = job
        self.type = 5
    def remove_and_update_t(self):
        if self.prev_by_op == None:
            if self.next_by_res:
                if self.next_by_res.t < self.t:
                    self.next_by_res.t = self.t
                self.next_by_res.prev_by_res = None
            return True
        return False
    def removable(self):
        return self.prev_by_op == None
    
class J(object):
    'Job'
    index = 1

    def __init__(self, block):
        self.index = J.index
        J.index = J.index + 1

        self.block = block
        o1 = O1(self)
        o2 = O2(self)
        o3 = O3(o1, o2, self)
        o4 = O4(o3, self)
        o5 = O5(o4, self)
        self.ops = [o1, o2, o3, o4, o5]
        
    def initialize(self):
        self.ops[0].prev_by_res = None
        self.ops[1].prev_by_res = None
        self.ops[2].prev_by_op1 = self.ops[0]
        self.ops[2].prev_by_op2 = self.ops[1]
        self.ops[2].next_by_res = None
        self.ops[3].prev_by_op = self.ops[2]
        self.ops[3].prev_by_res = None
        self.ops[3].next_by_res = None
        self.ops[4].prev_by_op = self.ops[3]
        self.ops[4].next_by_res = None
        for o in self.ops:
            o.t = 0
            o.scheduled = False
        self.ops[4].scheduled = True
        return self.ops

    def begin_node(self): return self.ops[0]
    def yt_begin(self): return self.ops[1]
    def yt_middle(self): return self.ops[2]
    def yt_end(self): return self.ops[3]

class D(J):
    'Discharging job'
    def __init__(self, block):
        J.__init__(self, block)
        self.ops[0].pt = 3
        self.ops[1].pt = 5
        self.ops[2].pt = 5
        self.ops[3].pt = 4
    def __repr__(self):
        return str(self.index) + ':D' + str(self.block)
    def qc_begin(self): return self.ops[0]
    def qc_end(self): return self.ops[2]
    def yc_begin(self): return self.ops[3]
    def yc_end(self): return self.ops[4]

class L(J):
    'Loading job'
    def __init__(self, block):
        J.__init__(self, block)
        self.ops[0].pt = 4
        self.ops[1].pt = 5
        self.ops[2].pt = 5
        self.ops[3].pt = 3
    def __repr__(self):
        return str(self.index) + ':L' + str(self.block)
    def qc_begin(self): return self.ops[3]
    def qc_end(self): return self.ops[4]
    def yc_begin(self): return self.ops[0]
    def yc_end(self): return self.ops[2]


# qs: qc schedule, ys: yc schedule, ts: yt schedule
def build_graph(qs, ys, ts):
    nodes = reduce(lambda x, j: x + j.initialize(), chain(*qs), [])
        
    for sq in qs:
        if sq:
            sq[0].qc_begin().scheduled = True
            for i in xrange(1, len(sq)):
                sq[i].qc_begin().set_prev_by_res(sq[i - 1].qc_end())
                sq[i].qc_begin().scheduled = True

    for sy in ys:
        if sy:
            sy[0].yc_begin().scheduled = True
            for i in xrange(1, len(sy)):
                sy[i].yc_begin().set_prev_by_res(sy[i - 1].yc_end())
                sy[i].yc_begin().scheduled = True
                
    for st in ts:
        if st:
            st[0].yt_begin().scheduled = True
            if st[0].begin_node().scheduled:
                st[0].yt_middle().scheduled = True
            for i in xrange(1, len(st)):
                st[i].yt_begin().set_prev_by_res(st[i - 1].yt_end())
                st[i].yt_begin().scheduled = True
                if st[i].begin_node().scheduled:
                    st[i].yt_middle().scheduled = True
                
    return nodes

def calc_makespan(qs, ys, ts):
    todo = build_graph(qs, ys, ts)
    makespan = 0
    while todo:
        for i in xrange(len(todo)):
            node = todo[i]
            if node.remove_and_update_t():
                if makespan < node.t:
                    makespan = node.t
                del todo[i]
                break
        else:  # cycle!
            return None
    return makespan

if __name__ == '__main__':
    # jobs and QC schedule
    j0, j1, j2, j3, j4 = D(0), L(1), D(1), L(0), L(0)
    qs = [[j0, j1, j2], [j3, j4]]

    # schedule example 1
    ys = [[j3, j0, j4], [j1, j2]]
    ts = [[j0, j2], [j1, j3, j4]]
    ms = calc_makespan(qs, ys, ts)
    print 'makespan = ', ms

    # schedule example 2
    ts = [[j0, j1, j2], [j3, j4]]
    ms = calc_makespan(qs, ys, ts)
    print 'makespan = ', ms
