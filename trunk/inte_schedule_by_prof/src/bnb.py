from job import *

M = 1000000

# ys = yc schedule (sequences of yc jobs), yf = yc finish times
# ts = yt schedule (sequences of yt jobs), tf = yt finish times
class Node:
    'Node for B&B'
    def __repr__(self):
        return '(' + str(self.lb) + ') ' + str(self.ys) + ' : ' + str(self.yf) + ' / ' + str(self.ts) + ' : ' + str(self.tf)
    def copy(self, other):
        self.ys = [sy[:] for sy in other.ys]
        self.yf = other.yf[:]
        self.ts = [st[:] for st in other.ts]
        self.tf = other.tf[:]
    def create_with_new_yc_node(self, other, index, job, qs):
        self.copy(other)
        self.ys[index].append(job)
        self.lb = calc_makespan(qs, self.ys, self.ts)
        self.yf[index] = job.yc_end().t
        self.num = other.num - 1
    def create_with_new_yt_node(self, other, index, job, qs):
        self.copy(other)
        self.ts[index].append(job)
        self.lb = calc_makespan(qs, self.ys, self.ts)
        self.tf[index] = job.yt_end().t
        self.num = other.num - 1


def solve(qs, num_yc, num_yt):
    # todo list and iteration #
    root = Node()
    root.ys = [[] for i in xrange(num_yc)]
    root.yf = [0 for i in xrange(num_yc)]
    root.ts = [[] for i in xrange(num_yt)]
    root.tf = [0 for i in xrange(num_yt)]
    root.lb = 0
    root.num = sum([len(sq) for sq in qs]) * 2
    todo = [root]
    t = 0

    # best makespan so far
    z_best = M
    n_best = None

    while todo:
        current = todo.pop()

        t = t + 1
        #print t, current
        #print t,

        if current.lb >= z_best:
            #print '\tprune because LB is not less than best so far'
            continue

        nodes = build_graph(qs, current.ys, current.ts)

        # remove nodes that are both scheduled and removable
        # t of node will be updated while removing
        while nodes:
            removed = False
            for i in xrange(len(nodes)):
                n = nodes[i]
                if n.scheduled and n.remove_and_update_t():
                    removed = True
                    del nodes[i]
                    break
            if not removed:
                break
            
        # collect schedulable nodes
        # yt node is included if job's beginning node is scheduled
        so = [n for n in nodes if n.removable() and (n.type != 2 or n.j.yt_middle().t > 0)]
        #print '\tSO:', so

        # find earlist finishable node
        min_f = M
        min_n = None
        min_i = None
        for n in so:
            assert(not n.scheduled)
            if n.type == 2: # yt
                for i in xrange(num_yt):
                    f = max(max(current.tf[i], n.t) + n.pt, n.j.yt_middle().t) + n.j.yt_middle().pt
                    if f < min_f:
                        min_f = f
                        min_n = n
                        min_i = i
            elif n.type == 1 or n.type == 4: # yc
                f = max(current.yf[n.j.block], n.t) + n.pt
                if f < min_f:
                    min_f = f
                    min_n = n
                    min_i = n.j.block
            else:
                assert(False)

        #print '\tEarlist finishable node:', min_f, min_n, min_i

        if min_n == None:
            # possibly infeasible
            continue

        # find nodes that can start earlier than min_f by the same resource
        ns = []
        if min_n.type == 2: # yt
            for n in so:
                if n.type == 2 and n.t < min_f:
                    ns.append(n)
            for n in ns:
                next = Node()
                next.create_with_new_yt_node(current, min_i, n.j, qs)
                #print '\t', next
                if next.lb:
                    if next.num > 0:
                        if next.lb < z_best:
                            todo.append(next)
                        else:
                            #print '\t\tpruned because LB is not less than best so far'
                            pass
                    else:
                        if next.lb < z_best:
                            #print '\t\tbest so far'
                            z_best = next.lb
                            n_best = next
                else:
                    #print '\t\tInfeasible'
                    pass
        else: #yc
            for n in so:
                if (n.type == 1 or n.type == 4) and n.j.block == min_i and n.t < min_f:
                    ns.append(n)
            for n in ns:
                next = Node()
                next.create_with_new_yc_node(current, min_i, n.j, qs)
                #print '\t', next
                if next.lb:
                    if next.num > 0:
                        if next.lb < z_best:
                            todo.append(next)
                        else:
                            #print '\t\tpruned because LB is not less than best so far'
                            pass
                    else:
                        if next.lb < z_best:
                            #print '\t\tbest so far'
                            z_best = next.lb
                            n_best = next
                else:
                    #print '\t\tInfeasible'
                    print

    return n_best


if __name__ == '__main__':
    # jobs and QC schedule
    #qs, ny, nt = [[D(0), L(1), D(1)], [L(0), L(0)]], 2, 2
    #qs, ny, nt = [[D(0), L(1), D(1)], [D(0), L(0), L(1)]], 2, 3
    qs, ny, nt = [[D(0), L(1), D(1), D(2)], [D(0), L(0), L(2), L(0)]], 3, 3

    # b&b
    opt = solve(qs, ny, nt)

    print 'Optimal: (' + str(opt.lb) + ')', opt
