from cmath import pi
from re import X
from marvelmind import MarvelmindHedge
from time import sleep
import matplotlib.pyplot as plt
import sys
import numpy
from threading import Thread


def update_line():

    pos = hedge.position()
    new_px = pos[1]
    new_py = pos[2]
    new_w = pos[4]/10/180*pi
    new_r = 3.
 
    plt.figure(1)

    axes1 = plt.gcf().get_axes()

    # Positiondaten
    xdata_p = numpy.append(plt.gca().lines[0].get_xdata(), plt.gca().lines[1].get_xdata())
    ydata_p = numpy.append(plt.gca().lines[0].get_ydata(),plt.gca().lines[1].get_ydata())

    plt.gca().lines[0].set_xdata(xdata_p)
    plt.gca().lines[0].set_ydata(ydata_p)
    
    plt.gca().lines[1].set_xdata([new_px])
    plt.gca().lines[1].set_ydata([new_py])

    plt.draw()

    #figure(2)
    plt.figure(2)
    axes2 = plt.gcf().get_axes()

    xdata_w = numpy.append(plt.gca().lines[0].get_xdata(), plt.gca().lines[1].get_xdata())
    ydata_w = numpy.append(plt.gca().lines[0].get_ydata(), plt.gca().lines[1].get_ydata())


    plt.gca().lines[0].set_xdata(xdata_w[-59:])
    plt.gca().lines[0].set_ydata(ydata_w[-59:])
    
    plt.gca().lines[1].set_xdata([new_w])
    plt.gca().lines[1].set_ydata([new_r])

    plt.draw()
    
def printThread():
    while True:
        try:
            sleep(3)
            pos = hedge.position()
            print (pos) # get last position and print
        except KeyboardInterrupt:
            hedge.stop()  # stop and close serial port
            sys.exit()


def main():
    
    global fig

    fig = plt.figure(1)
    plt.title('Position X-Y')
    ax = fig.add_subplot(111)
    ax.plot([],[], 'ro',ls='-')
    ax.grid(True)
    bx = fig.add_subplot(111)
    bx.plot([],[], 'bo',ls='-')
    plt.axis('equal')
    axes = plt.gca()
    axes.set_xlim([-5,10])
    axes.set_ylim([-5,10])
    axes.set_xlabel('X-Achse',fontsize=10)
    axes.set_ylabel('Y-Achse',fontsize=10)

    
    fig = plt.figure(2)
    plt.title('Winkel X-Y')
    cx = fig.add_subplot(111,projection='polar')
    cx.plot([],[], 'ro',ls='-')
    cx.grid(True)
    dx = fig.add_subplot(111,projection='polar')

    dx.plot([],[], 'bo',ls='-')


    axes = plt.gca()
    axes.set_rmax(4)

    global hedge
    hedge = MarvelmindHedge(tty = "/dev/ttyUSB0", adr=10, recieveUltrasoundPositionCallback=update_line) # create MarvelmindHedge thread
    hedge.start()
    
    plotThread = Thread(target=printThread) # create and start console out thread
    plotThread.start()
    
    plt.show()
    
main()
