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
        self.dataX = [0]
        self.dataY = [0]
        self.data = [self.dataX , self.dataY]
        self.create_main_panel()
        
        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)        
        self.redraw_timer.Start(100)
    
    def gen_data(self):
        self.dataX.append(len(self.dataX))
        self.dataY.append(self.dataY[-1] + random.uniform(-0.5, 0.5))
        
    def init_plot(self):
        self.dpi = 100
        self.fig = Figure((4.0, 3.0), dpi=self.dpi, facecolor='white')
        self.axes = self.fig.add_subplot(111)
        self.axes.set_axis_bgcolor('white')
        
        pylab.setp(self.axes.get_xticklabels(), fontsize=8)
        pylab.setp(self.axes.get_yticklabels(), fontsize=8)

        # plot the data as a line series, and save the reference 
        # to the plotted line series
        #
        self.plot_data = self.axes.plot(self.data[0],
                                        self.data[1],
                                        linewidth=1,
                                        color='black',
                                        )[0]
    
    def create_main_panel(self):
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('white')
        self.init_plot()
        self.canvas = FigCanvas(self.panel, -1, self.fig)
        self.pause_button = wx.Button(self.panel, -1, "Pause")
        
    def on_redraw_timer(self, _):
        self.gen_data()
        self.draw_plot()
        
    def draw_plot(self):
        """ Redraws the plot
        """
        xmax = len(self.data[0]) if len(self.data[0]) > 100 else 100
        xmin = 0

        # for ymin and ymax, find the minimal and maximal values
        # in the data set and add a mininal margin.
        # 
        # note that it's easy to change this scheme to the 
        # minimal/maximal value in the current display, and not
        # the whole data set.
        # 
        ymin = round(min(self.data[1]), 0) - 1
        ymax = round(max(self.data[1]), 0) + 1

        self.axes.set_xbound(lower=xmin, upper=xmax)
        self.axes.set_ybound(lower=ymin, upper=ymax)
#         self.axes.grid(False)
#         pylab.setp(self.axes.get_xticklabels(), visible=True)
        
        # Using setp here is convenient, because get_xticklabels
        # returns a list over which one needs to explicitly 
        # iterate, and setp already handles this.
        #  
        
        self.plot_data.set_xdata(np.array(self.data[0]))
        self.plot_data.set_ydata(self.data[1])
        
        self.canvas.draw()
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    app.frame = GraphFrame()
    app.frame.Show()
    app.MainLoop()
