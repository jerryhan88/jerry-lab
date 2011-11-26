from __future__ import division

import wx

class P_frame(wx.Frame):
    def __init__(self, parent, ID, title, pos, size, style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        f_size_x, f_size_y = size
        self.base = wx.Panel(self, -1, pos=(0, 0), size=(f_size_x, f_size_y))
        
        p_p = wx.Panel(self, -1, pos=(f_size_x * 1 / 6, 100), size=(f_size_x * 2 / 3, 150))
        p_p.SetBackgroundColour(wx.Colour(64, 117, 180, 100))
        p_p.SetFont(wx.Font(40, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        p_p_px, p_p_py = p_p.GetPosition()
        p_p_sx, p_p_sy = p_p.GetSize()
        m_title = wx.StaticText(p_p, -1, 'POSCO SYSTEM')
        t_x, t_y = m_title.GetSize()
        m_title.SetPosition(((p_p_sx - t_x) / 2 , (p_p_sy - t_y) / 2))
        m_title.SetForegroundColour(wx.Colour(255, 255, 255, 100))
                
        self.input_id = wx.TextCtrl(self, -1, '200727196', size=(p_p_sx / 5, 40))
        input_id_sx, input_id_sy = self.input_id.GetSize()
        self.input_id.SetPosition((p_p_px + p_p_sx - input_id_sx, p_p_py + p_p_sy + input_id_sy * 1.5))
        input_id_px, input_id_py = self.input_id.GetPosition()
        self.input_id.SetFont(wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        id_p = wx.Panel(self, -1, size=(p_p_sx / 6, 40))
        id_p.SetBackgroundColour(wx.Colour(64, 117, 180, 100))
        id_p_sx, id_p_sy = id_p.GetSize()
        id_p.SetPosition((input_id_px - id_p_sx - 15, input_id_py))
        id_p_px, id_p_py = id_p.GetPosition()
        id_p.SetFont(wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        id_t = wx.StaticText(id_p, -1, 'I D')
        id_x, id_y = id_t.GetSize()
        id_t.SetForegroundColour(wx.Colour(255, 255, 255, 100))
        id_t.SetPosition(((id_p_sx - id_x) / 2 , (id_p_sy - id_y) / 2))
    
        
        ps_p = wx.Panel(self, -1, size=(p_p_sx / 6, 40))
        ps_p.SetBackgroundColour(wx.Colour(64, 117, 180, 100))
        ps_p_sx, ps_p_sy = ps_p.GetSize()
        ps_p.SetPosition((id_p_px, id_p_py + id_p_sy + 15))
        ps_p_px, ps_p_py = ps_p.GetPosition()
        ps_p.SetFont(wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        pw_t = wx.StaticText(ps_p, -1, 'P W')
        pw_x, pw_y = pw_t.GetSize()
        pw_t.SetForegroundColour(wx.Colour(255, 255, 255, 100))
        pw_t.SetPosition(((ps_p_sx - pw_x) / 2 , (ps_p_sy - pw_y) / 2))
        self.input_pw = wx.TextCtrl(self, -1, '1234', size=(p_p_sx / 5, 40), style=wx.TE_PASSWORD)
        input_pw_sx, input_pw_sy = self.input_pw.GetSize()
        self.input_pw.SetPosition((ps_p_px + ps_p_sx + 15, ps_p_py))
        self.input_pw.SetFont(wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        l_btn = wx.Button(self.base, -1, "Log in", pos=(ps_p_px + (15 + input_pw_sx / 2), ps_p_py + 70), size=(80, 40))
        l_btn.SetFont(wx.Font(17, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        l_btn_px, l_btn_py = l_btn.GetPosition()
        l_btn_sx, l_btn_sy = l_btn.GetSize() 
         
        su_btn = wx.Button(self.base, -1, "Sign up a new POSCO Account", pos=(ps_p_px - 30, l_btn_py + l_btn_sy + 30), size=(ps_p_sx + input_id_sx + 15 + 60, 40))
        su_btn.SetFont(wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        su_btn_px, su_btn_py = su_btn.GetPosition()
        su_btn_sx, su_btn_sy = su_btn.GetSize()
        
        ca_btn = wx.Button(self.base, -1, "Can't access your account", pos=(su_btn_px, su_btn_py + su_btn_sy + 5), size=(su_btn_sx, su_btn_sy))
        ca_btn.SetFont(wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        
        c_t = wx.StaticText(self.base, -1, 'Copyright 2011 HeadFirst. Pusan Univ. All right reserved.')
        c_t_sx, c_t_sy = c_t.GetSize()
        c_t.SetPosition(((f_size_x - c_t_sx) / 2, f_size_y - 150))
        
        
        
# self.button1 = wx.BitmapButton(self.panel1, id=-1, bitmap=image1,
#            pos=(10, 20), size = (image1.GetWidth()+5, image1.GetHeight()+5))
#        self.button1.Bind(wx.EVT_BUTTON, self.button1Click)

if __name__ == '__main__':
    app = wx.PySimpleApp()
    mv = P_frame(None, -1, 'POSCO', pos=(100, 50), size=(1024, 768))
    mv.Show(True)
    app.MainLoop()
