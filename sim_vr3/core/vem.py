from __future__ import division

'''
def run(_SETTING_TIME, _PRT_SPEED, Network, PRTs, Customers, dispatcher=None, useVisualizer=False, useExperiment=False, bg_path=None):
    from time import sleep
    global SETTING_TIME, PRT_SPEED
    SETTING_TIME = _SETTING_TIME
    PRT_SPEED = _PRT_SPEED
    
    # Network
    #  Nodes, Edges = Network
    Algorithms.init_algorithms(Network[0])
    
    if dispatcher:
        init_dynamics(Network[0], PRTs, Customers, dispatcher)
        if useExperiment:
            now = 1e400
            process_events(now)
        else:
            now = 0.0
            while process_events(now):
                now += 1
                sleep(0.0001)
'''