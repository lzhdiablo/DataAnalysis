from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse
import pytz
from pandas.tseries.offsets import MonthEnd
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

now = datetime.now()
# print(now)
delta = datetime(2008, 6, 25, 23, 0) - datetime(2008, 6, 24, 8, 15)
# print(delta.days, delta.seconds) #时间差由天数和秒数组成
# print(timedelta(12))
# print(timedelta(12) + datetime(2009, 6, 11)) #天数运算
# print(datetime(2009, 6, 11) - 2 * timedelta(12))

stamp = datetime(2011, 1, 3)
# print(stamp) #默认输出
# print(stamp.strftime('%Y-%m-%d')) #转换格式
value = '2011-01-03'
# print(datetime.strptime(value, '%Y-%m-%d')) #将字符串转换为日期格式
# print(parse(value)) #parse可以解析所有的日期表现形式

datestrs = ['7/6/2011', '5/12/2018']
# print(pd.to_datetime(datestrs)) #pandas通常用于处理成组日期， 解析速度快
dates = [datetime(2011, 1, 2), datetime(2012, 1, 5), datetime(2013, 4, 23),
         datetime(2008, 2, 21), datetime(2002, 5, 2), datetime(2000, 7, 11)]
ts = pd.Series(np.random.randn(6), index=dates) #ts是一个TimeSeries对象
# print(ts)
# print(ts[::2])
# print(ts + ts[::2]) #跟其他Series不一样,算数运算时索引会根据自动对其到相同的日期再进行运算，如果运算的一方在该索引下没有找到值，则运算的结果为NaN
# print(ts['2008/2/21']) #可以直接传入一个可以解析为日期的字符串获取Series的值

longer_ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
# print(longer_ts['2001']) #可以直接传入年或年月对数据进行切片
# print(longer_ts['2001-5'])
# print(longer_ts[parse('1/1/2002'):]) #也可以传入一个datetime对象对Series切片，但仅限于Series
# print(longer_ts.truncate(after='1/3/2002'))

dates = ['1/1/2001', '1/2/2001', '1/2/2001', '1/2/2001', '1/3/2001']
dup_ts = pd.Series(np.arange(5), index=dates)
# print(dup_ts['1/2/2001']) #会输出多个值
# print(dup_ts.groupby(level=0).mean())

# print(pd.date_range('1/1/2000', '12/1/2000', freq='BM')) #生成一个由每月的最后一个工作日组成的日期索引
# print(pd.date_range('5/2/2012 12:56:31', periods=5)) #date_range会默认保留起始或结束时间戳的时间信息
# print(pd.date_range('1/1/2000', '1/3/2000 23:59', freq='4H')) #4H表示频率为四个小时，同样M为月，也可组合使用如2h20min
# print(pd.date_range('1/1/2012', '9/1/2012', freq='WOM-3FRI')) #表示每个月的第三个星期五

ts = pd.Series(np.random.randn(4), index=pd.date_range('1/1/2000', periods=4, freq="M"))
# print(ts)
# print(ts.shift(2)) #shift表示数据沿着时间索引向前或向后移动
# print(ts.shift(2, freq='M')) #如果频率已知， 则可以传入shift则可实现对时间索引位移

ts = pd.Series(np.random.randn(20), index=pd.date_range('1/15/2000', periods=20, freq='4d'))
offset = MonthEnd()
# print(ts.groupby(offset.rollforward).mean())
# print(ts.resample('M').mean()) #二者效果等价

# print(pytz.common_timezones) #所有时区的名称
ts = pd.Series(np.random.randn(4), index=pd.date_range('1/23/2001', periods=4, freq='90T'))
ts_utc = ts.tz_localize('UTC')
# print(ts_utc.tz_convert('US/Eastern')) #时区切换
ts_eastern = ts.tz_localize('US/Eastern')
# print(ts_eastern.tz_convert('UTC')) #可以先本地化到任何一个时区，然后再进行时区转换

stamp = pd.Timestamp('2011-02-13 04:00')
stamp_utc = stamp.tz_localize('utc')
stamp_eastern = stamp_utc.tz_convert('US/Eastern')
stamp_moscow = pd.Timestamp('2011-02-13 04:00', tz='Europe/Moscow')
# print(stamp_utc.value)
# print(stamp_eastern.value) #UTC时间戳不随时区的变化而变化

p = pd.Period(2007, freq='A-DEC') #表示一个时间段
# print(p - 2) #时间段根据频率位移
# print(pd.Period(2014, freq='A-DEC') - p) #相同频率的时间段之间的运算
rng = pd.period_range('1/1/2000', '6/30/2000', freq='M')
series = pd.Series(np.random.randn(6), index=rng) #保存了一组Period对象，可用做轴索引
# print(p.asfreq('M', how='start'))
# print(p.asfreq('M', how='end')) #转换时间段频率
p_JUN = pd.Period(2007, freq='A-JUN')
# print(p_JUN)
rng = pd.period_range('2006', '2009', freq='A-DEC')
ts = pd.Series(np.random.randn(len(rng)), index=rng)
# print(ts.asfreq('M', how='start'))

rng = pd.date_range('1/1/2000', periods=3, freq='M')
ts = pd.Series(np.random.randn(3), index=rng)
pts = ts.to_period()
# print(ts)
# print(pts)
rng = pd.date_range('1/29/2000', periods=6, freq='D')
ts2 = pd.Series(np.random.randn(6), index=rng)
pts2 = ts2.to_period('M')
# print(ts2)
# print(pts2)
t_s = pts.to_timestamp(how='end')
# print(t_s)

data = pd.read_csv('ch08/macrodata.csv')
index = pd.PeriodIndex(year=data.year, quarter=data.quarter, freq='Q-DEC') #通过数组创建PeriodIndex
data.index = index

rng = pd.date_range('1/1/2000', periods=100, freq='D')
ts = pd.Series(np.random.randn(len(rng)), index=rng)
ts_resample = ts.resample('M').mean()
ts_resample_period = ts_resample.to_period('M')
ts_period = ts.to_period('M')
# print(ts)
# print(ts_resample)
# print(ts_resample_period)
# print(ts_period)

rng = pd.date_range('1/1/2000', periods=12, freq='T')
ts = pd.Series(range(12), index=rng)
# print(ts)
# print(ts.resample('5min').sum())
# print(ts.resample('5min', closed='left', label='left').sum())
# print(ts.resample('5min', closed='left', label='right').sum())
# print(ts.resample('5min', closed='right').sum())
# print(ts.resample('5min', closed='right', label='right').sum())
# print(ts.resample('5min', closed='right', label='left').sum())
# print(ts.resample('5min', label='right').sum())
# print(ts.resample('5min').ohlc())

frame = pd.DataFrame(np.random.rand(2, 4), index=pd.date_range('1/1/2000', periods=2, freq='W-WED'),
                     columns=['Colorado', 'Texas', 'New York', 'Ohio'])
# print(frame.resample('D').ffill(limit=2))
# print(frame.resample('W-THU').ffill(limit=2))

close_px_all = pd.read_csv('ch09/stock_px.csv', parse_dates=True, index_col=0)
close_px = close_px_all[['AAPL', 'MSFT', 'XOM']]
close_px = close_px.resample('B').ffill()
# print(close_px_all)
# print(close_px)
# close_px.plot()
# close_px.loc['2009'].plot()
# close_px['AAPL'].loc['01-2011':'03-2011'].plot()
appl_q = close_px['AAPL'].resample('Q-DEC').ffill()
# appl_q.loc['2009':].plot()
# close_px.AAPL.plot()
# close_px.AAPL.rolling(window=250).mean().plot()

plt.show()
