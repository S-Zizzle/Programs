import numpy as np
import matplotlib.pyplot as plt 

q,w = (-1.25,0.055)
#zoom = 1 / 1000000
end = 220
res = 150

for k in range (0,end,1):
    #zoom = (1 - (k / end))
    zoom = np.exp(-0.1*k)

    x_min = (q - zoom*2)
    x_max = (q + zoom)

    y_min = (w - zoom)
    y_max = (w + zoom)

    m = int(3 * res)
    n = int(2 * res)

    x = np.linspace(x_min,x_max,num=m).reshape((1,m))
    y = np.linspace(y_min,y_max,num=n).reshape((n,1))

    C = np.tile(x,(n,1)) + 1j * np.tile(y,(1,m))

    Z = np.zeros((n,m), dtype=complex)
    M = np.full((n,m), True, dtype=bool)
    N = np.zeros((n,m))

    for i in range (0,100):
        Z[M] = Z[M] * Z[M] + C[M]
        M[np.abs(Z) > 2] = False
        O = np.logical_not(M)
        P = O.astype(int)
        N[O] = N[O] + P[O]
        print(i)


    im = plt.figure(frameon=False)
    #im = plt.imshow(N, cmap="terrain_r",interpolation="none")
    #im = plt.matshow(N, cmap="binary",interpolation="none")
    im = plt.matshow(N, cmap="hot_r", interpolation="none")
    plt.axis("off")
    plt.savefig("mandel"+ str(k) +".png",
    dpi = res * (3/5),frameon=False,
    bbox_inches="tight", pad_inches=0)
    plt.show(im)