'''
Created on 2010-12-30


The window of yc planning
    DrawPane is used to show the workload and overload of each block.
    DrawPane1 is used to show the view of the result
'''

import wx
import wx.grid
import parameter
import Interface
import yc_plan
import subprocess, _subprocess
import wait
class YC_plan(wx.MDIChildFrame):
    def __init__(self, parent=None, id=-1):
        wx.MDIChildFrame.__init__(self, parent, id, 'Yard crane plan', pos=(0, 0), size=(1535, 1300))
        #self.SetAutoLayout(True)
        panel = wx.Panel(self, -1)

        self.wnd = DrawPane(panel)
        
        self.period = 1
        font = wx.Font(15, False, wx.NORMAL, wx.NORMAL)
        panel.SetFont(font)
        button1 = wx.Button(panel, -1, "Plan", (320, 970))
        self.Bind(wx.EVT_BUTTON, self.On_plan, button1)
        button2 = wx.Button(panel, -1, "Previous", (530, 840))
        self.Bind(wx.EVT_BUTTON, self.On_previous, button2)
        button3 = wx.Button(panel, -1, "   Next   ", (1340, 840))
        self.Bind(wx.EVT_BUTTON, self.On_next, button3)    
        
        button4 = wx.Button(panel, -1, "Reset", (200, 970))
        self.Bind(wx.EVT_BUTTON, self.On_reset, button4)
        
        self.text1_content = ["Time period I","Time period II","Time period III","Time period IV"]
        self.text1 = wx.StaticText(panel, -1, self.text1_content[0], pos=(930, 840))
        box1_title = wx.StaticBox( panel, -1, "Workload view", pos=(5, 0),size=(450,1080) )
        box1 = wx.StaticBoxSizer( box1_title, wx.VERTICAL)
        box2_title = wx.StaticBox( panel, -1, "Plan", pos=(460, 0),size=(1060,885) )
        box2 = wx.StaticBoxSizer( box2_title, wx.VERTICAL)
        box3_title = wx.StaticBox( panel, -1, "Properties", pos=(450, 885),size=(1060,195) )
        box3 = wx.StaticBoxSizer( box3_title, wx.VERTICAL)

        font = wx.Font(9, False, wx.NORMAL, wx.NORMAL)
        panel.SetFont(font)
        begin_x = 530
        begin_y = 915
        gap = 30
        
        
        
        lable_list1 = ["Block ID","Time period","Row","Column","Total operation"]
        grid1 = wx.grid.Grid(panel, -1, pos=(begin_x, begin_y), size=(301,106), style=wx.WANTS_CHARS)
        grid1_col=1
        grid1_row=5
        grid1.CreateGrid(grid1_row,grid1_col)
        grid1.SetRowLabelSize(150)
        grid1.SetColSize(0,150)
        grid1.SetColLabelSize(0)
        
        grid1.SetDefaultCellAlignment(wx.ALIGN_CENTRE,wx.ALIGN_CENTRE)
        
        for row in range(5):
            grid1.SetRowSize(row,21)
            grid1.SetRowLabelValue(row, lable_list1[row])
        begin_x = 830
        lable_list2 = ["Load operation","Discharge operation","Gate in operation","Gate out operation","Premarshalling operation"]
        grid2 = wx.grid.Grid(panel, -1, pos=(begin_x, begin_y), size=(311,106), style=wx.WANTS_CHARS)
        grid2_col=1
        grid2_row=5
        grid2.CreateGrid(grid2_row,grid2_col)
        grid2.SetRowLabelSize(160)
        grid2.SetColSize(0,150)
        grid2.SetColLabelSize(0)
        
        grid2.SetDefaultCellAlignment(wx.ALIGN_CENTRE,wx.ALIGN_CENTRE)
        
        for row in range(5):
            grid2.SetRowSize(row,21)
            grid2.SetRowLabelValue(row, lable_list2[row])
        

        begin_x = 1140

        lable_list3 = ["YC ID","YC serve range","YC ID","YC serve range",""]
        grid3 = wx.grid.Grid(panel, -1, pos=(begin_x, begin_y), size=(301,106), style=wx.WANTS_CHARS)
        grid3_col=1
        grid3_row=5
        grid3.CreateGrid(grid3_row,grid3_col)
        grid3.SetRowLabelSize(150)
        grid3.SetColSize(0,150)
        grid3.SetColLabelSize(0)
        
        grid3.SetDefaultCellAlignment(wx.ALIGN_CENTRE,wx.ALIGN_CENTRE)
        
        self.grid1 = grid1
        self.grid2 = grid2
        self.grid3 = grid3
        for row in range(5):
            grid3.SetRowSize(row,21)
            grid3.SetRowLabelValue(row, lable_list3[row])
            
        self.wnd1 = DrawPane1(panel, _grid1=grid1, _grid2=grid2, _grid3=grid3)
        
    def On_reset(self,event):
        Interface.yc_reset()
        self.grid1.ClearGrid()
        self.grid2.ClearGrid()
        self.grid3.ClearGrid()
        
        self.wnd1.workload=Interface.get_workload_for_show()
        self.wnd1.yc_original_position, self.wnd1.yc_moved_position = Interface.get_yc_movement()
        self.wnd1.Refresh()
        
        self.wnd.workload=Interface.get_workload_for_show()
        self.wnd.overload=Interface.get_overload_for_show()
        self.wnd.Refresh()
        
        #time.sleep(20)

    def On_plan(self, event):
        #p = subprocess.Popen('pythonw wait.py')
        wait.start('IMPACT', 'Solving planning problem...')
        
        for period in range(1,5):
            yc_plan.deployment(period)
        self.wnd1.workload=Interface.get_workload_for_show()
        self.wnd1.yc_original_position, self.wnd1.yc_moved_position = Interface.get_yc_movement()
        self.wnd1.Refresh()
        self.wnd.overload=Interface.get_overload_for_show()
        self.wnd.Refresh()
        wait.stop()
        
      #  _subprocess.TerminateProcess(p._handle, 1)
        
    def On_previous(self, event):
        if self.period>1:
            self.period = self.period - 1
            self.wnd1.period = self.period
            self.text1.SetLabel(self.text1_content[self.period-1])
            self.wnd1.Refresh()
            
    def On_next(self, event):
        if self.period<4:
            self.period = self.period + 1
            self.wnd1.period = self.period
            self.text1.SetLabel(self.text1_content[self.period-1])
            self.wnd1.Refresh()

class DrawPane1(wx.ScrolledWindow):
    def __init__(self, parent=-1,  id=-1, _grid1=0, _grid2=0, _grid3=0):
        wx.ScrolledWindow.__init__(self, parent, id, pos=(472, 20), size=(1036,811))
        self.SetDoubleBuffered(True)
        ## constants for drawing
        self.workload=Interface.get_workload_for_show()
        self.yc_original_position, self.yc_moved_position = Interface.get_yc_movement()
        self.virtualsize_x = 1035
        self.virtualsize_y = 810
        self.SetBackgroundColour(wx.Colour(215, 245,  245, 128))
        self.SetVirtualSize((self.virtualsize_x, self.virtualsize_y))
        self.SetScrollRate(20, 20)
        self.Bind(wx.EVT_PAINT, self.On_Paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.On_show_info)
        self.period = 1
        self.l0=52
        self.t0=42
        self.gap_w = 245
        self.gap_h = 85
        self.grid1=_grid1
        self.grid2=_grid2
        self.grid3=_grid3
        
        self.period_content = ["I: ","II: ","III: ","IV: "]
        self.block_position = {"A1":(0,0), "B1":(1,0), "C1":(2,0), "D1":(3,0),
                               "A2":(0,1), "B2":(1,1), "C2":(2,1), "D2":(3,1),
                               "A3":(0,2), "B3":(1,2), "C3":(2,2), "D3":(3,2),
                               "A4":(0,3), "B4":(1,3), "C4":(2,3), "D4":(3,3),
                               "A5":(0,4), "B5":(1,4), "C5":(2,4), "D5":(3,4),
                               "A6":(0,5), "B6":(1,5), "C6":(2,5), "D6":(3,5),
                               "A7":(0,6), "B7":(1,6), "C7":(2,6), "D7":(3,6),
                               "A8":(0,7), "B8":(1,7), "C8":(2,7), "D8":(3,7),
                               "A9":(0,8), "B9":(1,8), "C9":(2,8), "D9":(3,8)}
        
        self.selected_block = None
        
    def On_Paint(self, event):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        dc.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        dc.SetPen(wx.GREY_PEN)

        Block_list = parameter.block_list
        
        
        penclr = wx.Colour(0, 0, 0, wx.ALPHA_OPAQUE)
        dc.SetPen(wx.Pen(penclr)) 
                  
        for i in range(len(Block_list)):
            self.draw_block(dc,Block_list[i], self.workload[i])        
    
    def On_show_info(self, event):
        x = event.GetX()
        y = event.GetY()
        row = 0   # from 1
        column = 0  # from 1
        for i in range(4):
            if x >= self.l0 + self.gap_w*i and x <= self.l0 + self.gap_w*i + 198:
                column = i+1
        
        for j in range(9):
            if y >= self.t0 + self.gap_h*j and y <= self.t0 + self.gap_h*j + 48:
                row = j+1
                
        if row!=0 and column!=0:
            block_index = (row-1)*4 + column-1
            block_id = parameter.block_list[block_index]
            self.selected_block = block_id
            self.grid1.SetCellValue(0, 0, block_id)
            self.grid1.SetCellValue(1, 0, str(self.period))
            self.grid1.SetCellValue(2, 0, str(self.block_position[block_id][1]+1))
            self.grid1.SetCellValue(3, 0, str(self.block_position[block_id][0]+1))
            self.grid1.SetCellValue(4, 0, str(self.workload[block_index][self.period-1]))
            
            l,d,i,o,p = Interface.get_detail_workload_for_show(block_id, self.period)
            
            self.grid2.SetCellValue(0, 0, str(l))
            self.grid2.SetCellValue(1, 0, str(d))
            self.grid2.SetCellValue(2, 0, str(i))
            self.grid2.SetCellValue(3, 0, str(o))
            self.grid2.SetCellValue(4, 0, str(p))

            if block_id in self.yc_original_position[self.period-1]:
                original_yc_list =  self.yc_original_position[self.period-1][block_id]
            else:
                original_yc_list = []
            if block_id in self.yc_moved_position[self.period-1]:
                moved_yc_list = self.yc_moved_position[self.period-1][block_id]
            else:
                moved_yc_list = []
            
            yc_position=[]
            
            if len(original_yc_list)==2:
                if len(moved_yc_list)==2:
                    yc_position.append([original_yc_list[0],0,parameter.total_time])
                    yc_position.append([original_yc_list[1],0,parameter.total_time])
                elif len(moved_yc_list)==1:
                    yc_position.append([moved_yc_list[0],0,parameter.total_time])
                    if moved_yc_list[0]==original_yc_list[0]:
                        yc_position.append([original_yc_list[1],0,Interface.get_yc_move_time(original_yc_list[1], self.period)])
                    else:
                        yc_position.append([original_yc_list[0],0,Interface.get_yc_move_time(original_yc_list[0], self.period)])
                elif len(moved_yc_list)==0:
                    yc_position.append([original_yc_list[0],0,Interface.get_yc_move_time(original_yc_list[0], self.period)])
                    yc_position.append([original_yc_list[1],0,Interface.get_yc_move_time(original_yc_list[1], self.period)])
                    
                    
            if len(original_yc_list)==1:
                if len(moved_yc_list)==2:
                    yc_position.append([original_yc_list[0],0,parameter.total_time])
                    if moved_yc_list[0]==original_yc_list[0]:
                        yc_position.append([moved_yc_list[1],Interface.get_yc_move_time(moved_yc_list[1], self.period),parameter.total_time])
                    else:
                        yc_position.append([moved_yc_list[0],Interface.get_yc_move_time(moved_yc_list[0], self.period),parameter.total_time])
                elif len(moved_yc_list)==1:
                    yc_position.append([original_yc_list[0],0,parameter.total_time])
                elif len(moved_yc_list)== 0:
                    yc_position.append([original_yc_list[0],0,Interface.get_yc_move_time(original_yc_list[0], self.period)])
                    
            if len(original_yc_list)==0:
                if len(moved_yc_list)==2:
                    yc_position.append([moved_yc_list[0],Interface.get_yc_move_time(moved_yc_list[0], self.period),parameter.total_time])
                    yc_position.append([moved_yc_list[1],Interface.get_yc_move_time(moved_yc_list[1], self.period),parameter.total_time])
                if len(moved_yc_list)==1:
                    yc_position.append([moved_yc_list[0],Interface.get_yc_move_time(moved_yc_list[0], self.period),parameter.total_time])
                
            self.grid3.ClearGrid()
            
            for yc in range(len(yc_position)):
                self.grid3.SetCellValue(yc*2, 0, yc_position[yc][0])
                min1=yc_position[yc][1]%12
                if min1<10:
                    _min1="0" + str(min1)
                else:
                    _min1=str(min1)
                min2=yc_position[yc][2]%12
                if min2<10:
                    _min2="0" + str(min2)
                else:
                    _min2= str(min2)
                self.grid3.SetCellValue(yc*2+1, 0, str((self.period-1)*6+yc_position[yc][1]/12)+":" + _min1 +" ~ "+ str((self.period-1)*6+yc_position[yc][2]/12)+ ":"+ _min2)
                        
            self.Refresh()

    def draw_block(self,dc, block,workload):
        font = wx.Font(8, False, wx.NORMAL, wx.NORMAL)
        dc.SetFont(font)
        r=250-int(0.25*workload[self.period-1])
        g=250-int(0.5*workload[self.period-1])
        b = 250
        brushclr = wx.Colour(r, g, b, 128)  
        dc.SetBrush(wx.Brush(brushclr))   
        x,y = self.block_position[block]
        if self.selected_block == block:
            old_pen = dc.GetPen()
            dc.SetPen(wx.Pen(wx.BLACK, 3))
            dc.DrawRectangle(self.l0+x*self.gap_w,self.t0+y*self.gap_h,198, 48)
            dc.SetPen(old_pen)
        else:
            dc.DrawRectangle(self.l0+x*self.gap_w,self.t0+y*self.gap_h,198, 48)
        dc.DrawText(block, self.l0+x*self.gap_w+4,self.t0+y*self.gap_h+4)
        
        if self.period<4:
            r=250-int(0.5*workload[self.period])
            g=200-int(0.5*workload[self.period])
            b = 250
            brushclr = wx.Colour(r, g, b, 128)  
            dc.SetBrush(wx.Brush(brushclr))           
            if self.selected_block == block:
                old_pen = dc.GetPen()
                dc.SetPen(wx.Pen(wx.BLACK, 3))
                dc.DrawPolygon([(self.l0+x*self.gap_w+198,self.t0+y*self.gap_h),(self.l0+x*self.gap_w+198,self.t0+y*self.gap_h+48),(self.l0+x*self.gap_w,self.t0+y*self.gap_h+48)],0,0)
                dc.SetPen(old_pen)
            else:
                dc.DrawPolygon([(self.l0+x*self.gap_w+198,self.t0+y*self.gap_h),(self.l0+x*self.gap_w+198,self.t0+y*self.gap_h+48),(self.l0+x*self.gap_w,self.t0+y*self.gap_h+48)],0,0)
            
        dc.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        if self.period<4:
            dc.DrawText(self.period_content[self.period-1]+str(workload[self.period-1])+"   "+self.period_content[self.period]+str(workload[self.period]), self.l0+x*self.gap_w+65,self.t0+y*self.gap_h+56)
        else:
            dc.DrawText(self.period_content[self.period-1]+str(workload[self.period-1]), self.l0+x*self.gap_w+64,self.t0+y*self.gap_h+55)
        font = wx.Font(8, False, wx.NORMAL, wx.NORMAL)
        dc.SetFont(font)
        
        if block in self.yc_original_position[self.period-1]:
            original_yc_list = self.yc_original_position[self.period-1][block]
        else:
            original_yc_list = []
        if block in self.yc_moved_position[self.period-1]:
            moved_yc_list = self.yc_moved_position[self.period-1][block]
        else:
            moved_yc_list = []
        self.draw_yc(dc,original_yc_list, moved_yc_list, block)
        
    def draw_yc(self,dc,original_yc_list, moved_yc_list, block_id):
        gap_x = 245
        gap_y = 85
        y0=36
        x,y = self.block_position[block_id]
                    
        if len(original_yc_list)!=0:
            r, g, b = (198, 238,  255)
            brushclr = wx.Colour(r, g, b, 128)  
            dc.SetBrush(wx.Brush(brushclr))
            x0=70
            dc.DrawRectangle(x0+x*gap_x,y0+y*gap_y,28,60)
            text = original_yc_list[0]
            ts = dc.GetTextExtent(text)[0]  
            dc.DrawText(text, x0+x*gap_x+14-ts/2,y0+y*gap_y+25)
            if len(original_yc_list)==2:
                dc.DrawRectangle(x0+x*gap_x+40,y0+y*gap_y,28,60)
                text = original_yc_list[1]
                ts = dc.GetTextExtent(text)[0]  
                dc.DrawText(text, x0+x*gap_x+54-ts/2,y0+y*gap_y+25)
        
        if len(moved_yc_list)!=0:
            r, g, b = (254, 255,  237)
            brushclr = wx.Colour(r, g, b, 128)  
            dc.SetBrush(wx.Brush(brushclr))
            x0=205
            dc.SetPen(wx.Pen(wx.BLACK, 1, wx.DOT_DASH))          
            dc.DrawRectangle(x0+x*gap_x,y0+y*gap_y,28,60)
            text = moved_yc_list[0]
            ts = dc.GetTextExtent(text)[0]  
            dc.DrawText(text, x0+x*gap_x+14-ts/2,y0+y*gap_y+25)
            if len(moved_yc_list)==2:
                dc.DrawRectangle(x0+x*gap_x-40,y0+y*gap_y,28,60)
                text = moved_yc_list[1]
                ts = dc.GetTextExtent(text)[0]  
                dc.DrawText(text, x0+x*gap_x-26-ts/2,y0+y*gap_y+25)                
            dc.SetPen(wx.Pen(wx.BLACK, 1, wx.SOLID))

            
class DrawPane(wx.ScrolledWindow):
    def __init__(self, parent=-1,  id=-1):
        wx.ScrolledWindow.__init__(self, parent, id, pos=(15, 25), size=(430,920))######################
        ## constants for drawing
        self.workload=Interface.get_workload_for_show()
        self.overload=Interface.get_overload_for_show()
        self.virtualsize_x = 410
        self.virtualsize_y = 4400
        self.SetBackgroundColour(wx.Colour(230, 251, 255, 128))
        self.SetVirtualSize((self.virtualsize_x, self.virtualsize_y))
        self.SetScrollRate(20, 20)
        self.Bind(wx.EVT_PAINT, self.On_Paint)
        
    def On_Paint(self, event):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        dc.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        dc.SetPen(wx.GREY_PEN)
        
        Block_list = parameter.block_list
        
        penclr = wx.Colour(0, 0, 0, wx.ALPHA_OPAQUE)
        dc.SetPen(wx.Pen(penclr)) 
        
        
        
        for i in range(len(Block_list)):
            self.draw_block(dc, i,Block_list[i],self.workload[i],'w')
            self.draw_block(dc, i,Block_list[i],self.overload[i],'o')
        
        
        dc.SetFont(wx.Font(13, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        dc.DrawText("Workloads",30, 15 )
        dc.DrawText("Overflowed",230, 15 )
        
    def draw_block(self, dc, no ,block,workload, type):
        dc.SetBrush(wx.Brush("WHITE"))   
        if type=='w':
            l0=30
        else:
            l0=230
        t0=51
        gap = 50
        gap_b = 120
        dc.DrawRectangle(l0+1,t0+no*gap_b+1,3*gap-2, 2*gap-2)
        dc.DrawText(block, l0-20,t0+no*gap_b+5)
                
        r, g, b = (255, 227, 198)
        brushclr = wx.Colour(r, g, b, 128)  
        dc.SetBrush(wx.Brush(brushclr))   

        dc.DrawLine(l0+22,t0+no*gap_b+80,l0+135,t0+no*gap_b+80)
        dc.DrawText("I     II     III     IV", l0+30,t0+no*gap_b+80)
        dc.DrawLine(l0+135,t0+no*gap_b+80, l0+130,t0+no*gap_b+76)#arrow
        dc.DrawLine(l0+135,t0+no*gap_b+80, l0+130,t0+no*gap_b+84)
        dc.DrawText("T", l0+139,t0+no*gap_b+72)
        
        
        dc.DrawLine(l0+22,t0+no*gap_b+20,l0+22,t0+no*gap_b+80)
        dc.DrawLine(l0+22,t0+no*gap_b+20,l0+18,t0+no*gap_b+25)#arrow
        dc.DrawLine(l0+22,t0+no*gap_b+20,l0+26,t0+no*gap_b+25)
        dc.DrawText("W", l0+15,t0+no*gap_b+7)
        
        dc.DrawLine(l0+22,t0+no*gap_b+55,l0+25,t0+no*gap_b+55)
        dc.DrawText("50", l0+5,t0+no*gap_b+47)
        
        dc.DrawLine(l0+22,t0+no*gap_b+30,l0+25,t0+no*gap_b+30)
        dc.DrawText("100", l0,t0+no*gap_b+22)
        r, g, b = (198, 238,  255)
        brushclr = wx.Colour(r, g, b, 128)  
        dc.SetBrush(wx.Brush(brushclr))
        gap_w = 0.5         
        for i in range(4):
            height = int(gap_w*workload[i])
            dc.DrawRectangle(l0+28+i*27, t0+no*gap_b+81-height,15, height)
                
            text = str(workload[i])
            ts = dc.GetTextExtent(text)[0]  
            dc.DrawText(text,l0+35+i*27-ts/2, t0+no*gap_b+65-height )
        
   

    
    
