from __future__ import division
import wx, time
import  wx.lib.anchors as anchors
from datetime import datetime, timedelta
from parameter_function import pyslot, pvslot
from parameter_function import container_hs, container_vs, l_sx, frame_milsec
import initializer
from classes import Bitt, QC_buffer, Block, TP

Play_speed = 4.0

Bitts = {}
QBs = {}
Blocks = {}
TPs = {}

class Input_dialog(wx.Dialog):


    def __init__(self, parent, name, size=(570, 180), pos=(400, 300)):
        wx.Dialog.__init__(self, None, -1, 'Monitoring Input', pos , size)
        wx.StaticText(self, -1, 'Vessel', (15, 10))
        wx.StaticText(self, -1, 'Voyage', (450, 10))
        wx.StaticText(self, -1, 'Date', (15, 50))
        
        v_name = ['HANJIN', 'MAERSK']
        vo_name = ['01', '02', '03', '04', '05', '06', '07']
        year = [str(x) for x in xrange(2005, 2012)]
        month = [str(x) for x in xrange(1, 13)]
        day = [str(x) for x in xrange(1, 32)]
        
        self.v_name_ch, self.vo_name_ch = wx.Choice(self, -1, (60, 10), choices=v_name), wx.Choice(self, -1, (510, 10), choices=vo_name)
        self.v_name_ch.SetSelection(0), self.vo_name_ch.SetSelection(1)
        
        self.sy_ch, self.sm_ch, self.sd_ch = wx.Choice(self, -1, (60, 50), choices=year), wx.Choice(self, -1, (120, 50), choices=month), wx.Choice(self, -1, (165, 50), choices=day)
        self.ey_ch, self.em_ch, self.ed_ch = wx.Choice(self, -1, (320, 50), choices=year), wx.Choice(self, -1, (380, 50), choices=month), wx.Choice(self, -1, (425, 50), choices=day)
        self.sy_ch.SetSelection(6), self.sm_ch.SetSelection(7), self.sd_ch.SetSelection(22)
        self.ey_ch.SetSelection(6), self.em_ch.SetSelection(7), self.ed_ch.SetSelection(22) 
        
        #test Vessel
#        self.sh_txt, self.smi_txt, self.ss_txt = wx.TextCtrl(self, -1, "09", (210, 50), size=(25, -1)), wx.TextCtrl(self, -1, "34", (240, 50), size=(25, -1)), wx.TextCtrl(self, -1, "40", (270, 50), size=(25, -1))

        #test QC
        self.sh_txt, self.smi_txt, self.ss_txt = wx.TextCtrl(self, -1, "09", (210, 50), size=(25, -1)), wx.TextCtrl(self, -1, "59", (240, 50), size=(25, -1)), wx.TextCtrl(self, -1, "40", (270, 50), size=(25, -1))
        
        #test YC
#        self.sh_txt, self.smi_txt, self.ss_txt = wx.TextCtrl(self, -1, "10", (210, 50), size=(25, -1)), wx.TextCtrl(self, -1, "05", (240, 50), size=(25, -1)), wx.TextCtrl(self, -1, "08", (270, 50), size=(25, -1))
        
        self.eh_txt, self.emi_txt, self.es_txt = wx.TextCtrl(self, -1, "15", (470, 50), size=(25, -1)), wx.TextCtrl(self, -1, "10", (500, 50), size=(25, -1)), wx.TextCtrl(self, -1, "20", (530, 50), size=(25, -1))
        
        wx.StaticText(self, -1, ':', (236, 50)), wx.StaticText(self, -1, ':', (266, 50)), wx.StaticText(self, -1, '-', (305, 50)), wx.StaticText(self, -1, ':', (496, 50)), wx.StaticText(self, -1, ':', (526, 50))
        
        setting_btn = wx.Button(self, -1, "setting", (480, 90))
        setting_btn.SetConstraints(anchors.LayoutAnchors(setting_btn, False, True, False, False))
        
        self.Bind(wx.EVT_BUTTON, self.setting, setting_btn)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Show(True)
        
    def OnClose(self, event):
        self.Destroy()
        
    def setting(self, event):
        self.vn, self.vo = self.v_name_ch.GetString(self.v_name_ch.GetSelection()), self.vo_name_ch.GetString(self.vo_name_ch.GetSelection())

        self.sy, self.sm, self.sd = self.sy_ch.GetString(self.sy_ch.GetSelection()), self.sm_ch.GetString(self.sm_ch.GetSelection()), self.sd_ch.GetString(self.sd_ch.GetSelection())
        self.sh, self.smi, self.ss = self.sh_txt.GetValue(), self.smi_txt.GetValue(), self.ss_txt.GetValue()
        
        self.ey, self.em, self.ed = self.ey_ch.GetString(self.ey_ch.GetSelection()), self.em_ch.GetString(self.em_ch.GetSelection()), self.ed_ch.GetString(self.ed_ch.GetSelection())
        self.eh, self.emi, self.es = self.eh_txt.GetValue(), self.emi_txt.GetValue(), self.es_txt.GetValue()
        
        win = MainFrame(self)
        win.Show(True)
        self.Show(False)

class MainFrame(wx.Frame):
    def __init__(self, input_info):
        wx.Frame.__init__(self, None, -1, 'Monitoring', size=(1024, 768))
        self.input_info = input_info
        f_sx, f_sy = self.GetSize()
        self.SetBackgroundColour(wx.Colour(236, 233, 216))
        self.SetAutoLayout(True)
        
        sy, sm, sd = int(input_info.sy), int(input_info.sm), int(input_info.sd) 
        sh, smi, ss = int(input_info.sh), int(input_info.smi), int(input_info.ss) 
        
        ey, em, ed = int(input_info.ey), int(input_info.em), int(input_info.ed)
        eh, emi, es = int(input_info.eh), int(input_info.emi), int(input_info.es)
        
        self.start_time, self.end_time = datetime(sy, sm, sd, sh, smi, ss), datetime(ey, em, ed, eh, emi, es)
        
        vechicles, containers = initializer.run(self.start_time, self.end_time)

        self.timer = wx.Timer(self)
        self.timer.Start(frame_milsec)
        self.simul_clock = datetime(sy, sm, sd, sh, smi, ss)
        self.saved_time = time.time()
        
        self.play_speed = Play_speed
        self.isReverse_play = False
        self.simul_clock_saved = None
                
        ip_py, ip_sy = 0 , 50
        vp_py, vp_sy = ip_py + ip_sy , 600
        cp_py, cp_sy = vp_py + vp_sy , f_sy - (vp_sy + ip_sy)
        
        Input_View_Panel(self , (0, ip_py), (f_sx, ip_sy), input_info.vn, input_info.vn, self.start_time, self.end_time)
        self.vp = Viewer_Panel(self, (45, vp_py), (f_sx - 100, vp_sy), vechicles, containers)
        self.cp = Control_Panel(self, (0, cp_py), (f_sx, cp_sy))        
        self.Show(True)
        
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
    def OnTimer(self, evt):
        if self.simul_clock_saved == None:
            cur_time = time.time()
            time_interval = cur_time - self.saved_time
            if not self.isReverse_play:
                self.simul_clock += timedelta(seconds=time_interval * self.play_speed)
            else:
                self.simul_clock -= timedelta(seconds=time_interval * self.play_speed)
            self.saved_time = cur_time
        else:
            self.simul_clock = self.simul_clock_saved
            print self.simul_clock_saved
            self.simul_clock_saved = None
            self.saved_time = time.time()
        self.vp.OnTimer(evt, self.simul_clock)
        self.cp.OnTimer(evt, self.simul_clock)
        
    def OnClose(self, event):
        self.input_info.Destroy()
        self.Destroy()
        
class Input_View_Panel(wx.Panel):
    def __init__(self, parent, pos, size, v_name, v_voyage, start_time, end_time):
        wx.Panel.__init__(self, parent, -1, pos, size)
        self.SetConstraints(anchors.LayoutAnchors(self, True, True, True, False))
        
        v_txt = []
        v_txt.append(wx.StaticText(self, -1, 'Vessel', (15, 10)))
        v_txt.append(wx.StaticText(self, -1, 'Voyage', (150, 10)))
        v_txt.append(wx.StaticText(self, -1, 'Date', (360, 10)))
        v_txt.append(wx.StaticText(self, -1, v_name, (65, 10), size=(65, -1)))
        v_txt.append(wx.StaticText(self, -1, v_voyage, (215, 10), size=(25, -1)))             
        for x in v_txt:
            x.SetFont(wx.Font(13, wx.SWISS, wx.NORMAL, wx.NORMAL)) 
        
        #Date/Time
        y_name1_px = 410
        sdt_edt_txt = []
        sdt_edt_txt.append(wx.StaticText(self, -1, str(start_time.year), (y_name1_px, 10), size=(40, -1)))
        sdt_edt_txt.append(wx.StaticText(self, -1, str(start_time.month), (y_name1_px + 40, 10), size=(25, -1)))
        sdt_edt_txt.append(wx.StaticText(self, -1, str(start_time.day), (y_name1_px + 70, 10), size=(25, -1)))
        sdt_edt_txt.append(wx.StaticText(self, -1, str(start_time.hour), (y_name1_px + 100, 10), size=(25, -1)))
        sdt_edt_txt.append(wx.StaticText(self, -1, ':', (y_name1_px + 120, 10)))
        sdt_edt_txt.append(wx.StaticText(self, -1, str(start_time.minute), (y_name1_px + 135, 10), size=(25, -1)))
        sdt_edt_txt.append(wx.StaticText(self, -1, ':', (y_name1_px + 155, 10)))
        sdt_edt_txt.append(wx.StaticText(self, -1, str(start_time.second), (y_name1_px + 170, 10), size=(25, -1)))
        sdt_edt_txt.append(wx.StaticText(self, -1, '-', (620, 10)))
        y_name2_px = 640
        sdt_edt_txt.append(wx.StaticText(self, -1, str(end_time.year), (y_name2_px, 10), size=(40, -1)))
        sdt_edt_txt.append(wx.StaticText(self, -1, str(end_time.month), (y_name2_px + 40, 10), size=(25, -1)))
        sdt_edt_txt.append(wx.StaticText(self, -1, str(end_time.day), (y_name2_px + 60, 10), size=(25, -1)))
        sdt_edt_txt.append(wx.StaticText(self, -1, str(end_time.hour), (y_name2_px + 100, 10), size=(25, -1)))
        sdt_edt_txt.append(wx.StaticText(self, -1, ':', (y_name2_px + 120, 10)))
        sdt_edt_txt.append(wx.StaticText(self, -1, str(end_time.minute), (y_name2_px + 135, 10), size=(25, -1)))
        sdt_edt_txt.append(wx.StaticText(self, -1, ':', (y_name2_px + 155, 10)))
        sdt_edt_txt.append(wx.StaticText(self, -1, str(end_time.second), (y_name2_px + 170, 10), size=(25, -1)))
        for x in sdt_edt_txt:
            x.SetFont(wx.Font(10, wx.SWISS, wx.ITALIC, wx.NORMAL))
        
        for x in v_txt + sdt_edt_txt:
            x.SetConstraints(anchors.LayoutAnchors(x, False, True, False, False))

class Drag_zoom_panel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, -1, pos, size, style=wx.SIMPLE_BORDER)
        self.SetConstraints(anchors.LayoutAnchors(self, True, True, True, True))
        self.SetBackgroundColour(wx.WHITE)
        self.SetBackgroundColour(wx.WHITE)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        # size and mouse events
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
        self.translate_mode = False
        self.translate_x, self.translate_y = 0, 0
        self.scale = 1.0
#        self.InitBuffer()
        
    def OnSize(self, evt):
        self.InitBuffer()
        evt.Skip()
        
    def OnLeftDown(self, evt):
        self.translate_mode = True
        self.prev_x, self.prev_y = evt.m_x, evt.m_y
        self.CaptureMouse()
        evt.Skip()
        
    def OnMotion(self, evt):
        if self.translate_mode:
            dx, dy = evt.m_x - self.prev_x, evt.m_y - self.prev_y
            self.translate_x += dx
            self.translate_y += dy
            self.prev_x, self.prev_y = evt.m_x, evt.m_y
            self.RefreshGC()
    
    def OnLeftUp(self, evt):
        if self.translate_mode:
            self.translate_mode = False
            self.ReleaseMouse()
            
    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self, self._buffer)
        
    def OnMouseWheel(self, evt):
        zoom_scale = 1.2
        old_scale = self.scale 
        if evt.m_wheelRotation > 0:
            self.scale *= zoom_scale
            self.translate_x = evt.m_x - self.scale / old_scale * (evt.m_x - self.translate_x)
            self.translate_y = evt.m_y - self.scale / old_scale * (evt.m_y - self.translate_y) 
        else:
            self.scale /= zoom_scale
            self.translate_x = evt.m_x - self.scale / old_scale * (evt.m_x - self.translate_x)
            self.translate_y = evt.m_y - self.scale / old_scale * (evt.m_y - self.translate_y)
        self.RefreshGC()
        
    def InitBuffer(self):
        sz = self.GetClientSize()
        sz.width = max(1, sz.width)
        sz.height = max(1, sz.height)
        self._buffer = wx.EmptyBitmap(sz.width, sz.height, 32)
        dc = wx.MemoryDC(self._buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)
        self.Draw(gc)
        
    def RefreshGC(self):
        dc = wx.MemoryDC(self._buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)
        self.Draw(gc)
        self.Refresh(False)
    
    def Draw(self, gc):
        pass            
            
class Viewer_Panel(Drag_zoom_panel):
    def __init__(self, parent, pos, size, vechicles, containers):
        Drag_zoom_panel.__init__(self, parent, pos, size)
        
        self.containers = containers
        self.vessels, self.qcs, self.ycs, self.scs = vechicles
        
        self.simul_clock = parent.simul_clock
    
        # initialize
        ## set Background position
        ### set Lines deco position
        l0_py = container_vs * 31.2
        l1_py = l0_py + container_vs
        l2_py = l1_py + container_vs * 0.5
        l3_py = l2_py + container_vs * 0.5
#        l4_py = l3_py + container_vs * 2.2
        self.lines_py = [eval('l%d_py' % x) for x in xrange(4)]
        
        ### make bitts
        total_num_bitt = 19
        bit0_px = container_hs * 0.7
        for x in xrange(total_num_bitt):
            Bitts[x + 1] = Bitt(x + 1, bit0_px + container_hs * 2.95 * x, l0_py)
        
        ### make QC Buffer
        total_num_qb = 4
        for x in xrange(total_num_qb):
            if x == 0:
                QBs[x + 1] = QC_buffer(x + 1, 0, l3_py)
            else:
                QBs[x + 1] = QC_buffer(x + 1, 0, l3_py + container_vs * (8 + x * 2.2))

        ### make TP and Block
        total_num_b = 15
        block0_px, block0_py = Bitts[3].px, QBs[4].py + container_vs * 31
        for x in xrange(total_num_b):
            Blocks[x + 1] = Block(x + 1, block0_px + x * container_hs * 2.8, block0_py)
            TPs[x + 1] = TP(x + 1, block0_px + x * container_hs * 2.8 + container_vs * 2, block0_py - container_hs * 3 / 2)
        
        ### set container position
        for c in self.containers:
            c.cur_position = c.moving_seq[0][1]
            c.cur_index_in_ms = 0
            if c.cur_position[0] == 'B':
                id = int(c.cur_position[1:3])
                Blocks[id].holding_containers.append(c)
                bay_id, _, _ = pyslot(c.cur_position)
                c.hs = container_vs
                c.vs = container_hs
                if bay_id % 2 != 0:
                    c.size = '20ft'
                    c.vs /= 2
            elif c.cur_position[:2] == 'SB':
                # container in vessel
                # ex of c.moving_seq[0]: ('2011-08-23-10-00-00', 'SB05-05-12', 'STS01', 'ABCDEF', '02')
                target_v_name = c.moving_seq[0][3]
                target_v_voyage = c.moving_seq[0][4]
                target_v = None
                for v in self.vessels:
                    if v.name == target_v_name and v.voyage == target_v_voyage:
                        target_v = v
                        break
                else:
                    assert False , 'there is no target_v'
                target_v.holding_containers.append(c)
                bay_id, _, _ = pvslot(c.cur_position)
                if bay_id % 2 != 0:
                    c.size = '20ft'
                    c.hs /= 2
                    
        ### set vehicles position
        for v in self.vessels: v.cur_evt_update(v.cur_evt_id, Bitts, self.simul_clock)
        for qc in self.qcs: qc.cur_evt_update(qc.cur_evt_id, self.vessels, QBs)
        for yc in self.ycs: yc.cur_evt_update(yc.cur_evt_id, TPs, Blocks)
            
        self.InitBuffer()
    
    def OnTimer(self, evt, simul_clock):
        for v in self.vessels + self.ycs + self.qcs:
            v.OnTimer(evt, simul_clock)
        self.RefreshGC()
    
    def Draw(self, gc):
        gc.Translate(self.translate_x, self.translate_y)
        gc.Scale(self.scale, self.scale)
        old_tr = gc.GetTransform()
        
        for x in Bitts.values() + QBs.values() + TPs.values() + Blocks.values():
            gc.Translate(x.px, x.py)
            x.draw(gc)
            gc.SetTransform(old_tr)
        
        gc.SetPen(wx.Pen("black", 1))
        for py in self.lines_py:
            gc.DrawLines([(0, py), (l_sx, py)])
                
        #draw vehicle
        old_tr = gc.GetTransform()
        for x in self.vessels + self.ycs + self.qcs:# + self.scs:
            gc.Translate(x.px, x.py)
            x.draw(gc)
            gc.SetTransform(old_tr)

class Control_Panel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, -1, pos, size)
        self.SetConstraints(anchors.LayoutAnchors(self, True, False, True, True))
        
        self.timer = parent.timer
        self.simul_clock = parent.simul_clock
        self.saved_time = time.time()
        
        self.c_time = wx.StaticText(self, -1, self.simul_clock.ctime(), (100, 40))
        self.paly_speed = wx.StaticText(self, -1, str(self.Parent.play_speed) + 'x', (500, 40))

        s_img, r_img, pa_img, pl_img = wx.Image('pic/stop.bmp', wx.BITMAP_TYPE_BMP), wx.Image("pic/reverse.bmp", wx.BITMAP_TYPE_BMP), wx.Image("pic/pause.bmp", wx.BITMAP_TYPE_BMP), wx.Image("pic/play.bmp", wx.BITMAP_TYPE_BMP) 
        s_bmp, r_bmp, pa_bmp, pl_bmp = s_img.Scale(30, 30), r_img.Scale(30, 30), pa_img.Scale(30, 30), pl_img.Scale(30, 30)
        
        s_btn = wx.BitmapButton(self, -1, wx.BitmapFromImage(s_bmp), (760, 35), (s_bmp.GetWidth() + 2, s_bmp.GetHeight() + 2))
        r_btn = wx.BitmapButton(self, -1, wx.BitmapFromImage(r_bmp), (790, 35), (r_bmp.GetWidth() + 2, r_bmp.GetHeight() + 2))
        pa_btn = wx.BitmapButton(self, -1, wx.BitmapFromImage(pa_bmp), (820, 35), (pa_bmp.GetWidth() + 2, pa_bmp.GetHeight() + 2))
        pl_btn = wx.BitmapButton(self, -1, wx.BitmapFromImage(pl_bmp), (850, 35), (pl_bmp.GetWidth() + 2, pl_bmp.GetHeight() + 2))
        
        self.start_time = parent.start_time
        end_time = parent.end_time
        total_time_interval = end_time - self.start_time 
        total_sec = total_time_interval.total_seconds()
        self.time_flow = wx.Slider(self, -1, 0, 0, total_sec, (30, 10), (950, -1), wx.SL_HORIZONTAL)
        
        self.c_time.SetConstraints(anchors.LayoutAnchors(self.c_time, True, False, True, False))
        for x in [s_btn, r_btn, pa_btn, pl_btn]:
            x.SetConstraints(anchors.LayoutAnchors(x, False, False, True, True))
        self.time_flow.SetConstraints(anchors.LayoutAnchors(self.time_flow, True, False, True, False))
        
        self.Bind(wx.EVT_BUTTON, self.time_flow_stop, s_btn)
        self.Bind(wx.EVT_BUTTON, self.time_flow_reverse, r_btn)
        self.Bind(wx.EVT_BUTTON, self.time_flow_pause, pa_btn)
        self.Bind(wx.EVT_BUTTON, self.time_flow_play, pl_btn)
        
    def time_flow_stop(self, evt):
        self.time_flow.SetValue(0)
        self.Parent.simul_clock = self.Parent.start_time
        self.timer.Stop() 
        
    def time_flow_reverse(self, evt):
        if not self.timer.IsRunning():
            self.timer.Start(frame_milsec)
        
        if self.Parent.play_speed > 0:
            self.Parent.play_speed -= 0.5
            self.paly_speed.SetLabel(str(self.Parent.play_speed) + 'x')
        else:
            self.Parent.isReverse_play = True
        
    def time_flow_pause(self, evt):
        self.Parent.simul_clock_saved = self.Parent.simul_clock 
        self.timer.Stop()
    
    def time_flow_play(self, evt):
        self.Parent.isReverse_play = False
        if self.timer.IsRunning():
            self.Parent.play_speed += 0.5
            self.paly_speed.SetLabel(str(self.Parent.play_speed) + 'x')
        else: 
            self.timer.Start(frame_milsec)

    def OnTimer(self, evt, simul_clock):
        cur_sec = time.time()
        if abs(self.saved_time - cur_sec) >= 1 :
            self.c_time.SetLabel(simul_clock.ctime())
            self.saved_time = cur_sec
        flow_time = (simul_clock - self.start_time).total_seconds()
        self.time_flow.SetValue(flow_time)
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    id = Input_dialog(None, 'dialog test')
    app.MainLoop()
