# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 17:07:03 2021

@author: margaret
"""

import pandas as pd

df = pd.read_csv('./data/nyc_temperatures.csv')

df.head()

df.columns

df.rename(
    columns = {'value':'temp_C',
               'attributes' : 'flags'},
    inplace = True)

df.columns

df.dtypes

df.loc[:, 'date'] = pd.to_datetime(df.date)
df.dtypes

df.date.describe(datetime_is_numeric=True) # not working

eastern = pd.read_csv('./data/nyc_temperatures.csv', index_col = 'date', parse_dates = True).tz_localize('EST')

eastern.head()

eastern.tz_convert('UTC').head()

eastern.tz_convert('EST').head()

df.head()

eastern.tz_localize(None).to_period('M').index

eastern.tz_localize(None).to_period('M').to_timestamp().index

df = pd.read_csv('./data/nyc_temperatures.csv').rename(
    columns = {'value':'temp_C', 'attributes' : 'flags'})

new_df = df.assign(
    date = pd.to_datetime(df.date),
    temp_F = (df.temp_C * 9/5) + 32)

new_df.dtypes

new_df.head()

df = df.assign(
    date = lambda x:pd.to_datetime(x.date),
    temp_C_whole = lambda x: x.temp_C.astype('int'),
    temp_F=lambda x:(x.temp_C *9/5) + 32,
    temp_F_whole = lambda x: x.temp_F.astype('int'))

df.head()

df_with_categories = df.assign(
    station = df.station.astype('category'),
    datatype = df.datatype.astype('category'))

df_with_categories.dtypes


df_with_categories.describe(include = 'category')

pd.Categorical([
    'med', 'med', 'low', 'high'],
    categories = ['low', 'med', 'high'],
    ordered = True)

df[df.datatype == 'TMAX']\
    .sort_values(by = 'temp_C', ascending = False).head(10)
    
df[df.datatype == 'TMAX'].sort_values(
    by = ['temp_C', 'date'], ascending = [False, True]).head(10)

df[df.datatype == 'TAVG'].nlargest(n = 10, columns = 'temp_C')

df.sample(5, random_state = 0).index

df.sample(5, random_state = 0).sort_index().index

df.sort_index(axis = 1).head()

df.loc[:, 'station':'temp_F_whole']

df.equals(df.sort_values(by = 'temp_C'))
df.equals(df.sort_values(by = 'temp_C').sort_index())

df.set_index('date', inplace = True)
df.head()

df['2018-10-11' : '2018-10-12']

df['2018-10-11' : '2018-10-12'].reset_index()

sp = pd.read_csv(
    './data/sp500.csv', index_col = 'date', parse_dates = True).drop(columns = ['adj_close'])

sp.head(10).assign(day_of_week = lambda x:x.index.day_name())

bitcoin = pd.read_csv(
    './data/bitcoin.csv', index_col = 'date', parse_dates = True).drop(columns = ['market_cap'])

portfolio = pd.concat([sp, bitcoin], sort = False).groupby(level = 'date').sum()

portfolio.head(10).assign(day_of_week = lambda x:x.index.day_name())

import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

ax = portfolio['2017-Q4' : '2018-Q2'].plot(
    y = 'close', figsize=(15,5), legend = False, title = 'Bitcoin + S&P 500 value without accounting'
    'for different indices')

ax.set_ylabel('price')
ax.yaxis\
    .set_major_formatter(StrMethodFormatter('${x:,.0f}'))

for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
    
plt.show()


sp.reindex(bitcoin.index, method = 'ffill').head(10)\
    .assign(day_of_week = lambda x:x.index.day_name())

np.where(boolean condition, value if True, value if False)

import numpy as np

sp_reindexed = sp.reindex(bitcoin.index).assign(
    # volume is 0 when the market is closed
    volume = lambda x:x.volume.fillna(0),
    
    close = lambda x:x.close.fillna(method = 'ffill'),
    open = lambda x:\
        np.where(x.open.isnull(), x.close, x.open),
    high = lambda x:\
        np.where(x.high.isnull(), x.close, x.high),
    low = lambda x:\
        np.where(x.low.isnull(), x.close, x.low))
    
sp_reindexed.head(10).assign(
    day_of_week = lambda x:x.index.day_name())

squares = []
for i in range(1, 101):
    squares.append(i**2)

print(squares)

squares2 = [i**2 for i in range(1,101)]
squares2

# gmovies = [title for title in movies if title.startswith("G")]

moviesbefore2000 = [title for title in movies[0] if movies[1] < 2000]
moviesbefore2000 = [title for (title, year) in movies if year < 2000]

# scalar multiplication
v = [2, -3, 1]
4*v # 4 * v = v+v+v+

fixed_portfolio = sp_reindexed + bitcoin

ax = fixed_portfolio['2017-Q4' : '2018-Q2'].plot(
    y = 'close', figsize = (15,5), linewidth = 2,
    label = 'reindexed portfolio of SP 500 + bitcoin',
    title = 'reindexed portfolio vs.')

portfolio['2017-Q4' : '2018-Q2'].plot(
    y = 'close', ax = ax, linestyle = 'dashed',
    label = 'portolio of SP 500')