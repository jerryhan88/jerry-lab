#-*- coding: cp949 -*-
from __future__ import division
import wx, color_src, datetime, math
orange = color_src.orange
purple = color_src.purple
white = color_src.white
dark_sky = color_src.dark_sky
red = color_src.red

class M_frame(wx.Frame):
    def __init__(self, parent, ID, title, pos, size, style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        f_size_x, f_size_y = size
        p = wx.Panel(self, -1)
        
        pro_p_px, pro_p_py = (0, 0)
        pro_p_sx, pro_p_sy = (f_size_x * 3 / 5, f_size_y / 2 - 40)
        msg_p_px, msg_p_py = (pro_p_px + pro_p_sx, pro_p_py)
        msg_p_sx, msg_p_sy = (f_size_x - pro_p_sx, pro_p_sy)
        proce_p_px, proce_p_py = (pro_p_px, pro_p_py + pro_p_sy)
        proce_p_sx, proce_p_sy = (f_size_x, f_size_y - pro_p_sy)
        self.project_display(p, pro_p_px, pro_p_py, pro_p_sx, pro_p_sy)
        self.message_display(p, msg_p_px, msg_p_py, msg_p_sx, msg_p_sy)
        self.process_display(p, proce_p_px, proce_p_py, proce_p_sx, proce_p_sy)
        
    def project_display(self, parent, px, py, p_sx, p_sy):
        pro_p = wx.Panel(parent, -1, pos=(px, py), size=(p_sx, p_sy))
        wx.StaticBox(pro_p, -1, "", pos=(5, 0), size=(p_sx - 7, p_sy))
        t_p = self.make_title_p(pro_p, 'pic/project_title.png', 7, 10, p_sx - 12, 60)
        btn_p = wx.Panel(pro_p, -1, pos=(7, p_sy - 40), size=(p_sx - 9, 40))
        btn_p.SetBackgroundColour(dark_sky)
        add_btn = self.make_pro_btn(btn_p, 'pic/+.png', p_sx - 85, 2)
        remove_btn = self.make_pro_btn(btn_p, 'pic/-.png', p_sx - 50, 2)
        add_btn.Bind(wx.EVT_BUTTON, self.project_add)
        remove_btn.Bind(wx.EVT_BUTTON, self.project_remove)
        
        px, py = t_p.GetPosition()
        t_sx, t_sy = t_p.GetSize()
        _, b_sy = btn_p.GetSize()
        
        self.pjv_p = wx.ScrolledWindow(pro_p, -1, pos=(px, py + t_sy + 2), size=(t_sx, p_sy - (t_sy + b_sy + 15)), style=wx.SUNKEN_BORDER)
        self.pjv_p.SetDoubleBuffered(True)
        sx, sy = self.pjv_p.GetSize()
        self.pjv_p.SetScrollRate(1, 1)        
        self.pjv_p.SetScrollbars(100, sy, 13, 1)
        
        inte_imgs = ['interior_pic1', 'interior_pic2']
        self.inte_lo_sc = ['전남, 전체', '부산, 실내']
        self.dates = ['2012.05.12', '2012.06.08']
        
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
        self.select_item = [0, 0]
        
    def OnProjectClick(self, e):
        x, y = e.GetX(), e.GetY()
        width = self.bit_imgs[0][1]
        btw = 30
        for i in xrange(len(self.select_item)):
            self.select_item[i] = 0
            if (btw + width) * i <= x <= (btw + width) * (i + 1):
                self.select_item[i] = 1

        self.pjv_p.Refresh()
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
            dc.DrawText(self.inte_lo_sc[i], c_px, btw + st_sy + t_btw)
            dc.DrawText(self.dates[i], c_px, btw + st_sy + t_btw * 2.5)
            
            if self.select_item[i] == 1:
                py = btw + (st_sy - self.bit_imgs[0][2]) / 2
                old_pen = dc.GetPen()
                dc.SetPen(wx.Pen(red, 2))
                margin = 5
                p_h = 50
                p1 = (px - margin-1, py - margin)
                p2 = (px + w + margin, py - margin)
                p3 = (px - margin-1, py + st_sy + margin + p_h)
                p4 = (px + w + margin, py + st_sy + margin + p_h)
                dc.DrawLine(p1[0], p1[1], p2[0], p2[1])
                dc.DrawLine(p1[0], p1[1], p3[0], p3[1])
                dc.DrawLine(p2[0], p2[1], p4[0], p4[1])
                dc.DrawLine(p3[0], p3[1], p4[0], p4[1])
                dc.SetPen(old_pen)
            
        dc.EndDrawing()
        
    def make_pro_btn(self, parent, img, px, py):
        pre_img = wx.Image(img, wx.BITMAP_TYPE_PNG)
        w = pre_img.GetWidth()
        h = pre_img.GetHeight()
        img = pre_img.Scale(w / 4, h / 4).ConvertToBitmap()
        btn = wx.BitmapButton(parent, id= -1, bitmap=img, pos=(px, py), size=(30, 30))
        return btn
    
    def project_add(self, evt):
        pass
    
    def project_remove(self, evt):
        pass
    
    def make_title_p(self, parent, img, px, py, sx, sy):
        t_p = wx.Panel(parent, -1, pos=(px, py), size=(sx, sy))
        pre_img = wx.Image(img, wx.BITMAP_TYPE_PNG)
        sx, sy = t_p.GetSize()
        w = pre_img.GetWidth()
        h = pre_img.GetHeight()
        xs, ys = sx / w, sy / h
        t_img = wx.BitmapFromImage(pre_img.Scale(w * xs, h * ys))
        wx.StaticBitmap(t_p, -1, t_img)
        return t_p
        
    def message_display(self, parent, px, py, p_sx, p_sy):
        msg_p = wx.Panel(parent, -1, pos=(px, py), size=(p_sx, p_sy))
        wx.StaticBox(msg_p, -1, "", pos=(2, 0), size=(p_sx - 15, p_sy))
        t_p = self.make_title_p(msg_p, 'pic/msg_title.png', 7, 10, p_sx - 24, 60)
        px, py = t_p.GetPosition()
        sx, sy = t_p.GetSize()
        self.notice_view = wx.TextCtrl(msg_p, -1, "", pos=(px + 2, py + sy + 2),
                           size=(sx, p_sy - sy - 50), style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
        self.notice_view.SetEditable(False)
        self.notice_view.SetBackgroundColour(wx.Colour(220, 230, 242, 100))
        self.notice_view.write('---------------------------------------------------------------------------------------');
        self.notice_view.write('2011-11-27  19:6:53                                                             ');
        self.notice_view.write('---------------------------------------------------------------------------------------');
        px, py = self.notice_view.GetPosition()
        sx, sy = self.notice_view.GetSize() 
        
        self.input_msg = wx.TextCtrl(msg_p, -1, '프로젝트 종료', pos=(px, py + sy), size=(sx - 50, 35))
        self.input_msg.SetFont(wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT))
        px, py = self.input_msg.GetPosition()
        sx, sy = self.input_msg.GetSize()
        s_btn = wx.Button(msg_p, -1, "Send", pos=(px + sx, py), size=(50, 35))
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
        wx.StaticBox(proce_p, -1, "", pos=(5, 0), size=(p_sx - 18, p_sy - 40))
        t_p = self.make_title_p(proce_p, 'pic/process_title.png', 7, 10, p_sx - 24, 60)
        px, py = t_p.GetPosition()
        t_p_sx, sy = t_p.GetSize()
        
        btns_p = self.make_btns(proce_p, px, py + sy, 130, p_sy - sy - 54)
        px, py = btns_p.GetPosition()
        sx, sy = btns_p.GetSize()
        
        pcv_p = wx.ScrolledWindow(proce_p, -1, pos=(px + sx, py), size=(t_p_sx - sx, sy), style=wx.SUNKEN_BORDER)
        pcv_p.SetDoubleBuffered(True)
        sx, sy = pcv_p.GetSize()
        pcv_p.SetScrollbars(100, sy, 13, 1)
        pcv_p.SetBackgroundColour(white)
        
    def make_btns(self, parent, px, py, sx, sy):
        btns_p = wx.Panel(parent, -1, pos=(px, py), size=(sx, sy))
        sx, sy = btns_p.GetSize()
        wx.StaticBox(btns_p, -1, "", pos=(5, 0), size=(sx - 10, sy - 44))
        btw = 10
        modeling_btns = ['circleBtn', 'recBtn' , 'arrowBtn', 'moneyBtn']
        mo_btns = []
        for i, name in enumerate(modeling_btns):
            img = wx.Image('pic/' + name + '.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
            w = img.GetWidth()
            h = img.GetHeight()
            btn = wx.BitmapButton(btns_p, id=i, bitmap=img, pos=(btw + (i % 2) * (w + btw), btw + (i // 2) * (h + btw) + 2), size=(w, h))
            selected_bitmap = wx.Image('pic/selected_' + name + '.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
            btn.SetBitmapSelected(selected_bitmap) 
            mo_btns.append(btn)
        
        px, py = mo_btns[2].GetPosition()
        sx, sy = mo_btns[2].GetSize()
        action_btns = ['Initialize', 'Recommend', 'Confirm']
        ac_btns = []
        for i, t in enumerate(action_btns):
            btn = wx.Button(btns_p, -1, t, pos=(px, btw + py + sy + i * 45), size=(110, 35))
            btn.SetFont(wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT))
            ac_btns.append(btn)
        
        px, py = ac_btns[-1].GetPosition()
        sx, sy = ac_btns[-1].GetSize()
         
        pre_logo_img = wx.Image('pic/PNU_logo.png', wx.BITMAP_TYPE_PNG)
        w = pre_logo_img.GetWidth()
        h = pre_logo_img.GetHeight()
        logo_img = wx.BitmapFromImage(pre_logo_img)
        wx.StaticBitmap(btns_p, -1, logo_img, pos=(px, py + sy + btw + 7), size=(w, h))
        return btns_p
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    mv = M_frame(None, -1, 'POCUS', pos=(100, 50), size=(1024, 768))
    mv.Show(True)
    app.MainLoop()
