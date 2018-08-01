import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv, qr

np.set_printoptions(suppress=True)
names = np.array(['Bob', 'Joe', 'Will', 'Bob', 'Will', 'Joe', 'Joe'])
data = np.random.randn(7, 4)
data[names == 'Bob']

points = np.arange(-5, 5, 0.01)
xs, ys = np.meshgrid(points, points)
z = np.sqrt(xs ** 2 + ys ** 2)
# plt.imshow(z, cmap=plt.cm.gray)
# plt.colorbar()
# plt.show()

xarr = np.arange(5)
yarr = np.arange(5, 10)
carr = np.array([True, True, False, True, False])
# print([x if c else y for x, y, c in zip(xarr, yarr, carr)])
# print(np.where(carr, xarr, yarr))

arr = np.random.randn(5, 4)
# print(arr)
# print(arr.mean())
# print(arr.mean(1))

arr = np.arange(10)
# np.save('some_array', arr)
# arr = np.load('some_array.npy')
# print(arr)

arr = np.random.randn(5,5)
# np.savetxt('array', arr, delimiter=', ', fmt='%.10f')
q, r = qr(arr)

nsteps = 1000
nwalks = 5000
draws = np.random.randint(0, 2, size=(nwalks, nsteps))
steps = np.where(draws > 0, 1, -1)
walks = steps.cumsum(1)
hits30 = (np.abs(walks) >= 30).any(1)
crossing_times = (np.abs(walks[hits30]) > 30).argmax(1)

