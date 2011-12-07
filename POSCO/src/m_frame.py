from __future__ import division

import wx, datetime, math
#from process import Process_info_Viewer

selected_item_id = None
code = None
sche_day = None
selected_partner = None

class M_frame(wx.Frame):
    def __init__(self, parent, ID, title, pos, size, style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        self.selected_item = None
        f_size_x, f_size_y = size
        wx.Panel(self, -1)
        self.t_b_color = wx.Colour(64, 117, 180, 100)
        self.t_color = wx.Colour(255, 255, 255, 100)
        self.t_font = wx.Font(30, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        
        pro_p_px, pro_p_py = (0, 0)
        pro_p_sx, pro_p_sy = (f_size_x * 3 / 5, f_size_y / 2 - 40)
        msg_p_px, msg_p_py = (pro_p_px + pro_p_sx, pro_p_py)
        msg_p_sx, msg_p_sy = (f_size_x - pro_p_sx, pro_p_sy)
        proce_p_px, proce_p_py = (pro_p_px, pro_p_py + pro_p_sy)
        proce_p_sx, proce_p_sy = (f_size_x, f_size_y - pro_p_sy)
        self.product_display(pro_p_px, pro_p_py, pro_p_sx, pro_p_sy)
        self.message_display(msg_p_px, msg_p_py, msg_p_sx, msg_p_sy)
        self.process_display(proce_p_px, proce_p_py, proce_p_sx, proce_p_sy)        
        
    def message_display(self, msg_p_px, msg_p_py, msg_p_sx, msg_p_sy):
        msg_p = wx.Panel(self, -1, pos=(msg_p_px, msg_p_py), size=(msg_p_sx, msg_p_sy))
        wx.StaticBox(msg_p, -1, "", pos=(2, 0), size=(msg_p_sx - 22, msg_p_sy))
        t_msg_p = wx.Panel(msg_p, -1, pos=(7, 10), size=(msg_p_sx - 28, 60))
        t_msg_p_px, t_msg_p_py = t_msg_p.GetPosition()
        t_msg_p_sx, t_msg_p_sy = t_msg_p.GetSize()
        
        RTM_img = wx.Image('pic/RTM.png', wx.BITMAP_TYPE_PNG)
        wx.StaticBitmap(t_msg_p, -1, wx.BitmapFromImage(RTM_img))
        
        self.notice_view = wx.TextCtrl(msg_p, -1, "", pos=(t_msg_p_px, t_msg_p_py + t_msg_p_sy),
                           size=(t_msg_p_sx, msg_p_sy - t_msg_p_sy - 50), style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
        
        self.notice_view.SetEditable(False)
        self.notice_view.SetBackgroundColour(wx.Colour(220, 230, 242, 100))
        self.notice_view.write('---------------------------------------------------------------------------------------');
        self.notice_view.write('\n  2011-11-27  19:6:53');
        self.notice_view.write('\n    earlier departure from Dong_he.cop');
        self.notice_view.write('\n---------------------------------------------------------------------------------------');
        notice_view_px, notice_view_py = self.notice_view.GetPosition()
        notice_view_sx, notice_view_sy = self.notice_view.GetSize() 
        
        self.input_msg = wx.TextCtrl(msg_p, -1, 'we are completed milling process', pos=(notice_view_px, notice_view_py + notice_view_sy), size=(notice_view_sx - 50, 35))
        self.input_msg.SetFont(wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT))
        self.input_msg_px, self.input_msg_py = self.input_msg.GetPosition()
        self.input_msg_sx, self.input_msg_sy = self.input_msg.GetSize()
        s_btn = wx.Button(msg_p, -1, "Send", pos=(self.input_msg_px + self.input_msg_sx, self.input_msg_py), size=(50, 35))
        s_btn.SetFont(wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.Bind(wx.EVT_BUTTON, self.add_log, s_btn)
        
    def add_log(self, evt):
        ct = datetime.datetime.now()
        self.notice_view.write('\n---------------------------------------------------------------------------------------');
        self.notice_view.write('\n ' + str(ct.date()) + '  ' + str(ct.time().hour) + ':' + str(ct.time().minute) + ':' + str(ct.time().second));
        self.notice_view.write('\n [HeadFirst]  ' + self.input_msg.GetValue())
        self.notice_view.write('\n---------------------------------------------------------------------------------------');
        self.input_msg.Clear()
        
    def process_display(self, proce_p_px, proce_p_py, proce_p_sx, proce_p_sy):
        proce_p = wx.Panel(self, -1, pos=(proce_p_px, proce_p_py), size=(proce_p_sx, proce_p_sy))
        wx.StaticBox(proce_p, -1, "", pos=(2, 0), size=(proce_p_sx - 22, proce_p_sy - 40))
        t_process_p = wx.Panel(proce_p, -1, pos=(7, 10), size=(proce_p_sx - 28, 60))
        t_process_p_px, t_process_p_py = t_process_p.GetPosition()
        t_process_p_sx, t_process_p_sy = t_process_p.GetSize()
        process_img = wx.Image('pic/our_process.png', wx.BITMAP_TYPE_PNG)
        wx.StaticBitmap(t_process_p, -1, wx.BitmapFromImage(process_img), pos=(-3, 0))
        
        m_p = wx.Panel(proce_p, -1, pos=(t_process_p_px, t_process_p_py + t_process_p_sy), size=(70, proce_p_sy - t_process_p_sy - 60))
        m_p_px, m_p_py = m_p.GetPosition() 
        m_p_sx, m_p_sy = m_p.GetSize()
        
        self.btn_img = ['circleBtn','recBtn' , 'arrowBtn', 'deliveryBtn', 'xBtn', 'moneyBtn']
        last_py = 0
        
        for i, name in enumerate(self.btn_img):
            img = wx.Image('pic/' + name + '.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
            w = img.GetWidth()
            h = img.GetHeight()
            i_btn = wx.BitmapButton(m_p, id=i, bitmap=img, pos=(10, last_py), size=(w, h))
            last_py = last_py + h
            i_btn.Bind(wx.EVT_BUTTON, eval('self.' + name))
        
        self.process_view = wx.ScrolledWindow(proce_p, -1, pos=(m_p_px + m_p_sx, m_p_py), size=(t_process_p_sx - m_p_sx, m_p_sy))
        self.process_view.SetDoubleBuffered(True)
        process_view_px, process_view_py = self.product_view.GetPosition()
        self.process_view_sx, self.process_view_sy = self.product_view.GetSize()

        self.process_view.SetScrollbars(100, self.process_view_sy, 13, 1)
#        self.process_view.SetBackgroundColour(wx.Colour(100, 200, 200, 100))
        self.process_view.Bind(wx.EVT_PAINT, self.drawing)
        self.process_view.Bind(wx.EVT_LEFT_DOWN, self.OnProcessClick)
        self.process_view.Bind(wx.EVT_LEFT_DCLICK, self.OnProcessDClick)
        
        self.process_view.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.processes = []
        self.edges = []
        
        process_b_img = wx.Image('pic/process_back.png', wx.BITMAP_TYPE_PNG)
        w = process_b_img.GetWidth()
        h = process_b_img.GetHeight()
        self.process_b_img = wx.BitmapFromImage(process_b_img.Scale(w * 0.6, h * 0.833))
        self.process_b_img_px = self.process_view_sx + 120
        self.process_b_img_py = 0
        
        confirm_btn = wx.Button(self.process_view, -1, 'confirm', pos=(self.process_b_img_px + 100, h * 0.833 - 50), size=(70, 35))
        confirm_btn.SetFont(wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT))
        
        self.prev_process = None
        self.next_process = None
        
    def OnProcessClick(self, e):
        dx, dy = self.process_view.GetViewStart()
        x, y = e.GetX() + dx * 100, e.GetY() + dy * 100
        for i, p in enumerate(self.processes):
            if p.px <= x <= p.px + self.btw_p_size and p.py <= y <= p.py + 50:
                if not self.prev_process:
                    self.prev_process = self.processes[i]
                else:
                    self.next_process = self.processes[i]
        self.process_view.Refresh()
    
    def OnProcessDClick(self, e):
        self.prev_process = None
        self.next_process = None
        dx, dy = self.process_view.GetViewStart()
        x, y = e.GetX() + dx * 100, e.GetY() + dy * 100
        
#        for i, p in enumerate(self.processes):
#            if p.type == 0:
#                if p.px <= x <= p.px + 150:
#                    process_info_view = Process_info_Viewer()
#                    process_info_view.Show(True)
#            if p.type == 1:
#                if p.px <= x <= p.px + 100:
        process_info_view = Process_info_Viewer()
        process_info_view.Show(True)
        self.process_view.Refresh()
                    
    def drawing(self, _):
        dc = wx.PaintDC(self.process_view)
        self.process_view.PrepareDC(dc)
        
        rec_img = wx.Image('pic/recBtn.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        circle_img = wx.Image('pic/circleBtn.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        x_img = wx.Image('pic/xBtn.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        delivery_img = wx.Image('pic/deliveryBtn.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        money_img = wx.Image('pic/moneyBtn.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        
        h_center_py = self.process_view_sy / 2
        d_start_px = 70
        self.btw_p_size = 80
        
        if self.selected_item == None or self.selected_item == 'TORX':
            p1_px, p1_py = d_start_px, h_center_py
            p2_px, p2_py = d_start_px + self.btw_p_size, h_center_py
            p3_px, p3_py = d_start_px + self.btw_p_size * 2, h_center_py - 50
            p4_px, p4_py = d_start_px + self.btw_p_size * 2, h_center_py + 50
            p5_px, p5_py = d_start_px + self.btw_p_size * 3, h_center_py
            p6_px, p6_py = d_start_px + self.btw_p_size * 4, h_center_py
            p7_px, p7_py = d_start_px + self.btw_p_size * 5, h_center_py
            p8_px, p8_py = d_start_px + self.btw_p_size * 6, h_center_py
            es = [(p1_px + 50, p1_py + 25, p2_px, p2_py + 25),
                  (p2_px + 50, p2_py + 25, p3_px, p3_py + 25),
                  (p2_px + 50, p2_py + 25, p4_px, p4_py + 25),
                  (p3_px + 50, p3_py + 25, p5_px, p5_py + 25),
                  (p4_px + 50, p4_py + 25, p5_px, p5_py + 25),
                  (p5_px + 50, p5_py + 25, p6_px, p6_py + 25),
                  (p6_px + 50, p6_py + 25, p7_px, p7_py + 25),
                  (p7_px + 50, p7_py + 25, p8_px, p8_py + 25)
                  ]
            dc.DrawBitmap(circle_img, p1_px, p1_py)
            dc.DrawBitmap(x_img, p2_px, p2_py)
            dc.DrawBitmap(rec_img, p3_px, p3_py)
            dc.DrawBitmap(rec_img, p4_px, p4_py)
            dc.DrawBitmap(x_img, p5_px, p5_py)
            dc.DrawBitmap(delivery_img, p6_px, p6_py)
            dc.DrawBitmap(money_img, p7_px, p7_py)
            dc.DrawBitmap(circle_img, p8_px, p8_py)
            for e in es:
                sx, sy, ex, ey = e[0], e[1], e[2], e[3]
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
        elif self.selected_item == 'TORXPLUS':
            p1_px, p1_py = d_start_px, h_center_py
            p2_px, p2_py = d_start_px + self.btw_p_size, h_center_py
            
            p3_px, p3_py = d_start_px + self.btw_p_size * 2, h_center_py - 50
            p4_px, p4_py = d_start_px + self.btw_p_size * 2, h_center_py + 50
            
            p5_px, p5_py = d_start_px + self.btw_p_size * 3, h_center_py - 50 - 30
            p6_px, p6_py = d_start_px + self.btw_p_size * 3, h_center_py - 50 + 30
            p7_px, p7_py = d_start_px + self.btw_p_size * 3, h_center_py + 50
            
            p8_px, p8_py = d_start_px + self.btw_p_size * 4, h_center_py
            p9_px, p9_py = d_start_px + self.btw_p_size * 5, h_center_py
            p10_px, p10_py = d_start_px + self.btw_p_size * 6, h_center_py
            p11_px, p11_py = d_start_px + self.btw_p_size * 7, h_center_py
            
            es = [(p1_px + 50, p1_py + 25, p2_px, p2_py + 25),
                  
                  (p2_px + 50, p2_py + 25, p3_px, p3_py + 25),
                  (p2_px + 50, p2_py + 25, p4_px, p4_py + 25),
                  
                  (p3_px + 50, p3_py + 25, p5_px, p5_py + 25),
                  (p3_px + 50, p3_py + 25, p6_px, p6_py + 25),
                  (p4_px + 50, p4_py + 25, p7_px, p7_py + 25),
                  
                  (p5_px + 50, p5_py + 25, p8_px, p8_py + 25),
                  (p6_px + 50, p6_py + 25, p8_px, p8_py + 25),
                  (p7_px + 50, p7_py + 25, p8_px, p8_py + 25),
                  
                  
                  (p8_px + 50, p8_py + 25, p9_px, p9_py + 25),
                  (p9_px + 50, p9_py + 25, p10_px, p10_py + 25),
                  ]
            
            dc.DrawBitmap(circle_img, p1_px, p1_py)
            dc.DrawBitmap(x_img, p2_px, p2_py)
            dc.DrawBitmap(rec_img, p3_px, p3_py)
            dc.DrawBitmap(rec_img, p4_px, p4_py)
            
            dc.DrawBitmap(rec_img, p5_px, p5_py)
            dc.DrawBitmap(rec_img, p6_px, p6_py)
            dc.DrawBitmap(rec_img, p7_px, p7_py)
            
            
            dc.DrawBitmap(x_img, p8_px, p8_py)
            dc.DrawBitmap(delivery_img, p9_px, p9_py)
            dc.DrawBitmap(money_img, p10_px, p10_py)
            
            dc.DrawBitmap(circle_img, p11_px, p11_py)
            for e in es:
                sx, sy, ex, ey = e[0], e[1], e[2], e[3]
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
        else:
            for p in self.processes:
                if p.type == 0:
                    dc.DrawBitmap(rec_img, p.px, p.py)
                elif p.type == 1:
                    dc.DrawBitmap(circle_img, p.px, p.py)
                elif p.type == 2:
                    dc.DrawBitmap(delivery_img, p.px, p.py)
                    global selected_partner
                    if selected_partner:
                        t = wx.Image('pic/partner.png', wx.BITMAP_TYPE_PNG)
                        partner_img = t.Scale(45, 45).ConvertToBitmap()
                        dc.DrawBitmap(partner_img, p.px + 2.5, p.py - 55)
                elif p.type == 3:
                    dc.DrawBitmap(x_img, p.px, p.py)    
                else:
                    dc.DrawBitmap(money_img, p.px, p.py)
                
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
        
        x, y = self.process_view.GetViewStart()
        self.back_img = dc.DrawBitmap(self.process_b_img , self.process_b_img_px + x * 100, self.process_b_img_py)
        dc.EndDrawing()

    def recBtn(self, evt):
        if not self.processes:
            px, py = (30, self.process_view_sy / 2)
        else:
            last_process = self.processes[-1]
            px, py = (last_process.px + self.btw_p_size, last_process.py)
        p = Process(0, px, py)
        self.processes.append(p)
        self.process_view.Refresh()
        
    def circleBtn(self, evt):
        if not self.processes:
            px, py = (30, self.process_view_sy / 2)
        else:
            last_process = self.processes[-1]
            px, py = (last_process.px + self.btw_p_size, last_process.py)
        p = Process(1, px, py)
        self.processes.append(p)
        self.process_view.Refresh()
        
    def arrowBtn(self, evt):
        if self.prev_process.next:
            self.next_process.py = self.processes[-2].py +50
            self.next_process.px = self.processes[-2].px
            self.processes[-2].py -= 50
            self.edges.pop()
            sx, sy = self.processes[-3].px + 50, self.processes[-3].py + 25  
            ex, ey = self.processes[-2].px, self.processes[-2].py + 25 
            e = Edge(sx, sy, ex, ey, self.prev_process, self.next_process)
            self.edges.append(e)
        sx, sy = self.prev_process.px + 50, self.prev_process.py + 25  
        ex, ey = self.next_process.px, self.next_process.py + 25 
        e = Edge(sx, sy, ex, ey, self.prev_process, self.next_process)
        self.edges.append(e)
        self.prev_process = None
        self.next_process = None
        self.process_view.Refresh()
        
    def deliveryBtn(self, evt):
        if not self.processes:
            px, py = (30, self.process_view_sy / 2)
        else:
            last_process = self.processes[-1]
            px, py = (last_process.px + self.btw_p_size, last_process.py)
        p = Process(2, px, py)
        self.processes.append(p)
        self.process_view.Refresh()
    def xBtn(self, evt):
        if not self.processes:
            px, py = (30, self.process_view_sy / 2)
        else:
            last_process = self.processes[-1]
            px, py = (last_process.px + self.btw_p_size, self.process_view_sy / 2)
        p = Process(3, px, py)
        self.processes.append(p)
        self.process_view.Refresh()
    def moneyBtn(self, evt):
        if not self.processes:
            px, py = (30, self.process_view_sy / 2)
        else:
            last_process = self.processes[-1]
            px, py = (last_process.px + self.btw_p_size, last_process.py)
        p = Process(4, px, py)
        self.processes.append(p)
        self.process_view.Refresh()

    def product_display(self, pro_p_px, pro_p_py, pro_p_sx, pro_p_sy):
        pro_p = wx.Panel(self, -1, pos=(pro_p_px, pro_p_py), size=(pro_p_sx, pro_p_sy))
        wx.StaticBox(pro_p, -1, "", pos=(5, 0), size=(pro_p_sx - 7, pro_p_sy))
        t_pro_p = wx.Panel(pro_p, -1, pos=(7, 10), size=(pro_p_sx - 9, 60))
        our_product_img = wx.Image('pic/our_product.png', wx.BITMAP_TYPE_PNG)
        wx.StaticBitmap(t_pro_p, -1, wx.BitmapFromImage(our_product_img))
        t_pro_p_px, t_pro_p_py = t_pro_p.GetPosition()
        t_pro_p_sx, t_pro_p_sy = t_pro_p.GetSize()
        
        btn_p = wx.Panel(pro_p, -1, pos=(7, pro_p_sy - 40), size=(pro_p_sx - 9, 40))
        btn_p_sx, btn_p_sy = btn_p.GetSize()
        btn_p.SetBackgroundColour(wx.Colour(189, 207, 231, 100))
        t_plus_img = wx.Image('pic/+.png', wx.BITMAP_TYPE_PNG)
        w = t_plus_img.GetWidth()
        h = t_plus_img.GetHeight()
        plus_img = t_plus_img.Scale(w / 4, h / 4).ConvertToBitmap()
        self.plus_btn = wx.BitmapButton(btn_p, id= -1, bitmap=plus_img, pos=(pro_p_sx - 85, 2), size=(30, 30))
        self.plus_btn.Bind(wx.EVT_BUTTON, self.item_add)
        
        t_minus_img = wx.Image('pic/-.png', wx.BITMAP_TYPE_PNG)
        w = t_minus_img.GetWidth()
        h = t_minus_img.GetHeight()
        minus_img = t_minus_img.Scale(w / 4, h / 4).ConvertToBitmap()
        self.plus_btn = wx.BitmapButton(btn_p, id= -1, bitmap=minus_img, pos=(pro_p_sx - 50, 2), size=(30, 30))
        self.plus_btn.Bind(wx.EVT_BUTTON, self.item_remove)
        
        self.product_view = wx.ScrolledWindow(pro_p, -1, pos=(t_pro_p_px, t_pro_p_py + t_pro_p_sy), size=(t_pro_p_sx - 5, pro_p_sy - t_pro_p_sy - btn_p_sy - 13), style=wx.BORDER_SIMPLE)
        self.product_view.SetDoubleBuffered(True)
        self.product_view_sx, self.product_view_sy = self.product_view.GetSize()
#        self.product_view.SetBackgroundColour("WHITE")
        self.product_view.SetScrollRate(1, 1)        
        self.product_view.SetScrollbars(100, self.product_view_sy, 13, 1)
        self.product_view.Bind(wx.EVT_LEFT_DOWN, self.OnItemClick)
        
#        self.plus_btn = wx.BitmapButton(btn_p, id= -1, bitmap=minus_img, pos=(pro_p_sx - 50, 2), size=(30, 30))
        self.imgs_name = ['TORX', 'TORXPLUS', 'TRILOBULAR']
        last_px = 25
        diminish_size = 0.8
        c_t = wx.StaticText(self, -1, 'Code', (10, 237))
        c_t.SetBackgroundColour(wx.Colour(239, 235, 222))
        c_t.SetFont(wx.Font(12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        sd_t = wx.StaticText(self, -1, 'Sche Day', (10, 260))
        sd_t.SetBackgroundColour(wx.Colour(239, 235, 222))
        sd_t.SetFont(wx.Font(12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        product_name = ['ad32454', 'de33454']
        product_info_font = wx.Font(11, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        product_name_b_color = wx.Colour(144, 124, 138)
        
        sds = ['11.12.11', '11.12.13']
        product_sd_b_color = wx.Colour(88, 74, 78)
        
        for i, name in enumerate(self.imgs_name):
            if i == 2:
                self.last_px = last_px
                continue
            img = wx.Image('pic/' + name + '.png', wx.BITMAP_TYPE_PNG)
            w = img.GetWidth()
            h = img.GetHeight()
            img_ = img.Scale(w * diminish_size, h * diminish_size).ConvertToBitmap()
            i_btn = wx.BitmapButton(self.product_view, id=i, bitmap=img_, pos=(last_px, 0), size=(200 * diminish_size, 200 * diminish_size))
            i_btn_px, i_btn_py = i_btn.GetPosition()
            i_btn_sx, i_btn_sy = i_btn.GetSize()
            
            info_txt_pos = (i_btn_px + 55, i_btn_py + i_btn_sy + 8)
            pn = wx.StaticText(self.product_view, -1, product_name[i], info_txt_pos)
            pn.SetBackgroundColour(product_name_b_color)
            pn.SetFont(product_info_font)
            pn_px, pn_py = pn.GetPosition()
            pn_sx, pn_sy = pn.GetSize()
            
            sd = wx.StaticText(self.product_view, -1, sds[i], (pn_px, pn_py + pn_sy + 5))
            sd.SetBackgroundColour(product_sd_b_color)
            sd.SetFont(product_info_font)
            
            i_btn.Bind(wx.EVT_BUTTON, eval('self.item' + str(i)))
            last_px = last_px + w * diminish_size
            
    def OnItemClick(self, e):
        global selected_item_id
        global code
        global sche_day
        diminish_size = 0.8
        product_info_font = wx.Font(11, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        product_name_b_color = wx.Colour(144, 124, 138)
        product_sd_b_color = wx.Colour(88, 74, 78) 
        if selected_item_id != None:
            img = wx.Image('pic/' + self.imgs_name[selected_item_id] + '.png', wx.BITMAP_TYPE_PNG)
            w = img.GetWidth()
            h = img.GetHeight()
            img_ = img.Scale(w * diminish_size, h * diminish_size).ConvertToBitmap()
            i_btn = wx.BitmapButton(self.product_view, id= -1, bitmap=img_, pos=(self.last_px, 0), size=(200 * diminish_size, 200 * diminish_size))
            i_btn_px, i_btn_py = i_btn.GetPosition()
            i_btn_sx, i_btn_sy = i_btn.GetSize()
            
            info_txt_pos = (i_btn_px + 55, i_btn_py + i_btn_sy + 8)
            pn = wx.StaticText(self.product_view, -1, code, info_txt_pos)
            pn.SetBackgroundColour(product_name_b_color)
            pn.SetFont(product_info_font)
            pn_px, pn_py = pn.GetPosition()
            pn_sx, pn_sy = pn.GetSize()
            
            sd = wx.StaticText(self.product_view, -1, sche_day, (pn_px, pn_py + pn_sy + 5))
            sd.SetBackgroundColour(product_sd_b_color)
            sd.SetFont(product_info_font)
            
            i_btn.Bind(wx.EVT_BUTTON, eval('self.item' + str(selected_item_id)))
            
    def item0(self, evt):
        self.selected_item = self.imgs_name[0]
        print self.imgs_name[0]
        self.item_info() 
        self.process_view.Refresh()
    
    def item1(self, evt):
        self.selected_item = self.imgs_name[1]
        self.item_info()
        self.process_view.Refresh()
        
    def item2(self, evt):
        self.selected_item = self.imgs_name[2]
        self.item_info()
        self.process_view.Refresh()
    
    def item3(self, evt):
        self.selected_item = self.imgs_name[3]
        self.item_info()
        self.process_view.Refresh()
        
    def item_info(self):
        item_info_view = Item_info_Viewer(self.selected_item)
        item_info_view.Show(True)
        
    def item_add(self, evt):
        item_select_view = Item_Select_Viewer()
        item_select_view.Show(True)
#        item_select_view.Destroy()
#        print code, sche_day
    
    def item_remove(self, evt):
        pass


class Item_Select_Viewer(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, 'Items', pos=(100, 100) , size=(330, 200))
#        wx.StaticText(self, -1, selected_item, (10, 10))
        '', '',
        self.img1_ = wx.Image('pic/TORX.png', wx.BITMAP_TYPE_PNG).Scale(100, 100).ConvertToBitmap()
        self.img2_ = wx.Image('pic/TORXPLUS.png', wx.BITMAP_TYPE_PNG).Scale(100, 100).ConvertToBitmap()
        self.img3_ = wx.Image('pic/TRILOBULAR.png', wx.BITMAP_TYPE_PNG).Scale(100, 100).ConvertToBitmap()
        
        px = 20
        py = 10
        btw = 100
        t = wx.StaticText(self, -1, 'Code : ', pos=(px, py + 105))
        t_px, t_py = t.GetPosition()
        t_sx, t_sy = t.GetSize()
        self.i_code = wx.TextCtrl(self, -1, 'cx31254', pos=(t_px + t_sx, t_py - 2), size=(65, 20))
        px, py = self.i_code.GetPosition()
        sx, sy = self.i_code.GetSize()
        
        t = wx.StaticText(self, -1, 'Sche Day : ', pos=(px + sx + 20, py + 2))
        t_px, t_py = t.GetPosition()
        t_sx, t_sy = t.GetSize()
        
        self.i_sche_day = wx.TextCtrl(self, -1, '11.12.11', pos=(t_px + t_sx, t_py - 2), size=(65, 20))
        
        button = wx.Button(self, -1, "Confirm", (t_px - 40, t_py + 25))
        self.Bind(wx.EVT_BUTTON, self.confirm, button)
        
        
        self.Bind(wx.EVT_PAINT, self.drawing)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnProcessClick)
    
    def drawing(self, _):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        global selected_item_id
        
        px = 20
        py = 10
        btw = 100
        self.img1 = dc.DrawBitmap(self.img1_, px, py)
        self.img2 = dc.DrawBitmap(self.img2_, px + btw, py)
        self.img3 = dc.DrawBitmap(self.img3_, px + btw * 2, py)
        
        if selected_item_id != None:
            px = 20 + selected_item_id * 100
#            old_pen = dc.GetPen()
            dc.SetPen(wx.Pen(wx.BLUE, 3))
            p1 = (px - 2, py - 2) 
            p2 = (px + 102, py - 2)
            p3 = (px - 2, py + 102)
            p4 = (px + 102, py + 102)
            dc.DrawLine(p1[0], p1[1], p2[0], p2[1])
            dc.DrawLine(p1[0], p1[1], p3[0], p3[1])
            dc.DrawLine(p2[0], p2[1], p4[0], p4[1])
            dc.DrawLine(p3[0], p3[1], p4[0], p4[1])
#        dc.SetPen(old_pen)
        dc.EndDrawing()
    
    def OnProcessClick(self, e):
        x, y = e.GetX(), e.GetY()
        px = 20
        btw = 100
        global selected_item_id
        if px <= x <= px + btw:
            selected_item_id = 0
        elif px <= x <= px + btw * 2:
            selected_item_id = 1
        elif px + btw * 2 <= x:
            selected_item_id = 2
        self.Refresh()
        
    def confirm(self, event):
        global code
        code = self.i_code.GetValue()
        global sche_day
        sche_day = self.i_sche_day.GetValue() 
        self.Destroy()

class Process:
    def __init__(self, type, px, py):
        # p_type
        # 0 = rec, 1 = circle, 2 = delivery, 3 = x, 4 = money 
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
        
        
class Process_info_Viewer(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, 'Process information', pos=(120, 100) , size=(904, 680))
        b_color = wx.Colour(222, 239, 247)
        self.selected_partner = None
        self.search_start = False
        
        self.r_box = wx.StaticBox(self, -1, "", pos=(7, 0), size=(345, 645))
        r_box_px, r_box_py = self.r_box.GetPosition()
        r_box_sx, r_box_sy = self.r_box.GetSize()
        repo_p = wx.Panel(self, -1, pos=(r_box_px + 2, r_box_py + 8), size=(342, 60))
        repo_p_px, repo_p_py = repo_p.GetPosition()
        repo_p_sx, repo_p_sy = repo_p.GetSize()
        resp_img = wx.Image('pic/repository.png', wx.BITMAP_TYPE_PNG)
        wx.StaticBitmap(repo_p, -1, wx.BitmapFromImage(resp_img))
        
        search_p = wx.Panel(self, -1, pos=(repo_p_px, repo_p_py + repo_p_sy), size=(342, 45))
        search_p.SetBackgroundColour(b_color)
        search_input = wx.TextCtrl(search_p, -1, '', pos=(10, 3),
                                    size=(repo_p_sx - 100, 34))
        search_input_px, search_input_py = search_input.GetPosition()
        search_input_sx, search_input_sy = search_input.GetSize()
        search_input.SetFont(wx.Font(17, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        search_img = wx.Image('pic/search.png', wx.BITMAP_TYPE_PNG)
        search_btn = wx.BitmapButton(search_p, -1, bitmap=wx.BitmapFromImage(search_img), pos=(search_input_px + search_input_sx + 3, search_input_py - 4))
        self.Bind(wx.EVT_BUTTON, self.search, search_btn)
        
        self.partner_finder = wx.ScrolledWindow(self, -1, pos=(repo_p_px, repo_p_py + repo_p_sy + 45),
                                              size=(repo_p_sx - 5, 480))
        self.partner_finder.SetDoubleBuffered(True)
        self.partner_finder.SetBackgroundColour(b_color)
        self.partner_finder.SetScrollRate(1, 1)        
        self.partner_finder.SetScrollbars(repo_p_sx, 100, 1, 13)
        
        partner_finder_px, partner_finder_py = self.partner_finder.GetPosition()
        partner_finder_sx, partner_finder_sy = self.partner_finder.GetSize()
        
        rep_b_img = wx.Image('pic/repository_b.png', wx.BITMAP_TYPE_PNG)
        wx.StaticBitmap(self, -1, wx.BitmapFromImage(rep_b_img), pos=(partner_finder_px, partner_finder_py + partner_finder_sy + 2))
        
        self.partner_finder.Bind(wx.EVT_LEFT_DOWN, self.OnPartnerClick)
        self.partner_finder.Bind(wx.EVT_PAINT, self.drawing_partner)
        
        self.info_task_box = wx.StaticBox(self, -1, "", pos=(r_box_px + r_box_sx + 5, r_box_py), size=(535, 280))
        info_task_box_px, info_task_box_py = self.info_task_box.GetPosition()
        info_task_box_sx, info_task_box_sy = self.info_task_box.GetSize()     
        self.info_p = wx.Panel(self, -1, pos=(info_task_box_px + 2, info_task_box_py + 12), size=(190, 50))
        info_p_px, info_p_py = self.info_p.GetPosition()
        info_p_sx, info_p_sy = self.info_p.GetSize()
        info_img = wx.Image('pic/information.png', wx.BITMAP_TYPE_PNG)
        wx.StaticBitmap(self.info_p, -1, wx.BitmapFromImage(info_img.Scale(190, 50)))
        self.task_p = wx.Panel(self, -1, pos=(info_p_px + info_p_sx, info_p_py), size=(341, 50))
        self.task_p.Bind(wx.EVT_LEFT_DOWN, self.OnTaskClick)
        self.task_p.Bind(wx.EVT_PAINT, self.drawing_task)
        
        self.info_task_viewer_p = wx.Panel(self, -1, pos=(info_p_px, info_p_py + info_p_sy + 4), size=(530, info_task_box_sy - 110))
        info_task_viewer_p_px, info_task_viewer_p_py = self.info_task_viewer_p.GetPosition()
        info_task_viewer_p_sx, info_task_viewer_p_sy = self.info_task_viewer_p.GetSize()
        self.info_task_viewer_p.SetBackgroundColour(b_color)

        info_task_viewer_b_p = wx.Panel(self, -1, pos=(info_task_viewer_p_px, info_task_viewer_p_py + info_task_viewer_p_sy), size=(info_task_viewer_p_sx, 40))
        info_task_viewer_b_p.SetBackgroundColour(wx.Colour(181, 203, 239))
        
        self.detail_process_box = wx.StaticBox(self, -1, "", pos=(info_task_box_px, info_task_box_py + info_task_box_sy),
                                           size=(534, 365))
    def display_info_task(self, choice):
        if self.selected_partner == 2:
            info_task_viewer_p_px, info_task_viewer_p_py = self.info_task_viewer_p.GetPosition()
            info_task_viewer_p_sx, info_task_viewer_p_sy = self.info_task_viewer_p.GetSize()
            if choice == 0:
                partner_img = wx.Image('pic/partner.png', wx.BITMAP_TYPE_PNG)
                w = partner_img.GetWidth()
                h = partner_img.GetHeight()
                wx.StaticBitmap(self.info_task_viewer_p, -1, wx.BitmapFromImage(partner_img), pos=(50, 25), size=(w, h))
                self.info_task_viewer_p.SetFont(wx.Font(17, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
                wx.StaticText(self.info_task_viewer_p, -1, 'Dung Liu Express Co.', pos=(190, 20))
                wx.StaticText(self.info_task_viewer_p, -1, 'Name : Dung Liu', pos=(190, 70))
                wx.StaticText(self.info_task_viewer_p, -1, 'Contack : 011-244-1547', pos=(190, 120))
    #            cops_n.SetFont()
            else:
                ipad_img = wx.Image('pic/ipad.png', wx.BITMAP_TYPE_PNG)
                w = ipad_img.GetWidth()
                h = ipad_img.GetHeight()
                wx.StaticBitmap(self.info_task_viewer_p, -1, wx.BitmapFromImage(ipad_img.Scale(w / 7, h / 7)), pos=(50, 20), size=(w / 7, h / 7))
                
#                iphone_img = wx.Image('pic/iphone.png', wx.BITMAP_TYPE_PNG)
#                w = iphone_img.GetWidth()
#                h = iphone_img.GetHeight()
#                wx.StaticBitmap(self.info_task_viewer_p, -1, wx.BitmapFromImage(iphone_img.Scale(w / 10, h / 9.4)), pos=(200, 20), size=(w / 10, h / 9.4))
    
    def display_detail_process(self, choice):
        detail_process_box_px, detail_process_box_py = self.detail_process_box.GetPosition()
        detail_process_box_sx, detail_process_box_sy = self.detail_process_box.GetSize()
        self.detail_process_p = wx.Panel(self, -1, pos=(detail_process_box_px, detail_process_box_py + 5), size=(detail_process_box_sx, detail_process_box_sy - 10))
        detail_process_p_sx, detail_process_p_sy = self.detail_process_p.GetSize()
#        detail_process_p.SetBackgroundColour(wx.Colour(255,123,21))
        # choice == 0  is detail
        if choice == 0:
            details_t_img = wx.Image('pic/detatils_t.png', wx.BITMAP_TYPE_PNG)
            self.datails_t = wx.StaticBitmap(self.detail_process_p, -1, wx.BitmapFromImage(details_t_img.Scale(detail_process_box_sx - 4, 50)), pos=(1, 3), size=(detail_process_box_sx - 4, 50))
            
            self.detail_process_viewer = wx.ScrolledWindow(self.detail_process_p, -1, pos=(0, 55),
                                                  size=(detail_process_box_sx - 5, 250))
            self.detail_process_viewer.SetDoubleBuffered(True)
            self.detail_process_viewer.SetBackgroundColour("white")
#            self.detail_process_viewer.SetScrollRate(1,0.1)        
            self.detail_process_viewer.SetScrollbars(detail_process_p_sx - 5, 10, 1, 130)
            
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
            last_py += 150 * 1.5 + 10
            wx.StaticText(self.detail_process_viewer, -1, 'Factory scale : 990 square meter ', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, 'Address : - Closed -  ', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, 'Num of Workers : 17 ', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, 'Related Works or News ', pos=(sub_px, last_py))
            last_py += 20
            web_address = wx.StaticText(self.detail_process_viewer, -1, '    htttp://www.hankyung.co.kr/der~', pos=(sub_px, last_py))
            web_address.SetForegroundColour(wx.Colour(85, 142, 213))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, '------------------------------------------------------------------------------------------', pos=(0, last_py))
            last_py += btw_line_size
            
            rc = wx.StaticText(self.detail_process_viewer, -1, '2.Record career', pos=(t_px, last_py))
            rc.SetFont(t_font)
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, 'Num of Total Project : 56 ', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, 'Num of Current Project : 3 ', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, 'Num of Completed Project : 45 ', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, 'Num of failed Project : 8 ', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.Button(self.detail_process_viewer, -1, 'Details', pos=(sub_px + 30, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, '------------------------------------------------------------------------------------------', pos=(0, last_py))
            last_py += btw_line_size
            
            ev = wx.StaticText(self.detail_process_viewer, -1, '3.Evaluation', pos=(t_px, last_py))
            ev.SetFont(t_font)
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, 'SCORE : 8.5/10 ', pos=(sub_px, last_py))
            last_py += btw_line_size
            details_btn = wx.Button(self.detail_process_viewer, -1, 'Details', pos=(sub_px + 30, last_py))
            self.Bind(wx.EVT_BUTTON, self.eval_show, details_btn)
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, '------------------------------------------------------------------------------------------', pos=(0, last_py))
            last_py += btw_line_size
            
            bd = wx.StaticText(self.detail_process_viewer, -1, '4.Benefit Distribution', pos=(t_px, last_py))
            bd.SetFont(t_font)
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, '- Closed -', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, '------------------------------------------------------------------------------------------', pos=(0, last_py))
            last_py += btw_line_size
            
            fs = wx.StaticText(self.detail_process_viewer, -1, '5.Financial Statements', pos=(t_px, last_py))
            fs.SetFont(t_font)
            last_py += btw_line_size
            self.detail_process_viewer.SetForegroundColour(wx.Colour(85, 142, 213))
            wx.StaticText(self.detail_process_viewer, -1, '1/4     2009 Year', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, '2/4     2009 Year', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, '3/4     2009 Year', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, '4/4     2009 Year', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, '1/4     2010 Year', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, '2/4     2010 Year', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, '3/4     2010 Year', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, '4/4     2010 Year', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, '------------------------------------------------------------------------------------------', pos=(0, last_py))
            last_py += btw_line_size
        else:
            # process
            process_t_img = wx.Image('pic/process_t.png', wx.BITMAP_TYPE_PNG)
            wx.StaticBitmap(self.detail_process_p, -1, wx.BitmapFromImage(process_t_img.Scale(detail_process_box_sx - 4, 50)), pos=(1, 3), size=(detail_process_box_sx - 4, 50))
            wx.StaticBitmap(self.detail_process_p, -1, wx.BitmapFromImage(wx.Image('pic/process_ex.png', wx.BITMAP_TYPE_PNG).Scale(detail_process_box_sx - 4, 250)), pos=(1, 50), size=(detail_process_box_sx - 4, 250))

        wx.StaticBitmap(self.detail_process_p, -1, wx.BitmapFromImage(wx.Image('pic/repository_b.png', wx.BITMAP_TYPE_PNG).Scale(detail_process_box_sx - 4, 50)),
                         pos=(1, detail_process_p_sy - 45), size=(detail_process_box_sx - 4, 50))
        
#        button = wx.Button(self, -1, "Confirm", (100, 150))
#        self.Bind(wx.EVT_BUTTON, self.confirm, button)
    def confirm(self, event):
        self.Destroy()
        
    def eval_show(self, e):
        self.es = wx.Dialog(None, -1, 'Evaluation Details', pos=(150,150) , size=(610, 490))
        self.es.Show(True)
        eval_img = wx.Image('pic/eval_ex.png', wx.BITMAP_TYPE_PNG)
        w = eval_img.GetWidth()
        h = eval_img.GetHeight()
        print w, h 
        wx.StaticBitmap(self.es, -1, wx.BitmapFromImage(eval_img), pos=(1, 3), size=(w,h))
        confirm_btn = wx.Button(self.es, -1, "Confirm", (270, 428))
        self.es.Bind(wx.EVT_BUTTON, self.eval_confirm, confirm_btn)
    def eval_confirm(self, e):
        self.es.Destroy()
    
    def search(self, e):
        self.search_start = True
        partner_select_btn = wx.Button(self.partner_finder, -1, "Select", pos=(240, 320), size=(70, 35))
        partner_select_btn.SetFont(wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.partner_finder.Refresh()
        self.Bind(wx.EVT_BUTTON, self.select_partner, partner_select_btn)
    def select_partner(self, e):
        global selected_partner
        selected_partner = True 
        self.Destroy()
        
    def OnPartnerClick(self, e):
        dx, dy = self.partner_finder.GetViewStart()
        x, y = e.GetX() + dx * 100, e.GetY() + dy * 100
        
        if 5 <= y <= 5 + 92:
            self.selected_partner = 0
        elif 5 + 92 <= y <= 5 + 95 * 2 + 15:
            self.selected_partner = 1
        else:
            self.selected_partner = 2
            self.info_task_viewer_p.Refresh()
            self.display_info_task(0)
            self.display_detail_process(0)
        print self.selected_partner
        self.partner_finder.Refresh()
    
    def drawing_partner(self, _):
        dc = wx.PaintDC(self.partner_finder)
        self.partner_finder.PrepareDC(dc)
        
        if self.search_start:
            partner_finder_px, partner_finder_py = self.partner_finder.GetPosition()
            partner_finder_sx, partner_finder_sy = self.partner_finder.GetSize()
            
            partners = ['DHL', 'FedEx', 'EX']
            
            for i, p in enumerate(partners):
                img = wx.Image('pic/' + p + '.png', wx.BITMAP_TYPE_PNG)
                if i == 0:
                    dc.DrawBitmap(wx.BitmapFromImage(img), 7, 5)
                if i == 1:
                    dc.DrawBitmap(wx.BitmapFromImage(img), 7, 5 + 92)
                else:
                    dc.DrawBitmap(wx.BitmapFromImage(img), 4, 5 + 95 * 2 + 15)
        
        if self.selected_partner == 2:
            old_pen = dc.GetPen()
            dc.SetPen(wx.Pen(wx.BLUE, 2))
            p1 = (4 - 2, 5 + 95 * 2 + 15 - 2)
            p2 = (4 + 2 + 319, 5 + 95 * 2 + 15 - 2)
            p3 = (4 - 2, 5 + 95 * 2 + 15 + 2 + 100 + 5)
            p4 = (4 + 2 + 319, 5 + 95 * 2 + 15 + 2 + 100 + 5)
            dc.DrawLine(p1[0], p1[1], p2[0], p2[1])
            dc.DrawLine(p1[0], p1[1], p3[0], p3[1])
            dc.DrawLine(p2[0], p2[1], p4[0], p4[1])
            dc.DrawLine(p3[0], p3[1], p4[0], p4[1])
            dc.SetPen(old_pen)
        dc.EndDrawing()
        
    def drawing_task(self, _):
        dc = wx.PaintDC(self.task_p)
        self.task_p.PrepareDC(dc)
        task_img = wx.Image('pic/task.png', wx.BITMAP_TYPE_PNG)
        dc.DrawBitmap(wx.BitmapFromImage(task_img.Scale(341, 50)), 0, 0)
        dc.EndDrawing()

    def OnTaskClick(self, _):
        self.info_task_viewer_p.Destroy()
        info_task_box_px, info_task_box_py = self.info_task_box.GetPosition()
        info_task_box_sx, info_task_box_sy = self.info_task_box.GetSize()
        b_color = wx.Colour(222, 239, 247)
        info_p_px, info_p_py = self.info_p.GetPosition()
        info_p_sx, info_p_sy = self.info_p.GetSize()
        
        self.info_task_viewer_p = wx.Panel(self, -1, pos=(info_p_px, info_p_py + info_p_sy + 4), size=(530, info_task_box_sy - 110))
        self.info_task_viewer_p.SetBackgroundColour(b_color)
        self.display_info_task(1)
        self.datails_t.Destroy()
        self.detail_process_viewer.Destroy()
        
        self.display_detail_process(1)

class Item_info_Viewer(wx.Dialog):
    def __init__(self, selected_item):
        wx.Dialog.__init__(self, None, -1, 'Item information', pos=(100, 100) , size=(400, 300))
        img = wx.Image('pic/' + selected_item + '.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        w = img.GetWidth()
        h = img.GetHeight()
        wx.StaticBitmap(self, -1, img, (10, 10), (w, h))
        button = wx.Button(self, -1, "Confirm", (300, 225))
        self.Bind(wx.EVT_BUTTON, self.confirm, button)
        
        item_info_px, item_info_py = (w + 10, 10)
        item_info_sx, item_info_sy = (170, 210)
        item_info = wx.TextCtrl(self, -1, '', pos=(item_info_px, item_info_py), size=(item_info_sx, item_info_sy)
                                , style=wx.TE_MULTILINE)
        item_info.SetEditable(True)
        if selected_item == 'TORX':
            item_info.write('TORX')
            item_info.write('\n    Size Designation : 10')
            item_info.write('\n    Dia/Inch : 0.0100')
            item_info.write('\n    Dia/mm : 0.245')
            item_info.write('\n    Pitch/TPI : 400.0')
            item_info.write('\n    Pitch/mm : 0.064')
            item_info.write('\n    CoreDia/" : 0.0068')
            item_info.write('\n    CoreDia/mm : 0.137')
            item_info.write('\n    Depth/Inch : 0.0016')
        elif selected_item == 'TORXPLUS':
            item_info.write('TORXPLUS')
            item_info.write('\n    Size Designation : 12')
            item_info.write('\n    Dia/Inch : 0.0120')
            item_info.write('\n    Dia/mm : 0.305')
            item_info.write('\n    Pitch/TPI : 350.0')
            item_info.write('\n    Pitch/mm : 0.073')
            item_info.write('\n    CoreDia/" : 0.0093')
            item_info.write('\n    CoreDia/mm : 0.237')
            item_info.write('\n    Depth/Inch : 0.0018')
        else:
            item_info.write('TRILOBULAR')
            
    def confirm(self, event):
        self.Destroy()
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    mv = M_frame(None, -1, 'POSCO', pos=(100, 50), size=(1024, 768))
    mv.Show(True)
#    mv = Item_info_Viewer('TORX')
#    mv.Show(True)
#    p = Process(0, 1, 1)
#    mv = Process_info_Viewer()
#    mv.Show(True)
    app.MainLoop()
