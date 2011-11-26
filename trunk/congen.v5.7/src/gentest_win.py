from __future__ import division
from datetime import datetime
import CustomDataTable as CDT
import distr, generator, master, wx
import wx.grid as gridlib

class Notice_Viewer(wx.Dialog):
    def __init__(self, parent, name, size=(400, 250), pos=(850, 50)):
        wx.Dialog.__init__(self, None, -1, 'Event_Viewer', pos , size)
        wx.StaticText(self, -1, name, (70, 50))
        button = wx.Button(self, -1, "Confirm", (100, 150))
        self.Bind(wx.EVT_BUTTON, self.confirm, button)
    def confirm(self, event):
        self.Destroy()
        mv.arriving_event_viewer.dispatch_event()

class Arriving_Event_Viewer(wx.Dialog):
    def __init__(self, parent, name, size=(640, 800), pos=(40, 40)):
        wx.Dialog.__init__(self, None, -1, 'Arriving Event Viewer', pos , size)
        
        wx.StaticBox(self, -1, "Notice Option", pos=(10, 0), size=(500, 45))
        self.stowage = wx.CheckBox(self, -1, "Stowage", pos=(30, 20))
        self.stowage.SetValue(True)
        self.COPINO = wx.CheckBox(self, -1, "COPINO", pos=(160, 20))
        self.va_notice = wx.CheckBox(self, -1, "Vessel arrival Notice", pos=(330, 20))
    
        self.Bind(wx.EVT_CHECKBOX, self.onAction, self.stowage)
        self.Bind(wx.EVT_CHECKBOX, self.onAction, self.COPINO)
        self.Bind(wx.EVT_CHECKBOX, self.onAction, self.va_notice)
        
        
        wx.StaticText(self, -1, name, (70, 50))
        
        wx.StaticBox(self, -1, "Arriving Event", pos=(10, 50), size=(620, 720)) #@UnusedVariable
        self.current_situation = wx.TextCtrl(self, -1,
                            "Current situation will be presented", pos=(20, 65),
                           size=(600, 700), style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
    
        button = wx.Button(self, -1, "Start", (530, 15))
        self.Bind(wx.EVT_BUTTON, self.start_generating, button)
        
    def add_log(self, s):
        self.current_situation.write(s)
    
    def onAction(self, event):
        
        if self.stowage.IsChecked():
            self.stowage.SetValue(True)
        else:
            self.stowage.SetValue(False)
        if self.COPINO.IsChecked():
            self.COPINO.SetValue(True)
        else:
            self.COPINO.SetValue(False)
        if self.va_notice.IsChecked():
            self.va_notice.SetValue(True)
        else:
            self.va_notice.SetValue(False)
    
    def start_generating(self, event):        
        s_year = eval(mv.start_year.GetValue())
        s_month = eval(mv.start_month.GetValue())
        s_day = eval(mv.start_day.GetValue())
        s_hour = eval(mv.start_hour.GetValue())
        s_minute = eval(mv.start_minute.GetValue())
        s_second = eval(mv.start_second.GetValue())
        
        e_year = eval(mv.end_year.GetValue())
        e_month = eval(mv.end_month.GetValue())
        e_day = eval(mv.end_day.GetValue())
        e_hour = eval(mv.end_hour.GetValue())
        e_minute = eval(mv.end_minute.GetValue())
        e_second = eval(mv.end_second.GetValue())
        
        import_max_dwell_time =eval(mv.import_max_dwell_time.GetValue())
        export_max_dwell_time =eval(mv.export_max_dwell_time.GetValue())
        
        i_XT_td = [eval(mv.i_table.GetValue(i,1))for i in range(mv.i_table.GetNumberRows())]
        e_XT_td = [eval(mv.e_table.GetValue(i,1))for i in range(mv.e_table.GetNumberRows())]
        
        inputed_vessels_property = mv.inputed_vessels_property
        
        cargo_character_table = mv.cargo_character_table 

        global g
        g = generator.Generator()
        
        g.set_duration(datetime(s_year, s_month, s_day, s_hour, s_minute, s_second),
                       datetime(e_year, e_month, e_day, e_hour, e_minute, e_second))
        
        g.set_yard_max_dwell_time(import_max_dwell_time, export_max_dwell_time)
        
        g.set_export_XT_time_distribution(e_XT_td)
        g.set_import_XT_time_distribution(i_XT_td)  
        
        informations_of_inputed_vessels = {}
        for x in range(inputed_vessels_property.GetItemCount()):
            vt = inputed_vessels_property.GetItem(x,0).GetText()
            name = inputed_vessels_property.GetItem(x,1).GetText()
            IAT = 'distr.'+inputed_vessels_property.GetItem(x,2).GetText()
            first_arrival = 'distr.'+inputed_vessels_property.GetItem(x,3).GetText()
            loading_limit = 'distr.'+inputed_vessels_property.GetItem(x,4).GetText()
            time_range = inputed_vessels_property.GetItem(x,5).GetText()
            informations_of_inputed_vessels[name]=generator.Vessel_information(master.vt_group[vt], name, eval(IAT),
                                                     eval(first_arrival), eval(loading_limit), eval(time_range))
#        v1 = generator.Vessel_information(master.vt1, 'Regina Maersk', distr.CONST(7), distr.CONST(2), distr.CONST(5), (13, 15))
#        v2 = generator.Vessel_information(master.vt1, 'Louis Maersk', distr.CONST(14), distr.CONST(3), distr.CONST(6), (15, 18))
#        v3 = generator.Vessel_information(master.vt3, 'Tokyo Bay', distr.EXPO(7.0), distr.CONST(2), distr.CONST(5), (12, 16))
        for k,v in informations_of_inputed_vessels.items():
            vessel_position_in_table = mv.find_position_in_table(cargo_character_table, k)
            e_containers_information = cargo_character_table.GetCellValue(0,vessel_position_in_table).split(' ')
            e_containers_information[1] = eval('distr.'+e_containers_information[1])
#            print 'e_containers_information :', e_containers_information
            i_containers_information = cargo_character_table.GetCellValue(vessel_position_in_table,0).split(' ')
#            print 'i_containers_information', i_containers_information 
            i_containers_information[1] = eval('distr.'+i_containers_information[1])
#            print 'i_containers_information :', i_containers_information
            th_containers_information = cargo_character_table.GetCellValue(vessel_position_in_table,vessel_position_in_table).split(' ')
            th_containers_information[1] = eval('distr.'+th_containers_information[1])
#            print 'th_containers_information :', th_containers_information
            tr_containers_information = {}
            for x in range(cargo_character_table.GetNumberCols()):
                if x != 0 and vessel_position_in_table != x and cargo_character_table.GetCellValue(vessel_position_in_table,x) != '':
                    row_th_containers_information = cargo_character_table.GetCellValue(vessel_position_in_table,x).split(' ')
                    row_th_containers_information[1] = eval('distr.'+row_th_containers_information[1])
                    tr_containers_information[cargo_character_table.GetColLabelValue(x)] = row_th_containers_information
#                print 'k: ', k
#                print 'tr_containers_information: ', tr_containers_information
            v.set_cargo_character(Through = th_containers_information,
                                  Import = i_containers_information,
                                  Export = e_containers_information,
                                  Trans = tr_containers_information) 
#            v.set_cargo_character()
#        v1.set_cargo_character(Through=distr.CONST(3), Import=(distr.CONST(2), 'A'), Export=(distr.CONST(2), 'B'),
#                                             Trans={'Louis Maersk' : (distr.CONST(1), 'C'), 'Tokyo Bay' : (distr.CONST(1), 'E')})
#        v2.set_cargo_character(Through=distr.CONST(2), Import=(distr.CONST(1), 'A'), Export=(distr.CONST(1), 'D'),
#                                             Trans={'Regina Maersk':(distr.CONST(3), 'C'), 'Tokyo Bay':(distr.CONST(1), 'B')})
#        v3.set_cargo_character(Through=distr.CONST(1), Import=(distr.CONST(4), 'A'), Export=(distr.CONST(3), 'C'),
#                                             Trans={'Louis Maersk' : (distr.CONST(2), 'B')})
#         
#        g.set_vessels(v1, v2, v3)
        print 'informations_of_inputed_vessels.values() : ', tuple(informations_of_inputed_vessels.values())
        
        g.set_vessels(informations_of_inputed_vessels.values())
        self.event_gen = g.next_event()
        
        self.dispatch_event()
        
    def dispatch_event(self):
        try:
            today, Class = self.event_gen.next()
        except StopIteration:
            dlg = wx.MessageDialog(self, 'End of Event')
            dlg.ShowModal()
            dlg.Destroy()
            return
        
        if isinstance(Class, generator.Vessel_information):
            if Class.time_of_generating_vessel <= g.duration_end:
                g.create_vessel_and_XT(Class)
                self.dispatch_event()
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
                s_info = infomation_format % (today, Class.name, Class.voyage, [aContainer.ID for aContainer in before_arrival_SP_list], [aContainer.ID for aContainer in loading_SP_list])
                self.add_log(s_info)
                self.dispatch_event()
            elif isinstance(Class, generator.Arrived_XT):
                infomation_format = '''
                        Current Time : %s
    XT ID : %s
    Import/Export : %s
    Container ID : %s
    '''  
                s_info = infomation_format % (today, Class.ID, Class.state, Class.container.ID)
                self.add_log(s_info)
                self.dispatch_event()  
            elif isinstance(Class, generator.Vessel_stowage):
                if self.stowage.GetValue():
                    print 'stowage will be.....'
                self.dispatch_event()
#                before_arrival_SP_list = [aContainer.ID for aContainer in g.traverse(Class.before_arrival_SP)]
            if isinstance(Class, generator.Notice_vessel_arrival):
                if self.va_notice.GetValue():   
                    s_current = 'Current : %s' % today
                    infomation_format = '''
    Vessel name : %s
    TA : %s   
    Voyage : %s'''  
                    s_info = infomation_format % (Class.name, Class.TA, Class.voyage)
                    vessel_arrival_notice = Notice_Viewer(None,'Notice!    Vessel arrival')
                    wx.StaticText(vessel_arrival_notice, -1, s_info,(100, 65))
                    wx.StaticText(vessel_arrival_notice, -1, s_current,(140, 10))
                    vessel_arrival_notice.Show(True)
                else:
                    self.dispatch_event()
            elif isinstance(Class, generator.COPINO):
                if self.COPINO.GetValue():
                    s_current = 'Current : %s' % today
                    infomation_format = '''
    XT ID : %s
    TA : %s    
    Import/Export : %s
    Container ID : %s'''
                    s_info = infomation_format % (Class.ID, Class.TA, Class.state, Class.container.ID)
                    
                    COPINO_notice = Notice_Viewer(None, 'COPINO')
                    wx.StaticText(COPINO_notice, -1, s_info,(100, 65))
                    wx.StaticText(COPINO_notice, -1, s_current,(140, 10))    
                    COPINO_notice.Show(True)
                else:
                    self.dispatch_event()
    
class Main_viewer(wx.Frame):
    def __init__(self, parent, ID, title, pos=wx.DefaultPosition, size=(1024, 768), style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        base_panel = wx.Panel(self, -1, pos=(0, 0), size=(810, 730))
        
        master_panel = wx.Panel(base_panel, -1, pos=(10, 10), size=(400, 150))
        XT_distribution_panel = wx.Panel(base_panel, -1, pos=(10, 160), size=(400, 170))
        duration_panel = wx.Panel(base_panel, -1, pos=(430, 10), size=(220, 100))
        vessel_property_panel = wx.Panel(base_panel, -1, pos=(430, 110), size=(580, 220))
        yard_max_dwell_time_panel = wx.Panel(base_panel, -1, pos=(650, 10), size=(140, 100))
        cargo_character_panel = wx.Panel(base_panel, -1, pos=(10, 330), size=(1000, 340))

        self.master_display(master_panel)        
        self.XT_distribution_display(XT_distribution_panel)
        self.duration_display(duration_panel)
        self.yard_max_dwell_time_display(yard_max_dwell_time_panel)
        self.vessel_property_display(vessel_property_panel)
        self.cargo_character_display(cargo_character_panel)
        
        s = '''If you input all information,
        please press Next button '''
        wx.StaticText(base_panel, -1, s, (810, 20))
        n_btn = wx.Button(base_panel, -1, "Next", (860, 60))
        self.Bind(wx.EVT_BUTTON, self.create_Event_Viewer, n_btn)
        
    def create_Event_Viewer(self, _):
        self.arriving_event_viewer = Arriving_Event_Viewer(None, 'Arriving Event')    
        self.arriving_event_viewer.Show(True)
        
    def find_position_in_table(self, table, value_for_finding):
            for x in range(table.GetNumberCols()):
                if table.GetColLabelValue(x) == value_for_finding:
                    return x
            
    def cargo_setting_panel(self, parent_panel):
        import_panel = wx.Panel(parent_panel, -1, pos=(110, 30), size=(222, 30))
        export_panel = wx.Panel(parent_panel, -1, pos=(332, 30), size=(270, 30))
        through_trans_panel = wx.Panel(parent_panel, -1, pos=(602, 30), size=(392, 30))
#        panel_group = [import_panel, through_panel, export_panel, trans_panel]
        panel_group = [import_panel, export_panel, through_trans_panel]
        s_group = ['Import', 'Export', 'Through/Trans']
#       
        self.containers_type = {}
        self.number_of_containers_of_v = {}
        self.containers_POD = {}
#       
        for s, p in zip(s_group, panel_group):
#            p.SetBackgroundColour("CYAN")
            if s == 'Through/Trans':
                wx.StaticText(p, -1, s, (5, 5))
                self.containers_type[s] = wx.Choice(p, -1, choices=['Dry', 'Empty'], pos=(95, 4), size=(60, 20))
                self.Bind(wx.EVT_CHOICE, self.v_type_EvtChoice, self.containers_type[s])
                self.number_of_containers_of_v[s] = wx.TextCtrl(p, -1, 'CONST(7)', pos=(160, 4), size=(65, 20))
                self.containers_POD[s] = wx.TextCtrl(p, -1, 'C', pos=(230, 4), size=(50, 20))
                self.tr_v_name = wx.Choice(p, -1, (285, 4), choices=[], size=(80, 20))
                for x in range(self.inputed_vessels_property.GetItemCount()):
                    self.tr_v_name.Append(self.inputed_vessels_property.GetItem(x, 1).GetText())
            else:    
                wx.StaticText(p, -1, s, (5, 5))
                self.containers_type[s] = wx.Choice(p, -1, choices=['Dry', 'Empty'], pos=(55, 4), size=(60, 20))
                self.Bind(wx.EVT_CHOICE, self.v_type_EvtChoice, self.containers_type[s])
                self.number_of_containers_of_v[s] = wx.TextCtrl(p, -1, 'CONST(7)', pos=(120, 4), size=(65, 20))
                if s == 'Export':
                    self.containers_POD[s] = wx.TextCtrl(p, -1, 'C', pos=(190, 4), size=(50, 20))
#                if s == 'Through/Trans':
#                    self.tr_v_name = wx.TextCtrl(p, -1, 'Louis Maersk', pos=(245, 4), size=(80, 20))
                    

        import_add_button = wx.Button(panel_group[0], -1, "*", pos=(200, 5), size=(20, 20))
        export_add_button = wx.Button(panel_group[1], -1, "+", pos=(245, 5), size=(20, 20))
        through_trans_add_button = wx.Button(panel_group[2], -1, "+", pos=(370, 5), size=(20, 20))
#        through_add_button = wx.Button(panel_group[1], -1, "*", pos=(200, 5), size=(20, 20))
        
#        trans_add_button = wx.Button(panel_group[3], -1, "+", pos=(330, 5), size=(20, 20))
        
        self.Bind(wx.EVT_BUTTON, self.import_add, import_add_button)
#        self.Bind(wx.EVT_BUTTON, self.through_add, through_add_button)
        self.Bind(wx.EVT_BUTTON, self.export_add, export_add_button)
        self.Bind(wx.EVT_BUTTON, self.through_trans_add, through_trans_add_button)
#        self.Bind(wx.EVT_BUTTON, self.trans_add, trans_add_button)
        self.Bind(wx.EVT_CHOICE, self.TT_v_name_EvtChoice, self.tr_v_name)
        
    def TT_v_name_EvtChoice(self, event):
        self.TT_v_name = event.GetString()

    def import_add(self, _):
        print self.choiced_container_type
        v_position_in_table = self.find_position_in_table(self.cargo_character_table, self.choiced_v)
        s = self.choiced_container_type + ' ' + self.number_of_containers_of_v['Import'].GetValue()
        self.cargo_character_table.SetCellValue(v_position_in_table, 0, s)
            
    def export_add(self, _):
        v_position_in_table = self.find_position_in_table(self.cargo_character_table, self.choiced_v)
        before_s = self.cargo_character_table.GetCellValue(0, v_position_in_table)
        if len(before_s)<1:
            s = '''%s %s %s''' %(self.choiced_container_type, self.number_of_containers_of_v['Export'].GetValue(), self.containers_POD['Export'].GetValue())
        else: 
            s = '''%s
%s %s %s''' %(before_s,self.choiced_container_type, self.number_of_containers_of_v['Export'].GetValue(), self.containers_POD['Export'].GetValue())
            self.cargo_character_table.AutoSizeRow(0, self.cargo_character_table.GetRowSize(0)+14)
            self.cargo_character_table.SetRowSize(0,self.cargo_character_table.GetRowSize(0)+14)
        
        self.cargo_character_table.SetCellValue(0, v_position_in_table, s)
    
    def through_trans_add(self, _):
        v_position_in_table = self.find_position_in_table(self.cargo_character_table, self.choiced_v)
        v_received_position_in_table = self.find_position_in_table(self.cargo_character_table, self.TT_v_name)
        before_s = self.cargo_character_table.GetCellValue(v_position_in_table, v_received_position_in_table)
        
        if self.TT_v_name == self.choiced_v:
            if len(before_s)<1:
                s = '''%s %s''' %(self.choiced_container_type, self.number_of_containers_of_v['Through/Trans'].GetValue())
            else:
                s = '''%s
%s %s''' %(before_s,self.choiced_container_type, self.number_of_containers_of_v['Through/Trans'].GetValue())
                self.cargo_character_table.AutoSizeRow(v_position_in_table, self.cargo_character_table.GetRowSize(v_position_in_table)+14)        
                self.cargo_character_table.SetRowSize(v_position_in_table,self.cargo_character_table.GetRowSize(v_position_in_table)+14)
        else:
            if len(before_s)<1:
                s = '''%s %s %s''' %(self.choiced_container_type, self.number_of_containers_of_v['Through/Trans'].GetValue(), self.containers_POD['Through/Trans'].GetValue())
            else:
                s = '''%s
%s %s %s''' %(before_s,self.choiced_container_type, self.number_of_containers_of_v['Through/Trans'].GetValue(), self.containers_POD['Through/Trans'].GetValue())
                self.cargo_character_table.AutoSizeRow(v_position_in_table, self.cargo_character_table.GetRowSize(v_position_in_table)+14)        
                self.cargo_character_table.SetRowSize(v_position_in_table,self.cargo_character_table.GetRowSize(v_position_in_table)+14)

        self.cargo_character_table.SetCellValue(v_position_in_table, v_received_position_in_table , s)
                
    def cargo_character_display(self, parent_panel):
        wx.StaticBox(parent_panel, -1, "Cargo Character", pos=(0, 0), size=(995, 335))
        wx.StaticText(parent_panel, -1, 'Vessel Choice', (15, 20))
        
        self.ch = wx.Choice(parent_panel, -1, (10, 40),
                choices=[], size=(100, 10))
        
        for x in range(self.inputed_vessels_property.GetItemCount()):
            self.ch.Append(self.inputed_vessels_property.GetItem(x, 1).GetText())
        
        self.cargo_setting_panel(parent_panel)         
        self.create_default_cargo_character_grid(parent_panel)
        
        cargo_character_remove_btn = wx.Button(parent_panel, -1, "Remove", pos=(900, 305))
        self.Bind(gridlib.EVT_GRID_SELECT_CELL, self.OnSelectCell,self.cargo_character_table)
        self.Bind(wx.EVT_BUTTON, self.cell_content_remove, cargo_character_remove_btn)

    def cell_content_remove(self, _):
        self.cargo_character_table.SetCellValue(self.current_cell[0],self.current_cell[1], '')
    
    def OnSelectCell(self, event):
        self.current_cell = (event.GetRow(), event.GetCol())
        event.Skip() 
        
    def create_default_cargo_character_grid(self, parent_panel):
        cargo_character_grid_panel = wx.Panel(parent_panel, -1, pos=(15, 55), size=(975, 245))
        
        wx.StaticText(cargo_character_grid_panel , -1, 'T    o', (500, 3))
        wx.StaticText(cargo_character_grid_panel , -1, 'F', (8, 50))
        wx.StaticText(cargo_character_grid_panel , -1, 'r', (9, 90))
        wx.StaticText(cargo_character_grid_panel , -1, 'o', (8, 130))
        wx.StaticText(cargo_character_grid_panel , -1, 'm', (7, 170))
        #---------------------------------------------------------------------------------------------------------------------------------------
        self.cargo_character_table = gridlib.Grid(cargo_character_grid_panel, -1, pos=(22, 22), size=(945, 220))
        #---------------------------------------------------------------------------------------------------------------------------------------
        self.cargo_character_table.CreateGrid(self.inputed_vessels_property.GetItemCount() + 1, self.inputed_vessels_property.GetItemCount() + 1)
        
        self.cargo_character_table.SetRowLabelSize(100)
        self.cargo_character_table.SetColLabelSize(18)
        
        self.cargo_character_table.SetRowLabelValue(0, 'XT')
        self.cargo_character_table.SetColLabelValue(0, 'XT')
        
        self.cargo_character_table.SetColSize(0, 130)
        self.cargo_character_table.SetRowSize(0, 20)
        
        table_size = self.inputed_vessels_property.GetItemCount()
        
        for x in range(table_size):
            self.cargo_character_table.SetRowLabelValue(x+1, self.inputed_vessels_property.GetItem(x, 1).GetText())
            self.cargo_character_table.SetColLabelValue(x+1, self.inputed_vessels_property.GetItem(x, 1).GetText())
            self.cargo_character_table.SetColSize(x + 1, 140)
            self.cargo_character_table.SetRowSize(x + 1, 20)
#        print self.find_position_in_table(self.cargo_character_table, 'Regina Maersk')
        
        regina_cargo_character = ('Regina Maersk', {'Through' : ('Dry', 'CONST(3)'), 'Import' : ('Dry', 'CONST(2)'),
                              'Export' : {'B' : ('Dry', 'CONST(2)', 'B')},
                              'Trans' : {'Louis Maersk' : ('Dry', 'CONST(1)', 'C'), 'Tokyo Bay' : ('Dry', 'CONST(1)', 'E')}})
        louis_cargo_character = ('Louis Maersk', {'Through' : ('Dry', 'CONST(2)'), 'Import' : ('Dry', 'CONST(1)'),
                              'Export' : {'D' : ('Dry', 'CONST(1)', 'D')},
                              'Trans' : {'Regina Maersk' : ('Dry', 'CONST(3)', 'C'), 'Tokyo Bay' : ('Dry', 'CONST(1)', 'B')}})
        tokyo_cargo_character = ('Tokyo Bay', {'Through' : ('Dry', 'CONST(1)'), 'Import' : ('Dry', 'CONST(4)'),
                              'Export' : {'C' : ('Dry', 'CONST(3)', 'C')},
                              'Trans' : {'Louis Maersk' : ('Dry', 'CONST(2)', 'B')}})

#        print self.cargo_character_table.GetSelectedCells(self)
        for v_name, CC in [regina_cargo_character, louis_cargo_character, tokyo_cargo_character]:
            v_position = self.find_position_in_table(self.cargo_character_table, v_name)
            v_cargo_character = CC
            #import containers
            i_containers_type, i_number_of_import_containers = v_cargo_character['Import']  
            self.cargo_character_table.SetCellValue(v_position, 0, i_containers_type + ' ' + i_number_of_import_containers)
            
            th_containers_type, th_number_of_import_containers = v_cargo_character['Through']  
            self.cargo_character_table.SetCellValue(v_position, v_position, th_containers_type + ' ' + th_number_of_import_containers)
            
            for k, v in v_cargo_character['Export'].items():
                e_containers_type, e_number_of_import_containers, e_POD = v
                self.cargo_character_table.SetCellValue(0, v_position, e_containers_type + ' ' + e_number_of_import_containers + ' ' + e_POD)
            
            for k, v in v_cargo_character['Trans'].items():
                received_v = k
                tr_containers_type, tr_number_of_import_containers, tr_POD = v  
                self.cargo_character_table.SetCellValue(v_position,
                                            self.find_position_in_table(self.cargo_character_table, received_v),
                                            tr_containers_type + ' ' + tr_number_of_import_containers + ' ' + tr_POD)

        self.Bind(wx.EVT_CHOICE, self.v_EvtChoice, self.ch)
        
    def v_EvtChoice(self, event):
        self.choiced_v = event.GetString()

    def v_type_EvtChoice(self, event):
        self.choiced_container_type = event.GetString()
    
    def vessel_property_remove(self, _):
        self.inputed_vessels_property.DeleteItem(self.selcected_vessel_property)

        before_table_size = self.cargo_character_table.GetNumberCols()
        p_of_remove = (before_table_size - 1) - self.selcected_vessel_property
        labels = [self.cargo_character_table.GetColLabelValue(i) for i in range(before_table_size)]
        labels.pop(p_of_remove)
        
        self.cargo_character_table.DeleteCols(p_of_remove, 1, True)
        self.cargo_character_table.DeleteRows(p_of_remove, 1, True)

        for i, L in enumerate(labels):
            self.cargo_character_table.SetColLabelValue(i, L)
            self.cargo_character_table.SetRowLabelValue(i, L)
        self.ch.Delete(self.selcected_vessel_property)
        self.tr_v_name.Delete(self.selcected_vessel_property)
    
    def vessel_property_add(self, _):
        number_of_inputed_vessel = self.inputed_vessels_property.GetItemCount()
        
        inputed_v = {'Type' : self.v_type.GetValue(),
                     'Name' : self.v_name.GetValue(),
                     'IAT' : self.v_IAT.GetValue(),
                     'First_arrival' : self.v_first_arrival.GetValue(),
                     'Loading_limit' : self.v_loading_limit.GetValue(),
                     'Time_range' : self.v_time_range.GetValue()}
        
        self.inputed_vessels_property.InsertStringItem(number_of_inputed_vessel, inputed_v['Type'])
        self.inputed_vessels_property.SetStringItem(number_of_inputed_vessel, 1, inputed_v['Name'])
        self.inputed_vessels_property.SetStringItem(number_of_inputed_vessel, 2, inputed_v['IAT'])
        self.inputed_vessels_property.SetStringItem(number_of_inputed_vessel, 3, inputed_v['First_arrival'])
        self.inputed_vessels_property.SetStringItem(number_of_inputed_vessel, 4, inputed_v['Loading_limit'])
        self.inputed_vessels_property.SetStringItem(number_of_inputed_vessel, 5, inputed_v['Time_range'])

        self.ch.Append(inputed_v['Name'])
        
        self.cargo_character_table.AppendCols(1, True)
        self.cargo_character_table.AppendRows(1, True)
        
        current_table_size = self.cargo_character_table.GetNumberCols()
        self.cargo_character_table.SetColLabelValue(current_table_size - 1, inputed_v['Name'])
        self.cargo_character_table.SetRowLabelValue(current_table_size - 1, inputed_v['Name'])
        self.cargo_character_table.SetColSize(current_table_size - 1, 140)
        self.cargo_character_table.SetRowSize(current_table_size - 1, 20)
            
    def default_vessel_input_result_foam(self):
        v1 = {'Type' : 'vt1', 'Name' : 'Regina Maersk', 'IAT' : 'CONST(7)',
              'First_arrival' : 'CONST(2)', 'Loading_limit' : 'CONST(5)',
              'Time_range' : '(13, 15)'}
        v2 = {'Type' : 'vt1', 'Name' : 'Louis Maersk', 'IAT' : 'CONST(14)',
              'First_arrival' : 'CONST(3)', 'Loading_limit' : 'CONST(6)', 'Time_range' : '(15, 18)'}
        v3 = {'Type' : 'vt3', 'Name' : 'Tokyo Bay', 'IAT' : 'EXPO(7.0)',
              'First_arrival' : 'CONST(2)', 'Loading_limit' : 'CONST(5)', 'Time_range' : '(12, 16)'}
        
        for i, v in enumerate([v1, v2, v3]):
            self.inputed_vessels_property.InsertStringItem(i, v['Type'])
            self.inputed_vessels_property.SetStringItem(i, 1, v['Name'])
            self.inputed_vessels_property.SetStringItem(i, 2, v['IAT'])
            self.inputed_vessels_property.SetStringItem(i, 3, v['First_arrival'])
            self.inputed_vessels_property.SetStringItem(i, 4, v['Loading_limit'])
            self.inputed_vessels_property.SetStringItem(i, 5, v['Time_range'])
#            self.inputed_vessels_property[v['Name']] = v
            
    def set_inputed_vessel_property_format(self, parent_panel):
        self.inputed_vessels_property.InsertColumn(0, 'Type')
        self.inputed_vessels_property.InsertColumn(1, 'Name')
        self.inputed_vessels_property.InsertColumn(2, 'IAT')
        self.inputed_vessels_property.InsertColumn(3, 'First Arrival')
        self.inputed_vessels_property.InsertColumn(4, 'Loading Limit')
        self.inputed_vessels_property.InsertColumn(5, 'Time Range')
        
        self.inputed_vessels_property.SetColumnWidth(0, 60)
        self.inputed_vessels_property.SetColumnWidth(1, 115)
        self.inputed_vessels_property.SetColumnWidth(2, 90)
        self.inputed_vessels_property.SetColumnWidth(3, 90)
        self.inputed_vessels_property.SetColumnWidth(4, 105)
        self.inputed_vessels_property.SetColumnWidth(5, 100)
        
        self.default_vessel_input_result_foam()
    
    def set_vessel_property_format(self, parent_panel):
        s_first_arival = ''' First
Arrival
        '''
        s_loading_limit = '''Loading
Limit
        '''
        s_time_range = '''Time
Range
        '''
        
        type_panel = wx.Panel(parent_panel, -1, pos=(10, 20), size=(95, 30))
        name_panel = wx.Panel(parent_panel, -1, pos=(160, 20), size=(130, 30))
        IAT_panel = wx.Panel(parent_panel, -1, pos=(325, 20), size=(110, 30))
        first_arrival_panel = wx.Panel(parent_panel, -1, pos=(10, 50), size=(110, 30))
        loading_limit_panel = wx.Panel(parent_panel, -1, pos=(160, 50), size=(120, 30))
        time_range_panel = wx.Panel(parent_panel, -1, pos=(325, 50), size=(110, 30))
        
        wx.StaticText(type_panel, -1, 'Type', (5, 5))
        wx.StaticText(name_panel, -1, 'Name', (0, 5))
        wx.StaticText(IAT_panel, -1, 'IAT', (5, 5))
        wx.StaticText(first_arrival_panel, -1, s_first_arival , (0, 0))
        wx.StaticText(loading_limit_panel, -1, s_loading_limit, (0, 0))
        wx.StaticText(time_range_panel, -1, s_time_range, (0, 0))
        
        #---------------------------------------------------------------------------------------------------
        self.v_type = wx.TextCtrl(type_panel, -1, 'vt1', pos=(40, 4), size=(50, 20))
        self.v_name = wx.TextCtrl(name_panel, -1, 'Regina Maersk', pos=(40, 4), size=(85, 20))
        self.v_IAT = wx.TextCtrl(IAT_panel, -1, 'CONST(7)', pos=(40, 4), size=(65, 20))
        self.v_first_arrival = wx.TextCtrl(first_arrival_panel, -1, 'CONST(2)', pos=(40, 4), size=(65, 20))
        self.v_loading_limit = wx.TextCtrl(loading_limit_panel, -1, 'CONST(2)', pos=(50, 4), size=(65, 20))
        self.v_time_range = wx.TextCtrl(time_range_panel, -1, '(13,15)', pos=(42, 4), size=(65, 20))
        #---------------------------------------------------------------------------------------------------
    
    def vessel_property_display(self, parent_panel):
        wx.StaticBox(parent_panel, -1, "Vessel Property", pos=(0, 0), size=(575, 215)) #@UnusedVariable
        #---------------------------------------------------------------------------------------------------------------------------------------
        self.inputed_vessels_property = wx.ListCtrl(parent_panel, -1, wx.Point(10, 80), wx.Size(560, 130), style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        #---------------------------------------------------------------------------------------------------------------------------------------
        self.set_vessel_property_format(parent_panel)
        self.set_inputed_vessel_property_format(parent_panel)
                
        vessel_property_add_btn = wx.Button(parent_panel, -1, "Add", (480, 20))
        vessel_property_remove_btn = wx.Button(parent_panel, -1, "Remove", pos=(480, 50))
        parent_panel.Bind(wx.EVT_BUTTON, self.vessel_property_add, vessel_property_add_btn)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.inputed_vessels_property)
        parent_panel.Bind(wx.EVT_BUTTON, self.vessel_property_remove, vessel_property_remove_btn)
        
    def OnItemSelected(self, event):
        self.selcected_vessel_property = event.m_itemIndex
        print self.selcected_vessel_property
        event.Skip()

    def XT_distribution_display(self, parent_panel):
        wx.StaticBox(parent_panel, -1, "XT distribution", pos=(0, 0), size=(395, 165)) #@UnusedVariable
        
        wx.StaticText(parent_panel, -1, 'Import', (10, 20))
        wx.StaticText(parent_panel, -1, 'Export', (205, 20))
        
        import_XT_distribution_grid = gridlib.Grid(parent_panel, -1, pos=(20, 40), size=(170, 120))
        export_XT_distribution_grid = gridlib.Grid(parent_panel, -1, pos=(215, 40), size=(170, 120))
        
        colLabels = ['Time', 'Distribution']
        dataTypes = [gridlib.GRID_VALUE_STRING, gridlib.GRID_VALUE_STRING]
        i_data = [
            ["0 ~ 2", "0"],
            ["2 ~ 4", "0"],
            ["4 ~ 6", "0.2"],
            ["6 ~ 8", "0.2"],
            ["8 ~ 10", "0"],
            ["10 ~ 12", "0.1"],
            ["12 ~ 14", "0.1"],
            ["14 ~ 16", "0"],
            ["16 ~ 18", "0.3"],
            ["18 ~ 20", "0"],
            ["20 ~ 22", "0"],
            ["22 ~ 24", "0.1"],
            ]
        e_data = [
            ["0 ~ 2", "0"],
            ["2 ~ 4", "0"],
            ["4 ~ 6", "0"],
            ["6 ~ 8", "0.1"],
            ["8 ~ 10", "0.1"],
            ["10 ~ 12", "0"],
            ["12 ~ 14", "0.4"],
            ["14 ~ 16", "0"],
            ["16 ~ 18", "0"],
            ["18 ~ 20", "0.3"],
            ["20 ~ 22", "0.1"],
            ["22 ~ 24", "0"],
            ]
            
        #---------------------------------------------------------------------------------------------------
        self.i_table = self.drawing_table(import_XT_distribution_grid, colLabels, dataTypes, i_data) 
        self.e_table = self.drawing_table(export_XT_distribution_grid, colLabels, dataTypes, e_data)
        #---------------------------------------------------------------------------------------------------

    def master_display(self, parent_panel):
        wx.StaticBox(parent_panel, -1, "Master", pos=(0, 0), size=(395, 140)) #@UnusedVariable
        master_gird = gridlib.Grid(parent_panel, -1, pos=(15, 15), size=(375, 120))
        
        master_text = open('master_table.txt')
        colLabels = master_text.readline().split(', ') 
        dataTypes = [gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_STRING,
                          ]
        vessel_master_data = master_text.readline().split(', ')
        data = []
        while vessel_master_data != ['']:
            data.append(vessel_master_data)
            vessel_master_data = master_text.readline().split(', ')
        #-----------------------------------------------------------------------------    
        self.m_table = self.drawing_table(master_gird, colLabels, dataTypes, data)
        #-----------------------------------------------------------------------------
        master_gird.SetColSize(0, 50)
        master_gird.SetColSize(1, 60)
        master_gird.SetColSize(2, 60)
        master_gird.SetColSize(3, 60)
        master_gird.SetColSize(4, 65)
        
    def drawing_table(self, grid, colLabels, dataTypes, data):
        table = CDT.CustomDataTable(colLabels, dataTypes, data)
        grid.SetTable(table, True)
        grid.SetRowLabelSize(0)
        grid.AutoSizeColumns(True)
        return table
        
    def yard_max_dwell_time_display(self, parent_panel):
        wx.StaticBox(parent_panel, -1, "Yard max dwell time", pos=(0, 0), size=(135, 95)) #@UnusedVariable
        
        wx.StaticText(parent_panel, -1, 'Import', (20, 30))
        wx.StaticText(parent_panel, -1, 'day', (90, 30))
        wx.StaticText(parent_panel, -1, 'Export', (20, 70))
        wx.StaticText(parent_panel, -1, 'day', (90, 70))
        #-----------------------------------------------------------------------------------------------------
        self.import_max_dwell_time = wx.TextCtrl(parent_panel, -1, '3', pos=(65, 28), size=(25, 20))
        self.export_max_dwell_time = wx.TextCtrl(parent_panel, -1, '4', pos=(65, 68), size=(25, 20))
        #-----------------------------------------------------------------------------------------------------
            
    def duration_display(self, parent_panel):
        wx.StaticBox(parent_panel, -1, "Duration", pos=(0, 0), size=(215, 95)) #@UnusedVariable
        
        wx.StaticText(parent_panel, -1, 'Start', (20, 30))
        wx.StaticText(parent_panel, -1, 'End', (20, 65))
        #------------------------------------------------------------------------------
        self.start_year = wx.TextCtrl(parent_panel, -1, '2007', pos=(65, 28), size=(35, 20))
        self.start_month = wx.TextCtrl(parent_panel, -1, '06', pos=(100, 28), size=(20, 20))
        self.start_day = wx.TextCtrl(parent_panel, -1, '29', pos=(120, 28), size=(20, 20)) 
        self.start_hour = wx.TextCtrl(parent_panel, -1, '00', pos=(140, 28), size=(20, 20))
        self.start_minute = wx.TextCtrl(parent_panel, -1, '00', pos=(160, 28), size=(20, 20))
        self.start_second = wx.TextCtrl(parent_panel, -1, '00', pos=(180, 28), size=(20, 20))
        
        self.end_year = wx.TextCtrl(parent_panel, -1, '2007', pos=(65, 63), size=(35, 20))
        self.end_month = wx.TextCtrl(parent_panel, -1, '07', pos=(100, 63), size=(20, 20))
        self.end_day = wx.TextCtrl(parent_panel, -1, '29', pos=(120, 63), size=(20, 20))
        self.end_hour = wx.TextCtrl(parent_panel, -1, '23', pos=(140, 63), size=(20, 20))
        self.end_minute = wx.TextCtrl(parent_panel, -1, '59', pos=(160, 63), size=(20, 20))
        self.end_second = wx.TextCtrl(parent_panel, -1, '59', pos=(180, 63), size=(20, 20))
        #------------------------------------------------------------------------------
    
if __name__ == '__main__':

    app = wx.PySimpleApp()
    mv = Main_viewer(None, -1, 'Main_viewer', pos=(10, 10), size=(1024, 700))
    mv.Show(True)
    mv.create_Event_Viewer(None)
    app.MainLoop()
