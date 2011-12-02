from __future__ import division

import wx
from m_frame import M_frame

class L_frame(wx.Frame):
    def __init__(self, parent, ID, title, pos, size, style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        f_size_x, f_size_y = size
        self.base = wx.Panel(self, -1, pos=(0, 0), size=(f_size_x, f_size_y))
        self.base.SetBackgroundColour(wx.Colour(21, 16, 23, 100))
        
        bottom_p = wx.Panel(self.base, -1, pos=(0, f_size_y - 80), size=(f_size_x, 80))
        bottom_p.SetBackgroundColour(wx.Colour(116, 28, 96, 100))
        
        p_p = wx.Panel(self.base, -1, size=(768, 232))
        p_p_sx, p_p_sy = p_p.GetSize()
        p_p.SetPosition(((f_size_x - p_p_sx) / 2, 75))
        p_p_px, p_p_py = p_p.GetPosition()        
        posco_t_img = wx.Image('pic/posco_background.png', wx.BITMAP_TYPE_PNG)
        wx.StaticBitmap(p_p, -1, wx.BitmapFromImage(posco_t_img))
        
        id_and_pw_font = wx.Font(23, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        id_and_pw_t_color = wx.Colour(86, 83, 87)
        id_and_pw_p_size = (p_p_sx / 6, 40)
        id_and_pw_input_color = wx.Colour(210, 193, 235, 100)
        id_and_pw_input_font = wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        id_and_pw_input_size = (p_p_sx / 5, 40)
        
        id_p = wx.Panel(self.base, -1, pos=(p_p_px + p_p_sx/2-50, p_p_py + p_p_sy + 60), size=id_and_pw_p_size)
        id_p_px, id_p_py = id_p.GetPosition()
        id_p_sx, id_p_sy = id_p.GetSize()        
        id_p.SetFont(id_and_pw_font)
        id_t = wx.StaticText(id_p, -1, 'I D')
        id_t.SetForegroundColour(id_and_pw_t_color)
        id_x, id_y = id_t.GetSize()
        id_t.SetPosition(((id_p_sx - id_x) / 2 , (id_p_sy - id_y) / 2))
        self.input_id = wx.TextCtrl(self.base, -1, 'HeadFirst', pos=(id_p_px + id_p_sx, id_p_py), size=id_and_pw_input_size)
        input_id_px, input_id_py = self.input_id.GetPosition()
        input_id_sx, input_id_sy = self.input_id.GetSize()
        self.input_id.SetFont(id_and_pw_input_font)
        self.input_id.SetBackgroundColour(id_and_pw_input_color)

        pw_p = wx.Panel(self.base, -1, size=id_and_pw_p_size)
        pw_p.SetPosition((id_p_px, id_p_py + id_p_sy + 10))
        pw_p_px, pw_p_py = pw_p.GetPosition()
        pw_p_sx, pw_p_sy = pw_p.GetSize()
        pw_p.SetFont(id_and_pw_font)
        pw_t = wx.StaticText(pw_p, -1, 'PW')
        pw_x, pw_y = pw_t.GetSize()
        pw_t.SetForegroundColour(id_and_pw_t_color)
        pw_t.SetPosition(((pw_p_sx - pw_x) / 2 , (pw_p_sy - pw_y) / 2))
        self.input_pw = wx.TextCtrl(self.base, -1, '1234', pos=(pw_p_px + pw_p_sx, pw_p_py), size=id_and_pw_input_size, style=wx.TE_PASSWORD)
        input_pw_px, input_pw_py = self.input_pw.GetPosition()
        input_pw_sx, input_pw_sy = self.input_pw.GetSize()
        self.input_pw.SetFont(id_and_pw_input_font)
        self.input_pw.SetBackgroundColour(id_and_pw_input_color)
        
        
        l_btn = wx.Button(self.base, -1, "Log in", pos=(input_id_px + input_id_sx + 30, id_p_py + (pw_p_py - id_p_py) / 2), size=(80, 40))
        l_btn.SetFont(wx.Font(17, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        l_btn.SetBackgroundColour(id_and_pw_t_color)
        l_btn.SetForegroundColour(wx.Colour(255, 255, 255))
        self.base.Bind(wx.EVT_BUTTON, self.log_in, l_btn)
        
        sign_up_txt = wx.StaticText(self.base, -1, "Sign up a new POSCO Account", pos=(input_pw_px, input_pw_py + input_pw_sy+40), size=(pw_p_sx + input_id_sx + 15 + 60, 40))
        sign_up_txt_px, sign_up_txt_py = sign_up_txt.GetPosition()
        sign_up_txt_sx, sign_up_txt_sy = sign_up_txt.GetSize()
        ca_txt = wx.StaticText(self.base, -1, "Can't access your account", pos=(sign_up_txt_px, sign_up_txt_py + sign_up_txt_sy + 10), size=(sign_up_txt_sx, sign_up_txt_sy))
        
        etc_txt_font = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        etc_txt_color = wx.Colour(174, 36, 140)
        for x in [sign_up_txt, ca_txt]:
            x.SetFont(etc_txt_font)
            x.SetForegroundColour(etc_txt_color)

        c_t = wx.StaticText(self.base, -1, 'Copyright 2011 HeadFirst. Pusan Univ. All right reserved.')
        c_t_sx, c_t_sy = c_t.GetSize()
        c_t.SetPosition(((f_size_x - c_t_sx) / 2, f_size_y - 150))
        
#        id_p.SetBackgroundColour(wx.Colour(64, 117, 180, 100))        
#        pw_p.SetBackgroundColour(wx.Colour(64, 117, 180, 100))
        
    def log_in(self, evt):
        mf = M_frame(None, -1, 'POSCO', pos=(100, 50), size=(1024, 768))
        mf.Show(True)
        self.Close()

if __name__ == '__main__':
    app = wx.PySimpleApp()
    mv = L_frame(None, -1, 'POSCO', pos=(100, 50), size=(1024, 768))
    mv.Show(True)
    app.MainLoop()
