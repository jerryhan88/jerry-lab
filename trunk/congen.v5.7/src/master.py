from __future__ import division

class Vessel_Master_Table:
    def __init__(self, LOA, beam, draft, slots_info, capacity):
        self.LOA = LOA
        self.beam = beam
        self.draft = draft
        self.slots_info = slots_info
        self.capacity = capacity
        
vt_group = {}

master_text = open('master_table.txt')
colLabels = master_text.readline().split(', ') 
data_of_vessels = []
vessel_master_data = master_text.readline().split(', ')
while vessel_master_data != ['']:
    data_of_vessels.append(vessel_master_data)
    vessel_master_data = master_text.readline().split(', ')

for vt_information in data_of_vessels:
    check_stowage_slots = [eval(i) for i in vt_information[4].split(' ')] 
    stowage = []
#    print 'before bay check_stowage_slots : ',check_stowage_slots
    number_of_bay = check_stowage_slots.pop(0)
#    print 'before row check_stowage_slots : ',check_stowage_slots
    number_of_row = check_stowage_slots.pop(0)
#    print 'before tier check_stowage_slots : ',check_stowage_slots
    number_of_tier = check_stowage_slots.pop(0)
    for no_b in range(number_of_bay):
        stowage.append([])
        for no_r in range(number_of_row):
            stowage[no_b].append([])
            for no_t in range(number_of_tier):
                stowage[no_b][no_r].append([])
    vt_group[vt_information[0]] = Vessel_Master_Table(vt_information[1], vt_information[2], vt_information[3], stowage, vt_information[5])

if __name__ == '__main__':
    print 'result'
    for k,v in vt_group.items():
        print 'key', k, 'velue : ', v
    print 'result'