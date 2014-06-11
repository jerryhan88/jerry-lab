import wx
import random

# The recommended way to use wx with mpl is with the WXAgg
# backend. 
#
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas
import numpy as np
import pylab

class GraphFrame(wx.Frame):
    """ The main frame of the application
    """
    title = 'Demo: dynamic matplotlib graph'
    def __init__(self):
        wx.Frame.__init__(self, None, -1, self.title, size=(800, 600))
        
        self.dataX = [[0], [0]]
        self.dataY = [[0], [0]]
        self.create_main_panel()
        
        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)        
        self.redraw_timer.Start(100)
    
    def gen_data(self):
        for x in self.dataX:
            x.append(len(x))
        for y in self.dataY:
            y.append(y[-1] + random.uniform(-0.5, 0.5))
        
    def init_plot(self):
        self.dpi = 100
        self.fig = Figure((4.0, 3.0), dpi=self.dpi, facecolor='white')
        self.axes = self.fig.add_subplot(1,2,1)
        self.axes.set_title('test1')
        self.axes.set_axis_bgcolor('white')
        pylab.setp(self.axes.get_xticklabels(), fontsize=8)
        pylab.setp(self.axes.get_yticklabels(), fontsize=8)
        
        self.plot_data = self.axes.plot(self.dataX[0],
                                        self.dataY[0],
                                        linewidth=1,
                                        color='black',
                                        )[0]
                                        
        self.axes1 = self.fig.add_subplot(1,2,2)
        self.axes1.set_axis_bgcolor('white')
        pylab.setp(self.axes1.get_xticklabels(), fontsize=8)
        pylab.setp(self.axes1.get_yticklabels(), fontsize=8)
        self.plot_data1 = self.axes1.plot(self.dataX[1],
                                        self.dataY[1],
                                        linewidth=1,
                                        color='black',
                                        )[0]
    
    def create_main_panel(self):
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('white')
        self.init_plot()
        self.canvas = FigCanvas(self.panel, -1, self.fig)
        
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.canvas, 1, flag=wx.LEFT | wx.TOP | wx.GROW)        
        
        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)
        
    def on_redraw_timer(self, _):
        self.gen_data()
        self.draw_plot()
        
    def draw_plot(self):
        xmax = len(self.dataX[0]) if len(self.dataX[0]) > 100 else 100
        xmin = 0
        ymin = round(min(self.dataY[0]), 0) - 1
        ymax = round(max(self.dataY[0]), 0) + 1
        self.axes.set_xbound(lower=xmin, upper=xmax)
        self.axes.set_ybound(lower=ymin, upper=ymax)
        self.plot_data.set_xdata(self.dataX[0])
        self.plot_data.set_ydata(self.dataY[0])
        
        xmax = len(self.dataX[1]) if len(self.dataX[1]) > 100 else 100
        xmin = 0
        ymin = round(min(self.dataY[1]), 0) - 1
        ymax = round(max(self.dataY[1]), 0) + 1
        self.axes1.set_xbound(lower=xmin, upper=xmax)
        self.axes1.set_ybound(lower=ymin, upper=ymax)
        self.plot_data1.set_xdata(self.dataX[1])
        self.plot_data1.set_ydata(self.dataY[1])
        
        self.canvas.draw()
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    app.frame = GraphFrame()
    app.frame.Show()
    app.MainLoop()
