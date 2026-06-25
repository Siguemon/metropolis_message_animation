import sys
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

try    : file  = str(sys.argv[1])
except : print(f'Usage for {sys.argv[0]} : ./{sys.argv[0]} <file.png> <tresh=40> <margin=10px>')

try : tresh = int(sys.argv[2])
except : tresh=40

try : margin = int(sys.argv[3])
except : margin = 10

print(f'Running {sys.argv[0]} for tresh={tresh} and margin={margin}px.\n')
###
#define the filter
def filter(val, tresh=50):
    if val < tresh : return 0
    else : return 255

vfilter = np.vectorize(filter, excluded={'tresh'})

###
img  = np.array(Image.open(file))
data = 255 - np.mean(img, axis=2)
shapey, shapex = data.shape #beware these are inverted !
print(f'Img dims : {shapex}x{shapey}px')

#remove the margins
X,Y = np.meshgrid(np.arange(shapex), np.arange(shapey))
cond = ((X <= margin) | (shapex - X <= margin)) | ((Y <= margin) | (shapey - Y <= margin))
data = np.where(cond, 0, data) #remove the margins

#filter the image
filtered = vfilter(data, tresh)

#save the image
rep = 255 - filtered
im = Image.fromarray(rep.astype(np.uint8))
im.save(f"filtered_{file}")
print(f'Saved image as filtered_{file}')

###
fig = plt.figure(figsize=(12,4))
grid = plt.GridSpec(1,3)
ax = fig.add_subplot(grid[1], title='Original')
bx = fig.add_subplot(grid[2], title=f'Filter applied (tresh : {tresh})')
cx = fig.add_subplot(grid[0], title='Filter', aspect=1, xlim=[-1,256], ylim=[-1,256])

#display the original image
ax.imshow(data, cmap='Greys')

#display the treated image
bx.imshow(filtered, cmap='Greys_r')

#plot the filter
tt = np.arange(255)
yy = vfilter(tt, tresh)
cx.plot(tt,tt, 'k--', lw=.5)
cx.plot(tt,yy, 'k-', lw=2)

plt.show()
