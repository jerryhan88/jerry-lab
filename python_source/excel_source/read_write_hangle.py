from xlrd import open_workbook
from xlwt import Workbook
from xlutils.copy import copy
p = r'test.xls'
rb = open_workbook(p)
wb = Workbook()
st = wb.add_sheet('test')
rst = rb.sheet_by_index(0)
rrow = rst.row(2)
row = st.row(1)

for i, r in enumerate(rrow):
    row.write(i,r.value)
    
wb.save(r'test1.xls')
