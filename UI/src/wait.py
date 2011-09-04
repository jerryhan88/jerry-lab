'''
usage:
    import wait
    wait.start('title', 'some text')
    # do some work that takes time, here
    wait.stop()
'''

import wx
import time

try:
    import pyprogress as PP
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.pyprogress as PP

class ProgressDlg(PP.PyProgress):
    def __init__(self, text):
        PP.PyProgress.__init__(self, None, -1, title, text, agwStyle=wx.PD_ELAPSED_TIME)
        self.SetWindowStyle(self.GetWindowStyle() | wx.STAY_ON_TOP)
        while True:
            self.UpdatePulse()
            time.sleep(0.03)

class MyApp(wx.App):
    def OnInit(self):
        self.dlg = ProgressDlg(text)
        return True

def start(title, text):
    assert (title + text).find('"') < 0, 'title and text should not contain {"} character'
    import subprocess
    global p
    p = subprocess.Popen('pythonw wait.py "%s" "%s"' % (title, text))

def stop():
    import _subprocess
    _subprocess.TerminateProcess(p._handle, 1)

if __name__ == '__main__':
    from sys import argv
    if len(argv) == 3:
        title, text = argv[1], argv[2]
        app = MyApp(0)
        app.MainLoop()
    else:
        start('IMPACT', 'Solving berth planning problem...')
        time.sleep(10)
        stop()
