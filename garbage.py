import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

try :
    file = sys.argv[1]
    name = file.split('.')[0]

    dimx = int(sys.argv[2])
    dimy = int(sys.argv[3])
except : raise TypeError(f'{sys.argv[0]} usage : ./{sys.argv[0]} <file> <dimx> <dimy> <interval=1ms>')

try : interval = int(sys.argv[4])
except : interval = 1 #ms

######
data = np.loadtxt(fr'to_show/{file}').T
(x, y) = (data[0], data[1])

fig = plt.figure()
ax = fig.add_subplot(aspect=1)

#init
line  = ax.plot(x[0], y[0], 'ko', ms=.5, alpha=.4)[0]
title = plt.suptitle(f'Nb of points : 1')
ax.set(xlim=[0,dimx], ylim=[0,dimy])
ax.set_axis_off()

#animation function
def update(frame):
    line.set_xdata(x[:frame])
    line.set_ydata(y[:frame])

    #for debug
    if frame==x.size-1 : title.set_text(f'')
    else :               title.set_text(f'Nb of points : {frame}')

    return line

#animation
frames = np.arange(x.size)
ani = animation.FuncAnimation(fig=fig, func=update, frames = frames, interval = interval, repeat=0)

manager = plt.get_current_fig_manager() ; manager.full_screen_toggle()
plt.show()
