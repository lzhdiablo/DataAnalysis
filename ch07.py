import numpy as np
import pandas as pd
from pandas.io.parsers import TextParser
import csv
import json
from lxml.html import parse
from lxml import etree
import urllib

df1 = pd.DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'a', 'b'], 'data1': np.arange(7)})
df2 = pd.DataFrame({'key': ['a', 'b', 'd'], 'data2': np.arange(3)})
# print(df1.merge(df2))
# print(df2.merge(df1))
print(pd.merge(df1, df2))
# print(pd.merge(df1, df2, on='key')) #只能指定重叠的列进行合并
# print(pd.merge(df1, df2, left_on='data1', right_on='data2'))
# print(pd.merge(df1, df2, how='outer'))
