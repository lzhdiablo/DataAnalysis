import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap, cm
from matplotlib import rcParams
from matplotlib.collections import LineCollection
import shapefile
import dbf

df = pd.DataFrame({'key1': ['a', 'a', 'b', 'b', 'a'],
                   'key2': ['one', 'two', 'one', 'two', 'one'],
                   'data1': np.random.randn(5),
                   'data2': np.random.randn(5)})
means1 = df['data1'].groupby(df['key1']).mean()
means2 = df['data1'].groupby([df['key1'], df['key2']]).mean() #等价于df.groupby('key1')['data1']
size = df['data1'].groupby([df['key1'], df['key2']]).size()
# print(means2.unstack(level=1))
# print(means2.unstack(level=0))
states = np.array(['Ohio', 'California', 'California', 'Ohio', 'Ohio'])
years = np.array([2005, 2005, 2006, 2005, 2006])
means3 = df['data1'].groupby([states, years]).mean()
# for name, group in df.groupby('key1'):
#     print(name)
#     print(group)
# for (k1, k2), group in df.groupby('key1', 'key2'):
#     print(k1, k2)
#     print(group)
pieces = dict(list(df.groupby('key1')))
# print(pieces['b'])

people = pd.DataFrame(np.random.randn(5, 5),
                      columns=['a', 'b', 'c', 'd', 'e'],
                      index=['Joe', 'Steve', 'Wes', 'Jim', 'Travis'])
people.ix[2:3, ['b', 'c']] = np.nan
mapping = {'a': 'red', 'b': 'red', 'c': 'blue', 'd': 'blue', 'e': 'red', 'f': 'orange'}
by_column = people.groupby(mapping, axis=1)
# for name, group in by_column:
#     print(name)
#     print(group)
# print(by_column.sum())
map_series = pd.Series(mapping)
# print(people.groupby(map_series, axis=1).sum())
# print(people.groupby(len).sum()) #任何被当作分组键的函数都会在各个索引值上被调用一次，其返回值就会被用作分组名称
key_list = ['one', 'one', 'one', 'two', 'two']
# for (k1, k2), group in people.groupby([len, key_list]):
#     print(k1, k2)
#     print(group)
# print(people.groupby([len, key_list]).min())

columns = pd.MultiIndex.from_arrays([['US', 'US', 'US', 'JP', 'JP'], [1, 3, 5, 1, 3]], names=['city', 'tenor'])
hier_df = pd.DataFrame(np.random.randn(4, 5), columns=columns)
# print(hier_df)
# print(hier_df.groupby(level='city', axis=1).count())

# grouped = df.groupby('key1')['data1']
def peak_to_peak(arr):
    return arr.max() - arr.min()
# print(grouped.agg(peak_to_peak)) #自定义聚合函数， 自定义函数通常比优化过的函数执行效率低

tips = pd.read_csv('ch08/tips.csv')
tips['tip_pct'] = tips['tip'] / tips['total_bill']
grouped = tips.groupby(['sex', 'smoker'])
mean_tip_pct = grouped['tip_pct'].mean()
# print(grouped['tip_pct'].agg(['mean', 'std', peak_to_peak]))
# print(grouped['tip_pct'].agg([('foo', 'mean'), ('bar', np.std)]))
functions = [('foo', 'mean'), ('bar', np.std)]
result = grouped['tip_pct', 'total_bill'].agg(functions)
# print(grouped.agg({'tip': np.max, 'size': np.sum}))
# print(grouped.agg({'tip_pct': [('foo', 'mean'), ('bar', np.std)], 'size': np.sum}))
# print(tips.groupby(['sex', 'smoker'], as_index=False).mean()) # as_index=False无索引

key = ['one', 'two', 'one', 'two', 'one']
def demean(arr):
    return arr - arr.mean()
demeaned = people.groupby(key).transform(demean)

def top(df, n=5, column='tip_pct'):
    return df.sort_values(by=column)[-n:]
grouped = tips.groupby('smoker').apply(top) # top函数在每个片段中应用，然后由pandas.concat连接
grouped = tips.groupby(['smoker', 'day']).apply(top, n=1, column='total_bill')
# 如果传入apply的函数能够接受参数， 可以将这些内容放在apply函数中一并传入
grouped = tips.groupby('smoker', group_keys=False).apply(top) # group_keys=False可以禁止分组键和原始索引构成层次化索引

frame = pd.DataFrame({'data1': np.random.randn(1000), 'data2': np.random.randn(1000)})
factor = pd.cut(frame.data1, 4)
def get_stats(group):
    return {'min': group.min(), 'max': group.max(), 'count': group.count(), 'mean': group.mean()}
grouped = frame.data2.groupby(factor)
# print(grouped.apply(get_stats).unstack())
factor = pd.qcut(frame.data1, 10, labels=False)
grouped = frame.data2.groupby(factor)
# print(grouped.apply(get_stats).unstack()) # 当分组后片段为Series时，apply的返回值可以是一个字典，结果和分组键构成层次化索引

states = ['Ohio', 'New York', 'Vermont', 'Florida',
          'Oregon', 'Nevada', 'California', 'Idaho']
group_key = ['East'] * 4 + ['West'] * 4
data = pd.Series(np.random.randn(8), index=states)
data['Vermont', 'Nevada', 'Idaho' ] = np.nan
fill_mean = lambda g: g.fillna(g.mean())
# print(data.groupby(group_key).apply(fill_mean))
fill_values = {'East': 0.5, 'West': -1}
fill_func = lambda g: g.fillna(fill_values[g.name])
# print(data.groupby(group_key).apply(fill_func))

suits = ['H', 'S', 'C', 'D']
card_val = (np.arange(1, 11).tolist() + [10] * 3) * 4
base_names = ['A'] + np.arange(2, 11).tolist() + ['J', 'K', 'Q']
cards = []
for suit in suits:
    cards.extend(str(num) + suit for num in base_names)
deck = pd.Series(card_val, index=cards)
def draw(deck, n=5):
    return deck.take(np.random.permutation(len(deck))[:n])
# print(draw(deck)) #随机抽取5张牌
get_suit = lambda card: card[-1]
deck.groupby(get_suit).apply(draw, n=2) #从每种花色中随机抽取两张牌

df = pd.DataFrame({'category': ['a', 'a', 'a', 'a', 'b', 'b', 'b', 'b'],
                   'data': np.random.randn(8),
                   'weights': np.random.randn(8)})
grouped = df.groupby('category')
get_wavg = lambda g: np.average(g['data'], weights=g['weights'])
grouped.apply(get_wavg) #计算分组加权平均数

mean1 = tips.groupby(['sex', 'smoker']).mean()
mean1 = tips.pivot_table(index=['sex', 'smoker']) # pivot_table默认聚合为取平均，效果和groupby相同
mean2 = tips.pivot_table(['tip_pct', 'size'], index=['sex', 'smoker'], columns='day', margins=True, aggfunc=sum)

data = pd.DataFrame({'Sample': np.arange(1, 11),
                     'Gender': ['Female', 'Male', 'Female', 'Male', 'Male', 'Male', 'Female', 'Female', 'Male', 'Female'],
                     'Handedness': ['Right-handed', 'Left-handed', 'Right-handed', 'Right-handed', 'Left-handed', 'Right-handed',
                                    'Right-handed', 'Left-handed', 'Right-handed', 'Right-handed']})
sum = data.pivot_table(index='Gender', columns='Handedness', aggfunc=len, margins=True)
sum = pd.crosstab(data.Gender, data.Handedness, margins=True) #此效果用pivot_table同样可以实现，但会出现重复数据，columns参数会和原来的columns构成层级化索引，数据重复
tip_sum = pd.crosstab([tips.time, tips.day], tips.smoker, margins=True)

fec = pd.read_csv('ch09/P00000001-ALL.csv', low_memory=False)
unique_cands = fec.cand_nm.unique()
parties = {'Bachmann, Michelle': 'Republican',
           'Romney, Mitt': 'Republican',
           'Obama, Barack': 'Democrat',
           "Roemer, Charles E. 'Buddy' III": 'Republican',
           'Pawlenty, Timothy': 'Republican',
           'Johnson, Gary Earl': 'Republican',
           'Paul, Ron': 'Republican',
           'Santorum, Rick': 'Republican',
           'Cain, Herman': 'Republican',
           'Gingrich, Newt': 'Republican'}
fec['party'] = fec.cand_nm.map(parties)
fec = fec[fec.contb_receipt_amt > 0] #只考虑赞助额不考虑退款情况
fec_mrbo = fec[fec.cand_nm.isin(['Obama, Barack', 'Romney, Mitt'])]
occ_mapping = {'C.E.O.': 'CEO',
               'INFORMATION REQUESTED': 'NOT PROVIDED',
               'INFORMATION REQUESTED PER BEST EFFORTS': 'NOT PROVIDED',
               'INFORMATION REQUESTED (BEST EFFORTS)': 'NOT PROVIDED'}
f = lambda x: occ_mapping.get(x, x)
fec.contbr_occupation = fec.contbr_occupation.map(f)
emp_mapping = {'SELF': 'SELF-EMPLOYED',
               'INFORMATION REQUESTED': 'NOT PROVIDED',
               'INFORMATION REQUESTED PER BEST EFFORTS': 'NOT PROVIDED',
               'SELF EMPLOYED': 'SELF-EMPLOYED'}
f = lambda x: emp_mapping.get(x, x)
fec.contbr_employer = fec.contbr_employer.map(f)
by_occupation = fec.pivot_table('contb_receipt_amt', index='contbr_occupation', columns='party', aggfunc=np.sum)
over_2mm = by_occupation[by_occupation.sum(1) > 2000000]
# over_2mm.plot(kind='bar')
def get_top_amount(group, key, n=5):
    totals = group.groupby(key)['contb_receipt_amt'].sum()
    return totals.sort_values(ascending=False)[:n]
top_contbr = fec_mrbo.groupby('cand_nm').apply(get_top_amount, 'contbr_occupation', n=7)
# print(top_contbr)
bins = np.array([0, 1, 10, 100, 1000, 10000, 100000, 1000000, 10000000])
labels = pd.cut(fec_mrbo.contb_receipt_amt, bins=bins)
grouped = fec_mrbo.groupby(['cand_nm', labels])
# print(grouped.size().unstack(level=0))
bucket_sums = grouped.contb_receipt_amt.sum().unstack(0)
normed_sums = bucket_sums.div(bucket_sums.sum(axis=1), axis=0)
# normed_sums[:-2].plot(kind='barh', stacked=True)
grouped = fec_mrbo.groupby(['cand_nm', 'contbr_st'])
totals = grouped.contb_receipt_amt.sum().unstack(0).fillna(0)
totals = totals[totals.sum(1) > 100000]
percent = totals.div(totals.sum(1), axis=0)
obama = percent['Obama, Barack']
fig = plt.figure(figsize=(12, 12))
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
lllat = 21; urlat = 53; lllon = -118; urlon = -62
m = Basemap(ax=ax, projection='stere', lon_0=(urlon + lllon) / 2, lat_0=(urlat + lllat) / 2,
            llcrnrlon=lllon, llcrnrlat=lllat, urcrnrlon=urlon, urcrnrlat=urlat, resolution='l')
m.drawcoastlines()
m.drawcounties()
shapefile.Writer().save('ch09/statesp020')
dbf = shapefile.Reader('ch09/statesp020.dbf')
shp = shapefile.Reader('ch09/statesp020.shp')
state_to_code = pd.read_table('ch09/state_to_code.txt',
                              index_col=0,
                              delimiter=', ',
                              engine='python',
                              header=None).loc[:,:]
state_to_code = state_to_code.to_dict()[1]
for npoly in range(shp.info()[0]):
    shpsegs = []
    shp_object = shp.read_object(npoly)
    verts = shp_object.vertices()
    rings = len(verts)
    for ring in range(rings):
        lons, lats = zip(*verts[ring])
        x, y = m(lons, lats)
        shpsegs.append(zip(x, y))
        if ring == 0:
            shapedict = dbf.read_record(npoly)
        name = shapedict['STATE']
    lines = LineCollection(shpsegs, antialiaseds=(1,))
    try:
        per = obama[state_to_code[name.upper()]]
    except KeyError:
        continue
    lines.set_facecolors('k')
    lines.set_alpha(0.75 * per)
    lines.set_edgecolors('k')
    lines.set_linewidth(0.3)

plt.show()