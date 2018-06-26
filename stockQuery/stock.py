import matplotlib.pyplot as plt
import pandas as pd
from googlefinance.client import get_price_data, get_prices_data, get_prices_time_data

param1 = {
    'q': "QCOM", # Stock symbol (ex: "AAPL")
    'i': "10", # Interval size in seconds ("86400" = 1 day intervals)
    'x': "NASD", # Stock exchange symbol on which stock is traded (ex: "NASD")
    'p': "1D" # Period (Ex: "1Y" = 1 year)
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

fig, ax = plt.subplots(figsize=(16,9))
ax.plot(close1.index, close1, label='QCOM')
ax.plot(close2.index, close2, label='CSCO')
ax.plot(close3.index, close3, label='INTC')
ax.set_xlabel('Date')
ax.set_ylabel('Closing price ($)')
ax.legend()
plt.show()

