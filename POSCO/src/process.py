from __future__ import division
import wx, m_frame

class Process_info_Viewer(wx.Dialog):
    def __init__(self, selected_process):
        wx.Dialog.__init__(self, None, -1, 'Process information', pos=(100, 100) , size=(904, 680))
        b_color = wx.Colour(222, 239, 247)
        self.selected_partner = None
        self.search_start = False
        
        self.r_box = wx.StaticBox(self, -1, "", pos=(7, 0), size=(345, 645))
        r_box_px, r_box_py = self.r_box.GetPosition()
        r_box_sx, r_box_sy = self.r_box.GetSize()
        repo_p = wx.Panel(self, -1, pos=(r_box_px + 2, r_box_py + 8), size=(342, 60))
        repo_p_px, repo_p_py = repo_p.GetPosition()
        repo_p_sx, repo_p_sy = repo_p.GetSize()
        resp_img = wx.Image('pic/repository.png', wx.BITMAP_TYPE_PNG)
        wx.StaticBitmap(repo_p, -1, wx.BitmapFromImage(resp_img))
        
        search_p = wx.Panel(self, -1, pos=(repo_p_px, repo_p_py + repo_p_sy), size=(342, 45))
        search_p.SetBackgroundColour(b_color)
        search_input = wx.TextCtrl(search_p, -1, '', pos=(10, 3),
                                    size=(repo_p_sx - 100, 34))
        search_input_px, search_input_py = search_input.GetPosition()
        search_input_sx, search_input_sy = search_input.GetSize()
        search_input.SetFont(wx.Font(17, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        search_img = wx.Image('pic/search.png', wx.BITMAP_TYPE_PNG)
        search_btn = wx.BitmapButton(search_p, -1, bitmap=wx.BitmapFromImage(search_img), pos=(search_input_px + search_input_sx + 3, search_input_py - 4))
        self.Bind(wx.EVT_BUTTON, self.search, search_btn)
        
        self.partner_finder = wx.ScrolledWindow(self, -1, pos=(repo_p_px, repo_p_py + repo_p_sy + 45),
                                              size=(repo_p_sx - 5, 480))
        self.partner_finder.SetDoubleBuffered(True)
        self.partner_finder.SetBackgroundColour(b_color)
        self.partner_finder.SetScrollRate(1, 1)        
        self.partner_finder.SetScrollbars(repo_p_sx, 100, 1, 13)
        
        partner_finder_px, partner_finder_py = self.partner_finder.GetPosition()
        partner_finder_sx, partner_finder_sy = self.partner_finder.GetSize()
        
        rep_b_img = wx.Image('pic/repository_b.png', wx.BITMAP_TYPE_PNG)
        wx.StaticBitmap(self, -1, wx.BitmapFromImage(rep_b_img), pos=(partner_finder_px, partner_finder_py + partner_finder_sy + 2))
        
        self.partner_finder.Bind(wx.EVT_LEFT_DOWN, self.OnPartnerClick)
        self.partner_finder.Bind(wx.EVT_PAINT, self.drawing_partner)
        
        self.info_task_box = wx.StaticBox(self, -1, "", pos=(r_box_px + r_box_sx + 5, r_box_py), size=(535, 280))
        info_task_box_px, info_task_box_py = self.info_task_box.GetPosition()
        info_task_box_sx, info_task_box_sy = self.info_task_box.GetSize()     
        self.info_p = wx.Panel(self, -1, pos=(info_task_box_px + 2, info_task_box_py + 12), size=(190, 50))
        info_p_px, info_p_py = self.info_p.GetPosition()
        info_p_sx, info_p_sy = self.info_p.GetSize()
        info_img = wx.Image('pic/information.png', wx.BITMAP_TYPE_PNG)
        wx.StaticBitmap(self.info_p, -1, wx.BitmapFromImage(info_img.Scale(190, 50)))
        self.task_p = wx.Panel(self, -1, pos=(info_p_px + info_p_sx, info_p_py), size=(341, 50))
        self.task_p.Bind(wx.EVT_LEFT_DOWN, self.OnTaskClick)
        self.task_p.Bind(wx.EVT_PAINT, self.drawing_task)
        
        self.info_task_viewer_p = wx.Panel(self, -1, pos=(info_p_px, info_p_py + info_p_sy + 4), size=(530, info_task_box_sy - 110))
        info_task_viewer_p_px, info_task_viewer_p_py = self.info_task_viewer_p.GetPosition()
        info_task_viewer_p_sx, info_task_viewer_p_sy = self.info_task_viewer_p.GetSize()
        self.info_task_viewer_p.SetBackgroundColour(b_color)

        info_task_viewer_b_p = wx.Panel(self, -1, pos=(info_task_viewer_p_px, info_task_viewer_p_py + info_task_viewer_p_sy), size=(info_task_viewer_p_sx, 40))
        info_task_viewer_b_p.SetBackgroundColour(wx.Colour(181, 203, 239))
        
        self.detail_process_box = wx.StaticBox(self, -1, "", pos=(info_task_box_px, info_task_box_py + info_task_box_sy),
                                           size=(534, 365))
    def display_info_task(self, choice):
        if self.selected_partner == 2:
            info_task_viewer_p_px, info_task_viewer_p_py = self.info_task_viewer_p.GetPosition()
            info_task_viewer_p_sx, info_task_viewer_p_sy = self.info_task_viewer_p.GetSize()
            if choice == 0:
                partner_img = wx.Image('pic/partner.png', wx.BITMAP_TYPE_PNG)
                w = partner_img.GetWidth()
                h = partner_img.GetHeight()
                wx.StaticBitmap(self.info_task_viewer_p, -1, wx.BitmapFromImage(partner_img), pos=(50, 25), size=(w, h))
                self.info_task_viewer_p.SetFont(wx.Font(17, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
                wx.StaticText(self.info_task_viewer_p, -1, 'Dung Liu Express Co.', pos=(190, 20))
                wx.StaticText(self.info_task_viewer_p, -1, 'Name : Dung Liu', pos=(190, 70))
                wx.StaticText(self.info_task_viewer_p, -1, 'Contact : 011-244-1547', pos=(190, 120))
    #            cops_n.SetFont()
            else:
                ipad_img = wx.Image('pic/ipad.png', wx.BITMAP_TYPE_PNG)
                w = ipad_img.GetWidth()
                h = ipad_img.GetHeight()
                wx.StaticBitmap(self.info_task_viewer_p, -1, wx.BitmapFromImage(ipad_img.Scale(w / 7, h / 7)), pos=(50, 20), size=(w / 7, h / 7))
                
                iphone_img = wx.Image('pic/iphone.png', wx.BITMAP_TYPE_PNG)
                w = iphone_img.GetWidth()
                h = iphone_img.GetHeight()
                wx.StaticBitmap(self.info_task_viewer_p, -1, wx.BitmapFromImage(iphone_img.Scale(w / 10, h / 9.4)), pos=(200, 20), size=(w / 10, h / 9.4))
    
    def display_detail_process(self, choice):
        detail_process_box_px, detail_process_box_py = self.detail_process_box.GetPosition()
        detail_process_box_sx, detail_process_box_sy = self.detail_process_box.GetSize()
        self.detail_process_p = wx.Panel(self, -1, pos=(detail_process_box_px, detail_process_box_py + 5), size=(detail_process_box_sx, detail_process_box_sy - 10))
        detail_process_p_sx, detail_process_p_sy = self.detail_process_p.GetSize()
#        detail_process_p.SetBackgroundColour(wx.Colour(255,123,21))
        # choice == 0  is detail
        if choice == 0:
            details_t_img = wx.Image('pic/detatils_t.png', wx.BITMAP_TYPE_PNG)
            self.datails_t = wx.StaticBitmap(self.detail_process_p, -1, wx.BitmapFromImage(details_t_img.Scale(detail_process_box_sx - 4, 50)), pos=(1, 3), size=(detail_process_box_sx - 4, 50))
            
            self.detail_process_viewer = wx.ScrolledWindow(self.detail_process_p, -1, pos=(0, 55),
                                                  size=(detail_process_box_sx - 5, 250))
            self.detail_process_viewer.SetDoubleBuffered(True)
            self.detail_process_viewer.SetBackgroundColour("white")
#            self.detail_process_viewer.SetScrollRate(1,0.1)        
            self.detail_process_viewer.SetScrollbars(detail_process_p_sx - 5, 10, 1, 130)
            
            btw_line_size = 30
            last_py = 15
            t_px = 40
            t_font = wx.Font(17, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
            sub_px = 60
            self.detail_process_viewer.SetFont(wx.Font(12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            sr = wx.StaticText(self.detail_process_viewer, -1, '1.Scale/Reputation', pos=(t_px, last_py))
            sr.SetFont(t_font)
            last_py += btw_line_size 
            wx.StaticBitmap(self.detail_process_viewer, -1, wx.BitmapFromImage(wx.Image('pic/factory.png', wx.BITMAP_TYPE_PNG).Scale(200 * 1.5, 150 * 1.5)),
                         pos=(sub_px, last_py), size=(200 * 1.5, 150 * 1.5))
            last_py += 150 * 1.5 + 10
            wx.StaticText(self.detail_process_viewer, -1, 'Factory scale : 990 square meter ', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, 'Address : - Closed -  ', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, 'Num of Workers : 17 ', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, 'Related Works or News ', pos=(sub_px, last_py))
            last_py += 20
            web_address = wx.StaticText(self.detail_process_viewer, -1, '    htttp://www.hankyung.co.kr/der~', pos=(sub_px, last_py))
            web_address.SetForegroundColour(wx.Colour(85, 142, 213))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, '------------------------------------------------------------------------------------------', pos=(0, last_py))
            last_py += btw_line_size
            
            rc = wx.StaticText(self.detail_process_viewer, -1, '2.Record career', pos=(t_px, last_py))
            rc.SetFont(t_font)
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, 'Num of Total Project : 56 ', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, 'Num of Current Project : 3 ', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, 'Num of Completed Project : 45 ', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, 'Num of failed Project : 8 ', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.Button(self.detail_process_viewer, -1, 'Details', pos=(sub_px + 30, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, '------------------------------------------------------------------------------------------', pos=(0, last_py))
            last_py += btw_line_size
            
            ev = wx.StaticText(self.detail_process_viewer, -1, '3.Evaluation', pos=(t_px, last_py))
            ev.SetFont(t_font)
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, 'SCORE : 8.5/10 ', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.Button(self.detail_process_viewer, -1, 'Details', pos=(sub_px + 30, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, '------------------------------------------------------------------------------------------', pos=(0, last_py))
            last_py += btw_line_size
            
            bd = wx.StaticText(self.detail_process_viewer, -1, '4.Benefit Distribution', pos=(t_px, last_py))
            bd.SetFont(t_font)
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, '- Closed -', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, '------------------------------------------------------------------------------------------', pos=(0, last_py))
            last_py += btw_line_size
            
            fs = wx.StaticText(self.detail_process_viewer, -1, '5.Financial Statements', pos=(t_px, last_py))
            fs.SetFont(t_font)
            last_py += btw_line_size
            self.detail_process_viewer.SetForegroundColour(wx.Colour(85, 142, 213))
            wx.StaticText(self.detail_process_viewer, -1, '1/4     2009 Year', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, '2/4     2009 Year', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, '3/4     2009 Year', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, '4/4     2009 Year', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, '1/4     2010 Year', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, '2/4     2010 Year', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, '3/4     2010 Year', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, '4/4     2010 Year', pos=(sub_px, last_py))
            last_py += btw_line_size
            wx.StaticText(self.detail_process_viewer, -1, '------------------------------------------------------------------------------------------', pos=(0, last_py))
            last_py += btw_line_size
        else:
            # process
            process_t_img = wx.Image('pic/process_t.png', wx.BITMAP_TYPE_PNG)
            wx.StaticBitmap(self.detail_process_p, -1, wx.BitmapFromImage(process_t_img.Scale(detail_process_box_sx - 4, 50)), pos=(1, 3), size=(detail_process_box_sx - 4, 50))
            wx.StaticBitmap(self.detail_process_p, -1, wx.BitmapFromImage(wx.Image('pic/process_ex.png', wx.BITMAP_TYPE_PNG).Scale(detail_process_box_sx - 4, 250)), pos=(1, 50), size=(detail_process_box_sx - 4, 250))

        wx.StaticBitmap(self.detail_process_p, -1, wx.BitmapFromImage(wx.Image('pic/repository_b.png', wx.BITMAP_TYPE_PNG).Scale(detail_process_box_sx - 4, 50)),
                         pos=(1, detail_process_p_sy - 45), size=(detail_process_box_sx - 4, 50))
        
#        button = wx.Button(self, -1, "Confirm", (100, 150))
#        self.Bind(wx.EVT_BUTTON, self.confirm, button)
    def confirm(self, event):
        self.Destroy()
        
    def search(self, e):
        self.search_start = True
        partner_select_btn = wx.Button(self.partner_finder, -1, "Select", pos=(240,320), size=(70, 35))
        partner_select_btn.SetFont(wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.partner_finder.Refresh()
        self.Bind(wx.EVT_BUTTON, self.select_partner, partner_select_btn)
    def select_partner(self, e):
        m_frame.selected_partner = True 
        self.Destroy()
        
    def OnPartnerClick(self, e):
        dx, dy = self.partner_finder.GetViewStart()
        x, y = e.GetX() + dx * 100, e.GetY() + dy * 100
        
        if 5 <= y <= 5 + 92:
            self.selected_partner = 0
        elif 5 + 92 <= y <= 5 + 95 * 2 + 15:
            self.selected_partner = 1
        else:
            self.selected_partner = 2
            self.info_task_viewer_p.Refresh()
            self.display_info_task(0)
            self.display_detail_process(0)
        print self.selected_partner
        self.partner_finder.Refresh()
        
    
    def drawing_partner(self, _):
        dc = wx.PaintDC(self.partner_finder)
        self.partner_finder.PrepareDC(dc)
        
        if self.search_start:
            partner_finder_px, partner_finder_py = self.partner_finder.GetPosition()
            partner_finder_sx, partner_finder_sy = self.partner_finder.GetSize()
            
            partners = ['DHL', 'FedEx', 'EX']
            
            for i, p in enumerate(partners):
                img = wx.Image('pic/' + p + '.png', wx.BITMAP_TYPE_PNG)
                if i == 0:
                    dc.DrawBitmap(wx.BitmapFromImage(img), 7, 5)
                if i == 1:
                    dc.DrawBitmap(wx.BitmapFromImage(img), 7, 5 + 92)
                else:
                    dc.DrawBitmap(wx.BitmapFromImage(img), 4, 5 + 95 * 2 + 15)
        
        if self.selected_partner == 2:
            old_pen = dc.GetPen()
            dc.SetPen(wx.Pen(wx.BLUE, 2))
            p1 = (4 - 2, 5 + 95 * 2 + 15 - 2)
            p2 = (4 + 2 + 319, 5 + 95 * 2 + 15 - 2)
            p3 = (4 - 2, 5 + 95 * 2 + 15 + 2 + 100 + 5)
            p4 = (4 + 2 + 319, 5 + 95 * 2 + 15 + 2 + 100 + 5)
            dc.DrawLine(p1[0], p1[1], p2[0], p2[1])
            dc.DrawLine(p1[0], p1[1], p3[0], p3[1])
            dc.DrawLine(p2[0], p2[1], p4[0], p4[1])
            dc.DrawLine(p3[0], p3[1], p4[0], p4[1])
            dc.SetPen(old_pen)
        dc.EndDrawing()
        
    def drawing_task(self, _):
        dc = wx.PaintDC(self.task_p)
        self.task_p.PrepareDC(dc)
        task_img = wx.Image('pic/task.png', wx.BITMAP_TYPE_PNG)
        dc.DrawBitmap(wx.BitmapFromImage(task_img.Scale(341, 50)), 0, 0)
        dc.EndDrawing()

    def OnTaskClick(self, _):
        self.info_task_viewer_p.Destroy()
        info_task_box_px, info_task_box_py = self.info_task_box.GetPosition()
        info_task_box_sx, info_task_box_sy = self.info_task_box.GetSize()
        b_color = wx.Colour(222, 239, 247)
        info_p_px, info_p_py = self.info_p.GetPosition()
        info_p_sx, info_p_sy = self.info_p.GetSize()
        
        self.info_task_viewer_p = wx.Panel(self, -1, pos=(info_p_px, info_p_py + info_p_sy + 4), size=(530, info_task_box_sy - 110))
        self.info_task_viewer_p.SetBackgroundColour(b_color)
        self.display_info_task(1)
        self.datails_t.Destroy()
        self.detail_process_viewer.Destroy()
        
        self.display_detail_process(1)
        
        
        
        
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    from m_frame import Process
    p = Process(0, 1, 1)
    mv = Process_info_Viewer(p)
    mv.Show(True)
    app.MainLoop()
