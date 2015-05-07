import matplotlib
matplotlib.use('TKAgg')
from matplotlib import pyplot as plt
import numpy as np

def mainhelp():
    print '\n'
    print 'You can use mouse to draw points on the axis. Some interaction to'
    print 'get information about the points:'
    print '  press \'c\': show covariance matrix and mean'
    print '  press \'m\': plot mean point'
    print '  press \'v\': remove mean point\n'


class MyData:
    def __init__(self, data):
        self.ax = plt.gca()
        self.cid1 = self.ax.figure.canvas.mpl_connect('button_press_event', self.append_data)
        self.cid2 = self.ax.figure.canvas.mpl_connect('key_press_event', self.calc_para)
        self.cid3 = self.ax.figure.canvas.mpl_connect('key_press_event', self.show_mean)
        self.data = data
        self.mean = []
        self.annotation = []

    def append_data(self, event):
        contains, attrd = self.ax.contains(event)
        if not contains: return 
        self.ax.plot(event.xdata, event.ydata, 'r+')
        self.ax.figure.canvas.draw()
        self.data = np.append(self.data, np.array([[event.xdata, event.ydata]]), axis=0)

    def calc_para(self, event):
        if event.key != 'c': return
        print '--Covariance matrix:'
        print np.ma.cov(self.data, None, False)
        print '--Mean:'
        print self.data.mean(axis=0)

    def show_mean(self, event):
        if event.key == 'm':
            mean = self.data.mean(axis = 0)
            print mean
            if len(self.mean) != 0: 
                self.mean.pop(0).remove()
                self.ax.figure.canvas.draw()
                self.ax.texts.remove(self.annotation)
            self.mean = self.ax.plot(mean[0], mean[1], 'b+', markeredgewidth=2)
            self.annotation = self.ax.annotate('mean point',xy=(mean[0], mean[1]), textcoords='offset points')
            self.ax.figure.canvas.draw()

        if event.key == 'v':
            if len(self.mean) == 0: return
            self.mean.pop(0).remove()
            self.ax.figure.canvas.draw()

        if event.key == 'w':
            self.ax.cla()
            self.ax.set_xlim((0, 10))
            self.ax.set_ylim((0, 10))
            self.ax.figure.canvas.draw()

mainhelp()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim((0, 10))
ax.set_ylim((0, 10))
a = MyData(np.empty((0,2), int))
plt.show()
