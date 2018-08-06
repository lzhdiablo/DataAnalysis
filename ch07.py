import numpy as np
import pandas as pd
from pandas.io.parsers import TextParser
import csv
import json
from lxml.html import parse
from lxml import etree
import urllib
from matplotlib import pylab as plt

'''
1. merge默认inner连接，多对多连接产生的是行的笛卡尔积，也就是相同的key,结果行数为合并数据集行数的积
2. concat是轴向连接，没有数据的为空

'''
df1 = pd.DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'a', 'b'], 'data1': np.arange(7)})
df2 = pd.DataFrame({'key': ['a', 'b', 'd', 'a'], 'data2': np.arange(4)})
# print(df1.merge(df2))
# print(df2.merge(df1))
# print(pd.merge(df1, df2))
# print(pd.merge(df1, df2, on='key')) #只能指定重叠的列进行合并
# print(pd.merge(df1, df2, left_on='data1', right_on='data2'))
# print(pd.merge(df1, df2, how='outer'))

df1 = pd.DataFrame(np.arange(6).reshape(3, 2), index=['a', 'b', 'c'], columns=['one', 'two'])
df2 = pd.DataFrame(np.arange(4).reshape(2, 2), index=['a', 'c'], columns=['three', 'four'])
# print(pd.concat([df1, df2], ignore_index=True, sort=False))

data = pd.DataFrame(np.arange(6).reshape(2, 3),
                    index=pd.Index(['Ohio', 'Colorado'], name='state'),
                    columns=pd.Index(['one', 'two', 'three'], name='number'))
# print(data)
# print("...............")
# print(data.stack())
# print("...............")
# print(data.unstack())

data = pd.DataFrame({'food': ['bacon', 'pulled pork', 'bacon', 'Pastrami', 'corned beef', 'Bacon', 'pastrami', 'honey ham', 'nova lox'],
                     'ounces': [4, 3, 12, 6, 7.5, 8, 3, 5, 6]})
met_to_animal={'bacon': 'pig',
               'pulled pork': 'pig',
               'pastrami': 'cow',
               'corned beef': 'cow',
               'honey ham': 'pig',
               'nova lox': 'salmon'}
data['animal'] = data['food'].map(str.lower).map(met_to_animal)

data = pd.Series([1, -999, 2, -999, -1000, 3])
# print(data.replace(-999, np.nan))
# print(data.replace([-999, -1000], np.nan))
# print(data.replace([-999, -1000], [np.nan, 0]))
# print(data.replace({-999: np.nan, -1000: 0}))

data = pd.DataFrame(np.arange(12).reshape(3, 4), index=['Ohio', 'Colorado', 'New York'], columns=['one', 'two', 'three', 'four'])
data.index = data.index.map(str.upper)
# print(data.rename(index=str.title, columns=str.upper)) #不修改源数据
# print(data)
# print(data.rename(index={'OHIO': 'INDIANA'}, columns={'three': 'peekaboo'}))

ages = [20, 22, 25, 27, 21, 23, 37, 31, 61, 45, 41, 32]
bins = [18, 25, 35, 60, 100]
cats = pd.cut(ages, bins, right=False) #right设置闭端和开端
group_name = ['Youth', 'YoungAdult', 'MiddleAged', 'Senior']
cats = pd.cut(ages, bins, labels=group_name)
data = np.random.rand(20)
# print(pd.cut(data, 4, precision=2)) #只传面元数量时，自动根据数据的最大和最小值计算等长面元
data = np.random.rand(1000)
cats = pd.qcut(data, 4)
# print(cats.value_counts()) #qcut按样本分位数进行切割，能切分出大小基本相等的面元
cats = pd.qcut(data, [0, 0.1, 0.5, 0.9, 1]) #也可设置自定义的分位数（0到1之间的数值，包含端点）
# print(cats.value_counts())

data = pd.DataFrame(np.random.randn(1000, 4))
col = data[3]
# print(col[abs(col) > 3])
# print(data[(abs(data) > 3).any(1)]) #选出绝对值大于3的行
data[abs(data) > 3] = np.sign(data) * 3 #将所有绝对值大于3的值用3，-3替换

df = pd.DataFrame(np.arange(20).reshape(5, 4))
sampler = np.random.permutation(5)
# print(df.take(sampler))
# print(df.take(np.random.permutation(len(df)[:3]))) #随机取子集

df = pd.DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'b'], 'data1': range(6)})
# print(pd.get_dummies(df))
# print(pd.get_dummies(df['key']))

##############################################################################################################################
db = json.load(open('ch07/foods-2011-10-03.json'))
nutrients = pd.DataFrame(db[0]['nutrients'])
info_keys = ['description', 'group', 'id', 'manufacturer']
info = pd.DataFrame(db, columns=info_keys)
nutrients = []
for rec in db:
    fnuts = pd.DataFrame(rec['nutrients'])
    fnuts['id'] = rec['id']
    nutrients.append(fnuts)
nutrients = pd.concat(nutrients, ignore_index=True)
nutrients = nutrients.drop_duplicates()
col_mapping = {'description': 'food', 'group': 'fgroup'}
info = info.rename(columns=col_mapping, copy=False)
col_mapping = {'description': 'nutrient', 'group': 'nutgroup'}
nutrients = nutrients.rename(columns=col_mapping, copy=False)
ndata = pd.merge(info, nutrients, on='id', how='outer')
result = ndata.groupby(['nutrient', 'fgroup'])['value'].quantile(0.5)
# result['Zinc, Zn'].sort_values().plot(kind='barh')
# plt.show()
by_nutrient = ndata.groupby(['nutgroup', 'nutrient'])
get_maximum = lambda x: x.xs(x.value.idxmax())
max_foods = by_nutrient.apply(get_maximum)[['value', 'food']]