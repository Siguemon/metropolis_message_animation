import numpy as np
import matplotlib.pyplot as plt

def domain()

#####
fig = plt.figure()
grid = plt.GridSpec(2,2, width_ratios=[8,1], height_ratios=[8,1])

ax = fig.add_subplot(grid[0,0],aspect=1)
bx = fig.add_subplot(grid[1,0],sharex=ax)
cx = fig.add_subplot(grid[0,1],sharey=ax)

# ax.hist2d(X,Y, bins=200)

plt.show()
