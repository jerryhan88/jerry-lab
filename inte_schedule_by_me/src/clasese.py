class Job:
    def __init__(self, id, state):
        self.id = id
        self.state = state
        
class QC:
#    def __init__(self, id, job_sequence = []):
    def __init__(self, id, job_sequence):
        self.id = id
        self.job_sequence = job_sequence
        
class YC:
    def __init__(self, id, job_list):
        self.id = id
        self.job_list = job_list
        self.job_sequence = []
        self.stop_position = None
        
class YT:
    def __init__(self, id):
        self.id = id
        self.job_sequence = []
        self.stop_position = None

class Node:
    def __init__(self, id, order):
        self.id = id
        self.order = order
        self.E_T = 0
        self.L_T = 1000000000
        self.S = self.L_T - self.E_T
        self.outgoings = []
        self.incomings = []
        self.planed = False
        
    def __str__(self):
        return self.id
    
class Edge:
    def __init__(self, start_n, end_n, vehicle, time) :
        self.start_n = start_n
        self.end_n = end_n
        self.vehicle = vehicle
        self.time = time
        start_n.outgoings.append(self)
        end_n.incomings.append(self)
        
    def del_edge(self):
        assert self.start_n.outgoings[-1] == self and self.end_n.incomings[-1] == self 
        self.start_n.outgoings.pop()
        self.end_n.incomings.pop()