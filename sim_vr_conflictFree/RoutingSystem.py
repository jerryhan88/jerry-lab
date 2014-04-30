from __future__ import division

TRANSFER, STATION, JUNCTION, DOT = range(4)

class Node():
    def __init__(self, _id, px, py, nodeType, numOfBerth=0):
        self.id = _id
        self.px, self.py = px, py
        self.nodeType = nodeType
        
class Edge():
    def __init__(self, _id, _from, _to, net_trackTime):
        self.id = _id
        self._from, self._to = _from, _to
        self.net_trackTime = net_trackTime

class PRT():
    def __init__(self, _id, init_node, schedules):
        self.id = _id
        self.arrived_n = init_node
        self.schedules = schedules
        self.cur_scheIndex = 0 if schedules else -1 
        self.n_arrT = None
        self.px, self.py = self.arrived_n.px, self.arrived_n.py
        
    def __repr__(self):
        return 'PRT%d(S%d-%s)' % (self.id, self.state, self.arrived_n.id)
    
def run(SETTING_TIME, PRT_SPEED, Network, PRTs):
    import wx, Visualizer
    app = wx.App(False)
    win = Visualizer.MainFrame(Network, PRTs)
    win.Show(True)
    app.MainLoop()
