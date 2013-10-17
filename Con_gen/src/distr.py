from __future__ import division
import random

def CONT(): assert False, 'Not implemented'
def DISC(): assert False, 'Not implemented'
def ERLA(ExpoMean, k): assert False, 'Not implemented'
def JOHN(Gamma, Delta, Lambda, Xi): assert False, 'Not implemented'
def LOGN(LongMean, LogStd): assert False, 'Not implemented'
def POIS(Mean): assert False, 'Not implemented'
def TRIA(Min, Mode, Max): assert False, 'Not implemented'
'''
class EXPO:
    def __init__(self, mean):
        self.lambd = 1 / mean
    def __call__(self):
        return random.expovariate(self.lambd)
'''
def CONST(number):
    return lambda: number
def BETA(Alpha, Beta):
    return lambda: random.betavariate(Alpha, Beta)
def EXPO(mean):
    return lambda: random.expovariate(1 / mean)
def GAMA(Alpha, Beta):
    return lambda: random.gammavariate()
def NORM(Mean, StdDev):
    return lambda: random.normalvariate(Mean, StdDev)
def UNIF(Min, Max):
    return lambda: random.uniform(Min, Max + 1)
def WEIB(Alpha, Beta):
    return lambda: random.weibullvariate(Alpha, Beta)

def export_XT_TIME_DISTR(export_XT_time_distribution):
    rv = random.random() - 0.000000000001
    time_period = 24 / len(export_XT_time_distribution) 
    return set_time(rv, time_period, export_XT_time_distribution)
            
def import_XT_TIME_DISTR(import_XT_time_distribution):
    rv = random.random() - 0.000000000001
    time_period = 24 / len(import_XT_time_distribution)     
    return set_time(rv, time_period, import_XT_time_distribution)

def set_time(rv, time_period, time_distribution):
    cumulative_distribution = [sum(time_distribution[:i]) for i in range(len(time_distribution))]
    
    for x, cumulative_distribution_value in enumerate(cumulative_distribution):
        if rv <= cumulative_distribution_value:
            the_time = time_period * random.random() 
            hour = x + int(the_time) 
            minute = int((the_time - int(the_time)) * 60)
            return (hour, minute)        

def Vessel_TIME_DISTR(start, end):
    rv = random.random() 
    hour = start + int(rv * (end - start))
    minute = int((rv - int(rv)) * 60)
    return (hour, minute)

if __name__ == '__main__':
    rv1 = CONST(10)
    rv3 = CONST(7)
    rv2 = EXPO(7)
    rv4 = EXPO(1)
    
    print rv1(), rv1(), rv3()
    print rv2(), rv2(), rv2()
    print rv4(), rv4(), rv4()
    
    
