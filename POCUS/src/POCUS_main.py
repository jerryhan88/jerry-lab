#-*- coding: cp949 -*-
from __future__ import division
import wx, color_src, datetime, math
#from process import Process_info_Viewer
orange = color_src.orange
purple = color_src.purple
white = color_src.white
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
#        pro_p.SetBackgroundColour(white)
        wx.StaticBox(pro_p, -1, "", pos=(5, 0), size=(p_sx - 7, p_sy))
        
        self.make_title_p(pro_p, 'pic/project_title.png', 7, 10, p_sx - 12, 60)
        
        btn_p = wx.Panel(pro_p, -1, pos=(7, p_sy - 40), size=(p_sx - 9, 40))
        btn_p.SetBackgroundColour(wx.Colour(189, 207, 231, 100))
        
        add_btn = self.make_pro_btn(btn_p, 'pic/+.png', p_sx - 85, 2)
        add_btn.Bind(wx.EVT_BUTTON, self.project_add)
        remove_btn = self.make_pro_btn(btn_p, 'pic/-.png', p_sx - 50, 2)
        remove_btn.Bind(wx.EVT_BUTTON, self.project_remove)
    
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
        sx, sy = t_p.GetSize()
        m_p = wx.Panel(proce_p, -1, pos=(px, py + sy), size=(70, p_sy - sy - 60))
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
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    mv = M_frame(None, -1, 'POCUS', pos=(100, 50), size=(1024, 768))
    mv.Show(True)
    app.MainLoop()
