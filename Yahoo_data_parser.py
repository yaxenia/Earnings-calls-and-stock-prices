import pandas as pd
import numpy as np
import re
import yfinance as yf
import requests
import datetime as dt
from datetime import datetime, timedelta

#read list of tickers
tick = pd.read_excel('/content/snp100.xlsx')


#extracting data from Yahoo finance
def yahoo(ticker, start, end, frequency, events, include_adj_close = 'true'):
    headers ={'User-agent': 'Mozilla/5.0'}

    url = "https://query1.finance.yahoo.com/v7/finance/download/" + str(ticker)
    x = int(datetime.strptime(start, '%Y-%m-%d').strftime("%s"))
    y = int(datetime.strptime(end, '%Y-%m-%d').strftime("%s"))
    url += "?period1=" + str(x) + "&period2=" + str(y) + "&events"+str(events) +"&includeAdjustedClose=" + str(include_adj_close)
    
    r = requests.get(url, headers=headers)
    df = pd.read_csv(io.StringIO(r.text), index_col=0, parse_dates=True)
    return df

fin_data = pd.DataFrame()

for i in tick.Symbol.values:
    a = yahoo(str(i), start="2020-01-01", end="2023-01-01", 
                             frequency='1d', events = 'history', include_adj_close = 'true' )
    a = a.reset_index()
    a["Company"] = str(i)
    fin_data = pd.concat([fin_data,a], ignore_index=True)

fin_data.to_csv("/content/snp100_fin_data.csv")

