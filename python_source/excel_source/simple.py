from xlrd import open_workbook

wb = open_workbook('simple.xls')

for s in wb.sheets():
    print 'Sheet:', s.name
    for row in range(s.nrows):
        values = []
        for col in range(s.ncols):
            print row,col, s.cell(row,col).value
            values.append(s.cell(row,col).value)
        print ','.join(values)
    print
    