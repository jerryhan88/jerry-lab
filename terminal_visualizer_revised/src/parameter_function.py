from __future__ import division
import wx

# standard size of 40ft container
container_hs = 20
container_vs = 5
#container_hs = int(12.192)
#container_vs = int(2.438)

#visualizer horizontal size
l_sx = container_hs * 54.8

# visualizer control
frame_milsec = 1000 / 15
play_speed = 30.0
play_x = 10.0

# num of resource
total_num_bitt = 19
total_num_qb = 4
total_num_b = 16

#lambda function

def calc_proportional_pos(start_pos, target_pos, start_time, target_time, simul_clock):
    time_interval = target_time - start_time
    assert 0 <= time_interval.total_seconds() < 3600 * 24, False
    return (target_pos - start_pos) * (simul_clock - start_time).total_seconds() / time_interval.total_seconds()

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
    
def find_target_evt(evt_id, evt_seq, simul_clock):
    evt_end = False
    if evt_id == -1:
        evt = evt_seq[evt_id + 1]
    else:
        evt = evt_seq[evt_id]
    while evt.dt < simul_clock:
        evt_id += 1
        if evt_id == len(evt_seq) - 1: 
            evt_end = True
            break
        evt = evt_seq[evt_id]
    return evt_id + 1, evt_end
