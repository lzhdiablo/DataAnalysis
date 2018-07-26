import json
import os
from collections import defaultdict, Counter

from matplotlib import pylab as plt
from pandas import DataFrame

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
tz_counts[:10].plot(kind='barh', rot=0)
plt.show()