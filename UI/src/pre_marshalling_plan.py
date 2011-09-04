from __future__ import division

import wx, MySQLdb
import ylee
import Interface
yard_UNITS = 33
bay_UNITS = 33
seq_UNITS = 20



class Pre_marshalling_plan(wx.wx.MDIChildFrame):
    def __init__(self, parent = None, id=-1): #@UndefinedVariable
        wx.MDIChildFrame.__init__(self, parent, id, 'pre_marshalling', pos=(0, 0), size=(1585, 1120))
        self.base_panel = wx.Panel(self, -1)

        db = Interface.db
        db.autocommit(True)
        self.cursor = db.cursor()
        self.read_database()
        
        view_gap = 10
        font = wx.Font(15, False, wx.NORMAL, wx.NORMAL)
        self.base_panel.SetFont(font)
        
        yard_box_px = 10
        yard_box_py = 5
        yard_box_sx, yard_box_sy = 790, 800
        wx.StaticBox(self.base_panel, -1, "Yard View", pos=(yard_box_px, yard_box_py), size=(yard_box_sx, yard_box_sy))
        self.make_yard_view_contents(yard_box_px, yard_box_py, yard_box_sx, yard_box_sy)

        bay_box_px = yard_box_px + yard_box_sx + view_gap
        bay_box_py = yard_box_py
        bay_box_sx = 1585 - (bay_box_px + view_gap)
        bay_box_sy = yard_box_sy
        wx.StaticBox(self.base_panel, -1, "Bay View", pos=(bay_box_px , bay_box_py), size=(bay_box_sx , bay_box_sy))
        self.make_bay_view_contents(bay_box_px, bay_box_py, bay_box_sx, bay_box_sy)
        
        sequence_box_px = yard_box_px
        sequence_box_py = yard_box_py + yard_box_sy
        sequence_box_sx = 1585 - view_gap * 2
        sequence_box_sy = 1050 - (yard_box_sy + yard_box_py)
        wx.StaticBox(self.base_panel, -1, "Sequence View", pos=(sequence_box_px, sequence_box_py), size=(sequence_box_sx, sequence_box_sy))
        self.make_sequence_view_contents(sequence_box_px, sequence_box_py, sequence_box_sx, sequence_box_sy)
#        
    def make_yard_view_contents(self, px, py, sx, sy):
        self.yard_view = wx.ScrolledWindow(self.base_panel, -1, pos=(px + 10, py + 35), size=(sx - 20, sy - 40), style=wx.BORDER_SIMPLE)
        self.yard_view.SetDoubleBuffered(True)
        self.yard_view_virtualsize_x = 100 * 15
        self.yard_view_virtualsize_y = 100 * 50
        self.yard_view.SetBackgroundColour("WHITE")
        self.yard_view.SetScrollRate(1, 1)        
        self.yard_view.SetScrollbars(100, 100, 13, 9)
        
        self.yard_view.Bind(wx.EVT_PAINT, self.OnViewPaint_yard)
        self.yard_view.Bind(wx.EVT_LEFT_DOWN, self.OnBlockClick)
        
        #after selection block  this is changed
        self.yard_view.selected_block = None

    def make_bay_view_contents(self, px, py, sx, sy):
        font = wx.Font(12, False, wx.NORMAL, wx.NORMAL)
        self.base_panel.SetFont(font)
        p_button = wx.Button(self.base_panel, -1, "Plan", (px + sx - 135, py + sy - 30), (60, 20))
        r_button = wx.Button(self.base_panel, -1, "Reset", (px + sx - 70, py + sy - 30), (60, 20))
        self.Bind(wx.EVT_BUTTON, self.plan_operation, p_button)
        self.Bind(wx.EVT_BUTTON, self.reset_operation, r_button)        
        self.bay_view = wx.ScrolledWindow(self.base_panel, -1, pos=(px + 10, py + 35), size=(sx - 20, sy - 75), style=wx.BORDER_SIMPLE)
        self.bay_view.SetDoubleBuffered(True)
        self.bay_view_virtualsize_x = 100 * 15
        self.bay_view_virtualsize_y = 100 * 50
        self.bay_view.SetBackgroundColour("WHITE")
        self.bay_view.SetScrollRate(1, 1)        
        self.bay_view.SetScrollbars(100, 100, 0, 25)
        self.bay_view.Bind(wx.EVT_PAINT, self.OnViewPaint_bay)
        self.bay_view.selected_bay = None
        
        self.CONTAINER_BRUSH = [wx.Brush(wx.Color(195, 249, 219)), wx.Brush(wx.Color(168, 246, 203)),
                                wx.Brush(wx.Color(134, 242, 183)), wx.Brush(wx.Color(99, 239, 162)),
                                wx.Brush(wx.Color(81, 237, 152)), wx.Brush(wx.Color(65, 235, 142)),
                                wx.Brush(wx.Color(47, 233, 131)), wx.Brush(wx.Color(23, 219, 112)),
                                wx.Brush(wx.Color(21, 201, 102)), wx.Brush(wx.Color(19, 185, 94))]
        self.bay_view.Bind(wx.EVT_LEFT_DOWN, self.OnBayClick)
        
        self.painted_bay_list = []

    def make_sequence_view_contents(self, px, py, sx, sy):
        self.sequence_view = wx.ScrolledWindow(self.base_panel, -1, pos=(px + 10, py + 35), size=(sx - 20, sy - 50), style=wx.BORDER_SIMPLE)
        self.sequence_view.SetDoubleBuffered(True)
        self.sequence_view_virtualsize_x = 100 * 100
        self.sequence_view_virtualsize_y = 100 * 50
        self.sequence_view.SetBackgroundColour("WHITE")
        self.sequence_view.SetScrollRate(1, 1)        
        self.sequence_view.SetScrollbars(100, 100, 100, 0)
        self.sequence_view.Bind(wx.EVT_PAINT, self.OnViewPaint_sequence)
        self.sequence_view.layout_seq = None

    def read_database(self):
        select = "SELECT distinct block_id FROM container;"
        self.cursor.execute(select)
        rows = self.cursor.fetchall()
        block_id_list = [r[0] for r in rows]

        trans_dic = {'A':0, 'B':1, 'C':2, 'D':3}
        self.block_position_dic = dict((block_id, (trans_dic[block_id[0:1]], int(block_id[1:]) - 1)) for block_id in block_id_list)
        
        self.yard = {}
        for block_id in block_id_list:
            select = "SELECT distinct bay FROM container where block_id = '%s';" % (block_id)
            self.cursor.execute(select)
            rows = self.cursor.fetchall()
            bay_id_list = [r[0] for r in rows]
            self.yard[block_id] = dict((bay_id, [None] * 5) for bay_id in bay_id_list)

        for block_id, bay_list in self.yard.items():
            for bay_id, bay_info in bay_list.iteritems():
                select = "SELECT container_id, row, tier, type_of_container FROM container where block_id = '%s' and bay = %s;" % (block_id, bay_id)
                self.cursor.execute(select)
                rows = self.cursor.fetchall()
                bay_info[0] = container_list = rows

                layout = self.make_layout(container_list)
                bay_info[3] = self.mis_overlay_index(layout)

                select = "select p_id from plan where block_id='%s' and bay_id=%s" % (block_id, bay_id)
                if self.cursor.execute(select):
                    p_id = self.cursor.fetchone()[0]

                    select = "select _from, _to from sequence where p_id=%s order by seq_num;" % p_id
                    self.cursor.execute(select)
                    bay_info[1] = sequence = self.cursor.fetchall()
                    assert sequence

                    bay_info[2] = self.make_final_layout(layout, sequence)
                    bay_info[4] = self.mis_overlay_index(bay_info[2])

    def mis_overlay_index(self, layout):
        sum_mis_overlay_index = 0
        for row in layout:
            mis_overlay_index = 0
            for x in range(len(row) - 1):
                if row[x][3] < row[x + 1][3]:
                    overlay_index = len(row) - (x + 1)
                    if overlay_index > mis_overlay_index:
                        mis_overlay_index = overlay_index
            sum_mis_overlay_index += mis_overlay_index
        return sum_mis_overlay_index
    
    def plan_operation(self, _):
        tar_bay = self.bay_view.selected_bay
        tar_block = self.yard_view.selected_block

        if tar_bay and tar_block:
            bay_info = self.yard[tar_block][tar_bay]
            if bay_info[1]:
                wx.MessageBox('Please, first reset plan before you make a new plan')
                return

            layout = self.make_layout(bay_info[0])
#            print layout 
            seq = ylee.start_algoritms(layout)

            if seq:
                print 'hello'
                print seq
                print 'hello'
                bay_info[1] = seq
                bay_info[2] = self.make_final_layout(layout, seq)
                bay_info[4] = self.mis_overlay_index(bay_info[2])
                 
                
                tar_block, tar_bay = self.yard_view.selected_block, self.bay_view.selected_bay
                seq = self.yard[tar_block][tar_bay][1]
                layout = self.make_layout(self.yard[tar_block][tar_bay][0])
                if seq:
                    print seq
                    self.sequence_view.layout_seq = []
                    for i, movement in enumerate(seq):
                        sfrom = movement[0]
                        sto = movement[1]
                        before_position = (sfrom, len(layout[sfrom]) - 1)
                        target_container = layout[sfrom].pop()
                        layout[sto].append(target_container)
                        after_position = (sto, len(layout[sto]) - 1)
                        print layout
                        self.sequence_view.layout_seq.append(([x[:] for x in layout], before_position, after_position))                

                insert = "insert into plan (block_id, bay_id) values ('%s', %s);" % (tar_block, tar_bay)
                self.cursor.execute(insert)
                
                select = "SELECT p_id from plan where block_id = '%s' and bay_id = '%s';" % (tar_block, tar_bay)
                self.cursor.execute(select)
                p_id = self.cursor.fetchone()[0]
                for i, x in enumerate(seq):
                    insert = "insert into sequence (p_id, seq_num, _from, _to) values ('%s' ,'%s','%s', '%s');" % (p_id, i, x[0], x[1])
                    self.cursor.execute(insert)
                
                
                self.yard_view.Refresh()    
                self.bay_view.Refresh()
                self.sequence_view.Refresh()
                
        self.sequence_view.Refresh()
    def reset_operation(self, _):
        tar_bay = self.bay_view.selected_bay
        tar_block = self.yard_view.selected_block
        
        if tar_bay and tar_block:
            select = "select p_id from plan where block_id='%s' and bay_id='%s'" % (tar_block, tar_bay)
            if self.cursor.execute(select):
                p_id = self.cursor.fetchone()[0]
                delete = "delete from sequence where p_id='%d'" % p_id
                self.cursor.execute(delete)
                delete = "delete from plan where block_id='%s' and bay_id='%s'" % (tar_block, tar_bay)
                self.cursor.execute(delete)
                
                bay_info = self.yard[tar_block][tar_bay]
                bay_info[1] = bay_info[2] = bay_info[4] = None
                
                self.bay_view.Refresh()
                self.sequence_view.Refresh()

    def make_layout(self, container_list):
        layout = [[] for _ in range(9)]
        for c in container_list:
            layout[c[1]].append(c)
        for row in layout:
            row.sort(key=lambda c: c[2])
        return layout
    
    def make_final_layout(self, layout, seq):
        final_layout = [x[:] for x in layout]
        for r_from, r_to in seq:
            target_container = final_layout[r_from].pop()
            final_layout[r_to].append(target_container)
        return final_layout
            
    def OnViewPaint_yard(self, _):
        #ready for drawing
        dc = wx.PaintDC(self.yard_view)
        self.yard_view.PrepareDC(dc)    
        #
        yard, block_position_dic = self.yard, self.block_position_dic
        bay_units_size = (yard_UNITS * 8) // 22
        
        for i, row in enumerate(['A', 'B', 'C', 'D']):
            for col in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                block_id = row + '%s' % (col)
                text_position_x = i * (yard_UNITS * 10) + yard_UNITS
                text_position_y = col * (yard_UNITS * 3) + yard_UNITS  
                dc.DrawText(block_id, text_position_x, text_position_y - yard_UNITS * 3.5)
                
                block_position_x = i * (yard_UNITS * 10) + yard_UNITS
                block_position_y = col * (yard_UNITS * 3) + yard_UNITS
                r, g, b = (200, 200, 200)
                brushclr = wx.Colour(r, g, b, 128)
                dc.SetBrush(wx.Brush(brushclr))
                
                
                
                if self.yard_view.selected_block == block_id:
                    # draw thick border if selected
                    old_pen = dc.GetPen()
                    dc.SetPen(wx.Pen(wx.BLUE, 3))
                    dc.DrawRectangle(block_position_x, block_position_y - yard_UNITS * 3, yard_UNITS * 8 + 1, yard_UNITS * 2)
                    dc.SetPen(old_pen)
                else:
                    dc.DrawRectangle(block_position_x, block_position_y - yard_UNITS * 3, yard_UNITS * 8 + 1, yard_UNITS * 2)
                dc.SetFont(wx.Font(7, wx.SWISS, wx.NORMAL, wx.NORMAL))
                for bay_id in range(1, 43):
                    if bay_id % 2 == 0:
                        dc.DrawText('%s' % bay_id, block_position_x + (bay_units_size) // 2 * (bay_id - 1)+5, block_position_y + yard_UNITS * 2-(yard_UNITS * 3))# - yard_UNITS * 3.5)
                dc.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
                        
        for block_id, bay_list in yard.items():
            block_position_x, block_position_y = block_position_dic[block_id]  
            first_bay_position_x = block_position_x * (yard_UNITS * 10) + yard_UNITS
            first_bay_position_y = block_position_y * (yard_UNITS * 3) + yard_UNITS
            
            for bay_id, (_, _, _, misoverlay_index, _) in bay_list.iteritems():
                if misoverlay_index <= 3:
                    r, g, b = (0, 255, 0)
                elif misoverlay_index <= 9:
                    r, g, b = (255, 255, 0)
                else:
                    r, g, b = (255, 0, 0)
                brushclr = wx.Colour(r, g, b, 128)
                dc.SetBrush(wx.Brush(brushclr))
                
                if bay_id % 2 == 0:
                    bay_position_x = first_bay_position_x + (bay_id - 2) * (bay_units_size // 2)
                    bay_position_y = first_bay_position_y
                    dc.DrawRectangle(bay_position_x, bay_position_y, bay_units_size * 2 + 1, yard_UNITS * 2)
                    if self.yard[block_id][bay_id][1]:
#                        brushclr = wx.Colour(30, 30, 30, 128)
#                        dc.SetBrush(wx.Brush(brushclr))
                        point1 = (bay_position_x + bay_units_size * 2, bay_position_y + yard_UNITS * 2 - 1)
                        point2 = (bay_position_x, bay_position_y + yard_UNITS * 2 - 1)
                        point3 = (bay_position_x + bay_units_size * 2, bay_position_y)
                        dc.DrawPolygon([point1, point2, point3])#, brushes=wx.Colour(30, 30, 30, 128))
                else:
                    bay_position_x = first_bay_position_x + (bay_id - 1) * (bay_units_size // 2)
                    bay_position_y = first_bay_position_y
                    dc.DrawRectangle(bay_position_x, bay_position_y, bay_units_size + 1, yard_UNITS * 2)
                    
        dc.EndDrawing()
    
    def OnBlockClick(self, e):
        dx, dy = self.yard_view.GetViewStart()
#        print dx, dy
        x, y = e.GetX() + dx * 100, e.GetY() + dy * 100
#        x, y = e.GetX() + dx * 100, e.GetY() + dy * 100
        bwidth, bheight = yard_UNITS * 8 + 1, yard_UNITS * 2
        block_position_dic = self.block_position_dic
        for block_id, (block_position_x, block_position_y) in block_position_dic.iteritems():
            first_bay_position_x = block_position_x * (yard_UNITS * 10) + yard_UNITS
            first_bay_position_y = block_position_y * (yard_UNITS * 3) + yard_UNITS
            if first_bay_position_x <= x <= first_bay_position_x + bwidth and first_bay_position_y <= y <= first_bay_position_y + bheight:
                self.FillBaysView(block_id)
                self.yard_view.Refresh()
                return
        self.yard_view.Refresh()
    
    def FillBaysView(self, block_id):
        self.yard_view.selected_block = block_id
        self.bay_view.Refresh()
    
    def OnBayClick(self, e):
        dx, dy = self.bay_view.GetViewStart()
        x, y = e.GetX() + dx * 100, e.GetY() + dy * 100
        bwidth, bheight = bay_UNITS * 9, bay_UNITS * 4
        for i, bay_id in enumerate(self.painted_bay_list):
            bay_position_x = bay_UNITS * 2
            bay_position_y = bay_UNITS * 2 + i * (bay_UNITS * 6.5)
            if bay_position_x <= x <= bay_position_x + bwidth and bay_position_y <= y <= bay_position_y + bheight: 
                self.bay_view.selected_bay = bay_id
                #if self.plan_exist:
                #    # make layout sequence and set "self.sequence_view.layout_seq"
                #    pass
                #else:
                
                tar_block, tar_bay = self.yard_view.selected_block, self.bay_view.selected_bay
                seq = self.yard[tar_block][tar_bay][1]
                layout = self.make_layout(self.yard[tar_block][tar_bay][0])
                
                
                
                if seq:
                    print seq
                    self.sequence_view.layout_seq = []
                    for i, movement in enumerate(seq):
                        sfrom = movement[0]
                        sto = movement[1]
                        before_position = (sfrom, len(layout[sfrom]) - 1)
                        target_container = layout[sfrom].pop()
                        layout[sto].append(target_container)
                        after_position = (sto, len(layout[sto]) - 1)
                        print layout
                        self.sequence_view.layout_seq.append(([x[:] for x in layout], before_position, after_position))
                        print self.sequence_view.layout_seq  
        self.bay_view.Refresh()
        self.sequence_view.Refresh()
    
    def FillSeqView(self, bay_id):
        pass

    def OnViewPaint_bay(self, _):
        dc = wx.PaintDC(self.bay_view)
        self.bay_view.PrepareDC(dc)
        dc.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        r, g, b = (224, 238, 255)
        brushclr = wx.Colour(r, g, b, 128)
        dc.SetBrush(wx.Brush(brushclr))
        if self.yard_view.selected_block:            
            tblock = self.yard_view.selected_block         
            bay_list = [int(bay_id) for bay_id in self.yard[tblock].keys()]
            bay_list.sort()
            
            self.painted_bay_list = bay_list     
            for i, bay_no in enumerate(bay_list):
                bay_position_x, bay_position_y = bay_UNITS * 1.5, bay_UNITS * 1.5 + i * (bay_UNITS * 6.5)
                dc.DrawText("Bay %s" % (bay_no), bay_position_x - 20, bay_position_y - 30)
                dc.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL))
                dc.DrawText("Workload : %s" % (self.yard[tblock][bay_no][3]), bay_position_x + bay_UNITS * 7 + 8, bay_position_y - 15)
                dc.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
                self.draw_bay_grid(dc, bay_position_x, bay_position_y)
                self.draw_container_list(dc, self.yard[tblock][bay_no][0], bay_position_x, bay_position_y, bay_UNITS, bay_no)
                
                if self.bay_view.selected_bay == bay_no:
                    old_pen = dc.GetPen()
                    dc.SetPen(wx.Pen(wx.BLUE, 3))
                    dc.DrawLine(bay_position_x - bay_UNITS  , bay_position_y - bay_UNITS * 1.5 + 10, bay_position_x + bay_UNITS * 9.5 - 10, bay_position_y - bay_UNITS * 1.5 + 10)
                    dc.DrawLine(bay_position_x - bay_UNITS  , bay_position_y + bay_UNITS * 4.5 + 5, bay_position_x + bay_UNITS * 9.5 - 10, bay_position_y + bay_UNITS * 4.5 + 5)
                    dc.DrawLine(bay_position_x - bay_UNITS  , bay_position_y - bay_UNITS * 1.5 + 10, bay_position_x - bay_UNITS, bay_position_y + bay_UNITS * 4.5 + 5)
                    dc.DrawLine(bay_position_x + bay_UNITS * 9.5 - 10  , bay_position_y - bay_UNITS * 1.5 + 10, bay_position_x + bay_UNITS * 9.5 - 10, bay_position_y + bay_UNITS * 4.5 + 5)
                    dc.SetPen(old_pen)

                if self.yard[tblock][bay_no][2]:
#                    print tblock, bay_no
                    planed_bay_p_x, planed_bay_p_y = bay_position_x + bay_UNITS * 11, bay_position_y 
                    dc.DrawText("Bay %s" % (bay_no), planed_bay_p_x - 20, planed_bay_p_y - 30)
                    dc.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL))
#                    dc.DrawText("Workload : %s" % (self.yard[tblock][bay_no][4]), planed_bay_p_x + bay_UNITS * 7 + 8, planed_bay_p_y - 15)
                        
                    dc.DrawText("Workload : %s" % (self.yard[tblock][bay_no][4]), planed_bay_p_x + bay_UNITS * 7 + 8, planed_bay_p_y - 15)
                    dc.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
                    self.draw_bay_grid(dc, planed_bay_p_x, planed_bay_p_y)
                    self.draw_containers_by_layout(dc, self.yard[tblock][bay_no][2], planed_bay_p_x, planed_bay_p_y, bay_UNITS, bay_no)    
        dc.EndDrawing()

    def draw_bay_grid(self, dc, bay_position_x, bay_position_y):
        old_pen = dc.GetPen()
        dc.SetPen(wx.LIGHT_GREY_PEN)
        for i in range(5):
            dc.DrawLine(bay_position_x, bay_position_y + i * bay_UNITS, bay_position_x + bay_UNITS * 9, bay_position_y + i * bay_UNITS)
        for i in range(10):
            dc.DrawLine(bay_position_x + i * bay_UNITS, bay_position_y, bay_position_x + i * bay_UNITS, bay_position_y + bay_UNITS * 4)
        for i in range(9):
            dc.DrawText("%s" % (i + 1), bay_position_x + i * bay_UNITS + bay_UNITS // 2 - 2, bay_position_y + bay_UNITS * 4 + 2)
        for i in range(4):    
            dc.DrawText("%s" % (i + 1), bay_position_x - 18, bay_position_y + bay_UNITS * 3.5 - (i * bay_UNITS + 10))
        dc.SetPen(old_pen)

    def draw_container_list(self, dc, container_list, x, y, grid_size, bay_no):
        dc.SetFont(wx.Font(7, wx.SWISS, wx.NORMAL, wx.NORMAL))
        for cid, row, tier, container_type in container_list:
            dc.SetBrush(self.CONTAINER_BRUSH[container_type])
            dc.DrawRectangle(x + grid_size * row, y + grid_size * (3 - tier), grid_size + 1, grid_size + 1)
            c_id1 = cid[:4]
            c_id2 = cid[4:8]
            c_id3 = cid[8:]
            dc.DrawText(c_id1, x + grid_size * row + 6.5, y + grid_size * (3 - tier) + 1)
            dc.DrawText(c_id2, x + grid_size * row + 9.5, y + grid_size * (3 - tier) + 9)
            dc.DrawText(c_id3, x + grid_size * row + 14, y + grid_size * (3 - tier) + 17)
            if bay_no % 2 == 0:
                c_size = '40`'
            else:
                c_size = '20`'
            dc.DrawText(c_size, x + grid_size * row + 3, y + grid_size * (3 - tier) + 24)
        dc.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
    def draw_containers_by_layout(self, dc, layout, x, y, grid_size, bay_no):
        dc.SetFont(wx.Font(7, wx.SWISS, wx.NORMAL, wx.NORMAL)) 
        for row, containers_in_row in enumerate(layout):
            for tier, (cid, _, _, container_type) in enumerate(containers_in_row):
                dc.SetBrush(self.CONTAINER_BRUSH[container_type])
                dc.DrawRectangle(x + grid_size * row, y + grid_size * (3 - tier), grid_size + 1, grid_size + 1)
                c_id1 = cid[:4]
                c_id2 = cid[4:8]
                c_id3 = cid[8:]
                dc.DrawText(c_id1, x + grid_size * row + 6.5, y + grid_size * (3 - tier) + 1)
                dc.DrawText(c_id2, x + grid_size * row + 9.5, y + grid_size * (3 - tier) + 9)
                dc.DrawText(c_id3, x + grid_size * row + 14, y + grid_size * (3 - tier) + 17)
                if bay_no % 2 == 0:
                    c_size = '40`'
                else:
                    c_size = '20`'
                dc.DrawText(c_size, x + grid_size * row + 3, y + grid_size * (3 - tier) + 24)
        dc.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))

    def OnViewPaint_sequence(self, _):
        dc = wx.PaintDC(self.sequence_view)
        self.sequence_view.PrepareDC(dc)        
        penclr = wx.Colour(0, 0, 0)
        dc.SetPen(wx.Pen(penclr))
#        if tar_bay and seq:
#            print layout 
        
        if self.sequence_view.layout_seq:
            print self.sequence_view.layout_seq
            # draw
            for i, (layout, before_position, after_position) in enumerate(self.sequence_view.layout_seq):
#                print i
#                print layout
                sequence_position_x, sequence_position_y = seq_UNITS * 2 + i * seq_UNITS * 12, seq_UNITS * 3 -15
#                print (sequence_position_x, sequence_position_y)
                font = wx.Font(12, False, wx.NORMAL, wx.NORMAL)
                dc.SetFont(font)
                dc.DrawText("Sequence %s" % (i + 1), sequence_position_x - 20, sequence_position_y - 30)
                font = wx.Font(10, False, wx.NORMAL, wx.NORMAL)
                dc.SetFont(font)
                self.draw_containers_sequence(dc, layout, sequence_position_x, sequence_position_y, seq_UNITS)
                for i in range(5):
                    dc.DrawLine(sequence_position_x, sequence_position_y + i * seq_UNITS, sequence_position_x + seq_UNITS * 9, sequence_position_y + i * seq_UNITS)
                    if i != 4:
                        dc.DrawText("%s" % (i + 1), sequence_position_x - seq_UNITS / 2, sequence_position_y + seq_UNITS * 4 - ((i + 1) * seq_UNITS))
                for i in range(10):
                    dc.DrawLine(sequence_position_x + i * seq_UNITS, sequence_position_y, sequence_position_x + i * seq_UNITS, sequence_position_y + seq_UNITS * 4)
                    if i != 9:
                        dc.DrawText("%s" % (i + 1), sequence_position_x + i * seq_UNITS + 8, sequence_position_y + seq_UNITS * 4 + 4)
                before_x, before_y = before_position
                after_x, after_y = after_position
#                old_pen = dc.GetPen()
#                    dc.SetPen(wx.Pen(wx.BLUE, 3))
#                    dc.SetPen(old_pen)
                penclr = wx.Colour(255, 0, 0)
                dc.SetPen(wx.Pen(penclr, 2))
                print (before_x, before_y)
                self.draw_pointer(dc, sequence_position_x , sequence_position_y, seq_UNITS , before_x, before_y)
                penclr = wx.Colour(0, 0, 255)
                dc.SetPen(wx.Pen(penclr, 2))
                self.draw_pointer(dc, sequence_position_x , sequence_position_y , seq_UNITS , after_x, after_y)
                
        dc.EndDrawing()
    def draw_pointer(self, dc, sequence_x, sequence_y, grid_size, x, y):
        dc.DrawLine(sequence_x + grid_size * x - 2, sequence_y + grid_size * (3 - y) - 2, sequence_x + grid_size * x + grid_size + 2, sequence_y + grid_size * (3 - y) - 2)
        dc.DrawLine(sequence_x + grid_size * x - 2, sequence_y + grid_size * (3 - y) - 2, sequence_x + grid_size * x - 2, sequence_y + grid_size * (3 - y) + grid_size + 2)
        dc.DrawLine(sequence_x + grid_size * x - 2, sequence_y + grid_size * (3 - y) + 2 + grid_size, sequence_x + grid_size * x + grid_size + 2, sequence_y + grid_size * (3 - y) + 2 + grid_size)
        dc.DrawLine(sequence_x + grid_size * x + grid_size + 2, sequence_y + grid_size * (3 - y) - 2, sequence_x + grid_size * x + grid_size + 2, sequence_y + grid_size * (3 - y) + grid_size + 2)
        penclr = wx.Colour(0, 0, 0, wx.ALPHA_OPAQUE)
        dc.SetPen(wx.Pen(penclr))
        
    def draw_containers_sequence(self, dc, layout, x, y, grid_size):
#        print (x,y) 
        for row, containers_in_row in enumerate(layout):
            for tier, (cid, _, _, container_type) in enumerate(containers_in_row):
                dc.SetBrush(self.CONTAINER_BRUSH[container_type])
                dc.DrawRectangle(x + grid_size * row, y + grid_size * (3 - tier), grid_size + 1, grid_size + 1)
