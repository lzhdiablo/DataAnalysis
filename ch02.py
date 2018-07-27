import json
import os
from collections import defaultdict, Counter

from matplotlib import pylab as plt
import numpy as np
import pandas as pd
from pandas import DataFrame, Series

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ch02\\usagov_bitly_data2012-03-16-1331923249.txt')
records = [json.loads(line) for line in open(path)]

time_zones = [record['tz'] for record in records if 'tz' in record]
def get_counts(sequence):
    counts = defaultdict(int)
    for x in sequence:
        counts[x] += 1
    return counts
counts = get_counts(time_zones)

def top_counts(count_dict, n=10):
    value_key_pairs = [(count, tz) for tz, count in count_dict.items()]
    value_key_pairs.sort()
    return value_key_pairs[-n:]
top_counts(counts)

counts = Counter(time_zones)
counts.most_common(10)

frame = DataFrame(records)
clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'Unknown'
tz_counts = clean_tz.value_counts()
# tz_counts[:10].plot(kind='barh', rot=0) #柱状图
# plt.show()

results = Series([x.split()[0] for x in frame.a.dropna()]) #frame.tz、frame.a...可取出frame中的某列数据
# print(results.value_counts()[:8])

cframe = frame[frame.a.notnull()]
operating_system = np.where(frame.a.dropna().str.contains('Windows'), 'Windows', 'Not Windows')
# operating_system = np.where(cframe.a.str.contains('Windows'), 'Windows', 'Not Windows') #和上一条效果一样
# print(operating_system)

by_tz_os = cframe.groupby(['tz', operating_system])
agg_counts = by_tz_os.size().unstack().fillna(0)
indexer = agg_counts.sum(1).argsort()
count_subset = agg_counts.take(indexer)[-10:]
# count_subset.plot(kind='bar', stacked=True)
# plt.show()
normed_subset = count_subset.div(count_subset.sum(1), axis=0)
# normed_subset.plot(kind='barh', stacked=True)
# plt.show()

################################################################################################################################################
dir_path = os.path.dirname(os.path.abspath(__file__))
user_path = os.path.join(dir_path, 'ch02\\movielens\\users.dat')
rate_path = os.path.join(dir_path, 'ch02\\movielens\\ratings.dat')
movie_path = os.path.join(dir_path, 'ch02\\movielens\\movies.dat')
unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table(user_path, engine='python', sep='::', header=None, names=unames)
rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table(rate_path, engine='python', sep='::', header=None, names=unames)
mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table(movie_path, engine='python', sep='::', header=None, names=mnames)