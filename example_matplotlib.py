from cmath import pi
from re import X
from marvelmind import MarvelmindHedge
from time import sleep
import matplotlib.pyplot as plt
import sys
import numpy
from threading import Thread
from scipy.interpolate import CubicSpline


def update_line():

    pos = hedge.position()
    new_px = pos[1]
    new_py = pos[2]
    new_w = pos[4]/10/180*pi
    new_r = 3.
 
    # figures = plt.get_current_fig_manager()
    # figure_1 = figures.get_figure()
    #figure(1)
    plt.figure(1)

    axes1 = plt.gcf().get_axes()
    # lines_p =axes[1].get_lines()
    # lines_w =axes[2].get_lines()

    # Positiondaten
    xdata_p = numpy.append(plt.gca().lines[0].get_xdata(), plt.gca().lines[1].get_xdata())
    ydata_p = numpy.append(plt.gca().lines[0].get_ydata(),plt.gca().lines[1].get_ydata())

    # x = xdata_p[-59:]
    # y = ydata_p[-59:]
    # xx = [] 
    # xnew =[]
    # ynew = []
    # for i in range(60):
    #  if i+1==len(x) or i+1==60:
    #   break
    #  #if x[i]>x[i+1]:
    
    #  xx = numpy.linspace(x[i], x[i+1], 10)  
    #  #yy = numpy.linspace(y[i], y[i+1], 10)
    #  xnew = numpy.append(xnew,xx)
    #  #ynew = numpy.append(yy)

    # f2 = CubicSpline(x, y,bc_type='natural')
    # x_new = xnew
    # y_new = f2(x_new)
    # plt.gca().lines[0].set_xdata(xdata_p[-59:])
    # plt.gca().lines[0].set_ydata(ydata_p[-59:])
    plt.gca().lines[0].set_xdata(xdata_p)
    plt.gca().lines[0].set_ydata(ydata_p)
    
    plt.gca().lines[1].set_xdata([new_px])
    plt.gca().lines[1].set_ydata([new_py])
    # xdata = numpy.append(plt.gca().lines[0].get_xdata(), plt.gca().lines[1].get_xdata())
    # ydata = numpy.append(plt.gca().lines[0].get_ydata(), plt.gca().lines[1].get_ydata())
    plt.draw()

    #figure(2)
    plt.figure(2)
    axes2 = plt.gcf().get_axes()
    # line1 = axes2[0].lines[0]
    # alpha1 = line1.get_xdata()
    # radius1 = line1.get_ydata()

    # line2 = axes2[0].lines[1]
    # alpha2 = line2.get_xdata()
    # radius2 = line2.get_ydata()

    #print("alpha1= alpha2 = radius1 =  radius2 = ",alpha1 ,alpha2 ,radius1 ,radius2)
    # Winkeldaten
    #winkel = numpy.append(plt.gca().lines[0].get_alpha(), plt.gca().lines[1].get_alpha())
    xdata_w = numpy.append(plt.gca().lines[0].get_xdata(), plt.gca().lines[1].get_xdata())
    ydata_w = numpy.append(plt.gca().lines[0].get_ydata(), plt.gca().lines[1].get_ydata())


    plt.gca().lines[0].set_xdata(xdata_w[-59:])
    plt.gca().lines[0].set_ydata(ydata_w[-59:])
    
    plt.gca().lines[1].set_xdata([new_w])
    plt.gca().lines[1].set_ydata([new_r])
    # plt.gca().lines[0].set_xdata(xdata[-59:])
    # plt.gca().lines[0].set_ydata(ydata[-59:])
    
    # plt.gca().lines[1].set_xdata([new_x])
    # plt.gca().lines[1].set_ydata([new_y])
    
    #plt.plot(new_x,new_y,'.')
    # plt.plot(xdata,ydata,'-r')
    # plt.pause(0.01)
    plt.draw()
    #sleep(0.01)
    
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
    
    #create plot
    global fig
    #plt.ion()
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
    #cx = fig.add_subplot(111)
    cx.plot([],[], 'ro',ls='-')
    #cx.plot(1,3, 'ro')
    cx.grid(True)
    dx = fig.add_subplot(111,projection='polar')
    #dx = fig.add_subplot(111)
    dx.plot([],[], 'bo',ls='-')
    #dx.plot(3,3, 'bo')
    #plt.axis('equal')
    axes = plt.gca()
    axes.set_rmax(4)
    #axes.set_xlim([0,500])
    #axes.set_ylim([0,500])
    # axes.set_xlabel('Zeit',fontsize=10)
    # axes.set_ylabel('Winkel',fontsize=10)

    global hedge
    hedge = MarvelmindHedge(tty = "/dev/ttyUSB0", adr=10, recieveUltrasoundPositionCallback=update_line) # create MarvelmindHedge thread
    hedge.start()
    
    plotThread = Thread(target=printThread) # create and start console out thread
    plotThread.start()
    
    plt.show()
    
main()
