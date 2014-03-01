import pprint
L = [['a', 'd'],
     ['b','e','g'],
     ['c','f'],]

pos_dic = {}
for i, items, in enumerate(L):
    for j, item, in enumerate(items):
        pos_dic[item] = (i,j)

print pos_dic
print
for l in L:
    print l
    
selected_item = ['a', 'e']
out = []
for l in L:
    for i, item in enumerate(l):
        if item in selected_item:
            out = out + l[i:]
print
print out

for out_item in out:
    i,j = pos_dic[out_item]
    L[i][j] = 0
    
print 
print L

result = []
for l in L:
    sub_re = []
    for item in l:
        if item != 0:
            sub_re.append(item)
    result.append(sub_re)

print result