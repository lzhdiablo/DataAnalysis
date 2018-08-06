import numpy as np
import pandas as pd
from pandas.io.parsers import TextParser
import csv
import json
from lxml.html import parse
from lxml import etree
import urllib

pd.set_option('precision', 15) #设置控制打印精度
df1 = pd.read_csv('ch06/ex1.csv')
df2 = pd.read_csv('ch06/ex2.csv', header=None)
df3 = pd.read_csv('ch06/csv_mindex.csv', index_col=['key1', 'key2'])
df4 = pd.read_table('ch06/ex3.txt', sep='\s+')
df5 = pd.read_csv('ch06/ex4.csv', skiprows=[0, 2, 3])
sentinels = {'message': ['foo', 'NA'], 'something': ['two']}
df6 = pd.read_csv('ch06/ex5.csv', na_values=sentinels)
df7 = pd.read_csv('ch06/ex6.csv', nrows=5)

chunk = pd.read_csv('ch06/ex6.csv', chunksize=1000)
tot = pd.Series([])
for piece in chunk:
    tot = tot.add(piece['key'].value_counts(), fill_value=0)
# print(tot.sort_values(ascending=False))

df8 = pd.read_csv('ch06/ex5.csv')
df8.to_csv('ch06/out.csv', sep=':', na_rep='NULL', index=False, header=False, columns=['a', 'b', 'c'])

dates = pd.date_range('1/1/2018', periods=7)
ts = pd.Series(np.arange(7), index=dates)
ts.to_csv('ch06/tseries.csv', sep=':')
# print(pd.read_csv('ch06/tseries.csv', sep=':', header=None, index_col=1))

with open('ch06/ex7.csv') as f:
    lines = list(csv.reader(f))
    header, values = lines[0], lines[1:]
    data_dict = {h: v for h, v in zip(header, zip(*values))}
    # print(data_dict)

with open('ch06/ex7.csv') as f:
    lines = list(csv.reader(f))
    header, values = lines[0], lines[1:]
    data_dict = {h: v for h, v in zip(header, zip(*values))}

obj = """
    {"name": "Wes",
    "places_lived": ["United States", "Spain", "Germany"],
    "pet": null,
    "siblings": [{"name": "Scott", "age": 25, "pet": "Zuko"}, {"name": "Katie", "age": 33, "pet": "Cisco"}]
    }
"""
result = json.loads(obj)
siblings = pd.DataFrame(result['siblings'], columns=['name', 'age'])
# siblings.to_json("ch06/json.txt")

# parsed = parse(urllib.request.urlopen('http://finance.yahoo.com/quote/AAPL/options?ltr=1&guccounter=1'))
# doc = parsed.getroot()
# links = doc.findall('.//a')
# urls = [link.get('href') for link in links if str(link.get('href')).startswith('http') | str(link.get('href')).startswith('https')]
# tables = doc.findall('.//table')
# calls = tables[0]
# puts = tables[1]
# rows = calls.findall(".//tr")
# def _unpack(row, kind='td'):
#     elts = row.findall('.//%s' % kind)
#     return [val.text_content() for val in elts]
# def parse_options_data(table):
#     rows = table.findall('.//tr')
#     header = _unpack(rows[0], kind='th')
#     data = [_unpack(r) for r in rows[1:]]
#     return TextParser(data, names=header).get_chunk()
# call_data = parse_options_data(calls)
# put_data = parse_options_data(puts)
# call_data.to_csv('ch06/call_data.csv')
# put_data.to_csv('ch06/put_data.csv')

path = 'ch06/mta_perf/Performance_MNR.xml'
root = etree.parse(path).getroot()
data = []
skip_fileds = ['INDICATOR_SEQ', 'PARENT_SEQ', 'DESIRED_CHANGE', 'DECIMAL_PLACES']
for elt in root:
    el_data = {}
    for child in elt:
        if child.tag in skip_fileds:
            continue
        el_data[child.tag] = child.text
    data.append(el_data)
pref = pd.DataFrame(data)
tag = '<a href="http://www.google.com">Google</a>'
root = etree.fromstring(tag)
# print(root.tag, root.text, root.get('href'))

excel_data = pd.read_excel('ch06/ex1.xlsx', sheet_name='Sheet1')