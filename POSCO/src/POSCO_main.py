from __future__ import division

import wx

class P_frame(wx.Frame):
    def __init__(self, parent, ID, title, pos, size, style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        f_size_x, f_size_y = size
        self.base = wx.Panel(self, -1, pos=(0, 0), size=(f_size_x, f_size_y))
        
        p_p = wx.Panel(self, -1, pos=(f_size_x*1/6, 100), size=(f_size_x*2/3, 150))
        p_p.SetBackgroundColour(wx.Colour(64, 117, 180, 100))
        p_p.SetFont(wx.Font(40, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        m_title = wx.StaticText(p_p, -1, 'POSCO SYSTEM')
        p_x, p_y = p_p.GetSize()
        s_x, s_y = m_title.GetSize()
        m_title.SetPosition(((p_x-s_x)/2 ,(p_y-s_y)/2))
        m_title.SetForegroundColour(wx.Colour(255, 255, 255, 100))
        
        
        
        
    

if __name__ == '__main__':
    app = wx.PySimpleApp()
    mv = P_frame(None, -1, 'POSCO', pos=(100, 50), size=(1024, 768))
    mv.Show(True)
    app.MainLoop()