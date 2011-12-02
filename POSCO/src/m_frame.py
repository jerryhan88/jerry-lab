from __future__ import division

import wx, datetime

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
        self.notice_view.write('---------------------------------------------------');
        self.notice_view.write('\n  2011-11-27  19:6:53');
        self.notice_view.write('\n    earlier departure from Dong_he.cop');
        notice_view_px, notice_view_py = self.notice_view.GetPosition()
        notice_view_sx, notice_view_sy = self.notice_view.GetSize() 
        
        self.input_msg = wx.TextCtrl(msg_p, -1, 'hello', pos=(notice_view_px, notice_view_py + notice_view_sy), size=(notice_view_sx - 50, 35))
        self.input_msg.SetFont(wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT))
        self.input_msg_px, self.input_msg_py = self.input_msg.GetPosition()
        self.input_msg_sx, self.input_msg_sy = self.input_msg.GetSize()
        s_btn = wx.Button(msg_p, -1, "Send", pos=(self.input_msg_px + self.input_msg_sx, self.input_msg_py), size=(50, 35))
        s_btn.SetFont(wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.Bind(wx.EVT_BUTTON, self.add_log, s_btn)
        
#        self.input_msg.Bind(wx.EVT_KEY_DOWN, self.add_log)
        
    def add_log(self, evt):
        ct = datetime.datetime.now()
        self.notice_view.write('\n---------------------------------------------------');
        self.notice_view.write('\n ' + str(ct.date()) + '  ' + str(ct.time().hour) + ':' + str(ct.time().minute) + ':' + str(ct.time().second));
        self.notice_view.write('\n ' + self.input_msg.GetValue())
        self.notice_view.write('\n---------------------------------------------------');
        self.input_msg.Clear()
        
        
    def process_display(self, proce_p_px, proce_p_py, proce_p_sx, proce_p_sy):
        proce_p = wx.Panel(self, -1, pos=(proce_p_px, proce_p_py), size=(proce_p_sx, proce_p_sy))
        wx.StaticBox(proce_p, -1, "", pos=(2, 0), size=(proce_p_sx - 22, proce_p_sy - 40))
        t_process_p = wx.Panel(proce_p, -1, pos=(7, 10), size=(proce_p_sx - 28, 60))
        t_process_p_px, t_process_p_py = t_process_p.GetPosition()
        t_process_p_sx, t_process_p_sy = t_process_p.GetSize()
        
        process_img = wx.Image('pic/our_process.png', wx.BITMAP_TYPE_PNG)
        wx.StaticBitmap(t_process_p, -1, wx.BitmapFromImage(process_img), pos = (-3,0))
        
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
        self.process_view_sx, self.process_view_sy = self.product_view.GetSize()
        self.process_view.SetScrollbars(100, self.process_view_sy, 13, 1)
#        self.process_view.SetBackgroundColour(wx.Colour(100, 200, 200, 100))
        self.process_view.Bind(wx.EVT_PAINT, self.drawing)
        self.process_view.Bind(wx.EVT_LEFT_DOWN, self.OnProcessClick)
        self.processes = []
        self.edges = []
        
    def OnProcessClick(self, e):
        dx, dy = self.process_view.GetViewStart()
        x, y = e.GetX() + dx * 100, e.GetY() + dy * 100
        
        for i, p in enumerate(self.processes):
            if p.type ==0:
                if p.px <= x <= p.px + 150:
                    print 'rec',i
                    process_info_view = Process_info_Viewer('rec' + str(i))
                    process_info_view.Show(True)
            if p.type ==1:
                if p.px <= x <= p.px + 100:
                    print 'circle',i
                    process_info_view = Process_info_Viewer('circle' + str(i))
                    process_info_view.Show(True) 
                    
                    
    def drawing(self, _):
        dc = wx.PaintDC(self.process_view)
        self.process_view.PrepareDC(dc)
        for p in self.processes:
            if p.type == 0:
                dc.DrawRectangle(p.px, p.py, 100, 100)
            if p.type == 1:
                dc.DrawCircle(p.px, p.py, 50)
            
        for i, e in enumerate(self.edges):
            last_process = self.processes[i]
            if last_process.type == 0:
                sx, sy, ex, ey = e.sx, e.sy, e.ex, e.ey
            elif last_process.type == 1:
                sx, sy, ex, ey = e.sx - 50, e.sy - 50, e.ex - 50, e.ey - 50
            dc.DrawLine(sx, sy, ex, ey)
            dc.DrawLine(ex, ey, ex - 15, ey - 15)
            dc.DrawLine(ex, ey, ex - 15, ey + 15)
            
        dc.EndDrawing()

    def recBtn(self, evt):
        if not self.processes:
            px, py = (30, (self.process_view_sy - 100) / 2)
        else:
            last_process = self.processes[-1]
            if last_process.type == 0:  
                px, py = (last_process.px + 150, last_process.py)
            elif last_process.type == 1:
                px, py = (last_process.px + 100, last_process.py - 50)
        p = Process(0, px, py)
        self.processes.append(p)
        self.process_view.Refresh()
        
    def circleBtn(self, evt):
        if not self.processes:
            px, py = (50 + 30, 50 + (self.process_view_sy - 100) / 2)
        else:
            last_process = self.processes[-1]
            if last_process.type == 0:  
                px, py = (last_process.px + 200, last_process.py + 50)
            elif last_process.type == 1:
                px, py = (last_process.px + 150, last_process.py)
        p = Process(1, px, py)
        self.processes.append(p)
        self.process_view.Refresh()
        
    def arrowBtn(self, evt):
        last_process = self.processes[-1]
        sx, sy = last_process.px + 100, last_process.py + 50
        e = Edge(sx, sy, sx + 50, sy)
        self.edges.append(e)
        self.process_view.Refresh()
        
    def deliveryBtn(self, evt):
        pass
    def xBtn(self, evt):
        pass
    def moneyBtn(self, evt):
        pass

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
#        self.product_view.Bind(wx.EVT_LEFT_DOWN, self.OnItemClick)
        
        self.imgs_name = ['TORX', 'TORXPLUS', 'TRILOBULAR']
        last_px = 0
#        self.plus_btn = wx.BitmapButton(btn_p, id= -1, bitmap=minus_img, pos=(pro_p_sx - 50, 2), size=(30, 30))
        for i, name in enumerate(self.imgs_name):
            img = wx.Image('pic/' + name + '.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
            w = img.GetWidth()
            h = img.GetHeight()
            i_btn = wx.BitmapButton(self.product_view, id=i, bitmap=img, pos=(last_px, 0), size=(200, 200))
            last_px = last_px + w
            i_btn.Bind(wx.EVT_BUTTON, eval('self.item' + str(i)))
    
    def item0(self, evt):
        self.selected_item = self.imgs_name[0]
        self.item_info() 
        print 'hi1'
    
    def item1(self, evt):
        self.selected_item = self.imgs_name[1]
        self.item_info()
        
    def item2(self, evt):
        self.selected_item = self.imgs_name[2]
        self.item_info()
        
    def item_info(self):
        item_info_view = Item_info_Viewer(self.selected_item)
        item_info_view.Show(True)
        
    def item_add(self, evt):
        print 'hi'
        pass
    
    def item_remove(self, evt):
        print 'hi'
        pass
            
class Item_info_Viewer(wx.Dialog):
    def __init__(self, selected_item):
        wx.Dialog.__init__(self, None, -1, 'Item information', pos=(100, 100) , size=(400, 300))
        wx.StaticText(self, -1, selected_item, (10, 10))
        img = wx.Image('pic/' + selected_item + '.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        w = img.GetWidth()
        h = img.GetHeight()
        wx.StaticBitmap(self, -1, img, (10, 50), (w, h))
        button = wx.Button(self, -1, "Confirm", (100, 150))
        self.Bind(wx.EVT_BUTTON, self.confirm, button)
    def confirm(self, event):
        self.Destroy()

class Process_info_Viewer(wx.Dialog):
    def __init__(self, selected_process):
        wx.Dialog.__init__(self, None, -1, 'Process information', pos=(100, 100) , size=(400, 300))
        wx.StaticText(self, -1, selected_process, (10, 10))
        button = wx.Button(self, -1, "Confirm", (100, 150))
        self.Bind(wx.EVT_BUTTON, self.confirm, button)
    def confirm(self, event):
        self.Destroy()

class Process:
    def __init__(self, type, px, py):
        # p_type
        # 1 = rec, 2 = circle, 3 = delivery, 4 = x, 5 = money 
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
    mv = M_frame(None, -1, 'POSCO', pos=(100, 50), size=(1024, 768))
    mv.Show(True)
    app.MainLoop()
