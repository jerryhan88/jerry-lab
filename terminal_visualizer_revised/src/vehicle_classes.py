from __future__ import division

class Vehicles(object):
    def __init__(self):
        self.veh_id, self.name = None, None
        self.evt_seq, self.cur_evt_id, self.evt_end = [], -1, False
        self.start_time, self.start_px, self.start_py = None, None, None
        self.ce_time, self.ce_pos, self.ce_container, self.ce_state, self.ce_px, self.ce_py = None, None, None, None, None, None
        self.px, self.py = None, None
        self.pe_time, self.pe_px, self.pe_py = None, None, None
        self.end_time, self.end_px, self.end_py = None, None, None
        self.holding_containers = {}
    def __repr__(self):
        return str(self.name + str(self.veh_id))
    def set_evt_data(self, cur_evt_id):
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
    
    def set_evt_data(self, cur_evt_id, Bitts, simul_clock):
        if cur_evt_id == -1:
            self.start_time
#            self.ar_s_time = self.ce_time - timedelta(0, 15)
            self.start_px, self.start_py = None, None, None
            pass
#        self.cur_evt = self.evt_seq[cur_evt_id]
#        self.ce_time, self.work_type = self.cur_evt.dt
        
#        ce_time, self.ce_state, ce_pos = self.cur_evt
#        year, month, day, hour, minute, second = tuple(ce_time.split('-'))
#        self.ce_time = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
#        bitt_id = int(ce_pos[-2:])
#        self.ce_px, self.ce_py = Bitts[bitt_id].px - self.LOA * 1 / 3, Bitts[bitt_id].py - self.B * 1.1
#        
#        ne_time, self.ne_state, ne_pos = self.next_evt
#        year, month, day, hour, minute, second = tuple(ne_time.split('-'))
#        self.ne_time = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
#        bitt_id = int(ne_pos[-2:])
#        self.ne_px, self.ne_py = Bitts[bitt_id].px - self.LOA * 1 / 3, Bitts[bitt_id].py - self.B * 1.1
#        self.ar_s_px, self.ar_s_py = self.dp_e_px, self.dp_e_py = self.px, self.py = self.ce_px, self.ce_py - container_hs * 2
#        
#        if self.ce_time <= simul_clock<= self.ne_time:
#            self.px, self.py = self.ce_px, self.ce_py
#        self.ar_s_time = self.ce_time - timedelta(0, 15)
#        self.dp_e_time = self.ne_time + timedelta(0, 20)

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
