import numpy as np
import matplotlib.pyplot as plt

for i in range(1,100):
    N = 10
    x = np.random.rand(N)
    y = np.random.rand(N)
    plt.figure()
    plt.axis((0,1,0,1))
    plt.scatter(x, y)
    np.delete(x,0)
    np.delete(y,0)
    name = 'images/foo'+str(i)+'.png'
    plt.savefig(name)
    plt.close()
