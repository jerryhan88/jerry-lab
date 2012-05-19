#-*- coding: cp949 -*-
from __future__ import division
import wx, color_src, datetime, math
orange = color_src.orange
purple = color_src.purple
white = color_src.white
dark_sky = color_src.dark_sky
red = color_src.red
blue = color_src.blue
sky = color_src.sky

class M_frame(wx.Frame):
    def __init__(self, parent, ID, title, pos, size, style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        f_size_x, f_size_y = size
        p = wx.Panel(self, -1)
        p.SetBackgroundColour(white)
        pro_p_px, pro_p_py = (0, 0)
        pro_p_sx, pro_p_sy = (f_size_x * 3 / 5, f_size_y / 2 - 40)
        
        margin = 8
        msg_p_px, msg_p_py = (pro_p_px + pro_p_sx, pro_p_py)
        msg_p_sx, msg_p_sy = (f_size_x - pro_p_sx - margin, pro_p_sy)
        
        proce_p_px, proce_p_py = (pro_p_px, pro_p_py + pro_p_sy)
        proce_p_sx, proce_p_sy = (f_size_x - margin, f_size_y - pro_p_sy)
        
        self.project_display(p, pro_p_px, pro_p_py, pro_p_sx, pro_p_sy)
        self.message_display(p, msg_p_px, msg_p_py, msg_p_sx, msg_p_sy)
        self.process_display(p, proce_p_px, proce_p_py, proce_p_sx, proce_p_sy)
        
    def project_display(self, parent, px, py, p_sx, p_sy):
        self.pro_p = wx.Panel(parent, -1, pos=(px, py), size=(p_sx, p_sy))
        self.pro_p.SetBackgroundColour(white)        
        wx.StaticBox(self.pro_p, -1, "", pos=(5, 0), size=(p_sx - 7, p_sy))
        t_p = self.make_title_p(self.pro_p, 'pic/project_title.png', 7, 10, p_sx - 12, 60)
        t_p.SetBackgroundColour(white)
        btn_p = wx.Panel(self.pro_p, -1, pos=(7, p_sy - 40), size=(p_sx - 9, 40))
        btn_p.SetBackgroundColour(white)
        
        pre_btm_img = wx.Image('pic/project_btm.png', wx.BITMAP_TYPE_PNG)
        sx, sy = btn_p.GetSize()
        w = pre_btm_img.GetWidth()
        h = pre_btm_img.GetHeight()
        xs, ys = sx / w, sy / h
        t_img = wx.BitmapFromImage(pre_btm_img.Scale(w, h * ys * 0.90))
        wx.StaticBitmap(btn_p, -1, t_img)
        
        
        add_btn = self.make_pro_btn(btn_p, 'pic/+.png', 'pic/+_.png', p_sx - 85, 2)
        remove_btn = self.make_pro_btn(btn_p, 'pic/-.png', 'pic/-_.png', p_sx - 50, 2)
        
        add_btn.Bind(wx.EVT_BUTTON, self.project_add)
        remove_btn.Bind(wx.EVT_BUTTON, self.project_remove)
        
        self.new_pro_added = False
        
        px, py = t_p.GetPosition()
        t_sx, t_sy = t_p.GetSize()
        _, b_sy = btn_p.GetSize()
        
        self.pjv_p = wx.ScrolledWindow(self.pro_p, -1, pos=(px, py + t_sy + 2), size=(t_sx, p_sy - (t_sy + b_sy + 15)), style=wx.SUNKEN_BORDER)
        self.pjv_p.SetBackgroundColour(white)
        self.pjv_p.SetDoubleBuffered(True)
        _, self.pjv_py = self.pjv_p.GetPosition()
        _, self.pjv_sy = self.pjv_p.GetSize()
        self.pjv_p.SetScrollRate(1, 1)        
        self.pjv_p.SetScrollbars(100, self.pjv_sy, 13, 1)
        
        inte_imgs = ['interior_pic1', 'interior_pic2']
        self.inte_lo_sc = ['전남, 전체', '부산, 실내', 'Freight Forwarder']
        self.dates = ['2012.05.12', '2012.06.08', '2012.06.08']
        
        self.bit_imgs = []
        diminish_size = 1
        for i, name in enumerate(inte_imgs):
            pre_img = wx.Image('pic/' + name + '.png', wx.BITMAP_TYPE_PNG)
            w = pre_img.GetWidth()
            h = pre_img.GetHeight()
            img = pre_img.Scale(w * diminish_size, h * diminish_size).ConvertToBitmap()
            self.bit_imgs.append((img, img.GetWidth(), img.GetHeight())) 
            
        self.pjv_p.Bind(wx.EVT_PAINT, self.drawProject)
        self.pjv_p.Bind(wx.EVT_LEFT_DOWN, self.OnProjectClick)
#        self.select_item = [1, 0, 0]
        self.select_item = [0, 0, 1]
#        self.select_item = [0, 0]
        
    def OnProjectClick(self, e):
        x, y = e.GetX(), e.GetY()
        width = self.bit_imgs[0][1]
        btw = 30
        if y < self.pjv_py + self.pjv_sy:
            for i in xrange(len(self.select_item)):
                self.select_item[i] = 0
                if (btw + width) * i <= x <= (btw + width) * (i + 1):
                    self.select_item[i] = 1
            self.pjv_p.Refresh()
            self.pcv_p.Refresh()

    def drawProject(self, _):
        dc = wx.PaintDC(self.pjv_p)
        self.pjv_p.PrepareDC(dc)
        st_sy = self.bit_imgs[0][0].GetHeight()
        btw = 30
        
        for i, b in enumerate(self.bit_imgs):    
            w = b[1]
            h = b[2]
            px = btw + i * (w + btw)
            py = btw + (st_sy - h) / 2
            dc.DrawBitmap(self.bit_imgs[i][0], px , py)
            t_btw = 15
            c_px = px + 30
            if i != 2:
                dc.DrawText(self.inte_lo_sc[i], c_px, btw + st_sy + t_btw)
            else:
                dc.DrawText(self.inte_lo_sc[i], c_px - 20, btw + st_sy + t_btw)
            dc.DrawText(self.dates[i], c_px, btw + st_sy + t_btw * 2.5)
            
            if self.select_item[i] == 1:
                py = btw + (st_sy - self.bit_imgs[0][2]) / 2
                old_pen = dc.GetPen()
                dc.SetPen(wx.Pen(red, 2))
                margin = 5
                p_h = 50
                p1 = (px - margin - 1, py - margin)
                p2 = (px + w + margin, py - margin)
                p3 = (px - margin - 1, py + st_sy + margin + p_h)
                p4 = (px + w + margin, py + st_sy + margin + p_h)
                dc.DrawLine(p1[0], p1[1], p2[0], p2[1])
                dc.DrawLine(p1[0], p1[1], p3[0], p3[1])
                dc.DrawLine(p2[0], p2[1], p4[0], p4[1])
                dc.DrawLine(p3[0], p3[1], p4[0], p4[1])
                dc.SetPen(old_pen)
            
        dc.EndDrawing()
        
    def make_pro_btn(self, parent, img, selected_img, px, py):
        pre_img = wx.Image(img, wx.BITMAP_TYPE_PNG)
        w = pre_img.GetWidth()
        h = pre_img.GetHeight()
        img = pre_img.Scale(w, h).ConvertToBitmap()
        btn = wx.BitmapButton(parent, id= -1, bitmap=img, pos=(px, py), size=(30, 30), style=wx.NO_BORDER)
        
        s_pre_img = wx.Image(selected_img, wx.BITMAP_TYPE_PNG)
        w = s_pre_img.GetWidth()
        h = s_pre_img.GetHeight()
        s_img = s_pre_img.Scale(w / 4, h / 4).ConvertToBitmap()
        btn.SetBitmapSelected(s_img)
        
        return btn
    
    def project_add(self, evt):
        project_v = Project(self)
        project_v.Show(True)
    
    def project_remove(self, evt):
        pass
    
    def make_title_p(self, parent, img, px, py, sx, sy):
        t_p = wx.Panel(parent, -1, pos=(px, py), size=(sx, sy))
        pre_img = wx.Image(img, wx.BITMAP_TYPE_PNG)
#        sx, sy = t_p.GetSize()
#        w = pre_img.GetWidth()
#        h = pre_img.GetHeight()
#        xs, ys = sx / w, sy / h
        t_img = wx.BitmapFromImage(pre_img)
        wx.StaticBitmap(t_p, -1, t_img)
        return t_p
        
    def message_display(self, parent, px, py, p_sx, p_sy):
        msg_p = wx.Panel(parent, -1, pos=(px, py), size=(p_sx, p_sy))
        msg_p.SetBackgroundColour(white)
        wx.StaticBox(msg_p, -1, "", pos=(2, 0), size=(p_sx - 15, p_sy))
        t_p = self.make_title_p(msg_p, 'pic/msg_title.png', 7, 10, p_sx - 24, 60)
        px, py = t_p.GetPosition()
        sx, sy = t_p.GetSize()
        self.notice_view = wx.TextCtrl(msg_p, -1, "", pos=(px + 2, py + sy + 2),
                           size=(sx, p_sy - sy - 50), style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
        self.notice_view.SetEditable(False)
        self.notice_view.SetBackgroundColour(wx.Colour(248, 238, 211))
        self.notice_view.write('---------------------------------------------------------------------------------------');
        self.notice_view.write('2011-11-27  19:6:53                                                             ');
        self.notice_view.write('---------------------------------------------------------------------------------------');
        px, py = self.notice_view.GetPosition()
        sx, sy = self.notice_view.GetSize() 
        
        self.input_msg = wx.TextCtrl(msg_p, -1, '프로젝트 종료', pos=(px, py + sy), size=(sx - 85, 35))
        self.input_msg.SetFont(wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT))
        px, py = self.input_msg.GetPosition()
        sx, sy = self.input_msg.GetSize()
#        s_btn = wx.Button(msg_p, -1, "Send", pos=(px + sx, py), size=(50, 35))
        img = wx.Image('pic/sendBtn.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        s_btn = wx.BitmapButton(msg_p, id= -1, bitmap=img, pos=(px + sx, py), style=wx.NO_BORDER)
        
        s_btn.SetFont(wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.Bind(wx.EVT_BUTTON, self.add_log, s_btn)
    
    def add_log(self, evt):
        ct = datetime.datetime.now()
        self.notice_view.write('굈---------------------------------------------------------------------------------------');
        self.notice_view.write('굈 ' + str(ct.date()) + '  ' + str(ct.time().hour) + ':' + str(ct.time().minute) + ':' + str(ct.time().second));
        self.notice_view.write('굈 [HeadFirst]  ' + self.input_msg.GetValue())
        self.notice_view.write('굈---------------------------------------------------------------------------------------');
        self.input_msg.Clear()
        
    def process_display(self, parent, px, py, p_sx, p_sy):
        proce_p = wx.Panel(parent, -1, pos=(px, py), size=(p_sx, p_sy))
        proce_p.SetBackgroundColour(white)
        wx.StaticBox(proce_p, -1, "", pos=(5, 0), size=(p_sx - 18, p_sy - 40))
        t_p = self.make_title_p(proce_p, 'pic/process_title.png', 7, 10, p_sx - 24, 60)
        t_p.SetBackgroundColour(white)
        
        px, py = t_p.GetPosition()
        t_p_sx, sy = t_p.GetSize()
        
        btns_p = self.make_btns(proce_p, px, py + sy, 130, p_sy - sy - 54)
        px, py = btns_p.GetPosition()
        sx, sy = btns_p.GetSize()
        
        init_btn = self.ac_btns[0] 
        self.Bind(wx.EVT_BUTTON, self.pc_init, init_btn)
        
        recom_btn = self.ac_btns[1]
        self.Bind(wx.EVT_BUTTON, self.recommand, recom_btn)
        self.isReco = False
        
        circleBtn = self.mo_btns[0] 
        recBtn = self.mo_btns[1] 
        arrowBtn = self.mo_btns[2] 
        moneyBtn = self.mo_btns[3]
        
        self.Bind(wx.EVT_BUTTON, self.circleBtn, circleBtn)
        self.Bind(wx.EVT_BUTTON, self.recBtn, recBtn)
        self.Bind(wx.EVT_BUTTON, self.moneyBtn, moneyBtn)
        self.Bind(wx.EVT_BUTTON, self.arrowBtn, arrowBtn)
        
        self.prev_process = None
        self.next_process = None
        self.edges = []
        
        self.pcv_p = wx.ScrolledWindow(proce_p, -1, pos=(px + sx, py + 7), size=(t_p_sx - sx, sy - 7), style=wx.SUNKEN_BORDER)
        self.pcv_p.SetDoubleBuffered(True)
        self.pcv_sx, self.pcv_sy = self.pcv_p.GetSize()
        self.pcv_p.SetScrollbars(100, self.pcv_sy, 13, 1)
        self.pcv_p.SetBackgroundColour(white)
        
        self.pcv_p.Bind(wx.EVT_PAINT, self.drawProcess)
        self.pcv_p.Bind(wx.EVT_LEFT_DOWN, self.OnTaskClick)
        
        pre_pb_img = wx.Image('pic/process_back.png', wx.BITMAP_TYPE_PNG)
        w = pre_pb_img.GetWidth()
        h = pre_pb_img.GetHeight()
        self.pb_img = wx.BitmapFromImage(pre_pb_img.Scale(w * 0.6, h * 0.833))
        
        self.rec_img = wx.Image('pic/recBtn.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.circle_img = wx.Image('pic/circleBtn.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.money_img = wx.Image('pic/moneyBtn.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        
        self.h_center_py = self.pcv_sy / 2 - 35
        self.d_start_px = 50
        self.p_btw = 80
        
        self.inte1_pos = []
        self.inte1_pos.append((self.d_start_px, self.h_center_py))
        
        self.inte1_pos.append((self.inte1_pos[-1][0] + self.p_btw, self.inte1_pos[0][1]))
        
        self.inte1_pos.append((self.inte1_pos[-1][0] + self.p_btw, self.inte1_pos[0][1] - 50))
        self.inte1_pos.append((self.inte1_pos[-1][0], self.inte1_pos[0][1] + 50))
        
        self.inte1_pos.append((self.inte1_pos[-1][0] + self.p_btw, self.inte1_pos[0][1]))
        
        self.inte1_pos.append((self.inte1_pos[-1][0] + self.p_btw, self.inte1_pos[0][1] - 80))
        self.inte1_pos.append((self.inte1_pos[-1][0], self.inte1_pos[0][1]))
        self.inte1_pos.append((self.inte1_pos[-1][0], self.inte1_pos[0][1] + 80))
        
        self.inte1_pos.append((self.inte1_pos[-1][0] + self.p_btw, self.inte1_pos[0][1]))
        
        self.inte1_pos.append((self.inte1_pos[-1][0] + self.p_btw, self.inte1_pos[0][1] - 50))
        self.inte1_pos.append((self.inte1_pos[-1][0], self.inte1_pos[0][1] + 50))
        
        self.inte1_pos.append((self.inte1_pos[-1][0] + self.p_btw, self.inte1_pos[0][1]))
        
        self.inte1_pos.append((self.inte1_pos[-1][0] + self.p_btw, self.inte1_pos[0][1]))
        
        self.inte1_pos.append((self.inte1_pos[-1][0] + self.p_btw, self.inte1_pos[0][1]))
        
        inte1_es = [(0, 1),
              (1, 2), (1, 3),
              (2, 4), (3, 4),
              (4, 5), (4, 6), (4, 7),
              (5, 8), (6, 8), (7, 8),
              (8, 9), (8, 10),
              (9, 11), (10, 11),
              (11, 12),
              (12, 13),
              ]
        self.inte1_pos_es = self.make_edges(inte1_es, self.inte1_pos)
        
        self.inte1_names = ['철거', '목공', '철공', '샤시', '타일', '페인트', '필름', '도배', '주방', '욕실', '바닥' ]
        self.inte1_fixed = [1, 2, 6, 10]
        self.inte1_reco = [3, 4, 5, 7, 8, 9, 11]
        self.chassis_selected = False
        
        self.inte2_pos = []
        
        self.inte2_pos.append((self.d_start_px, self.h_center_py))
        self.inte2_pos.append((self.inte2_pos[-1][0] + self.p_btw, self.inte2_pos[0][1]))
        self.inte2_pos.append((self.inte2_pos[-1][0] + self.p_btw, self.inte2_pos[0][1] - 50))
        self.inte2_pos.append((self.inte2_pos[-1][0], self.inte2_pos[0][1] + 50))
        
        self.inte2_pos.append((self.inte2_pos[-1][0] + self.p_btw, self.inte2_pos[0][1] - 50 - 30))
        self.inte2_pos.append((self.inte2_pos[-1][0], self.inte2_pos[0][1] - 50 + 30))
        self.inte2_pos.append((self.inte2_pos[-1][0], self.inte2_pos[0][1] + 50))
        
        self.inte2_pos.append((self.inte2_pos[-1][0] + self.p_btw, self.inte2_pos[0][1]))
        self.inte2_pos.append((self.inte2_pos[-1][0] + self.p_btw, self.inte2_pos[0][1]))
        self.inte2_pos.append((self.inte2_pos[-1][0] + self.p_btw, self.inte2_pos[0][1]))
        self.inte2_pos.append((self.inte2_pos[-1][0] + self.p_btw, self.inte2_pos[0][1]))
        
        inte2_es = [(0, 1),
              (1, 2), (1, 3),
              (2, 4), (2, 5),
              (3, 6),
              (4, 7), (5, 7), (6, 7),
              (7, 8),
              (8, 9),
              (9, 10)]
        
        self.inte2_pos_es = self.make_edges(inte2_es, self.inte2_pos)
        
        self.tasks_in_pro = []
        self.isInit = False
    def make_edges(self, es, pos):
        edges = []
        for p, n in es:
            edges.append((pos[p][0] + 50, pos[p][1] + 25, pos[n][0], pos[n][1] + 25))
        return edges
        
    def drawProcess(self, _):
        dc = wx.PaintDC(self.pcv_p)
        self.pcv_p.PrepareDC(dc)
        dc.DrawBitmap(self.pb_img, 640, 0)
        if self.select_item[1] == 1:
            self.drawInte2(dc)
        elif self.select_item[0] == 1:
            self.drawInte1(dc)
        else:
            self.drawNewProcess(dc)
        dc.EndDrawing()
        
    def drawNewProcess(self, dc):
        for p in self.tasks_in_pro:
            if p.type == 0:
                dc.DrawBitmap(self.circle_img, p.px, p.py)
            elif p.type == 1:
                dc.DrawBitmap(self.rec_img, p.px, p.py)
            elif p.type == 2:
                dc.DrawBitmap(self.money_img, p.px, p.py)
                
        if self.prev_process:
            old_pen = dc.GetPen()
            dc.SetPen(wx.Pen(wx.BLUE, 3))
            p1 = (self.prev_process.px - 3, self.prev_process.py - 3)
            p2 = (self.prev_process.px - 3 + 56, self.prev_process.py - 3)
            p3 = (self.prev_process.px - 3, self.prev_process.py - 3 + 56)
            p4 = (self.prev_process.px - 3 + 56, self.prev_process.py - 3 + 56)
            dc.DrawLine(p1[0], p1[1], p2[0], p2[1])
            dc.DrawLine(p1[0], p1[1], p3[0], p3[1])
            dc.DrawLine(p2[0], p2[1], p4[0], p4[1])
            dc.DrawLine(p3[0], p3[1], p4[0], p4[1])
            dc.SetPen(old_pen)
            
        if self.next_process:
            old_pen = dc.GetPen()
            dc.SetPen(wx.Pen(wx.RED, 3))
            p1 = (self.next_process.px - 3, self.next_process.py - 3)
            p2 = (self.next_process.px - 3 + 56, self.next_process.py - 3)
            p3 = (self.next_process.px - 3, self.next_process.py - 3 + 56)
            p4 = (self.next_process.px - 3 + 56, self.next_process.py - 3 + 56)
            dc.DrawLine(p1[0], p1[1], p2[0], p2[1])
            dc.DrawLine(p1[0], p1[1], p3[0], p3[1])
            dc.DrawLine(p2[0], p2[1], p4[0], p4[1])
            dc.DrawLine(p3[0], p3[1], p4[0], p4[1])
            dc.SetPen(old_pen)
            
        for e in self.edges:
                sx, sy, ex, ey = e.sx, e.sy, e.ex, e.ey
                ax = ex - sx;
                ay = ey - sy;
                la = math.sqrt(ax * ax + ay * ay);
                ux = ax / la;
                uy = ay / la;
                px = -uy;
                py = ux;
                dc.DrawLine(sx, sy, ex, ey)
                dc.DrawLine(ex, ey, ex - int((ux * 5)) + int(px * 3), ey
                        - int(uy * 5) + int(py * 3));
                dc.DrawLine(ex, ey, ex - int(ux * 5) - int(px * 3), ey
                        - int(uy * 5) - int(py * 3));
    
    def drawInte1(self, dc):
        if not self.isInit:
            dc.DrawBitmap(self.circle_img, self.inte1_pos[0][0], self.inte1_pos[0][1])
            for x in xrange(1, 12):
                dc.DrawBitmap(self.rec_img, self.inte1_pos[x][0], self.inte1_pos[x][1])
                if x == 6:
                    px = self.inte1_pos[x][0]
                else:
                    px = self.inte1_pos[x][0] + 8
                dc.DrawText(self.inte1_names[x - 1], px, self.inte1_pos[x][1] + 16)
            dc.DrawBitmap(self.money_img, self.inte1_pos[-2][0], self.inte1_pos[-2][1])
            dc.DrawBitmap(self.circle_img, self.inte1_pos[-1][0], self.inte1_pos[-1][1])
            self.drawEdges(dc, self.inte1_pos_es, -1)
            
            old_pen = dc.GetPen()
            old_brush = dc.GetBrush()
            old_t_clr = dc.GetTextForeground() 
            dc.SetPen(wx.Pen(red, 1))
            dc.SetBrush(wx.Brush(red))
            dc.SetTextForeground(red)
            for x in self.inte1_fixed:
                px = self.inte1_pos[x][0]
                py = self.inte1_pos[x][1]
                dc.DrawText('Fixed', px - 7, py - 7)
                dc.DrawCircle(px + 47, py + 47, 5)
            dc.SetBrush(old_brush)    
            dc.SetPen(old_pen)
            dc.SetTextForeground(old_t_clr)
            
            if self.chassis_selected:
                old_t_clr = dc.GetTextForeground()
                dc.SetTextForeground(red)
                px = self.inte1_pos[4][0]
                py = self.inte1_pos[4][1]
                dc.DrawText('Fixed', px - 7, py - 7)
                dc.SetTextForeground(old_t_clr)
                
            if self.isReco:
                old_t_clr = dc.GetTextForeground()
                dc.SetTextForeground(blue)
                for x in self.inte1_reco:
                    px = self.inte1_pos[x][0]
                    py = self.inte1_pos[x][1]
                    dc.DrawText('Reco', px - 7, py - 7)
                dc.SetTextForeground(old_t_clr)
                dc.SetFont(wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT))
                dc.DrawText('Lead Time : 24  |  Cost : 80,000,000원', 530, 255)
        
    def drawInte2(self, dc):
        dc.DrawBitmap(self.circle_img, self.inte2_pos[0][0], self.inte2_pos[0][1])
        for x in xrange(1, 9):
            dc.DrawBitmap(self.rec_img, self.inte2_pos[x][0], self.inte2_pos[x][1])
        dc.DrawBitmap(self.money_img, self.inte2_pos[9][0], self.inte2_pos[9][1])
        dc.DrawBitmap(self.circle_img, self.inte2_pos[10][0], self.inte2_pos[10][1])
        self.drawEdges(dc, self.inte2_pos_es, 6)

    def drawEdges(self, dc, es_pos, state):
        for i, e in enumerate(es_pos):
            old_pen = dc.GetPen()
            if i > state:
                dc.SetPen(wx.Pen(red, 1))
            else:
                dc.SetPen(wx.Pen(blue, 1))
            
            sx, sy, ex, ey = e[0], e[1], e[2], e[3]
            ax = ex - sx;
            ay = ey - sy;
            la = math.sqrt(ax * ax + ay * ay);
            ux = ax / la;
            uy = ay / la;
            px = -uy;
            py = ux;
            dc.DrawLine(sx, sy, ex, ey)
            dc.DrawLine(ex, ey, ex - int((ux * 5)) + int(px * 3), ey - int(uy * 5) + int(py * 3));
            dc.DrawLine(ex, ey, ex - int(ux * 5) - int(px * 3), ey - int(uy * 5) - int(py * 3));
            dc.SetPen(old_pen)

    def OnTaskClick(self, e):
        if self.select_item[0] == 1 :
            participant_v = Participant(self)
            participant_v.Show(True)
            
        dx, dy = self.pcv_p.GetViewStart()
        x, y = e.GetX() + dx * 100, e.GetY() + dy * 100
        for i, p in enumerate(self.tasks_in_pro):
            if p.px <= x <= p.px + self.p_btw and p.py <= y <= p.py + 50:
                if not self.prev_process:
                    self.prev_process = self.tasks_in_pro[i]
                else:
                    self.next_process = self.tasks_in_pro[i]
        self.pcv_p.Refresh()
        
        
    def make_btns(self, parent, px, py, sx, sy):
        btns_p = wx.Panel(parent, -1, pos=(px, py), size=(sx, sy))
        sx, sy = btns_p.GetSize()
        wx.StaticBox(btns_p, -1, "", pos=(5, 0), size=(sx - 10, sy - 44))
        btw = 10
        modeling_btns = ['circleBtn', 'recBtn' , 'arrowBtn', 'moneyBtn']
        self.mo_btns = []
        for i, name in enumerate(modeling_btns):
            img = wx.Image('pic/' + name + '.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
            w = img.GetWidth()
            h = img.GetHeight()
            
            btn = wx.BitmapButton(btns_p, id=i, bitmap=img, pos=(btw + (i % 2) * (w + btw), btw + (i // 2) * (h + btw) + 2), style=wx.NO_BORDER)
            selected_bitmap = wx.Image('pic/selected_' + name + '.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
            btn.SetBitmapSelected(selected_bitmap) 
            self.mo_btns.append(btn)
        
        px, py = self.mo_btns[2].GetPosition()
        sx, sy = self.mo_btns[2].GetSize()
        action_btns = ['Initialize', 'Recommend', 'Confirm']
        self.ac_btns = []
        for i, name in enumerate(action_btns):
#            a_img = wx.Image('pic/' + name + '.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
#            a_btn = wx.BitmapButton(btns_p, id=i, bitmap=a_img, pos=(px, btw + py + sy + i * 45), style=wx.NO_BORDER)
            btn = wx.Button(btns_p, -1, name, pos=(px, btw + py + sy + i * 45), size=(110, 35))
            btn.SetFont(wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT))
            self.ac_btns.append(btn)
        px, py = self.ac_btns[-1].GetPosition()
        sx, sy = self.ac_btns[-1].GetSize()
         
        pre_logo_img = wx.Image('pic/PNU_logo.png', wx.BITMAP_TYPE_PNG)
        w = pre_logo_img.GetWidth()
        h = pre_logo_img.GetHeight()
        logo_img = wx.BitmapFromImage(pre_logo_img)
        wx.StaticBitmap(btns_p, -1, logo_img, pos=(px, py + sy + btw + 7), size=(w, h))
        return btns_p
    
    def pc_init(self, _):
        self.isReco = False
        self.isInit = True
        self.pcv_p.Refresh()
    
    def recommand(self, _):
        recom_graph = Graph(self)
        recom_graph.Show(True)

    def circleBtn(self, _):
        if not self.tasks_in_pro:
            px, py = (self.d_start_px, self.h_center_py)
        else:
            last_process = self.tasks_in_pro[-1]
            px, py = (last_process.px + self.p_btw, last_process.py)
        p = Process(0, px, py)
        self.tasks_in_pro.append(p)
        self.pcv_p.Refresh()
        
    def recBtn(self, evt):
        last_process = self.tasks_in_pro[-1]
        px, py = (last_process.px + self.p_btw, last_process.py)
        p = Process(1, px, py)
        self.tasks_in_pro.append(p)
        self.pcv_p.Refresh()
    
    def moneyBtn(self, evt):
        last_process = self.tasks_in_pro[-1]
        px, py = (last_process.px + self.p_btw, last_process.py)
        p = Process(2, px, py)
        self.tasks_in_pro.append(p)
        self.pcv_p.Refresh()
    
    def arrowBtn(self, evt):
        if self.prev_process.next:
            self.next_process.py = self.tasks_in_pro[-2].py + 50
            self.next_process.px = self.tasks_in_pro[-2].px
            self.tasks_in_pro[-2].py -= 50
            self.edges.pop()
            sx, sy = self.tasks_in_pro[-3].px + 50, self.tasks_in_pro[-3].py + 25  
            ex, ey = self.tasks_in_pro[-2].px, self.tasks_in_pro[-2].py + 25 
            e = Edge(sx, sy, ex, ey, self.prev_process, self.next_process)
            self.edges.append(e)
        sx, sy = self.prev_process.px + 50, self.prev_process.py + 25  
        ex, ey = self.next_process.px, self.next_process.py + 25 
        e = Edge(sx, sy, ex, ey, self.prev_process, self.next_process)
        self.edges.append(e)
        self.prev_process = None
        self.next_process = None
        self.pcv_p.Refresh()
        
class Participant(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, 'Find Participant', pos=(120, 100) , size=(360, 680))
        self.r_box = wx.StaticBox(self, -1, "", pos=(7, 0), size=(341, 640))
        px, py = self.r_box.GetPosition()
        sx, _ = self.r_box.GetSize()
        sp_p = wx.Panel(self, -1, pos=(px + 2, py + 11), size=(sx - 7, 60))
        sx, sy = sp_p.GetSize()
        btw = 2
        sp_sx = (sx - btw) / 2 
        s_p = wx.Panel(sp_p, -1, pos=(0, 0), size=(sp_sx, sy))
        s_p.SetBackgroundColour(blue)
        px, py = s_p.GetPosition()
        sx, _ = s_p.GetSize()
        p_p = wx.Panel(sp_p, -1, pos=(px + sx + btw, py), size=(sp_sx, sy))
        p_p.SetBackgroundColour(purple)
        
        px, py = sp_p.GetPosition()
        sx, sy = sp_p.GetSize()
        f_p = wx.Panel(self, -1, pos=(px, py + sy + btw), size=(sx, 45))
        f_p.SetBackgroundColour(sky)
        f_par = wx.TextCtrl(f_p, -1, '샤시', pos=(25, 6), size=(sx - 100, 34))
        f_par.SetFont(wx.Font(17, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        
        px, py = f_par.GetPosition()
        sx, sy = f_par.GetSize()
        f_img = wx.Image('pic/find.png', wx.BITMAP_TYPE_PNG)
        f_btn = wx.BitmapButton(f_p, -1, bitmap=wx.BitmapFromImage(f_img), pos=(px + sx + btw, py - 5))
        
        px, py = f_p.GetPosition()
        sx, sy = f_p.GetSize()
        
        self.parti_v = wx.ScrolledWindow(self, -1, pos=(px, py + sy), size=(sx, 480))
        self.parti_v.SetDoubleBuffered(True)
        self.parti_v.SetBackgroundColour(sky)
        self.parti_v.SetScrollRate(1, 1)        
        self.parti_v.SetScrollbars(sx, 100, 1, 13)
        
        self.parti_v.Bind(wx.EVT_PAINT, self.drawParticipant)
        self.parti_v.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
        
        parti_name = ['chassis1', 'chassis2', 'chassis3', 'chassis4']
        self.parti_imgs = []
        sx, _ = self.parti_v.GetSize()
        for ad in parti_name:
            img = wx.Image('pic/' + ad + '.png', wx.BITMAP_TYPE_PNG)
            w = img.GetWidth()
            h = img.GetHeight()
            diminish_size = sx / w
            self.parti_imgs.append(img.Scale(w * diminish_size, h * diminish_size).ConvertToBitmap())
        
        px, py = self.parti_v.GetPosition()
        sx, sy = self.parti_v.GetSize()
        partner_select_btn = wx.Button(self, -1, "Select", pos=(px + 250, py + sy + btw), size=(70, 35))
        partner_select_btn.SetFont(wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        
    def drawParticipant(self, _):
        dc = wx.PaintDC(self.parti_v)
        self.parti_v.PrepareDC(dc)
        
        h = self.parti_imgs[0].GetHeight()
        margin = 10
        for i, img in enumerate(self.parti_imgs):
            dc.DrawBitmap(img, 0, (h + margin) * i)
    
    def OnClick(self, e):
#        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        btw = 2
        self.SetSize((900, 680))
        px, py = self.r_box.GetPosition()
        sx, _ = self.r_box.GetSize()
        self.info_task_box = wx.StaticBox(self, -1, "", pos=(px + sx + 5, py), size=(535, 280))
        
        px, py = self.info_task_box.GetPosition()
        sx, _ = self.info_task_box.GetSize()
        ia_p = wx.Panel(self, -1, pos=(px + 2, py + 11), size=(sx - 7, 60))
        
        sx, sy = ia_p.GetSize()
        sp_sx = (sx - btw) / 2 
        i_p = wx.Panel(ia_p, -1, pos=(0, 0), size=(sp_sx, sy))
        i_p.SetBackgroundColour(blue)
        px, py = i_p.GetPosition()
        sx, _ = i_p.GetSize()
        t_p = wx.Panel(ia_p, -1, pos=(px + sx + btw, py), size=(sp_sx, sy))
        t_p.SetBackgroundColour(purple)
        
        
        px, py = ia_p.GetPosition()
        sx, sy = ia_p.GetSize()
        
        self.info_task_viewer_p = wx.Panel(self, -1, pos=(px, py + sy + btw), size=(sx, 200))
        self.info_task_viewer_p.SetBackgroundColour(white)
        partner_img = wx.Image('pic/partner.png', wx.BITMAP_TYPE_PNG)
        w = partner_img.GetWidth()
        h = partner_img.GetHeight()
        wx.StaticBitmap(self.info_task_viewer_p, -1, wx.BitmapFromImage(partner_img), pos=(50, 25), size=(w, h))
        self.info_task_viewer_p.SetFont(wx.Font(17, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        wx.StaticText(self.info_task_viewer_p, -1, 'Dung Liu Express Co.', pos=(190, 20))
        wx.StaticText(self.info_task_viewer_p, -1, 'Name : Dung Liu', pos=(190, 70))
        wx.StaticText(self.info_task_viewer_p, -1, 'Contack : 011-244-1547', pos=(190, 120))
        
        
        
        
        px, py = self.info_task_box.GetPosition()
        sx, sy = self.info_task_box.GetSize()
        
        self.detail_info_box = wx.StaticBox(self, -1, "", pos=(px, py + sy - 1), size=(sx, 362))
        px, py = self.detail_info_box.GetPosition()
        sx, _ = self.detail_info_box.GetSize()
        d_p = wx.Panel(self, -1, pos=(px + 2, py + 11), size=(sx - 7, 60))
        d_p.SetBackgroundColour(blue)
        
        px, py = d_p.GetPosition()
        sx, sy = d_p.GetSize()
        
        self.detail_process_viewer = wx.ScrolledWindow(self, -1, pos=(px, py + sy + btw), size=(sx, 280))
        self.detail_process_viewer.SetDoubleBuffered(True)
        self.detail_process_viewer.SetBackgroundColour("white")
        self.detail_process_viewer.SetScrollbars(sx, 10, 1, 130)
        btw_line_size = 30
        last_py = 15
        t_px = 40
        t_font = wx.Font(17, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        sub_px = 60
        self.detail_process_viewer.SetFont(wx.Font(12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        sr = wx.StaticText(self.detail_process_viewer, -1, '1.Scale/Reputation', pos=(t_px, last_py))
        sr.SetFont(t_font)
        last_py += btw_line_size 
        wx.StaticBitmap(self.detail_process_viewer, -1, wx.BitmapFromImage(wx.Image('pic/factory.png', wx.BITMAP_TYPE_PNG).Scale(200 * 1.5, 150 * 1.5)),
                     pos=(sub_px, last_py), size=(200 * 1.5, 150 * 1.5))
        self.Refresh()
#        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
#        self.Parent.chassis_selected = True
#        self.Parent.inte1_reco.pop(1)
#        self.Parent.pcv_p.Refresh()
        pass
        
#        self.Destroy()    
        
class Graph(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, 'Recommend', pos=(120, 100) , size=(600, 400))
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_PAINT, self.drawGraph)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
        
        _, sy = self.GetSize()
        
        self.ori_px = 50 
        self.ori_py = sy - 90
        
    def OnClick(self, e):
        self.Parent.isReco = True
        self.Parent.pcv_p.Refresh()
        self.Destroy()
        
    def drawGraph(self, _):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        x_axi_px, x_axi_py = self.ori_px + 480, self.ori_py
        arr_es = 10
        dc.DrawLine(self.ori_px, self.ori_py, x_axi_px, x_axi_py)
        dc.DrawLine(x_axi_px, x_axi_py, x_axi_px - arr_es, x_axi_py + arr_es / 2)
        dc.DrawLine(x_axi_px, x_axi_py, x_axi_px - arr_es, x_axi_py - arr_es / 2)
        
        y_axi_px, y_axi_py = self.ori_px, self.ori_py - 260
        dc.DrawLine(self.ori_px, self.ori_py, y_axi_px, y_axi_py)
        dc.DrawLine(y_axi_px, y_axi_py, y_axi_px + arr_es / 2, y_axi_py + arr_es)
        dc.DrawLine(y_axi_px, y_axi_py, y_axi_px - arr_es / 2, y_axi_py + arr_es)
        
    def OnCloseWindow(self, _):
        self.Destroy()

class Project(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, 'Project', pos=(120, 100) , size=(600, 400))
        self.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
    
    def OnClick(self, e):
        self.Parent.new_pro_added = True
        diminish_size = 1
        pre_img = wx.Image('pic/freight_for.png', wx.BITMAP_TYPE_PNG)
        w = pre_img.GetWidth()
        h = pre_img.GetHeight()
        img = pre_img.Scale(w * diminish_size, h * diminish_size).ConvertToBitmap()
        
        self.Parent.bit_imgs.append((img, img.GetWidth(), img.GetHeight()))
        self.Parent.pro_p.Refresh()
        self.Destroy()
        
class Process:
    def __init__(self, type, px, py):
        # p_type
        # 0 = circle, 1 = rec, 2 = money  
        self.type = type
        self.px = px
        self.py = py
        self.prev = None
        self.next = None
    
class Edge:
    def __init__(self, sx, sy, ex, ey, prev_p, next_p):
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
        prev_p.next = next_p
        next_p.prev = prev_p
            
if __name__ == '__main__':
    app = wx.PySimpleApp()
    mv = M_frame(None, -1, 'POCUS', pos=(100, 50), size=(1024, 768))
    mv.Show(True)
    
#    recom_graph = Graph(None)
#    recom_graph.Show(True)

#    participant_v = Participant(None)
#    participant_v.Show(True)

#    project_v = Project(None)
#    project_v.Show(True)
         
    app.MainLoop()
