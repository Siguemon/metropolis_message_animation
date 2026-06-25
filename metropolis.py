import sys
from numba import njit
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import RegularGridInterpolator as RGI

try :
    file = sys.argv[1]
    name = file.split('.')[0]
except : raise TypeError(f'{sys.argv[0]} usage : ./{sys.argv[0]} <file> <npoints=5000> <ctrbound=20> <saturationbound=400>')

try : npoints = int(sys.argv[2])
except : npoints = 5000

try : ctrbound = int(sys.argv[3])
except : ctrbound = 20

try : saturationbound = int(sys.argv[4])
except : saturationbound = 400

print(f'Running {sys.argv[0]} for {file}, npoints={npoints}, ctrbound={ctrbound} and satbound={saturationbound}.\n')
#importer l'image et quelques notations pour les dimensions
Z = np.loadtxt(file).T
shax, shay = Z.shape
x,y = np.arange(shax), np.arange(shay)
print(f'Image dimensions : {shax}.{shay}px')

#faire l'interpolation sur l'image pour donner l'effet continu et virer les effets de bords en prolongeant la fonction
interp = RGI((x,y), Z)
def f(X,Y):
    if (0<=X<=shax-1) & (0<Y<shay-1): return interp((X,Y))
    else : return 0

#metropolis-hastings pour évoluer dans le plan
def metropolis_hastings(f, npoints=3000, scale=shay/15, ctrbound=10, saturationbound=500):
    (repx, repy) = (np.array([]), np.array([]))

    for i in range(int(npoints)):
        (initx, inity) = (np.random.uniform(0,shax-1), np.random.uniform(0,shay-1)) #tirer une position au pif dans le domaine

        (ctr, saturation) = (0, 0)
        while ctr<ctrbound and saturation<saturationbound:
            (propx, propy) = (np.random.normal(loc=initx, scale=scale), np.random.normal(loc=inity, scale=scale))

            if (f(propx, propy) > f(initx, inity) * np.random.random()):
                ctr += 1
                (initx, inity) = (propx, propy)
                del propx, propy

            saturation += 1

        if ctr==ctrbound:
            print(i, end='\r       ')
            repx = np.append(repx, initx)
            repy = np.append(repy, inity)

        del initx, inity, ctr, saturation

    return repx, shay - 1 - repy #inversé parce que l'interpolation fait la transposition pour une raison obscure

##########
print(f'Running {sys.argv[0]} for {file}')

scale = shay/20
(datax, datay) = metropolis_hastings(f, npoints, scale, ctrbound, saturationbound)

np.savetxt(fr'to_show/{file}', np.array([datax, datay]).T)
print(f'Saved output as ./to_show/{name}.txt')
######

fig = plt.figure(figsize=(10,5))
grid = plt.GridSpec(1,2)
ax = fig.add_subplot(grid[0])
bx = fig.add_subplot(grid[1], aspect=1)

ax.imshow(Z.T, cmap='Greys')
# bx.hist2d(datay, datax, bins=100, cmap='Greys')
bx.plot(datax, datay, 'bo', ms=.5, alpha=.1)


bx.set_xlim(0, shax-1)
bx.set_ylim(0, shay-1)
# bx.yaxis.set_inverted(1)

ax.set_title('Probability Density Field')
bx.set_title(f'Simulated random position on the field : \n{datax.size}/{npoints} dots placed')

plt.show()
