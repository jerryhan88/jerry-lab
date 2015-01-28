from os import listdir, getcwd, rename
txtPath = getcwd()
for f in listdir(txtPath):
    ar, a, b = f.split(' ')
    new_ar = ar[:-3]+')'
    print f
    #print ' '.join([new_ar, a, b])
    if f =='temp.py':
        continue
    rename(f,' '.join([new_ar, a, b]))
        
    
