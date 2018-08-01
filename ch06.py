import numpy as np
import pandas as pd

df1 = pd.read_csv('ch06/ex1.csv')
df2 = pd.read_csv('ch06/ex2.csv', header=None)
df3 = pd.read_csv('ch06/csv_mindex.csv', index_col=['key1', 'key2'])
df4 = pd.read_table('ch06/ex3.txt', sep='\s+')
df5 = pd.read_csv('ch06/ex4.csv', skiprows=[0, 2, 3])
sentinels = {'message': ['foo', 'NA'], 'something': ['two']}
df6 = pd.read_csv('ch06/ex5.csv', na_values=sentinels)

print(df6)