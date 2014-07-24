import win32com.client 
from win32com.client import constants 
 
win32com.client.gencache.EnsureDispatch("Visio.Application") 
visapp = win32com.client.Dispatch("Visio.Application") 
 
doc = visapp.Documents.Add("") 
page = visapp.ActivePage 
 
stencilname = "basic_u.vss" 
stencildocflags = constants.visOpenRO | constants.visOpenDocked 
stencildoc = visapp.Documents.OpenEx(stencilname , stencildocflags ) 
 
masterrect = stencildoc.Masters.ItemU("rectangle") 
mastercircle = stencildoc.Masters.ItemU("circle") 
masterconnector= stencildoc.Masters.ItemU("dynamic connector") 
 
shape1 = page.Drop(masterrect, 1,1) 
for i in range(3): 
 shape2 = page.Drop(mastercircle, 3+2*i,3+2*i) 
 connector = page.Drop(masterconnector, -1,-1) 
 
 connector.CellsU("BeginX").GlueTo(shape1.CellsSRC(1, 1, 0)) 
 connector.CellsU("EndY").GlueTo(shape2.CellsSRC(1, 1, 0)) 
 shape1 = shape2