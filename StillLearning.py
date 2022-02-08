import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from Objects import Body



#sun = Body('Sun', 1.989*10**30, 696.3*10**6, [0, 0, 0], [0, 0, 0])
#earth = Body('Earth', 5.972*10**24,6.371*10**6, [149.6*10**9, 0, 0], [0, 30000, 0])
sun = Body('Sun', 10, [-30, -30, 0], [6, 0, 0])
earth = Body('Earth', 500, [0, 0, 0], [0, 0, 0])






fig = plt.figure()
ax1 = fig.add_subplot()
ax2 = fig.add_subplot()
Svi = sun.get_position()
Evi = earth.get_position()
xdata1, ydata1 = [], []
ln1, = plt.plot([], [])
xdata2, ydata2 = [], []
ln2, = plt.plot([], [])
theta = np.linspace(0,2*np.pi,500)
dt = 0.1
#G = 6.67408*10**-11
G = 2
def init():
    for ax in (ax1, ax2):
        ax.set_xlim(-50,50)
        ax.set_ylim(-50,50)
    return ln1, ln2

def update(i):

    sp = sun.get_position()
    ep = earth.get_position()
    sm = sun.get_mass()
    em = earth.get_mass()
    sv = sun.get_velocity()
    ev = earth.get_velocity()
    
    r = []
    r.append(sp[0]-ep[0])
    r.append(sp[1]-ep[1])
    r.append(sp[2]-ep[2])
    rmag = np.sqrt((sp[0]-ep[0])**2 + (sp[1]-ep[1])**2 + (sp[2]-ep[2])**2)
    

    Fx = ((G*sm*em)/rmag**3)*r[0]
    Fy = ((G*sm*em)/rmag**3)*r[1]
    Fz = ((G*sm*em)/rmag**3)*r[2]

    Sax = -Fx/sm
    Say = -Fy/sm
    Saz = -Fz/sm

    Eax = Fx/em
    Eay = Fy/em
    Eaz = Fz/em

    Svx = sv[0] + Sax * dt
    Svy = sv[1] + Say * dt
    Svz = sv[2] + Saz * dt
    newsv = [Svx, Svy, Svz]
    sun.update_velocity(newsv)

    Evx = ev[0] + Eax * dt
    Evy = ev[1] + Eay * dt
    Evz = ev[2] + Eaz * dt
    newev = [Evx, Evy, Evz]
    earth.update_velocity(newev)
    
    Spx = sp[0] + Svx * dt
    Spy = sp[1] + Svy * dt
    Spz = sp[2] + Svz * dt
    newsp = [Spx, Spy, Spz]
    sun.update_position(newsp)

    Epx = ep[0] + Evx * dt
    Epy = ep[1] + Evy * dt
    Epz = ep[2] + Evz * dt
    newep = [Epx, Epy, Epz]
    earth.update_position(newep)
    
    xdata1.append(Spx)
    ydata1.append(Spy)
    xdata2.append(Epx)
    ydata2.append(Epy)
    ln1.set_data(xdata1, ydata1)
    ln2.set_data(xdata2, ydata2)
    return ln1, ln2


ani = animation.FuncAnimation(fig, update, frames=500, interval=100, init_func=init)

plt.show()






































