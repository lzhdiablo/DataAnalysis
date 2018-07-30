import json
import os
from collections import defaultdict, Counter

from matplotlib import pylab as plt
import numpy as np
import pandas as pd
from pandas import DataFrame, Series


def ch02_01():
    path = os.path.join(os.getcwd(), 'ch02\\usagov_bitly_data2012-03-16-1331923249.txt')
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

    results = Series([x.split()[0] for x in frame.a.dropna()])  # frame.tz、frame.a...可取出frame中的某列数据
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
def ch02_02():
    user_path = os.path.join(os.getcwd(), 'ch02\\movielens\\users.dat')
    rate_path = os.path.join(os.getcwd(), 'ch02\\movielens\\ratings.dat')
    movie_path = os.path.join(os.getcwd(), 'ch02\\movielens\\movies.dat')
    unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
    users = pd.read_table(user_path, engine='python', sep='::', header=None, names=unames)
    rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
    ratings = pd.read_table(rate_path, engine='python', sep='::', header=None, names=rnames)
    mnames = ['movie_id', 'title', 'genres']
    movies = pd.read_table(movie_path, engine='python', sep='::', header=None, names=mnames)

    data = pd.merge(pd.merge(ratings, users), movies)
    # excel_writer = pd.ExcelWriter('data_excel.xlsx') #输出excel
    # data.to_excel(excel_writer, 'Sheet1')
    # excel_writer.save()
    mean_rating = data.pivot_table('rating', index='title', columns='gender', aggfunc='mean')
    ratings_by_title = data.groupby('title').size()
    active_titles = ratings_by_title.index[ratings_by_title >= 250]
    mean_rating = mean_rating.loc[active_titles]
    top_female_ratings = mean_rating.sort_values(by='F', ascending=False)

    mean_rating['diff'] = mean_rating['M'] - mean_rating['F']
    sorted_by_diff = mean_rating.sort_values(by='diff')

    rating_std_by_title = data.groupby('title')['rating'].std()
    rating_std_by_title = rating_std_by_title.loc[active_titles]
    # print(rating_std_by_title.sort_values(ascending=False)[:10])

################################################################################################################################################
def ch02_03():
    names1880_path = os.path.join(os.getcwd(), 'ch02\\names\\yob1880.txt')
    names1880 = pd.read_csv(names1880_path, names=['name', 'sex', 'births'])
    # print(names1880.groupby('sex').births.sum())
    years = range(1880, 2011)
    pieces = []
    columns = ['name', 'sex', 'births']
    for year in years:
        path = os.path.join(os.getcwd(), 'ch02\\names\\yob%d.txt' % year)
        frame = pd.read_csv(path, names=columns)
        frame['year'] = year
        pieces.append(frame)
    names = pd.concat(pieces, ignore_index=True) #指定ignore_index=True是为了删除read_csv所返回的原始行号
    # total_births = names.pivot_table(index=['year'], columns=['sex'], aggfunc=sum) #aggfunc默认为求平均
    # total_births.plot(title='Total births by sex and year')
    # plt.show()

    def add_prop(group):
        group['prop'] = group.births / group.births.sum()
        return group
    names = names.groupby(['year', 'sex']).apply(add_prop)
    # print(np.allclose(names.groupby(['year', 'sex']).prop.sum(), 1))

    def get_top1000(group):
        return group.sort_values(by='births', ascending=False)[:1000]
    top1000 = names.groupby(['year', 'sex']).apply(get_top1000)
    #上述功能也可通过下面的方式实现：
    # pieces = []
    # for year, group in names.groupby(['year', 'sex']):
    #     pieces.append(group.sort_values(by='births', ascending=False)[:1000])
    # top1000 = pd.concat(pieces, ignore_index=False)

    # total_births = top1000.pivot_table('prop', index=['year'], columns=['sex'], aggfunc=sum, fill_value=0)
    # total_births.plot(title='Sum of table1000.prop by year and sex', yticks=np.linspace(0, 1.2, 13), xticks=range(1880, 2020, 10))
    # plt.show()

    boys = top1000[top1000.sex == 'M']
    girls = top1000[top1000.sex == 'F']
    # df = boys[boys.year == 2010]
    # prop_cumsum = df.prop.cumsum()
    # print(prop_cumsum.searchsorted(0.5)[0] + 1)

    def get_quantile_count(group, q=0.5):
        group = group.sort_values(by='prop', ascending=False)
        return group.prop.cumsum().searchsorted(q)[0] + 1
    # diversity = top1000.groupby(['year', 'sex']).apply(get_quantile_count)
    #FutureWarning: 'year' is both an index level and a column label.
    #Defaulting to column, but this will raise an ambiguity error in a future version
    # diversity = diversity.unstack('sex')
    # diversity.plot(title='Number of popular names in top 50%')
    # plt.show()

    get_last_letter = lambda x: x[-1]
    last_letters = names.name.map(get_last_letter)
    last_letters.name = 'last_letter'
    table = names.pivot_table('births', index=last_letters, columns=['sex', 'year'], aggfunc=sum)
    subtable = table.reindex(columns=[1910, 1960, 2010], level='year')
    letter_prop = subtable / subtable.sum()
    fig, axes = plt.subplots(2, 1, figsize=(10, 8))
    # letter_prop['M'].plot(kind='bar', rot=0, ax=axes[0], title='Male')
    # letter_prop['F'].plot(kind='bar', rot=0, ax=axes[1], title='Female', legend=False)
    # plt.show()

    letter_prop  = table / table.sum()
    dny_ts = letter_prop.loc[['d', 'n', 'y'], 'M'].T
    # dny_ts.plot()
    # plt.show()

    all_names = top1000.name.unique()
    mask = np.array(['lesl' in x.lower() for x in all_names])
    lesley_like = all_names[mask]
    filtered= top1000[top1000.name.isin(lesley_like)]
    # filtered.groupby('name').births.sum()
    # table = filtered.pivot_table('births', index='year', columns='sex', aggfunc=sum)
    # table = table.div(table.sum(1), axis=0)
    # table.plot(style={'M': 'k-', 'F': 'k--'})
    # plt.show()

ch02_03()