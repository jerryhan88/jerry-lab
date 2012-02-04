import wx

#standard size of 40ft container
container_hs = 20
container_vs = 5

#frame
frame_milsec = 1000 / 15

#lambda function
pyslot = lambda x: (int(x[4:6]), int(x[7:9]), int(x[10:12]))
pvslot = lambda x: (int(x[2:4]), int(x[5:7]), int(x[8:10]))

def change_b_color(gc, color):
    if color == 'orange':
        r, g, b = 228, 108, 10
    elif color == 'white':
        r, g, b = 255, 255, 255
    elif color == 'black':
        r, g, b = 0, 0, 0
    brushclr = wx.Colour(r, g, b)
    gc.SetBrush(wx.Brush(brushclr))
