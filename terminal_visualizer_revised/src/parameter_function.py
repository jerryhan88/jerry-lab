from __future__ import division
import wx

# standard size of 40ft container
container_hs = 20
container_vs = 5

#visualizer horizontal size
l_sx = container_hs * 54.8

# visualizer control
frame_milsec = 1000 / 15
play_speed = 1.0
play_x = 3.0

# num of resource
total_num_bitt = 19
total_num_qb = 4
total_num_b = 16

def change_b_color(gc, color):
    if color == 'orange': r, g, b = 228, 108, 10
    elif color == 'white': r, g, b = 255, 255, 255
    elif color == 'black': r, g, b = 0, 0, 0
    elif color == 'purple': r, g, b = 90, 14, 160
    elif color == 'red': r, g, b = 255, 0, 0
    elif color == 'green': r, g, b = 0, 255, 0
    elif color == 'blue': r, g, b = 0, 0, 255
    brushclr = wx.Colour(r, g, b)
    gc.SetBrush(wx.Brush(brushclr))