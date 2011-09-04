'''
This is the main of all this project. 
It is used to run the whole project.
To show the main window of this project. 

'''
import  wx
import wx.grid
import berth_plan
import yard_crane_plan
import pre_marshalling_plan
import images
import parameter
import xmlrpclib
import threading

from SimpleXMLRPCServer import SimpleXMLRPCServer
SHOW_BACKGROUND = 1

#----------------------------------------------------------------------

ID_Berth_plan = wx.NewId()
ID_Yard_crane_plan = wx.NewId()
ID_Pre_marshalling_plan = wx.NewId()
ID_Exit = wx.NewId()

#----------------------------------------------------------------------

class MyParentFrame(wx.MDIParentFrame):
    def __init__(self):
        wx.MDIParentFrame.__init__(self, None, -1, "IMPACT", size=(1800,1350))

        self.winCount = 0
        menu = wx.Menu()
        menu.Append(ID_Berth_plan, "&Berth_plan")
        menu.Append(ID_Yard_crane_plan, "&Yard_crane_plan")
        menu.Append(ID_Pre_marshalling_plan, "&Pre-marshalling_plan")
        
        menu.AppendSeparator()
        menu.Append(ID_Exit, "&Exit")

        menubar = wx.MenuBar()
        menubar.Append(menu, "&File")
        self.SetMenuBar(menubar)

        self.CreateStatusBar()
        
        self.Bind(wx.EVT_MENU, self.On_Berth_plan, id=ID_Berth_plan)
        self.Bind(wx.EVT_MENU, self.On_Yard_crane_plan, id=ID_Yard_crane_plan)
        self.Bind(wx.EVT_MENU, self.On_Pre_marshalling_plan, id=ID_Pre_marshalling_plan)
        
        self.Bind(wx.EVT_MENU, self.OnExit, id=ID_Exit)

        if SHOW_BACKGROUND:
            self.bg_bmp = images.GridBG.GetBitmap()
            self.GetClientWindow().Bind(
                wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)


    def OnExit(self, evt):
        self.Close(True)


    def On_Berth_plan(self, evt):
        win = berth_plan.Berth_plan(self,parameter.child_id['berth_plan'])     
        win.Show(True)
    
    def On_Yard_crane_plan(self, evt):
        win = yard_crane_plan.YC_plan(self,parameter.child_id['yc_plan'])     
        win.Show(True)

    def On_Pre_marshalling_plan(self, evt):
        win = pre_marshalling_plan.Pre_marshalling_plan(self,parameter.child_id['pre-marshalling_plan'])     
        win.Show(True)
             

        
    def OnEraseBackground(self, evt):
        dc = evt.GetDC()

        if not dc:
            dc = wx.ClientDC(self.GetClientWindow())

        # tile the background bitmap
        sz = self.GetClientSize()
        w = self.bg_bmp.GetWidth()
        h = self.bg_bmp.GetHeight()
        x = 0
        
        while x < sz.width:
            y = 0

            while y < sz.height:
                dc.DrawBitmap(self.bg_bmp, x, y)
                y = y + h

            x = x + w




 
#----------------------------------------------------------------------
def server():
    port = parameter.port['MDI_test']
    server = SimpleXMLRPCServer(("localhost", port))
    server.register_introspection_functions()
    job_queue=[]
    #print 'Listening on port %d..' % port
    server.socket.settimeout(0.001)
    parameter.request_handler(server,job_queue)
#----------------------------------------------------------------------



if __name__ == '__main__':
    global s
    s = xmlrpclib.Server('http://localhost:'+str(parameter.port['tos_server']))
    mutex=threading.Lock()
    global refresh_info 
    refresh_info=None  
    class MyApp(wx.App):
        def OnInit(self):
            wx.InitAllImageHandlers()
            frame = MyParentFrame()
            frame.Show(True)
            self.SetTopWindow(frame)
            return True

    threading.Thread(target=server,args=()).start() 
    app = MyApp(False)
    app.MainLoop()




#----------------------------------------------------------------------

