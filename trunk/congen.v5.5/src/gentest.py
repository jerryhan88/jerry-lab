from __future__ import division

import master, generator, distr
from datetime import datetime

g = generator.Generator()
  
g.set_duration(datetime(2010, 6, 29, 0, 0, 0), datetime(2010, 7, 29, 23, 59, 59))

g.set_yard_max_dwell_time(3, 4)  

v1 = generator.Vessel_information(master.vt1, 'Regina Maersk', distr.CONST(7), distr.CONST(2), distr.CONST(5), (13, 15))
v2 = generator.Vessel_information(master.vt1, 'Louis Maersk', distr.CONST(14), distr.CONST(3), distr.CONST(6), (15, 18))
v3 = generator.Vessel_information(master.vt3, 'Tokyo Bay', distr.EXPO(7.0), distr.CONST(2), distr.CONST(5), (12, 16))

v1.set_cargo_character(Through=distr.CONST(3), Import=(distr.CONST(2), 'A'), Export=(distr.CONST(2), 'B'),
                                     Trans={'Louis Maersk' : (distr.CONST(1), 'C'), 'Tokyo Bay' : (distr.CONST(1), 'E')})
v2.set_cargo_character(Through=distr.CONST(2), Import=(distr.CONST(1), 'A'), Export=(distr.CONST(1), 'D'),
                                     Trans={'Regina Maersk':(distr.CONST(3), 'C'), 'Tokyo Bay':(distr.CONST(1), 'B')})
v3.set_cargo_character(Through=distr.CONST(1), Import=(distr.CONST(4), 'A'), Export=(distr.CONST(3), 'C'),
                                     Trans={'Louis Maersk' : (distr.CONST(2), 'B')})

g.set_export_XT_time_distribution([0, 0, 0, 0.1, 0.1, 0, 0.4, 0, 0, 0.3, 0.1, 0])
g.set_import_XT_time_distribution([0, 0, 0.2, 0.2, 0, 0.1, 0.1, 0, 0.3, 0, 0, 0.1, 0])
 
g.set_vessels(v1, v2, v3)
    
for today, Class in g.next_event(): 
    if isinstance(Class, generator.Vessel_information):
        if Class.time_of_generating_vessel <= g.duration_end:
            g.create_vessel_and_XT(Class)
    elif Class.TA <= g.duration_end:
        if isinstance(Class, generator.Vessel):
            before_arrival_SP_list = [aContainer for aContainer in g.traverse(Class.before_arrival_SP)]
            loading_SP_list = [aContainer for aContainer in g.traverse(Class.after_departure_SP)]
            infomation_format = '''
                    Current Time : %s
Vessel name : %s
Voyage : %s
Container before unloading : %s
Container after loading : %s
'''  
            s_info = infomation_format % (today, Class.name       , Class.voyage, [aContainer.ID for aContainer in before_arrival_SP_list], [aContainer.ID for aContainer in loading_SP_list])
            print s_info  
        elif isinstance(Class, generator.Arrived_XT):
            infomation_format = '''
                    Current Time : %s
XT ID : %s
Import/Export : %s
Container ID : %s
'''  
            s_info = infomation_format % (today, Class.ID, Class.state, Class.container.ID)
            print s_info  
        elif isinstance(Class, generator.Vessel_stowage):
            before_arrival_SP_list = [aContainer.ID for aContainer in g.traverse(Class.before_arrival_SP)]
            print s_info               
        elif isinstance(Class, generator.Notice_vessel_arrival):
            infomation_format = '''
                    Current Time : %s
Vessel name : %s
TA : %s   
Voyage : %s
'''  
            s_info = infomation_format % (today, Class.name, Class.TA, Class.voyage)
            print s_info            
        elif isinstance(Class, generator.COPINO):
            infomation_format = '''
                    Current Time : %s
XT ID : %s
TA : %s    
Import/Export : %s
Container ID : %s      
'''
            s_info = infomation_format % (today, Class.ID, Class.TA, Class.state, Class.container.ID)
            print s_info
