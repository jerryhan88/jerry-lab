import win32com.client
from win32com.client import constants
import sys, os

def run():
    current_folder = os.path.dirname(sys.argv[0])        
    win32com.client.gencache.EnsureDispatch("Visio.Application")

    visapp = win32com.client.Dispatch("Visio.Application")
#     visapp.Visible = 0
#     doc = visapp.Documents.Open(current_folder + '\\network_ex.vsd')
    
    
    doc = visapp.Documents.Add(current_folder + '\\network_ex.vsd')

#     for x in get_user_attributes(doc):
#         print x
#     for x in dir(doc):
#         print x
#     print dir(doc.Pages.Item(1))
    page = visapp.ActivePage
    
#     for x in dir(page):
#         print x,'        ', dir(x)
#     
#     
    page = doc.Pages.Item(1)
#     print page.XRulerOrigin
#     print page.Sheet
#     assert False
#     for x in dir(page):
#         print x
#     print '------------------------------------------------------'
#     print page.Layout().PlayStyle
#     print '------------------------------------------------------'
#     for x in page._prop_map_get_:
#         print x
#     print '------------------------------------------------------'
# #     for x in dir(page.Shapes._prop_map_get_):
# #         print x, type(x)
#     print '------------------------------------------------------'
    print page.Layers
    print page.Index
    print page.PageSheet
    print page.BackPageAsObj
    print page.Application
    print page.Document
    print page.Type
    print dir(page.OLEObjects._prop_map_get_)
#     print page.Picture
    print page.Stat
    print page.Connects
    print page.PersistsEvents
    print page.Background
    print page.BackPage
    print page.ObjectType
#     print page.ReviewerID
    print page.Name
    print page.EventList
    print page.Shapes
    print page.NameU
    print page.ThemeEffects
    print page.ID
#     print page.ThemeColors
    print page.PrintTileCount
#     print page.OriginalPage
    print page.ID16

#     for s in page.Shapes:
#         print s.CellsU('XRulerOrigin')
#         if s.Name[0] == 'n':
#             print s.Name, s.Text, s.Cells('Prop.capa.Value').Formula, s.Cells('PinX').Result("m"), s.Cells('PinY').Result("m")
#             print s.Cells('Prop.x.Value')
#         if s.Name[0] == 'l':
#             print s.Name, s.Text, s.Cells('Prop.Row_1.Value').Formula, s.Cells("BeginX").Result("m"), s.Cells("BeginY").Result("m")
#         else:
#             print s.Name, s.Text
    
    doc.Close()
    visapp.Quit()
#     

            
    
#     s = page.Shapes(5)
#     print s.Cells("BeginX").Result("mm")
#     print 
#     print int(eval(s.Cells('PinX.Value').Formula))
    
# node name

if __name__ == '__main__':
    run()
    
