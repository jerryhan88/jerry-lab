import wx
import MySQLdb

class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title, pos=wx.DefaultPosition, size=(1024, 768), style=wx.DEFAULT_FRAME_STYLE): 
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
         
        db = MySQLdb.connect(host='localhost', user='root', passwd='1234', db='book_management')
        db.autocommit(True)
        self.cursor = db.cursor()
        
        self.p = wx.Panel(self,-1)
        b = wx.Button(self.p, -1, "Press^^", (200,30))
        
        wx.StaticText(self.p, -1, 'Studnent ID', (10, 30))
        wx.StaticText(self.p, -1, 'Studnent Name', (10, 60))
        wx.StaticText(self.p, -1, 'borrowed book', (10, 90))
        self.s_id_typed= wx.TextCtrl(self.p, -1, 'type stuID', pos=(100, 30), size=(80, 20))
#        self.s_id = eval(s_id_typed.GetValue()) 
        
        self.p.Bind(wx.EVT_BUTTON, self.print_hello, b)#@UndefinedVariable
        
        self.s_name_show = None
        self.s_borrowed_book = None


    def print_hello(self, evt):
        s_id = self.s_id_typed.GetValue()
        select = "select s_name, borrowed_b_id from student where s_id = '%s'" %(s_id)
        self.cursor.execute(select)
        result = self.cursor.fetchall()
        s_name, borrowed_b = result[0]
        print result
        if self.s_name_show == None:
            self.s_name_show = wx.StaticText(self.p, -1, s_name, (120, 60))
            self.s_borrowed_book = wx.StaticText(self.p, -1, borrowed_b, (120, 90))
        else:
            self.s_name_show.Destroy()
            self.s_borrowed_book.Destroy()
            self.s_name_show = wx.StaticText(self.p, -1, s_name, (120, 60))
            self.s_borrowed_book = wx.StaticText(self.p, -1, borrowed_b, (120, 90))
            
        print 'hello'   
        print s_id
        
        

if __name__ == '__main__':
    app = wx.PySimpleApp()
    win = MyFrame(None, -1, 'Hello wxPython', (100,100), (300,300))
    win.Show(True)
    app.MainLoop()




