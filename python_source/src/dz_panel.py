from __future__ import division

import wx

DEFAULT_FONT_SIZE = 8  # NOTE strange! Effect of size is not continuous.

class DragZoomPanel(wx.Panel):
    '''
    CAUTION Do not access members directly!!!
    
    scale: current scale
    scale_ref: reference scale level, e.g., a line will have a pixel width at scale with scale_ref
    
    Transformation
      dp = s * lp + t, where dp, lp, s, and t are device point, logical point, scale factor,
        and translation factor, respectively.
    
    NOTE In the current version of wxPython 2.8.12.1, GraphicsContext conflicts with
         SetDoubleBuffered(True). Hence, memory buffer is used to prevent flickering.
    '''
    def __init__(self, parent, wid, scale_ref=1, init_scale=1, init_translate=(0, 0), scale_inc=2 ** (1 / 2), *args, **kwargs):
        wx.Panel.__init__(self, parent, wid, *args, **kwargs)
        self.scale, self.scale_ref, self.scale_inc = init_scale, scale_ref, scale_inc
        (self.translate_x, self.translate_y), self.translate_mode = init_translate, False
        # event binding
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
        # prepare stock objects.
        self.default_pen = self.create_pen(wx.BLACK, 1)
        self.default_font = self.create_font(DEFAULT_FONT_SIZE, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
    def OnSize(self, e):
        w, h = self.GetSize()
        w, h = max(100, w), max(100, h)
        self.mem_buffer = wx.EmptyBitmap(w, h, 32)
        self.RefreshGC(False)
    def OnPaint(self, _):
        wx.BufferedPaintDC(self, self.mem_buffer)
    def RefreshGC(self, update=True):
        # TODO think of update, because all the drawing work is done even when update is False!!
        mdc = wx.MemoryDC(self.mem_buffer)
        mdc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        mdc.Clear()
        gc = wx.GraphicsContext.Create(mdc)
        gc.SetPen(self.default_pen)
        gc.SetFont(self.default_font, wx.BLACK)
        
        oldTransform = gc.GetTransform()
        
        gc.Translate(self.translate_x, self.translate_y)
        gc.Scale(self.scale, self.scale)
        self.OnDraw(gc)
        
        gc.SetTransform(oldTransform)
        # TODO
        # why excute 'gc.Scale(0, 0)'? 
        gc.Scale(0, 0)
        #
        self.OnDrawDevice(gc)
        
        self.Refresh(False)
        if update:
            self.Update()
    def OnDraw(self, gc):
        pass

    def OnLeftDown(self, e):
        self.translate_mode, self.prev_x, self.prev_y = True, e.GetX(), e.GetY()
        self.SetFocus()
        self.CaptureMouse()
    def OnMotion(self, e):
        if self.translate_mode:
            dx, dy = e.GetX() - self.prev_x, e.GetY() - self.prev_y
            self.translate_x += dx
            self.translate_y += dy
            self.prev_x, self.prev_y = e.GetX(), e.GetY()
            self.RefreshGC()
    def OnLeftUp(self, _):
        if self.translate_mode:
            self.translate_mode = False
            self.ReleaseMouse()
    def OnMouseWheel(self, e):
        self.set_scale(self.scale * (self.scale_inc if e.GetWheelRotation() > 0 else (1 / self.scale_inc)), e.GetX(), e.GetY())
        self.RefreshGC()

    def set_scale(self, s, x, y):
        '''
        change scale based on (x, y) as center.
        '''
        old_scale, self.scale = self.scale, s
        self.translate_x = x - self.scale / old_scale * (x - self.translate_x)
        self.translate_y = y - self.scale / old_scale * (y - self.translate_y)
    def lp_to_dp(self, lx, ly):
        '''
        from logical point to device point: dp = s * lp + t
        '''
        return int(self.scale * lx + self.translate_x + 0.5), int(self.scale * ly + self.translate_y + 0.5)
    def dp_to_lp(self, dx, dy):
        '''
        from device point to logical point: lp = (dp - t) / s
        '''
        return (dx - self.translate_x) / self.scale, (dy - self.translate_y) / self.scale

    def create_pen(self, color, width):
        return wx.Pen(color, max(1, int(width / self.scale_ref + 0.5)))
    def create_font(self, size, family, style, weight):
        return wx.Font(max(1, int(size / self.scale_ref + 0.5)), family, style, weight)
