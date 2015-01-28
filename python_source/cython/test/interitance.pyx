from math import sin

cdef class Function:
    def __init__(self):
        print 1
    cpdef double evaluate(self, double x) except *:
        return 0
    
cdef class SinOfSquareFunction(Function):
    def __init__(self):
        print 2
    cpdef double evaluate(self, double x) except *:
        return sin(x**2)
    