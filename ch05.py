import numpy as np
import pandas as pd

df = pd.DataFrame(np.random.randn(7, 3))
df.ix[:4, 1] = None
df.ix[:2, 2] = None
# print(df)
# print(df.dropna(thresh=2)) #thresh=n表示滤除非NA个数小于n的行

