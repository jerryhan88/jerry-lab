from __future__ import division
import copy, random, datetime, distr
from datetime import timedelta
from heapq import heappush, heappop

XT_ID = 0 
class Arrived_XT:
    def __init__(self):
        global XT_ID
        XT_ID = XT_ID + 1
        self.ID = 'aa %s' % XT_ID
    def set_container(self, container):
        self.container = container
    def set_state(self, state):
        self.state = state
    def set_TA(self, TA):
        self.TA = TA

class COPINO:
    def __init__(self):
        global XT_ID
        self.ID = 'aa %s' % XT_ID
    def set_container(self, container):
        self.container = container        
    def set_state(self, state):
        self.state = state 
    def set_TA(self, TA):
        self.TA = TA

class Vessel_stowage:
    def set_name(self, name):
        self.name = name
    def set_before_arrival_SP(self, baSP):
        self.before_arrival_SP = baSP
    def set_TA(self, TA):
        self.TA = TA    

class Notice_vessel_arrival:
    def set_name(self, name):
        self.name = name    
    def set_TA(self, TA):
        self.TA = TA
    def set_voyage(self, voyage):        
        self.voyage = voyage

class Vessel:
    def set_TA(self, TA):
        self.TA = TA
    def set_name(self, name):
        self.name = name
    def set_voyage(self, voyage):        
        self.voyage = voyage
    def set_before_arrival_SP(self, before_arrival_SP):
        self.before_arrival_SP = before_arrival_SP    
    def set_after_departure_SP(self, after_departure_SP):
        self.after_departure_SP = after_departure_SP

class Vessel_information:
    def __init__(self, vessel_type, vessel_name, IAT, first_arrival, loading_limit, time_range):
        self.type = vessel_type
        self.name = vessel_name
        self.IAT = IAT
        self.first_arrival = first_arrival
        self.loading_limit = loading_limit
        self.next_vessel_voyage = 1
        self.time_range = time_range
        self.slots_info = []
        for slots in self.type.slots_info[:]:
            self.slots_info.append(slots)
    def set_cargo_character(self, **transported_dict):
        self.set_cargo_character = transported_dict
    def renew_voyage(self):
        self.next_vessel_voyage = self.next_vessel_voyage + 1 

class Container_Terminal:
    import_containers = []
    export_containers = {}
    trans_containers = {}

CT = Container_Terminal()

container_ID = 0
class Container:
    def __init__(self, container_type, size, vehicle=None, POD=None):
        global container_ID
        container_ID = container_ID + 1
        self.ID = container_ID
        self.type = container_type
        self.size = size
        self.vehicle = vehicle
        self.POD = POD

class Generator:
    def __init__(self):
        self.ordered_output = []
    def set_duration(self, start, end):
        self.duration_start = start
        self.duration_end = end
    def set_yard_max_dwell_time(self, Import, Export):
        self.Import_max_dwell_time = Import
        self.Export_max_dwell_time = Export

    def set_export_XT_time_distribution(self, export_distribution):
        self.export_XT_time_distribution = export_distribution
    
    def set_import_XT_time_distribution(self, import_distribution):
        self.import_XT_time_distribution = import_distribution

    def set_vessels(self, *vessel):
        for aVessel in vessel:
            self.create_vessel_and_XT(aVessel)
                    
    def create_vessel_and_XT(self, aVessel_input):
        
        if aVessel_input.next_vessel_voyage == 1:
            the_date = self.duration_start + timedelta(aVessel_input.first_arrival() + 7)
        else:
            the_date = aVessel_input.time_of_generating_vessel + timedelta(self.Export_max_dwell_time)
        v_start, v_end = aVessel_input.time_range
        hour, minute = distr.Vessel_TIME_DISTR(v_start, v_end)
        TA = datetime.datetime(the_date.year, the_date.month, the_date.day, hour, minute)
     
        v = Vessel()
        v.set_name(aVessel_input.name)
        v.set_TA(TA)    
        v.set_voyage(aVessel_input.next_vessel_voyage)
        
        aVessel_input.time_of_generating_vessel = TA + timedelta(aVessel_input.IAT() - (self.Export_max_dwell_time))
        aVessel_input.renew_voyage()
        heappush(self.ordered_output, (aVessel_input.time_of_generating_vessel, aVessel_input))
        
        aNotice_vessel_arrival = Notice_vessel_arrival()
        aNotice_vessel_arrival.set_name(v.name)
        aNotice_vessel_arrival.set_TA(v.TA)
        aNotice_vessel_arrival.set_voyage(v.voyage)
        heappush(self.ordered_output, (v.TA - timedelta(7), aNotice_vessel_arrival))
        
        created_containers = self.create_containers(aVessel_input.set_cargo_character, aVessel_input.name)
        
        self.create_export_XT(v.TA, created_containers['Export'], self.Export_max_dwell_time)
        
        trough_SP = self.through_stowage_plan(aVessel_input.slots_info, created_containers['Through'])
        before_arriving_SP, unloading_containers = self.before_arriving_stowage_plan(created_containers['Import'], created_containers['Trans'], trough_SP)
        self.unloading_to_Container_Terminal(unloading_containers)
        
        aStowage = Vessel_stowage()
        aStowage.set_name(v.name)
        aStowage.set_TA(v.TA)
        aStowage.set_before_arrival_SP(before_arriving_SP)
        heappush(self.ordered_output, (v.TA - timedelta(2), aStowage))
        
        for_departure_SP = self.for_departure_stowage_plan(trough_SP, self.loading_to_vessel(v.name, aVessel_input.loading_limit))
        self.create_import_XT(v.TA, created_containers['Import'], self.Import_max_dwell_time)
        v.set_before_arrival_SP(before_arriving_SP)
        v.set_after_departure_SP(for_departure_SP)
        
        heappush(self.ordered_output, (v.TA, v))

    def create_containers(self, cargo_dict, Vessel_name):
        container_character = {'Import' : [], 'Export' : [], 'Trans' : [], 'Through' : []}
        I_number_of_container = cargo_dict['Import'][0]
        I_POD = cargo_dict['Import'][1]
        for _ in range(I_number_of_container()):
            container_character['Import'].append(Container('DRY', '20ft', 'Arrived_XT', I_POD))
        
        E_number_of_container = cargo_dict['Export'][0]
        E_POD = cargo_dict['Export'][1]
        for _ in range(E_number_of_container()):
            container_character['Export'].append(Container('DRY', '20ft', Vessel_name, E_POD)) 
        
        Thr_number_of_container = cargo_dict['Through']
        for _ in range(Thr_number_of_container()):
            container_character['Through'].append(Container('DRY', '20ft'))
                
        for v_name, number_of_container_and_POD in cargo_dict['Trans'].items():
            number_of_container = number_of_container_and_POD[0]
            POD = number_of_container_and_POD[1] 
            for _ in range(number_of_container()):
                container_character['Trans'].append(Container('DRY', '20ft', v_name, POD))
        return container_character 
    
    def unloading_to_Container_Terminal(self, unloading_containers):         
        while unloading_containers:
            aContainer_for_CT = unloading_containers.pop()
            if aContainer_for_CT.vehicle == 'Arrived_XT':
                CT.import_containers.append(aContainer_for_CT)
            else:
                CT.trans_containers.setdefault(aContainer_for_CT.vehicle, []).append(aContainer_for_CT) 
    
    def loading_to_vessel(self, v_name, loading_limit):
        if len(CT.export_containers.setdefault(v_name, [])):
            random.shuffle(CT.export_containers[v_name])
            
        if len(CT.trans_containers.setdefault(v_name, [])):
            random.shuffle(CT.trans_containers[v_name])
            
        loading_containers = []
        while len(CT.export_containers[v_name]):
            if len(loading_containers) < loading_limit:
                aContainer = CT.export_containers[v_name].pop()
                loading_containers.append(aContainer)
            else:
                break
        
        while len(CT.trans_containers[v_name]):
            if len(loading_containers) < loading_limit:
                aContainer = CT.trans_containers[v_name].pop()
                loading_containers.append(aContainer)
            else:
                break
        return loading_containers
    
    def through_stowage_plan(self, slots_info, through_containers):
#        current_stowage = slots_info[:]
        current_stowage = []
        for item in slots_info:
            current_stowage.append(item)
        current_stowage = copy.deepcopy(slots_info)
        while through_containers:
            aContainer = through_containers.pop()
            bay = random.choice(current_stowage)
            row = random.choice(bay)
            if len(row[0]) == 0:
                row[0].append(aContainer)
            elif len([self.traverse(current_stowage)]) < sum([len(x) for x in current_stowage]) :
                through_containers = [aContainer] + through_containers
                continue
            elif len([self.traverse(row)]) < len(row):
                row[len([self.traverse(row)]) - 1].append(aContainer)
            else:
                through_containers = [aContainer] + through_containers
                continue
        return current_stowage
    
    def before_arriving_stowage_plan(self, import_containers, trans_containers, trough_SP):
#        before_arrival_SP = trough_SP[:]
        before_arrival_SP = copy.deepcopy(trough_SP)
        unloading_containers = []
      
        while import_containers:
            aContainer = import_containers.pop()
            unloading_containers.append(aContainer)
        
        while trans_containers:
            aContainer = trans_containers.pop()
            unloading_containers.append(aContainer)
        
        unloading_to_CT = unloading_containers[:]
        
        unloading_containers.sort(key=lambda Container:Container.POD)
        while len(unloading_containers) != 0:
            aContainer = unloading_containers.pop(0)
            bay = random.choice(before_arrival_SP)
            row = random.choice(bay)
            if len([self.traverse(row)]) < len(row):
                row[len([self.traverse(row)]) - 1].append(aContainer)
            else:
                unloading_containers = [aContainer] + unloading_containers
                continue
        return (before_arrival_SP, unloading_to_CT)
        
    def for_departure_stowage_plan(self, trough_SP, loading_list):
#        after_departure_SP = trough_SP[:]
        after_departure_SP = copy.deepcopy(trough_SP)
        loading_list.sort(key=lambda Container:Container.POD)
        
        while len(loading_list) != 0:
            aContainer = loading_list.pop(0)
            bay = random.choice(after_departure_SP)
            row = random.choice(bay)
            if len([self.traverse(row)]) < len(row):
                row[len([self.traverse(row)]) - 1].append(aContainer)
            else:
                loading_list = [aContainer] + loading_list
                continue
        return after_departure_SP
    
    def create_export_XT(self, vessel_TA, export_containers, Export_max_dwell_time):
        export_container_list = export_containers[:]
        variable = 2 * len(export_container_list) / (Export_max_dwell_time * (Export_max_dwell_time + 1))
        
        number_of_containers = [int(variable * (day + 1)) for day in range(Export_max_dwell_time)]
        
        if sum(number_of_containers) != len(export_container_list):
            for x in range(len(export_container_list) - sum(number_of_containers)):
                number_of_containers[-(1 + x)] = number_of_containers[-(1 + x)] + 1
        
        number_of_containers.reverse()
        
        while export_container_list:
            for i, x in enumerate(number_of_containers):
                for _ in range(x):
                    aContainer = export_container_list.pop()
                    the_time = vessel_TA - timedelta(i + 1)
                    hour, minute = distr.export_XT_TIME_DISTR(self.export_XT_time_distribution)
                    arrival_date_time = datetime.datetime(the_time.year, the_time.month, the_time.day, hour, minute)
                    
                    aXT = Arrived_XT()
                    aXT.set_TA(arrival_date_time)
                    aXT.set_container(aContainer)
                    aXT.set_state('Export')
                    aCopino = COPINO()
                    aCopino.set_TA(arrival_date_time)
                    aCopino.set_container(aContainer)
                    aCopino.set_state('Export')
                    heappush(self.ordered_output, (arrival_date_time - timedelta(1) , aCopino))
                    heappush(self.ordered_output, (arrival_date_time, aXT))

                    CT.export_containers.setdefault(aContainer.vehicle, []).append(aContainer)
    
    def create_import_XT(self, vessel_TA, import_containers, Import_max_dwell_time):
        variable = 2 * len(CT.import_containers) / (Import_max_dwell_time * (Import_max_dwell_time + 1))
        
        number_of_containers = [int(variable * (day + 1)) for day in range(Import_max_dwell_time)]
        number_of_containers.reverse()
        
        if sum(number_of_containers) != len(CT.import_containers):
            for x in range(len(CT.import_containers) - sum(number_of_containers)):
                number_of_containers[x] = number_of_containers[x] + 1
        
        while CT.import_containers:
            for i, x in enumerate(number_of_containers):
                for _ in range(x):
                    aContainer = CT.import_containers.pop()                  
                    the_time = vessel_TA + timedelta(i + 1)
                    time = distr.import_XT_TIME_DISTR(self.import_XT_time_distribution)
                    arrival_date_time = datetime.datetime(the_time.year, the_time.month, the_time.day, time[0], time[1])
                     
                    aXT = Arrived_XT()
                    aXT.set_TA(arrival_date_time)
                    aXT.set_container(aContainer)
                    aXT.set_state('Import')
                    
                    aCopino = COPINO()
                    aCopino.set_TA(arrival_date_time)
                    aCopino.set_container(aContainer)
                    aCopino.set_state('Import')
                    
                    heappush(self.ordered_output, (arrival_date_time - timedelta(1) , aCopino))
                    heappush(self.ordered_output, (arrival_date_time, aXT))

    def next_event(self):
        while self.ordered_output:
            yield heappop(self.ordered_output)
    
    def traverse(self, l):
        for el in l:
            if isinstance(el, type([])):
                for k in self.traverse(el):
                    yield k
            else:
                yield el

if __name__ == '__main__':
    pass
