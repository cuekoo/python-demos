#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
from subprocess import call
import sklearn.svm as svm

def mainhelp():
    print """\n
    A framework to get data from mouse for classification. 
      press \'n\': toggle input neg/pos data (default pos)
      press \'c\': print data
      press \'w\': clear data\n
      """


class MyData:
    def __init__(self, data):
        self.ax = plt.gca()
        self.ax.figure.canvas.mpl_connect('button_press_event', self.append_data)
        self.ax.figure.canvas.mpl_connect('key_press_event', self.classify_data)
        self.ax.figure.canvas.mpl_connect('key_press_event', self.clear_data)
        self.ax.figure.canvas.mpl_connect('key_press_event', self.change_mode)
        self.data = data
        self.label = np.empty((0, 1), int)
        self.mode = self.ax.annotate('positive', xy=(0.1, 9.7), color='r')
        self.datastyle = 'r+'
        self.ispos = True

        self.clf = svm.SVC(gamma = 0.001, C = 100.)

    def append_data(self, event):
        contains, attrd = self.ax.contains(event)
        if not contains: return 
        self.ax.plot(event.xdata, event.ydata, self.datastyle, markeredgewidth=2)
        self.ax.figure.canvas.draw()
        self.data = np.append(self.data, np.array([[event.xdata, event.ydata]]), axis=0)
        if self.ispos:
            self.label = np.append(self.label, [[1]], axis=0) 
        else:
            self.label = np.append(self.label, [[2]], axis=0) 


    def change_mode(self, event):
        if event.key != 'n': return
        self.ax.texts.remove(self.mode)
        if self.ispos:
            self.mode = self.ax.annotate('negtive', xy=(0.1, 9.7), color='b')
            self.ispos = False
            self.datastyle = 'b+'
        else:
            self.mode = self.ax.annotate('positive', xy=(0.1, 9.7), color='r')
            self.ispos = True
            self.datastyle = 'r+'
        self.ax.figure.canvas.draw()


    def classify_data(self, event):
        if event.key != 'c': return

        self.clf.fit(self.data, self.label.ravel())
        delta = 0.05
        X, Y = np.meshgrid(np.arange(0,10,delta), np.arange(0,10,delta))
        Z = self.clf.predict(np.c_[X.ravel(), Y.ravel()])
        Z = Z.reshape(X.shape)
        self.ax.contourf(X, Y, Z, levels=[1,1.5])
        self.ax.texts.remove(self.mode)
        self.mode = self.ax.annotate('classification result', xy=(0.1, 9.7), color='r')
        self.ax.figure.canvas.draw()

    def clear_data(self, event):
        if event.key != 'w': return
        self.ax.cla()
        self.ax.set_xlim((0, 10))
        self.ax.set_ylim((0, 10))
        self.ax.figure.canvas.draw()
        self.data = np.empty((0,2), int)
        self.label = np.empty((0, 1), int)
        self.mode = self.ax.annotate('positive', xy=(0.1, 9.7), color='r')
        self.datastyle = 'r+'
        self.ispos = True
        self.ax.figure.canvas.draw()

mainhelp()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim((0, 10))
ax.set_ylim((0, 10))
a = MyData(np.empty((0,2), int))
plt.show()
