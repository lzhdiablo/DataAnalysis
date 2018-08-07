from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
from mpl_toolkits.basemap import Basemap #使用该命令安装basemap: conda install -c conda-forge basemap

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

# fig, axes = plt.subplots(2, 2)
# axes[0][0].plot(np.random.randn(30).cumsum(), 'ko--')
# axes[0][1].plot(np.random.randn(30).cumsum(), color='r', linestyle='dashed', marker='o')
# plt.xlim(0, 5) #设置只对最后一个axes生效，除非sharex=True，可以应用到所有axes上
# axes[0][0].set_xlim(0, 5) #单独设置某个axes的坐标范围
# axes[1][0].plot(np.random.randn(1000).cumsum(), color='k', label='one')
# axes[1][0].plot(np.random.randn(1000).cumsum(), color='g', label='two')
# axes[1][0].plot(np.random.randn(1000).cumsum(), color='r', label='three')
# axes[1][0].legend(loc='best') #配置图例
# axes[1][0].set_xticks(np.arange(0, 1250, step=250)) #设置坐标刻度
# axes[1][0].set_xticklabels(('Tom', 'Dick', 'Harry', 'Sally', 'Sue')) #设置刻度显示名称
# axes[1][0].text(500, 11, 'Hello World!') #在指定坐标增加注释

# ax = plt.subplot(1, 1, 1)
# data = pd.read_csv('ch08/spx.csv', index_col=0, parse_dates=True)
# spx = data.SPX
# spx.plot(ax=ax, style='k-')
# crisis_data = {datetime(2007, 10, 11): 'Peak of bull market',
#                datetime(2008, 3, 12): 'Bear Stearns Fails',
#                datetime(2008, 9, 15): 'Lehman Bankruptcy'}
# for date, label in crisis_data.items():
#     ax.annotate(label,
#                 xy=(date, spx.asof(date) + 50),
#                 xytext=(date, spx.asof(date) + 200),
#                 arrowprops=dict(facecolor='red'),
#                 horizontalalignment='left',
#                 verticalalignment='top')
# ax.set_xlim('1/1/2007', '1/1/2011')
# ax.set_ylim([600, 1800])
# ax.set_title('Important dates in 2008-2009 financial crisis')

# ax = plt.subplot(1, 1, 1)
# rect = plt.Rectangle((0.2, 0.75), 0.4, 0.15, color='k', alpha=0.3)
# circ = plt.Circle((0.7, 0.2), 0.15, color='b', alpha=0.3)
# pgon = plt.Polygon([[0.15, 0.15], [0.35, 0.4], [0.2, 0.6]], color='r', alpha=0.5)
# ax.add_patch(rect)
# ax.add_patch(circ)
# ax.add_patch(pgon)
# plt.savefig('figpath.png', dpi=400, bbox_inches='tight')

# fig, axes = plt.subplots(3, 1)
# tips = pd.read_csv('ch08/tips.csv')
# party_counts = pd.crosstab(tips['day'], tips['size'])
# party_pcts = party_counts.div(party_counts.sum(1), axis=0)
# party_reversed = party_pcts.stack().unstack(level=0) #level控制将哪一级索引转换为列索引
# party_pcts.plot(kind='bar', stacked=True, ax=axes[0])
# party_reversed.plot(kind='bar', stacked=True, ax=axes[1])
# tips['tip_pct'] = tips['tip'] / tips['total_bill']
# # tips['tip_pct'].hist(bins=50, ax=axes[2])
# tips['tip_pct'].plot(kind='kde', ax=axes[2]) #kde需要引入scipy包

# comp1 = np.random.normal(0, 1, size=200)
# comp2 = np.random.normal(10, 2, size=200)
# values = pd.Series(np.concatenate([comp1, comp2]))
# values.hist(bins=100, alpha=0.3, color='k', density=True)
# values.plot(kind='kde', style='k--')

# macro = pd.read_csv('ch08/macrodata.csv')
# data = macro[['cpi', 'm1', 'tbilrate', 'unemp']]
# trans_data = np.log(data).diff().dropna()
# # plt.scatter(trans_data['m1'], trans_data['unemp'])
# # plt.title('Changes in log %s vs. log %s' % ('m1', 'unemp'))
# pd.plotting.scatter_matrix(trans_data, diagonal='kde', color='k', alpha=0.3)

data = pd.read_csv('ch08/Haiti.csv')
data = data[(data.LATITUDE > 18)
            & (data.LATITUDE < 20)
            & (data.LONGITUDE > -75)
            & (data.LONGITUDE < -70)
            & data.CATEGORY.notnull()]
def to_cat_list(catstr):
    stripped = (x.strip() for x in catstr.split(','))
    return [x for x in stripped if x]
def get_all_categories(cat_series):
    cat_sets = (set(to_cat_list(x)) for x in cat_series)
    return sorted(set.union(*cat_sets))
def get_english(cat):
    code, names = cat.split('.')
    if '|' in names:
        names = names.split('|')[1]
    return code, names.strip()
all_cats  = get_all_categories(data.CATEGORY)
english_mapping = dict(get_english(x) for x in all_cats)
def get_code(seq):
    return [x.split('.')[0] for x in seq if x]
all_codes = get_code(all_cats)
code_index = pd.Index(np.unique(all_codes))
dummy_frame = pd.DataFrame(np.zeros((len(data), len(code_index))), index=data.index, columns=code_index)
for row, cat in zip(data.index, data.CATEGORY):
    codes = get_code(to_cat_list(cat))
    dummy_frame.loc[row, codes] = 1

print(dummy_frame)

plt.show()