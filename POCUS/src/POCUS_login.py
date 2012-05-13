#-*- coding: cp949 -*-
from __future__ import division
import wx, color_src
deco_strip_sy = 50
orange = color_src.orange
purple = color_src.purple
white = color_src.white
#id_and_pw_t_color = wx.Colour(86, 83, 87)
dark_blue_clr = wx.Colour(219, 238, 244)
class L_frame(wx.Frame):
    def __init__(self, parent, ID, title, pos, size, style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        f_size_x, f_size_y = size
        self.base = wx.Panel(self, -1, pos=(0, 0), size=(f_size_x, f_size_y)) 
        px, py = self.base.GetPosition()
        top_p = wx.Panel(self, -1, pos=(px, py), size=(f_size_x, deco_strip_sy))
        top_p.SetBackgroundColour(orange)
        btm_p1 = wx.Panel(self, -1, pos=(px, f_size_y - deco_strip_sy * 3), size=(f_size_x, deco_strip_sy))
        btm_p1.SetBackgroundColour(orange)
        btm_p2 = wx.Panel(self, -1, pos=(px, f_size_y - deco_strip_sy * 2), size=(f_size_x, deco_strip_sy))
        btm_p2.SetBackgroundColour(purple)
        px, py = top_p.GetPosition()
        _, sy = top_p.GetSize()
        pic_sy = f_size_y - deco_strip_sy * 4
         
        main_pic_p = wx.Panel(self.base, -1, pos=(px, py + sy), size=(f_size_x, pic_sy))
        main_pic_p.SetBackgroundColour(white)
        pre_main_img = wx.Image('pic/login_main.png', wx.BITMAP_TYPE_PNG)
        sx, sy = main_pic_p.GetSize()
        w = pre_main_img.GetWidth()
        h = pre_main_img.GetHeight()
        scl = sx / w
        main_img = wx.BitmapFromImage(pre_main_img.Scale(w * scl, h * scl * 0.85))
        m_img = wx.StaticBitmap(main_pic_p, -1, main_img)
        sx, sy = m_img.GetSize() 
        
        id_pw_p_sy = pic_sy - sy
        id_pw_p = wx.Panel(main_pic_p, -1, pos=(px - 2, sy), size=(f_size_x - 4, id_pw_p_sy))
        id_pw_p.SetBackgroundColour(dark_blue_clr)
        
        pre_m_text_img = wx.Image('pic/m_text.png', wx.BITMAP_TYPE_PNG)
        w = pre_m_text_img.GetWidth()
        h = pre_m_text_img.GetHeight()
        scl = 0.66
        m_text_img = wx.BitmapFromImage(pre_m_text_img.Scale(w * scl, h * scl))
        m_text = wx.StaticBitmap(id_pw_p, -1, m_text_img, pos=(80, 30))
        px, py = m_text.GetPosition()
        sx, sy = m_text.GetSize()
        
        id_p = wx.Panel(id_pw_p, -1, pos=(px + sx + 160, py + 10), size=(300, 45))
        id_p.SetBackgroundColour(orange)
        px, py = id_p.GetPosition()
        sx, sy = id_p.GetSize()
       
        pw_p = wx.Panel(id_pw_p, -1, pos=(px, py + sy + 20), size=(300, 45))
        pw_p.SetBackgroundColour(orange)
        
        id_and_pw_font = wx.Font(23, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        id_t = wx.StaticText(id_p, -1, 'I D', pos=(30, 3))
        id_t.SetFont(id_and_pw_font)
        self.input_id = wx.TextCtrl(id_p, -1, 'HeadFirst', pos=(100, 2), size=(198, sy - 4))
        self.input_id.SetFont(id_and_pw_font)
        
        pw_t = wx.StaticText(pw_p, -1, 'PW', pos=(26, 3))
        pw_t.SetFont(id_and_pw_font)
        self.input_pw = wx.TextCtrl(pw_p, -1, '1234', pos=(100, 2), size=(198, sy - 4), style=wx.TE_PASSWORD)
        self.input_pw.SetFont(id_and_pw_font)
        
        px, py = pw_p.GetPosition()
        sx, sy = pw_p.GetSize()
        
        l_btn = wx.Button(id_pw_p, -1, "Log in", pos=(px + sx - 80, py + sy+20), size=(80, 40))
        l_btn.SetFont(wx.Font(17, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        l_btn.SetBackgroundColour(white)
        self.base.Bind(wx.EVT_BUTTON, self.log_in, l_btn)
        
        c_t = wx.StaticText(self.base, -1, 'Copyright 2012 HeadFirst. Pusan Univ. All right reserved.')
        c_t_sx, c_t_sy = c_t.GetSize()
        c_t.SetPosition(((f_size_x - c_t_sx) / 2, f_size_y - c_t_sy))
        c_t.SetPosition((f_size_x - c_t_sx - 20, 718))

        
    def log_in(self, evt):
#        mf = M_frame(None, -1, 'POSCO', pos=(0, 0), size=(1024, 768))
#        mf.Show(True)
        self.Close()

if __name__ == '__main__':
    app = wx.PySimpleApp()
    mv = L_frame(None, -1, 'POCUS', pos=(100, 100), size=(1024, 768))
    mv.Show(True)
    app.MainLoop()
