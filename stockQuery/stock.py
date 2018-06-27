import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
from googlefinance.client import get_price_data, get_prices_data, get_prices_time_data
from yahoofinancials import YahooFinancials
from collections import defaultdict
import time, datetime
import quandl

# define plot size and layout
# fig, ax = plt.subplots(nrows=3, ncols=5, figsize=(16,9))
fig1, ax1 = plt.subplots(nrows=5, ncols=1, figsize=(16,9))
fig2, ax2 = plt.subplots(nrows=5, ncols=1, figsize=(16,9))
fig3, ax3 = plt.subplots(nrows=5, ncols=1, figsize=(16,9))

stock_dict = defaultdict(list)
stocks = ['QCOM', 'CSCO', 'INTC', 'AAPL', 'GOOG']
# stocks = ['AAPL']
time_list = []
time_list1 = []

quandl.ApiConfig.api_key = 'k9Xs_yso27irbXnFsGxz'

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

# def update_fig1(i):
#     ######################
#     # google finance
#     ######################
#     param1 = {
#         'q': "QCOM", # Stock symbol (ex: "AAPL")
#         'i': "60", # Interval size in seconds ("86400" = 1 day intervals)
#         'x': "NASD", # Stock exchange symbol on which stock is traded (ex: "NASD")
#         'p': "1H" # Period (Ex: "1Y" = 1 year)
#     }
#     df1 = get_price_data(param1)
#     close1 = df1['Close']
#
#     param2 = {
#         'q': "CSCO", # Stock symbol (ex: "AAPL")
#         'i': "10", # Interval size in seconds ("86400" = 1 day intervals)
#         'x': "NASD", # Stock exchange symbol on which stock is traded (ex: "NASD")
#         'p': "1D" # Period (Ex: "1Y" = 1 year)
#     }
#     df2 = get_price_data(param2)
#     close2 = df2['Close']
#
#     param3 = {
#         'q': "INTC", # Stock symbol (ex: "AAPL")
#         'i': "10", # Interval size in seconds ("86400" = 1 day intervals)
#         'x': "NASD", # Stock exchange symbol on which stock is traded (ex: "NASD")
#         'p': "1D" # Period (Ex: "1Y" = 1 year)
#     }
#     df3 = get_price_data(param3)
#     close3 = df3['Close']
#
#     param4 = {
#         'q': "AAPL", # Stock symbol (ex: "AAPL")
#         'i': "10", # Interval size in seconds ("86400" = 1 day intervals)
#         'x': "NASD", # Stock exchange symbol on which stock is traded (ex: "NASD")
#         'p': "1D" # Period (Ex: "1Y" = 1 year)
#     }
#     df4 = get_price_data(param4)
#     close4 = df4['Close']
#
#     param5 = {
#         'q': "GOOG", # Stock symbol (ex: "AAPL")
#         'i': "10", # Interval size in seconds ("86400" = 1 day intervals)
#         'x': "NASD", # Stock exchange symbol on which stock is traded (ex: "NASD")
#         'p': "1D" # Period (Ex: "1Y" = 1 year)
#     }
#     df5 = get_price_data(param5)
#     close5 = df5['Close']
#     # plot 3*5 graph
#     ax[0][0].clear()
#     ax[0][0].plot(close1.index, close1, label='QCOM')
#     ax[0][0].set_xlabel('Date')
#     ax[0][0].set_ylabel('Closing price ($)')
#     ax[0][0].legend()
#
#     ax[0][1].clear()
#     ax[0][1].plot(close2.index, close2, label='CSCO')
#     ax[0][1].set_xlabel('Date')
#     ax[0][1].set_ylabel('Closing price ($)')
#     ax[0][1].legend()
#
#     ax[0][2].clear()
#     ax[0][2].plot(close3.index, close3, label='INTC')
#     ax[0][2].set_xlabel('Date')
#     ax[0][2].set_ylabel('Closing price ($)')
#     ax[0][2].legend()
#
#     ax[0][3].clear()
#     ax[0][3].plot(close4.index, close4, label='AAPL')
#     ax[0][3].set_xlabel('Date')
#     ax[0][3].set_ylabel('Closing price ($)')
#     ax[0][3].legend()
#
#     ax[0][4].clear()
#     ax[0][4].plot(close5.index, close5, label='GOOG')
#     ax[0][4].set_xlabel('Date')
#     ax[0][4].set_ylabel('Closing price ($)')
#     ax[0][4].legend()
#
#     now = datetime.datetime.now()
#     time_list.append(now)
#     j = 0
#     k = 0
#     data = quandl.get_table('WIKI/PRICES', ticker = stocks,
#         qopts = { 'columns': ['ticker', 'date', 'adj_close'] },
#         date = { 'gte': '2017-10-31', 'lte': '2018-1-31' },
#         paginate=True)
#
#     for stock in stocks:
#         ticker = stock
#         print("processing stock "+stock)
#         yahoo_financials = YahooFinancials(ticker)
#         stock_dict[stock].append(yahoo_financials.get_current_price())
#         ax[1][j].clear()
#         ax[1][j].plot(time_list, stock_dict[stock], label=stock)
#         ax[1][j].set_xlabel('Date Time')
#         ax[1][j].set_ylabel('Closing price ($)')
#
#         stock_data = data[data['ticker'] == stock]
#         stock_data.set_index('date', inplace=True)
#         quandl_close = stock_data['adj_close']
#
#         ax[2][k].clear()
#         ax[2][k].plot(quandl_close.index, quandl_close, label=stock)
#         ax[2][k].set_xlabel('Date')
#         ax[2][k].set_ylabel('Closing price ($)')
#         # ax[2][k].legend()
#
#         j += 1
#         k += 1
#
# ani = animation.FuncAnimation(fig, update_fig1, interval=10000)

def update_google(i):
    ######################
    # google finance
    ######################
    param1 = {
        'q': "QCOM", # Stock symbol (ex: "AAPL")
        'i': "60", # Interval size in seconds ("86400" = 1 day intervals)
        'x': "NASD", # Stock exchange symbol on which stock is traded (ex: "NASD")
        'p': "1H" # Period (Ex: "1Y" = 1 year)
    }
    df1 = get_price_data(param1)
    close1 = df1['Close']

    param2 = {
        'q': "CSCO", # Stock symbol (ex: "AAPL")
        'i': "10", # Interval size in seconds ("86400" = 1 day intervals)
        'x': "NASD", # Stock exchange symbol on which stock is traded (ex: "NASD")
        'p': "1D" # Period (Ex: "1Y" = 1 year)
    }
    df2 = get_price_data(param2)
    close2 = df2['Close']

    param3 = {
        'q': "INTC", # Stock symbol (ex: "AAPL")
        'i': "10", # Interval size in seconds ("86400" = 1 day intervals)
        'x': "NASD", # Stock exchange symbol on which stock is traded (ex: "NASD")
        'p': "1D" # Period (Ex: "1Y" = 1 year)
    }
    df3 = get_price_data(param3)
    close3 = df3['Close']

    param4 = {
        'q': "AAPL", # Stock symbol (ex: "AAPL")
        'i': "10", # Interval size in seconds ("86400" = 1 day intervals)
        'x': "NASD", # Stock exchange symbol on which stock is traded (ex: "NASD")
        'p': "1D" # Period (Ex: "1Y" = 1 year)
    }
    df4 = get_price_data(param4)
    close4 = df4['Close']

    param5 = {
        'q': "GOOG", # Stock symbol (ex: "AAPL")
        'i': "10", # Interval size in seconds ("86400" = 1 day intervals)
        'x': "NASD", # Stock exchange symbol on which stock is traded (ex: "NASD")
        'p': "1D" # Period (Ex: "1Y" = 1 year)
    }
    df5 = get_price_data(param5)
    close5 = df5['Close']
    # plot 5*1 graph
    ax1[0].clear()
    ax1[0].plot(close1.index, close1, label='QCOM')
    ax1[0].set_xlabel('Date')
    ax1[0].set_ylabel('Closing price ($)')
    ax1[0].legend()

    ax1[1].clear()
    ax1[1].plot(close2.index, close2, label='CSCO')
    ax1[1].set_xlabel('Date')
    ax1[1].set_ylabel('Closing price ($)')
    ax1[1].legend()

    ax1[2].clear()
    ax1[2].plot(close3.index, close3, label='INTC')
    ax1[2].set_xlabel('Date')
    ax1[2].set_ylabel('Closing price ($)')
    ax1[2].legend()

    ax1[3].clear()
    ax1[3].plot(close4.index, close4, label='AAPL')
    ax1[3].set_xlabel('Date')
    ax1[3].set_ylabel('Closing price ($)')
    ax1[3].legend()

    ax1[4].clear()
    ax1[4].plot(close5.index, close5, label='GOOG')
    ax1[4].set_xlabel('Date')
    ax1[4].set_ylabel('Closing price ($)')
    ax1[4].legend()

ani1 = animation.FuncAnimation(fig1, update_google, interval=10000)

# ######################
# # yahoo finance
# ######################
def update_yahoo(i):
    now = datetime.datetime.now()
    time_list1.append(now)
    j = 0
    for stock in stocks:
        ticker = stock
        print("processing stock "+stock)
        yahoo_financials = YahooFinancials(ticker)
        stock_dict[stock].append(yahoo_financials.get_current_price())
        ax2[j].clear()
        ax2[j].plot(time_list, stock_dict[stock], label=stock)
        ax2[j].set_xlabel('Date Time')
        ax2[j].set_ylabel('Closing price ($)')

        j += 1

ani2 = animation.FuncAnimation(fig2, update_yahoo, interval=10000)

######################
# quandl
######################
def update_quandl(i):
    data = quandl.get_table('WIKI/PRICES', ticker = stocks,
            qopts = { 'columns': ['ticker', 'date', 'adj_close'] },
            date = { 'gte': '2017-10-31', 'lte': '2018-1-31' },
            paginate=True)
    #
    # fig2, ax2 = plt.subplots(nrows=5, ncols=1, figsize=(16,9))
    i = 0
    for stock in stocks:
        stock_data = data[data['ticker'] == stock]
        stock_data.set_index('date', inplace=True)
        quandl_close = stock_data['adj_close']

        ax3[i].clear()
        ax3[i].plot(quandl_close.index, quandl_close, label=stock)
        ax3[i].set_xlabel('Date')
        ax3[i].set_ylabel('Closing price ($)')
        ax3[i].legend()
        i += 1
ani3 = animation.FuncAnimation(fig3, update_quandl, interval=10000)

plt.show()
