from __future__ import division #@UnresolvedImport
import wx, LeeHa

class Main_viewer(wx.Frame):
    def __init__(self, parent, ID, title, pos=wx.DefaultPosition, size=(1024, 768), style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style) 
        base_panel = wx.Panel(self, -1, pos=(0, 0), size=(200, 100))
        
#        btn = wx.Button(base_panel, -1, "start", (30, 60))
#        self.Bind(wx.EVT_BUTTON, self.start_plan, btn)
#        
#        
#    def start_plan(self, _):
#        print 'start'

#    operation = LeeHa.run()
#    for x in operation:
#        print x

        operation = LeeHa.run()
        while operation:
            try:
                n = operation.next()
                self.process_viewer = Process_viewer(n, None, 'Arriving Event')    
                self.process_viewer.Show(True)
            except StopIteration:
                dlg = wx.MessageDialog(self, 'End of Event')
                dlg.ShowModal()
                dlg.Destroy()
                return
            
#        n = [(0, 0), (0, 1), (0, 2), (0, 3),
#             (1, 0), (1, 1), (1, 2), (1, 3),
#             (2, 0), (2, 1), (2, 2), (2, 3),
#             (3, 0), (3, 1), (3, 2), (3, 3),
#             (4, 0), (4, 1), (4, 2), (4, 3),
#             (5, 0), (5, 1), (5, 2), (5, 3)]
#        
#        self.process_viewer = Process_viewer(n, None, 'Arriving Event')    
#        self.process_viewer.Show(True)
        
#        self.Destroy()
class Process_viewer(wx.Dialog):
    def __init__(self, nodes , parent, name, size=(1024, 500), pos=(230, 30)):
        wx.Dialog.__init__(self, None, -1, 'Arriving Event Viewer', pos , size)
        self.panel = wx.Panel(self, -1, pos=(0, 0), size=(1024, 500))
        
        self.nodes = nodes
        self.panel.Bind(wx.EVT_PAINT, self.OnViewPaint)
        
        
        button = wx.Button(self, -1, "Confirm", (860, 400))
        self.Bind(wx.EVT_BUTTON, self.confirm, button)
    
    def OnViewPaint(self, _):
        dc = wx.PaintDC(self.panel)
        self.panel.PrepareDC(dc)
        
        for n in self.nodes:
#            x = n.id
            if n.id > 2:
                n.y = n.id % 3 * 120 + 100 
                n.x = n.order * 120 + 580
            else:
                n.y = n.id % 3 * 120 + 100 
                n.x = n.order * 120 + 80
        
        
        for n in self.nodes:
            dc.DrawCircle(n.x, n.y, 30)
            for e in n.outgoings:
                angle = (e.end_n.x -n.x) // (e.end_n.y -n.y) 
                dc.DrawLine(n.x + angle *30,n.y + angle *30,e.end_n.x - angle *30, e.end_n.y - angle *30)
#            if n.id > 2:
#                print 'hi'
#                dc.DrawCircle(x + 580, y * 120 + 100, 30)
#            else:
#                dc.DrawCircle(x + 80, y * 120 + 100, 30)
#            for e in n.outgoings:
#                next_n_y = e.end_n.id % 3
#                next_n_x = e.end_n.order * 120
#                dc.DrawLine(x + 580, y, next_n_x, next_n_y)
            
        
        dc.EndDrawing()
    
    def confirm(self, event):
        self.Destroy()
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    mv = Main_viewer(None, -1, 'Main_viewer', pos=(30, 30), size=(200, 150))
    mv.Show(True)
    app.MainLoop()
    
    
    
    
#    
#    operation = LeeHa.run()
#    for x in operation:
#        print x
        
