'''
Created on 2010-12-30


The window of berth planning
    DrawPane1, DrawPane2, and DrawPane3 are just used to show the label.
    DrawPane is used to show the view of the result

'''

import wx
import wx.grid
import Interface
import BerthQCPlan
import random
import subprocess, _subprocess
import wait
class Berth_plan(wx.MDIChildFrame):
    def __init__(self, parent=None, id=-1):
        wx.MDIChildFrame.__init__(self, parent, id, 'Berth Plan', pos=(0, 0), size=(1585,950))#1585, 1120))
        #self.SetAutoLayout(True)
        panel = wx.Panel(self, -1)
        self.wnd1 = DrawPane1(panel)
        self.wnd2 = DrawPane2(panel)
        self.wnd3 = DrawPane3(panel)
        self.wnd = DrawPane(panel,-1,self.wnd1, self.wnd2)
        self.click = False
        self.select_row = []
        button1 = wx.Button(panel, -1, "Plan", (270, 870))
        self.Bind(wx.EVT_BUTTON, self.plan, button1)
        
        button2 = wx.Button(panel, -1, "Reset", (170, 870))
        self.Bind(wx.EVT_BUTTON, self.reset, button2)
      
      
        font = wx.Font(10, False, wx.NORMAL, wx.NORMAL)
        panel.SetFont(font)  
        grid1 = wx.grid.Grid(panel, -1, pos=(15, 50), 
                           size=(350,800), style=wx.WANTS_CHARS)
        
        yard_plan_grid1_col=4
        yard_plan_grid1_row=100
        grid1.DisableCellEditControl()
        grid1.DisableDragColMove()
        grid1.DisableDragGridSize()
        grid1.CreateGrid(yard_plan_grid1_row,yard_plan_grid1_col)
        grid1.SetRowLabelSize(20)
        grid1.SetColSize(0, 60);
        grid1.SetColSize(1, 100);
        grid1.SetColSize(2, 100);
        grid1.SetColSize(3, 50);
        

        
        grid1.SetDefaultCellAlignment(wx.ALIGN_CENTRE,wx.ALIGN_CENTRE)
        grid1.SetSelectionMode(wx.grid.Grid.SelectRows)
        grid1_label = ["Vessel", "ETA", "ETD", "Plan"]
        for col in range(4):
            grid1.SetColLabelValue(col, grid1_label[col])
            
        self.vessel_list = Interface.get_vessel_list_for_show()    
        

        for i in range(len(self.vessel_list)):
            for j in range(len(self.vessel_list[i])):
                grid1.SetCellValue(i, j, self.vessel_list[i][j])
                
        grid1.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.check)

        self.grid1 = grid1
        
        font = wx.Font(15, False, wx.NORMAL, wx.NORMAL)
        panel.SetFont(font)
        box1_title = wx.StaticBox( panel, -1, "Vessel List", pos=(5, 10),size=(370,900) )
        box1 = wx.StaticBoxSizer( box1_title, wx.VERTICAL)
        box1.Add(grid1)
        box2_title = wx.StaticBox( panel, -1, "Berth Plan", pos=(380, 10),size=(875,900) )
        box2 = wx.StaticBoxSizer( box2_title, wx.VERTICAL)
        box3_title = wx.StaticBox( panel, -1, "Properties", pos=(1260, 10),size=(300,900) )
        font = wx.Font(10, False, wx.NORMAL, wx.NORMAL)
        panel.SetFont(font)
        box3 = wx.StaticBoxSizer( box3_title, wx.VERTICAL)
        box4_title = wx.StaticBox( panel, -1, "Vessel", pos=(1280, 40),size=(260,320) )
        box4 = wx.StaticBoxSizer( box4_title, wx.VERTICAL)
        box5_title = wx.StaticBox( panel, -1, "Schedule", pos=(1280, 400),size=(260,350) )
        box5 = wx.StaticBoxSizer( box5_title, wx.VERTICAL)        
        
        begin_x = 1290
        begin_y = 75
        gap = 30
        lable_list1 = ["Vessel ID","ETA","ETD","Length","Total operation","Favorite position","Max QC","Min QC"]
        
        grid2 = wx.grid.Grid(panel, -1, pos=(begin_x, begin_y), 
                           size=(241,241), style=wx.WANTS_CHARS)
        grid2.SetDefaultCellAlignment(wx.ALIGN_CENTRE,wx.ALIGN_CENTRE)
        grid2_col=1
        grid2_row=8
        grid2.DisableCellEditControl()
        grid2.DisableDragColMove()
        grid2.DisableDragGridSize()

        grid2.CreateGrid(grid2_row,grid2_col)
        grid2.SetRowLabelSize(120)
        grid2.SetColSize(0,120)
        grid2.SetColLabelSize(0)
        for row in range(8):
            grid2.SetRowSize(row,30)
            grid2.SetRowLabelValue(row, lable_list1[row])
        

        self.grid2 = grid2
        lable_list2 = ["Location","From","To"]
        
        begin_y = 430
        grid3 = wx.grid.Grid(panel, -1, pos=(begin_x, begin_y), 
                           size=(241,91), style=wx.WANTS_CHARS)
        grid3.SetDefaultCellAlignment(wx.ALIGN_CENTRE,wx.ALIGN_CENTRE)
        grid3_col=1
        grid3_row=3
        
        grid3.DisableCellEditControl()
        grid3.DisableDragColMove()
        grid3.DisableDragGridSize()

        grid3.CreateGrid(grid3_row,grid3_col)
        grid3.SetRowLabelSize(120)
        grid3.SetColSize(0,120)
        grid3.SetColLabelSize(0)
        for row in range(3):
            grid3.SetRowSize(row,30)
            grid3.SetRowLabelValue(row, lable_list2[row])
            
        
        self.grid3=grid3
    
 
    def check(self,event):
        row = event.GetRow()
        if event.ControlDown()==False:
            ship_id= self.grid1.GetCellValue(row, 0)
            try:  # whether there is some info in that row
                vessel_info = Interface.check_vessel(ship_id)
                for _row in range(8):
                    self.grid2.SetCellValue(_row,0,str(vessel_info[_row]))
                    
                vessel_schedule = Interface.check_vessel_schedule(ship_id)
                for _row in range(3):
                    self.grid3.SetCellValue(_row,0,str(vessel_schedule[_row]))
            except:
                pass    
            self.select_row=[]
            
        self.select_row.append(row)
        event.Skip()
        
        
        
        
    def reset(self,event):
        Interface.initiate_db_for_berth()
        self.grid1.ClearGrid()
        self.grid2.ClearGrid()
        self.grid3.ClearGrid()
        
        self.vessel_list = Interface.get_vessel_list_for_show()    
        for i in range(len(self.vessel_list)):
            for j in range(len(self.vessel_list[i])):
                self.grid1.SetCellValue(i, j, self.vessel_list[i][j])
                
        self.wnd.vessel_info_list = Interface.get_vessel_position_for_show()
        self.wnd.if_plan = False
        self.wnd.Refresh()
    
    def plan(self,event):        
        #p = subprocess.Popen('pythonw wait.py')
        wait.start('IMPACT', 'Solving planning problem...')
        self.selected_vessel_list = []
        
        for row in self.select_row:
            self.selected_vessel_list.append(self.grid1.GetCellValue(row, 0))

        print self.selected_vessel_list    
    
        BerthQCPlan.run_algorithm(self.selected_vessel_list)

        self.wnd.vessel_info_list = Interface.get_vessel_position_for_show()
        self.wnd.if_plan = True
        for row in self.select_row:
            self.grid1.SetCellValue(row,3,"OK")
        self.wnd.Refresh()
        wait.stop()
        #_subprocess.TerminateProcess(p._handle, 1)

class DrawPane1(wx.Window):
    def __init__(self, parent=-1,  id=-1):
        wx.Window.__init__(self, parent, id, pos=(448, 50), size=(780,55))       #pos=(338, 50), size=(910,950)
        ## constants for drawing
        self.SetBackgroundColour("WHITE")
        self.Bind(wx.EVT_PAINT, self.On_Paint)
        self.x=0
        
        self.SetDoubleBuffered(True)
    def On_Paint(self, event):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        dc.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        dc.SetPen(wx.GREY_PEN)
        
        r, g, b = (207 , 202, 252)
        brushclr = wx.Colour(r, g, b, 128)
        dc.SetBrush(wx.Brush(brushclr))
        dc.DrawRectangle(0,0, 830,55)
        
        dc.DrawText("Location", 5, 2)
        r, g, b = (250,  250,  250)
        brushclr = wx.Colour(r, g, b, 28)   
        dc.SetBrush(wx.Brush(brushclr))
        for i in range(21):
            dc.DrawCircle(20+i*50-self.x, 46, 5)
            text = str(i*5)
            ts = dc.GetTextExtent(text)[0]
            dc.DrawText(text,19+i*50-ts/2-self.x, 23 )
    


class DrawPane2(wx.Window):
    def __init__(self, parent=-1,  id=-1):
        wx.Window.__init__(self, parent, id, pos=(388, 110), size=(60,725))       #pos=(338, 50), size=(910,950)
        ## constants for drawing
        self.SetBackgroundColour("WHITE")
        self.Bind(wx.EVT_PAINT, self.On_Paint)
        self.time_list=["00:00","03:00","06:00","09:00","12:00","15:00","18:00","21:00"]    
        self.data_list = ["10/12/20","10/12/21","10/12/22","10/12/23","10/12/24","10/12/25","10/12/26","10/12/27","10/12/28","10/12/29","10/12/30","10/12/31"]
        self.y=0
        
            
        self.SetDoubleBuffered(True)
            
    def On_Paint(self, event):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        dc.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        dc.SetPen(wx.GREY_PEN)
        
        r, g, b = (207 , 202, 252)
        brushclr = wx.Colour(r, g, b, 128)
        dc.SetBrush(wx.Brush(brushclr))
        dc.DrawRectangle(0,0,55, 870)

        r, g, b = (240 , 220, 255)
        brushclr = wx.Colour(r, g, b, 128)
        dc.SetBrush(wx.Brush(brushclr))
        
        for i in range(3):
            dc.DrawRectangle(0,425+i*800-self.y,55, 400)
        
        r, g, b = (250,  250,  250)
        brushclr = wx.Colour(r, g, b, 28)   
        dc.SetBrush(wx.Brush(brushclr))
        time_list = self.time_list[:]
        data_list = self.data_list[:]
        for i in range(34):
            dc.DrawCircle(45, 36+i*50-self.y, 5)
            text = time_list[i%8]
            ts = dc.GetTextExtent(text)[0]
            dc.DrawText(text,22-ts/2, 27+i*50-self.y)
            
            dc.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
            if i%8 == 0:
                text = data_list.pop(0)
                ts = dc.GetTextExtent(text)[0]
                dc.DrawText(text,27-ts/2, 204+i*50-self.y)
            
            dc.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))


class DrawPane3(wx.Window):
    def __init__(self, parent=-1,  id=-1):
        wx.Window.__init__(self, parent, id, pos=(388, 50), size=(60,60))      
        ## constants for drawing
        self.SetBackgroundColour("WHITE")
        self.Bind(wx.EVT_PAINT, self.On_Paint)

    def On_Paint(self, event):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        dc.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        dc.SetPen(wx.GREY_PEN)
        dc.DrawText("Time", 13, 45)
        
                                
class DrawPane(wx.ScrolledWindow):
    def __init__(self, parent=-1,  id=999,col1=-1 , col2=-1):
        wx.ScrolledWindow.__init__(self, parent, id, pos=(448, 105), size=(800,745))       
        ## constants for drawing
        self.if_plan = False
        self.col1=col1
        self.col2=col2
        self.virtualsize_x = 1080
        self.virtualsize_y = 1800
        self.SetBackgroundColour("WHITE")
        self.SetVirtualSize((self.virtualsize_x, self.virtualsize_y))
        self.SetScrollRate(1, 1)
        self.vessel_info_list = Interface.get_vessel_position_for_show() ##vessel_id, length, location, begin, end
        self.Bind(wx.EVT_PAINT, self.On_Paint)
        self.Bind(wx.EVT_SCROLLWIN, self.On_Scroll)
        self.SetDoubleBuffered(True)
        self.vessel_color_dic={}
        for vessel in self.vessel_info_list:
            self.vessel_color_dic[vessel[0]] = (random.randint(180,225), random.randint(180,225), 250)
        #self.Draw_vessel = False
    def On_Scroll(self,event):
        x,y = self.GetViewStart()
        self.col1.x=x
        self.col1.Refresh()
        self.col2.y=y
        self.col2.Refresh()
        event.Skip()
    
    def On_Paint(self, event):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
    
        dc.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        dc.SetPen(wx.GREY_PEN)
        
        rect = wx.Rect(0,0, self.virtualsize_x-20, self.virtualsize_y-45)             
        r, g, b = (215, 245,  245)
        brushclr = wx.Colour(r, g, b, 128)   
        dc.SetBrush(wx.Brush(brushclr))
        rect.SetPosition((0,5))
        dc.DrawRoundedRectangleRect(rect, 8)
        
        
        
        r, g, b = (224, 238,  255)
        brushclr = wx.Colour(r, g, b, 128)   
        dc.SetBrush(wx.Brush(brushclr))
        
        
        for i in range((self.virtualsize_y-100)/100):
            dc.DrawRectangle(0,40+i*100, self.virtualsize_x-20, 51)
        
        penclr = wx.Colour(255, 255, 255, wx.ALPHA_OPAQUE)
        dc.SetPen(wx.Pen(penclr))
        
        for i in range((self.virtualsize_y-100)/50):    #heng
            dc.DrawLine(1, 40+i*50, self.virtualsize_x-21, 40+i*50)
        
        for i in range((self.virtualsize_x-20)/50):    #shu
            dc.DrawLine(20+i*50, 6, 20+i*50, self.virtualsize_y-97)
        

        for vessel_info in self.vessel_info_list: ##vessel_id, length, location, begin, end
            self.draw_vessel(dc, vessel_info[0], vessel_info[2], vessel_info[1]/10, vessel_info[3], vessel_info[4])    

        if self.if_plan:
            self.draw_qc(dc)
            
           
    def draw_vessel(self, dc, Vessel, Location, Length, From, To):
        r, g, b = self.vessel_color_dic[Vessel]
        brushclr = wx.Colour(r, g, b, 128)   
        dc.SetBrush(wx.Brush(brushclr))               
        l0=20
        t0=40
        gap_l = 10
        gap_t = 50.0/3
        dc.DrawRectangle(l0+Location*gap_l+1,t0+From*gap_t+1, int(Length*gap_l)-1, int((To-From)*gap_t)-1)
        dc.DrawText(Vessel, l0+int(Location*gap_l)+10,t0+int(From*gap_t)+10)
        
   
    def draw_qc(self,dc):
        brushclr = wx.Colour(100, 120, 250, 128)   
        dc.SetBrush(wx.Brush(brushclr))
        
        penclr = wx.Colour(0, 0, 0, wx.ALPHA_OPAQUE)
        dc.SetPen(wx.Pen(penclr))
        time_range_list, qc_assign_list, vessel_position_dic, vessel_leave_dic = Interface.get_db_qc()
        self.Qc_position = {"QC1":(120,40),"QC2":(220,40),"QC3":(320,40),"QC4":(420,40), "QC5":(520,40), "QC6":(620,40), "QC7":(720,40), "QC8":(820,40)}
        
        for key in self.Qc_position:
            dc.DrawText(key, self.Qc_position[key][0]-15,25)
        
        
        for t in range(len(time_range_list)):
            for qc in range(len(qc_assign_list[t])):
                _from, _to = time_range_list[t]
                vessel_p = vessel_position_dic[qc_assign_list[t][qc][1]]
                no=qc_assign_list[t][qc][2]
                qc_id = qc_assign_list[t][qc][0]
                vessel_leave_time = vessel_leave_dic[qc_assign_list[t][qc][1]]
                if vessel_leave_time <= _to:
                    _to = vessel_leave_time
                    dc.DrawText(qc_id, 70 + 10*vessel_p + no*50,20 + int(_to*50.0/3))
                self.draw_qc_route(dc, vessel_p, no, _from, _to, qc_id)
        
        
    def draw_qc_route(self, dc, vessel_p, no, From, To, QC_id): 
        l0=100
        t0=40
        gap_l = 10
        gap_t = 50.0/3
        
        x = l0 + gap_l*vessel_p + no*gap_l*5
        y = t0 + int(From*gap_t) 
        penclr = wx.Colour(70, 150, 130, wx.ALPHA_OPAQUE)
        dc.SetPen(wx.Pen(penclr))
        
        x0,y0 = self.Qc_position[QC_id]
        dc.DrawLine(x0,y0,x+5,y)
        
        penclr = wx.Colour(0, 0, 0, wx.ALPHA_OPAQUE)
        dc.SetPen(wx.Pen(penclr))
        
        
        height = int((To - From)*gap_t)-3
        dc.DrawRectangle(x, y, 10, height)
        
        self.Qc_position[QC_id]=(x+5, y+height)
        
        