#-*- coding: cp949 -*-
from __future__ import division
from POCUS_main import M_frame
import wx, color_src
deco_strip_sy = 50
orange = color_src.orange
purple = color_src.purple
white = color_src.white
dark_blue_clr = wx.Colour(222, 239, 247)

class L_frame(wx.Frame):
    def __init__(self, parent, ID, title, pos, size, style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        f_size_x, f_size_y = self.GetSize()
        base = wx.Panel(self, -1)
        b_img1 = wx.Image('pic/login/login_back1.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        bg1 = wx.StaticBitmap(base, -1, b_img1)
        px, py = bg1.GetPosition()
        sx, sy = bg1.GetSize()
        b_img2 = wx.Image('pic/login/login_back2.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        bg2 = wx.StaticBitmap(base, -1, b_img2, pos=(px, py + sy))

        px, py = bg2.GetPosition()
        sx, sy = bg2.GetSize()
        id_pw_p = wx.Panel(base, -1, pos=(px + sx, py), size=(f_size_x - sx, sy))
        id_pw_p.SetBackgroundColour(dark_blue_clr)
        
        id_p = wx.Panel(id_pw_p, -1, pos=(15, 38), size=(300, 45))
        id_p.SetBackgroundColour(orange)
        px, py = id_p.GetPosition()
        sx, sy = id_p.GetSize()
       
        pw_p = wx.Panel(id_pw_p, -1, pos=(px, py + sy + 20), size=(300, 45))
        pw_p.SetBackgroundColour(orange)
        
        id_and_pw_font = wx.Font(23, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        id_t = wx.StaticText(id_p, -1, 'I D', pos=(30, 3))
        id_t.SetForegroundColour(white)
        id_t.SetFont(id_and_pw_font)
        self.input_id = wx.TextCtrl(id_p, -1, 'HeadFirst', pos=(100, 2), size=(198, sy - 4))
        self.input_id.SetBackgroundColour(dark_blue_clr)
        self.input_id.SetFont(id_and_pw_font)
        pw_t = wx.StaticText(pw_p, -1, 'PW', pos=(26, 3))
        pw_t.SetFont(id_and_pw_font)
        pw_t.SetForegroundColour(white)
        self.input_pw = wx.TextCtrl(pw_p, -1, '1234', pos=(100, 2), size=(198, sy - 4), style=wx.TE_PASSWORD)
        self.input_pw.SetBackgroundColour(dark_blue_clr)
        self.input_pw.SetFont(id_and_pw_font)
        
        px, py = pw_p.GetPosition()
        sx, sy = pw_p.GetSize()
        
        loginBtn = wx.Image('pic/login/loginBtn.png', wx.BITMAP_TYPE_PNG)
        l_btn = wx.BitmapButton(id_pw_p, -1, bitmap=wx.BitmapFromImage(loginBtn), pos=(px + sx - 130, py + sy + 20), style=wx.NO_BORDER)
        base.Bind(wx.EVT_BUTTON, self.log_in, l_btn)
        
        px, py = bg2.GetPosition()
        sx, sy = bg2.GetSize()
        pre_b_img3 = wx.Image('pic/login/login_back3.png', wx.BITMAP_TYPE_PNG)
        w = pre_b_img3.GetWidth()
        h = pre_b_img3.GetHeight()
        b_img3 = wx.BitmapFromImage(pre_b_img3.Scale(w, h * 0.55))
        bg3 = wx.StaticBitmap(base, -1, b_img3, pos=(px, py + sy))
        c_t = wx.StaticText(base, -1, 'Copyright 2012 HeadFirst. Pusan Univ. All right reserved.')
        c_t_sx, c_t_sy = c_t.GetSize()
        c_t.SetPosition(((f_size_x - c_t_sx) / 2, f_size_y - c_t_sy))
        c_t.SetPosition((f_size_x - c_t_sx - 10, 718))
        
    def log_in(self, evt):
        mf = M_frame(None, -1, 'POSCO', pos=(0, 0), size=(1024, 768))
        mf.Show(True)
        self.Close()

if __name__ == '__main__':
    app = wx.PySimpleApp()
    mv = L_frame(None, -1, 'POCUS', pos=(100, 100), size=(1024, 768))
    mv.Show(True)
    app.MainLoop()
