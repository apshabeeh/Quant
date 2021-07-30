from datetime import date
from statistics import mean
from scipy import stats
import pandas as pd
import numpy as np
import yfinance as yf

df = pd.read_csv('niftymidcap50.csv')
# df

niftyn50 = df[['Symbol']]
# niftyn50

rv_columns = [
    'Ticker',
    'Price',
    'Number of Shares to Buy',
    'Price-to-Earnings Ratio',
    'PE Percentile',
    'Price-to-Book Ratio',
    'PB Percentile',
    'Price-to-Sales Ratio',
    'PS Percentile',
    'EV/EBITDA',
    'EV/EBITDA Percentile',
    'EV/GP',
    'EV/GP Percentile',
    'RV Score'
]

rv_dataframe = pd.DataFrame(columns=rv_columns)

for i in range(0, len(df)):
    a = df.loc[i, 'Symbol']
    b = a + '.NS'
    m = yf.Ticker(b)
    mf = m.financials
    try:
        mg = mf.loc['Gross Profit']
    except:
        mg = np.NaN
    try:
        latest_price = m.info['regularMarketPrice']
    except:
        latest_price = np.NaN
    try:
        pe_ratio = m.info['trailingPE']
    except:
        pe_ratio = np.NaN
    try:
        pb_ratio = m.info['priceToBook']
    except:
        pb_ratio = np.NaN
    try:
        ps_ratio = m.info['priceToSalesTrailing12Months']
    except:
        ps_ratio = np.NaN
    try:
        ev_to_ebitda = m.info['enterpriseToEbitda']
    except:
        ev_to_ebitda = np.NaN
    try:
        enterprise_value = m.info['enterpriseValue']
    except:
        enterprise_value = np.NaN
    try:
        if(isinstance(mg.iloc[0], float) | isinstance(mg.iloc[0], int)):
            gross_profit = mg.iloc[0]
    except:
        gross_profit = np.NaN
    try:
        if(isinstance(enterprise_value, float) | isinstance(enterprise_value, int)):
            ev_to_gross_profit = enterprise_value/gross_profit
    except:
        ev_to_gross_profit = np.NaN

    rv_dataframe = rv_dataframe.append(
        pd.Series([a,
                   latest_price,
                   'N/A',
                   pe_ratio,
                   'N/A',
                   pb_ratio,
                   'N/A',
                   ps_ratio,
                   'N/A',
                   ev_to_ebitda,
                   'N/A',
                   ev_to_gross_profit,
                   'N/A',
                   'N/A'],
                  index=rv_columns),
        ignore_index=True
    )

# rv_dataframe

rv_dataframe = rv_dataframe.dropna()
# rv_dataframe

metrics = {
    'Price-to-Earnings Ratio': 'PE Percentile',
    'Price-to-Book Ratio': 'PB Percentile',
    'Price-to-Sales Ratio': 'PS Percentile',
    'EV/EBITDA': 'EV/EBITDA Percentile',
    'EV/GP': 'EV/GP Percentile'
}

for row in rv_dataframe.index:
    for metric in metrics.keys():
        rv_dataframe.loc[row, metrics[metric]] = stats.percentileofscore(
            rv_dataframe[metric], rv_dataframe.loc[row, metric])/100

for metric in metrics.values():
    print(rv_dataframe[metric])

# rv_dataframe


for row in rv_dataframe.index:
    value_percentiles = []
    for metric in metrics.keys():
        value_percentiles.append(rv_dataframe.loc[row, metrics[metric]])
    rv_dataframe.loc[row, 'RV Score'] = mean(value_percentiles)

# rv_dataframe

rv_dataframe.sort_values(by='RV Score', inplace=True)
rv_dataframe = rv_dataframe[:10]
rv_dataframe.reset_index(drop=True, inplace=True)

# rv_dataframe

day = date.today()
rv_dataframe.to_csv(f'niftymidcap50-{day}.csv')
