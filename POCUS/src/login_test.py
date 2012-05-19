#-*- coding: cp949 -*-
from __future__ import division
import wx, color_src
deco_strip_sy = 50
orange = color_src.orange
purple = color_src.purple
white = color_src.white
dark_blue_clr = wx.Colour(219, 238, 244)

class L_frame(wx.Frame):
    def __init__(self, parent, ID, title, pos, size, style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        base = wx.Panel(self, -1)
        pre_main_img = wx.Image('pic/login_back1.png', wx.BITMAP_TYPE_PNG)
        sx, sy = base.GetSize()
#        w = pre_main_img.GetWidth()
        h = pre_main_img.GetHeight()
        print h
#        scl = sx / w
        main_img = wx.BitmapFromImage(pre_main_img)
        wx.StaticBitmap(base, -1, main_img)
        
#        id_input_p = wx.Panel(base, -1, size=(100, 100))
#        id_input_p.SetBackgroundColour(orange)
        
    def log_in(self, evt):
#        mf = M_frame(None, -1, 'POSCO', pos=(0, 0), size=(1024, 768))
#        mf.Show(True)
        self.Close()

if __name__ == '__main__':
    app = wx.PySimpleApp()
    mv = L_frame(None, -1, 'POCUS', pos=(100, 100), size=(1024, 768))
    mv.Show(True)
    app.MainLoop()
