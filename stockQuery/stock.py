import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
from googlefinance.client import get_price_data, get_prices_data, get_prices_time_data
from yahoofinancials import YahooFinancials
from collections import defaultdict
import time, datetime

######################
# google finance
######################
# param1 = {
#     'q': "QCOM", # Stock symbol (ex: "AAPL")
#     'i': "60", # Interval size in seconds ("86400" = 1 day intervals)
#     'x': "NASD", # Stock exchange symbol on which stock is traded (ex: "NASD")
#     'p': "1H" # Period (Ex: "1Y" = 1 year)
# }
# df1 = get_price_data(param1)
# close1 = df1['Close']
#
# param2 = {
#     'q': "CSCO", # Stock symbol (ex: "AAPL")
#     'i': "10", # Interval size in seconds ("86400" = 1 day intervals)
#     'x': "NASD", # Stock exchange symbol on which stock is traded (ex: "NASD")
#     'p': "1D" # Period (Ex: "1Y" = 1 year)
# }
# df2 = get_price_data(param2)
# close2 = df2['Close']
#
# param3 = {
#     'q': "INTC", # Stock symbol (ex: "AAPL")
#     'i': "10", # Interval size in seconds ("86400" = 1 day intervals)
#     'x': "NASD", # Stock exchange symbol on which stock is traded (ex: "NASD")
#     'p': "1D" # Period (Ex: "1Y" = 1 year)
# }
# df3 = get_price_data(param3)
# close3 = df3['Close']
#
# param4 = {
#     'q': "AAPL", # Stock symbol (ex: "AAPL")
#     'i': "10", # Interval size in seconds ("86400" = 1 day intervals)
#     'x': "NASD", # Stock exchange symbol on which stock is traded (ex: "NASD")
#     'p': "1D" # Period (Ex: "1Y" = 1 year)
# }
# df4 = get_price_data(param4)
# close4 = df4['Close']
#
# param5 = {
#     'q': "GOOG", # Stock symbol (ex: "AAPL")
#     'i': "10", # Interval size in seconds ("86400" = 1 day intervals)
#     'x': "NASD", # Stock exchange symbol on which stock is traded (ex: "NASD")
#     'p': "1D" # Period (Ex: "1Y" = 1 year)
# }
# df5 = get_price_data(param5)
# close5 = df5['Close']
#
# # define plot size and layout
# fig, ax = plt.subplots(nrows=5, ncols=1, figsize=(16,9))
# ax[0].plot(close1.index, close1, label='QCOM')
# ax[0].set_xlabel('Date')
# ax[0].set_ylabel('Closing price ($)')
# ax[0].legend()
#
# ax[1].plot(close2.index, close2, label='CSCO')
# ax[1].set_xlabel('Date')
# ax[1].set_ylabel('Closing price ($)')
# ax[1].legend()
#
# ax[2].plot(close3.index, close3, label='INTC')
# ax[2].set_xlabel('Date')
# ax[2].set_ylabel('Closing price ($)')
# ax[2].legend()
#
# ax[3].plot(close4.index, close4, label='AAPL')
# ax[3].set_xlabel('Date')
# ax[3].set_ylabel('Closing price ($)')
# ax[3].legend()
#
# ax[4].plot(close5.index, close5, label='GOOG')
# ax[4].set_xlabel('Date')
# ax[4].set_ylabel('Closing price ($)')
# ax[4].legend()

######################
# yahoo finance
######################
stock_dict = defaultdict(list)
stocks = ['QCOM', 'CSCO', 'INTC', 'AAPL', 'GOOG']
# stocks = ['AAPL']
time_list = []

fig1, ax1 = plt.subplots(nrows=5, ncols=1, figsize=(16,9))

def update_stock(i):
    now = datetime.datetime.now()
    time_list.append(now)
    j = 0
    for stock in stocks:
        ticker = stock
        print("processing stock "+stock)
        yahoo_financials = YahooFinancials(ticker)
        stock_dict[stock].append(yahoo_financials.get_current_price())
        ax1[j].clear()
        ax1[j].plot(time_list, stock_dict[stock], label=stock)
        ax1[j].set_xlabel('Date Time')
        ax1[j].set_ylabel('Closing price ($)')
        j += 1

ani = animation.FuncAnimation(fig1, update_stock, interval=10000)
plt.show()
######################
# quandl
######################
# import quandl
# quandl.ApiConfig.api_key = 'k9Xs_yso27irbXnFsGxz'
# stocks = ['QCOM', 'CSCO', 'INTC', 'AAPL', 'GOOG']

# data = quandl.get_table('WIKI/PRICES', ticker = stocks,
#                         qopts = { 'columns': ['ticker', 'date', 'adj_close'] },
#                         date = { 'gte': '2017-10-31', 'lte': '2018-1-31' },
#                         paginate=True)

# fig2, ax2 = plt.subplots(nrows=5, ncols=1, figsize=(16,9))
# i = 0
# for stock in stocks:
#     stock_data = data[data['ticker'] == stock]
#     stock_data.set_index('date', inplace=True)
#     quandl_close = stock_data['adj_close']

#     ax2[i].plot(quandl_close.index, quandl_close, label=stock)
#     ax2[i].set_xlabel('Date')
#     ax2[i].set_ylabel('Closing price ($)')
#     ax2[i].legend()
#     i += 1

# plt.show()
