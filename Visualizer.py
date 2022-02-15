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

#Replace these with the actual position files
readPositions('TestCoords01.txt')
readPositions('TestCoords02.txt')


fig = plt.figure(figsize=(10,8))
ax = p3.Axes3D(fig)
def setup():            
    ax.axis('off')
    X = []
    Y = []
    Z = []
    for bod in bodlist:
        X.append(bod[0][0])
        Y.append(bod[0][1])
        Z.append(bod[0][2])
    scat = ax.scatter(X, Y, Z, marker = 'o', color='blue')
    return scat, 

def Update(i):  #replaces the previous coordinates with the next ones for each frame
    X = []
    Y = []
    Z = []
    for bod in bodlist:
        X.append(bod[i][0])
        Y.append(bod[i][1])
        Z.append(bod[i][2])
    scat = ax.scatter(X, Y, Z, marker = 'o', color='blue')


    return scat,

#the interval is how much time there is between each frame in milliseconds.
ani = animation.FuncAnimation(fig, Update, init_func=setup, interval=1000, repeat=True)
plt.show()
