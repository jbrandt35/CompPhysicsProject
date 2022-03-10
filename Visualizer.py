import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

bodlist = []
def readPositions(fileName):  # Gets the body's positions from the text file and adds it to a list
    with open(fileName) as tc:
        tccoords = tc.readlines()

    b = tccoords[0].split('\t')
    theb = []
    for l in range(len(b)):
        alist = []
        x = b[l].split(',')
        for y in range(len(x)):
            a = float(x[y])
            alist.append(a)
        theb.append(alist)
    bodlist.append(theb)

fig = plt.figure(figsize=(10,8))
ax = p3.Axes3D(fig)

"""""""""
Body One
"""""""""
readPositions('TestCoords01.txt')
x1list = []
y1list = []
z1list = []
def addtolist1(x,y,z):
    x1list.append(x)
    y1list.append(y)
    z1list.append(z)

"""""""""
Body Two
"""""""""
readPositions('TestCoords02.txt')
x2list = []
y2list = []
z2list = []
def addtolist2(x,y,z):
    x2list.append(x)
    y2list.append(y)
    z2list.append(z)

"""""""""
Body Three
"""""""""
"""
x3list = []
y3list = []
z3list = []
def addtolist3(x,y,z):
    x3list.append(x)
    y3list.append(y)
    z3list.append(z)
ax31 = p3.Axes3D(fig)
ax32 = p3.Axes3D(fig)

...etc.
"""

def setup():
    ax.axis('off')
    ax.set_facecolor('black')
    
    #For Body One
    bod1 = bodlist[0]
    X1 = bod1[0][0]
    Y1 = bod1[0][1]
    Z1 = bod1[0][2]
    addtolist1(X1, Y1, Z1)
    scat1 = ax.scatter(X1, Y1, Z1, s=400, marker = 'o', color='blue')
    lin1 = ax.scatter(x1list, y1list, z1list, color='blue')

    #For Body Two
    bod2 = bodlist[1]
    bod2 = bodlist[1] 
    X2 = bod2[0][0]
    Y2 = bod2[0][1]
    Z2 = bod2[0][2]
    addtolist2(X2, Y2, Z2)
    scat2 = ax.scatter(X2, Y2, Z2, marker = 'o', color='red')
    lin2 = ax.scatter(x2list, y2list, z2list, color='red')

    return scat1, lin1, lin2, scat2

def Update(i):
    ax.clear()
    ax.axis('off')
    ax.set_facecolor('black')
    
    #For Body One
    bod1 = bodlist[0]
    X1 = bod1[i][0]
    Y1 = bod1[i][1]
    Z1 = bod1[i][2]
    addtolist1(X1,Y1,Z1)
    scat1 = ax.scatter(x1list[i+1], y1list[i+1], z1list[i+1],s=400, marker = 'o', color='blue')
    lin1 = ax.plot(x1list, y1list, z1list, color='blue')

    #For Body Two
    bod2 = bodlist[1]
    X2 = bod2[i][0]
    Y2 = bod2[i][1]
    Z2 = bod2[i][2]
    addtolist2(X2,Y2,Z2)
    scat2 = ax.scatter(x2list[i+1], y2list[i+1], z2list[i+1], marker = 'o', color='red')
    lin2 = ax.plot(x2list, y2list, z2list, color='red')

    return scat1, lin1, lin2, scat2

#the interval is how much time there is between each frame in milliseconds.
ani = animation.FuncAnimation(fig, Update, init_func=setup, interval=1000, repeat=True)
plt.show()
