from matplotlib import pyplot as plt
import numpy as np

# fig = plt.figure()
# ax1 = fig.add_subplot(2, 2, 1)
# ax2 = fig.add_subplot(2, 2, 2)
# ax3 = fig.add_subplot(2, 2, 3)
# plt.plot(np.random.randn(50), 'k--')
array = np.random.randn(100)
# ax1.hist(array, bins=20, color='k', alpha=0.3) #alpha表示透明度
# ax2.scatter(array, array + 3 * np.random.randn(100))

# fig, axes = plt.subplots(2, 2, sharex=True, sharey=True)
# for i in range(2):
#     for j in range(2):
#         axes[i, j].hist(np.random.randn(500), bins=50, color='g', alpha=0.5)
# plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0,
#                     wspace=0) #这个设置在pycharm自带的SciView中不生效

fig, axes = plt.subplots(2, 2)
axes[0][0].plot(np.random.randn(30).cumsum(), 'ko--')
axes[0][1].plot(np.random.randn(30).cumsum(), color='r', linestyle='dashed', marker='o')
plt.xlim(0, 5) #设置只对最后一个axes生效，除非sharex=True，可以应用到所有axes上
axes[0][0].set_xlim(0, 5) #单独设置某个axes的坐标范围

plt.show()