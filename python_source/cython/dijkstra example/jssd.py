from __future__ import division

'''
Job shop scheduling by dispatching
'''

#
# object definition and scheduling
#

class Mac(object):
    def __init__(self, mid):
        self.mid = mid
    def __repr__(self):
        return str(self.mid)

class Job(object):
    '''
    r: ready (arrival) time
    d: due date
    O: list of sequential operations, each of which is described by (machine, processing time)
    '''
    def __init__(self, jid, r, d, O):
        self.jid, self.r, self.d, self.O = jid, r, d, O
    def __repr__(self):
        return str(self.jid)

def schedule(M, J, disp_fn):
    '''
    M: list of machines
    J: list of jobs
    disp_fn: function for dispatching policy

    example schedule:
      m1, m2, m3 = M
      j1, j2, j3, j4 = J
      m1.Seq = [(j2, 1, 1), (j1, 0, 5), (j4, 2,  9), (j3, 2, 10)]
      m2.Seq = [(j2, 0, 0), (j4, 0, 4), (j3, 1,  7), (j1, 1,  9)]
      m3.Seq = [(j3, 0, 0), (j4, 1, 7), (j2, 2, 10), (j1, 2, 12)]
      j1.ST = [(m1, 5), (m2, 9), (m3, 12)]
      j2.ST = [(m2, 0), (m1, 1), (m3, 10)]
      j3.ST = [(m3, 0), (m2, 7), (m1, 10)]
      j4.ST = [(m2, 0), (m3, 7), (m1,  9)]
    '''

#
# dispatching rules
#

def FIFO(t, JO):
    '''
    ex) t = 3, JO = [(j1, 0), (j2, 1), (j3, 2), (j4, 3)]
    '''
    
    return None

#
# problem instances
#

def ex0():
    '''
    Example job shop problem instance in Ch. 11 of Baker, 1998
    '''
    M = m1, m2, m3 = Mac(1), Mac(2), Mac(3)
    J = [Job(1, 0, 0, [(m1, 4), (m2, 3), (m3, 2)]),
         Job(2, 0, 0, [(m2, 1), (m1, 4), (m3, 4)]),
         Job(3, 0, 0, [(m3, 3), (m2, 2), (m1, 3)]),
         Job(4, 0, 0, [(m2, 3), (m3, 3), (m1, 1)])]
    return M, J

def ex1():
    '''
    Modified from ex0
    '''
    M = m1, m2, m3 = Mac(1), Mac(2), Mac(3)
    J = [Job(1, 0,  8, [(m1, 4), (m2, 3), (m1, 2)]),
         Job(2, 3, 10, [(m2, 1), (m1, 4), (m3, 4)]),
         Job(3, 6, 12, [(m3, 3), (m2, 2), (m3, 3)]),
         Job(4, 6,  9, [(m2, 3), (m3, 3), (m1, 1)])]
    return M, J

#
# misc.
#

def display_schedule(M, J):
    print '[Machine]'
    for m in M:
        print '  M%d: %s' % (m.mid, ' '.join('%.1f-J%d(%d)' % (t, j.jid, oindex) for j, oindex, t in m.Seq))
    print '\n[Job]'
    for j in J:
        print '  J%d: %s' % (j.jid, ' '.join('%.1f-M%d' % (t, m.mid) for m, t in j.ST))


def test():
    M, J = ex0()
    schedule(M, J, FIFO)
    display_schedule(M, J)

if __name__ == '__main__':
    test()
