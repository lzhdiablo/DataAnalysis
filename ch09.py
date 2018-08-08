import numpy as np
import pandas as pd

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

print(tips)
mean1 = tips.groupby(['sex', 'smoker']).mean()
mean1 = tips.pivot_table(index=['sex', 'smoker']) # pivot_table默认聚合为取平均，效果和groupby相同
mean2 = tips.pivot_table(['tip_pct', 'size'], index=['sex', 'day'], columns='smoker')
print(mean2)