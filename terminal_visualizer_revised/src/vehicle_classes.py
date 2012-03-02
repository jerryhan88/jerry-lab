from __future__ import division

class Vehicles(object):
    def __init__(self):
        self.veh_id, self.name = None, None
        self.evt_seq, self.cur_evt_id = [], 0
        self.start_time, self.start_px, self.start_py = None, None, None
        self.ce_time, self.ce_pos, self.ce_container, self.ce_state, self.ce_px, self.ce_py = None, None, None, None, None, None
        self.px, self.py = None, None
        self.pe_time, self.pe_px, self.pe_py = None, None, None
        self.end_time, self.end_px, self.end_py = None, None, None
        self.holding_containers = {}
    def __repr__(self):
        return str(self.name + str(self.veh_id))
    def cur_evt_update(self, cur_evt_id):
        if len(self.moving_seq) <= 1: assert False, 'length of evt_seq is smaller than 2'
    def find_cur_evt(self, cur_evt_id, simul_clock):
        pass
    def OnTimer(self, evt, simul_time):
        pass
    def draw(self, gc):
        pass
    
class Vessel(Vehicles):
    def __init__(self, name, voyage):
        Vehicles.__init__(self)
        self.name = name
        self.voyage = voyage
    def __repr__(self):
        return str(self.name + str(self.voyage))

class QC(Vehicles):
    def __init__(self, veh_id):
        Vehicles.__init__(self)
        self.name = 'STS'
        self.veh_id = veh_id
        
class YC(Vehicles):
    def __init__(self, veh_id):
        Vehicles.__init__(self)
        self.name = 'ASC'
        self.veh_id = veh_id
        
class SC(Vehicles):
    def __init__(self, veh_id):
        Vehicles.__init__(self)
        self.name = 'SH'
        self.veh_id = veh_id