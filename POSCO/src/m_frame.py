from __future__ import division

import wx, datetime, math
from process import Process_info_Viewer

selected_item_id = None
code = None
sche_day = None

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
        
        self.input_msg = wx.TextCtrl(msg_p, -1, 'hello', pos=(notice_view_px, notice_view_py + notice_view_sy), size=(notice_view_sx - 50, 35))
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
        
        self.btn_img = ['recBtn', 'circleBtn', 'arrowBtn', 'deliveryBtn', 'xBtn', 'moneyBtn']
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
            if p.px <= x <= p.px + self.btw_p_size:
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
        
        for i, p in enumerate(self.processes):
            if p.type == 0:
                if p.px <= x <= p.px + 150:
                    process_info_view = Process_info_Viewer('rec' + str(i))
                    process_info_view.Show(True)
            if p.type == 1:
                if p.px <= x <= p.px + 100:
                    process_info_view = Process_info_Viewer('circle' + str(i))
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
        sx, sy = self.prev_process.px + 50, self.prev_process.py + 25  
        ex, ey = self.next_process.px, self.next_process.py + 25 
        e = Edge(sx, sy, ex, ey)
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
            px, py = (last_process.px + self.btw_p_size, last_process.py)
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
            
class Item_info_Viewer(wx.Dialog):
    def __init__(self, selected_item):
        wx.Dialog.__init__(self, None, -1, 'Item information', pos=(100, 100) , size=(400, 300))
        img = wx.Image('pic/' + selected_item + '.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        w = img.GetWidth()
        h = img.GetHeight()
        wx.StaticBitmap(self, -1, img, (10, 50), (w, h))
        button = wx.Button(self, -1, "Confirm", (100, 150))
        self.Bind(wx.EVT_BUTTON, self.confirm, button)
        
        if selected_item =='TORX':
            item_info = wx.TextCtrl(self, -1, 'TORX', pos=(w+10, 50), size=(120,10))
        elif selected_item =='TORXPLUS':
            item_info = wx.TextCtrl(self, -1, 'TORXPLUS', pos=(w+10, 50), size=(120,10))
    def confirm(self, event):
        self.Destroy()

class Process:
    def __init__(self, type, px, py):
        # p_type
        # 0 = rec, 1 = circle, 2 = delivery, 3 = x, 4 = money 
        self.type = type
        self.px = px
        self.py = py

class Edge:
    def __init__(self, sx, sy, ex, ey):
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
        
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
#    mv = M_frame(None, -1, 'POSCO', pos=(100, 50), size=(1024, 768))
#    mv.Show(True)
    mv = Item_info_Viewer('TORX')
    mv.Show(True)
    app.MainLoop()
