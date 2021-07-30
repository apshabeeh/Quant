import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# data = yf.download('TCS.NS', period = 'max')
# print(data)

df =pd.read_csv('option-chain')
print(df)







# plt.plot(data['Close'], label = 'TCS Close Price')
# plt.xlabel('Dates')
# plt.ylabel('Price')
# plt.legend()
# plt.show()

# df = pd.read_csv('https://www1.nseindia.com/content/indices/ind_nifty50list.csv')