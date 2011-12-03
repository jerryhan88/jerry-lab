import wx, os
filenames = ["image.gif", "image.jpg", "image.png"]

class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Loading Images")
        p = wx.Panel(self)
        
        fgs = wx.FlexGridSizer(cols=2, hgap=10, vgap=10)
        for name in filenames:
#            img1 = wx.Image('pic//image.gif', wx.BITMAP_TYPE_GIF)
            img1 = wx.Image('pic/image.gif', wx.BITMAP_TYPE_GIF).ConvertToBitmap()
#            print img1.GetImageCount()
#            print img1 , name
            w = img1.GetWidth()
            h = img1.GetHeight()
#            
#            img2 = img1.Scale(w/2, h/2)
            
#            sb1 = wx.StaticBitmap(p, -1, wx.BitmapFromImage(img1))
            sb1 = wx.StaticBitmap(p, -1, img1, (10,10),(w, h))
#            sb2 = wx.StaticBitmap(p, -1, wx.BitmapFromImage(img2))
            
            fgs.Add(sb1)
#            fgs.Add(sb2)
            
        p.SetSizerAndFit(fgs)
        self.Fit()

def opj(path):
    """Convert paths to the platform-specific separator"""
    str = apply(os.path.join, tuple(path.split('/')))
    # HACK: on Linux, a leading / gets lost...
    if path.startswith('/'):
        str = '/' + str
    return str
    
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frm = TestFrame()
    frm.Show()
    app.MainLoop()
    
