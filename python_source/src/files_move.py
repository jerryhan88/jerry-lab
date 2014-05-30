import os, shutil
for x in range(11,21):
    files = [f for f in os.listdir(r'C:\Users\JerryHan88\Desktop\temp\experimentResult%d\textFiles'% x)]
    src = r'C:\Users\JerryHan88\Desktop\temp\experimentResult%d\textFiles/' % x
    dst = r'C:\Users\JerryHan88\Desktop\v2_summaryExper\experimentResult%d\textFiles'% x
    for fn in files:
        fp = src + fn
        shutil.move(fp,dst)
    files = [f for f in os.listdir(r'C:\Users\JerryHan88\Desktop\temp\experimentResult%d\graphFiles\waitingTime' % x)]
    src = r'C:\Users\JerryHan88\Desktop\temp\experimentResult%d\graphFiles\waitingTime/' % x
    dst =r'C:\Users\JerryHan88\Desktop\v2_summaryExper\experimentResult%d\graphFiles\waitingTime' % x
    for fn in files:
        fp = src + fn
        shutil.move(fp,dst)