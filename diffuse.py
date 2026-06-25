import sys
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from numba import njit

try :
    file = sys.argv[1]
    name = file.split('.')[0]
except : raise TypeError(f'{sys.argv[0]} usage : ./{sys.argv[0]} <file> <mean_width=5px> <n_iterations=10>')

try : wid = int(sys.argv[2])
except : wid = 5 #px

try : it = int(sys.argv[3])
except : it = 10

print(f'Running {sys.argv[0]} for {file}, {wid}px and {it} iterations.')
####define some functions and use numba to speed up the process
@njit
def process(a, wid=10):
    rep = np.zeros(a.shape)

    for (i,j),k in np.ndenumerate(a[wid:-wid, wid:-wid]):
        (x,y) = (i+wid, j+wid)

        window = a[x-wid:x+wid , y-wid:y+wid]
        rep[x,y] = (np.mean(window))

    return rep

@njit
def diffuse(a, wid=10, iterations=6):
    rep = process(a, wid=wid)
    for i in range(iterations - 1):
        print(f'It. {i+1}/{iterations}...')
        rep = process(rep, wid=wid)

    print('Done !')
    return 255/np.max(rep) * rep



#### let us begin
a = np.asarray(Image.open(file))
print(a.shape)
if len(a.shape)-2: a = 255 - a[:,:,0]
else :             a = 255 - a

print(f'Image dimensions : {a.shape[1]}.{a.shape[0]}px')

a = diffuse(a, wid, it)

######
fig = plt.figure()
ax = fig.add_subplot()

im = ax.imshow(a, cmap='magma')

plt.colorbar(im, ax=ax)

ax.set_title(fr'wid_{wid}_it_{it}.png')
plt.show()

# plt.savefig(fr'wid_{wid}_it_{it}.png', dpi=300)

np.savetxt(f'{name}.txt', a)
print(f'Saved output as ./{name}.txt')
