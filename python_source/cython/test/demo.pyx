from libc.math cimport sin

cdef double f(double x):
    return sin(x*x)

def f_test(double x):
    return f(x)