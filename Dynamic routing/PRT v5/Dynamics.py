from __future__ import division
import Input_gen, Scenarios

Nodes, Edges = Input_gen.network1()
PRTs, customers = Scenarios.scenario2(Nodes)

def run():
    print Nodes 

if __name__ == '__main__':
    run()
