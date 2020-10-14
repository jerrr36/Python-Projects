import pandas_datareader as pdr
import datetime
import numpy as np
#import yfinance
import matplotlib.pyplot as plt
import pandas as pd
import time


path = '/content/gdrive/My Drive/nyse.csv'
p2='/content/gdrive/My Drive/constituents_csv.csv'

sp =pd.read_csv(p2)
#sp = sp[sp['IPOyear']!= 2020]
#sp = sp.drop(labels='Unnamed:8')
#sp = sp.dropna(axis=0)
t_list = []
p = '.'
s ='^'
t = '$'
for ticker in sp['Symbol']:
  if p in ticker or s in ticker or t in ticker:
    continue
  t_list.append(ticker)

print(t_list)

sp.head()
ind_it = sp[sp['Sector'] =='Information Technology']
t_list = []
p = '.'
s ='^'
t = '$'
for ticker in ind_it['Symbol']:
  if p in ticker or s in ticker or t in ticker:
    continue
  t_list.append(ticker)

cl_df = pd.read_csv(path)
cl_df = cl_df[cl_df['IPOyear']!= 2020]
cl_df = cl_df.dropna(axis = 0)

t_list = []
p = '.'
s ='^'
t = '$'
for ticker in sp['ACT Symbol']:
  if p in ticker or s in ticker or t in ticker:
    continue
  t_list.append(ticker)

tickers = ['TSLA','MSFT','SBUX','AAPL','GPRO','APT','ABB','ACM','J']

#pharma
tickers = ['LLY','PFE','BMY','ABBV','RDY','DRRX','AGN','NVS','MRK','ABT','ZTS','TAK']

#S&P 500
t_list = ['MMM','ABT','ABBV','ABMD','ACN','ATVI','ADBE','AMD','AAP','AES','AFL','A','APD','GOOGL','GOOG','MO','AMZN','ANSS','ADSK','ADP']

def share_finder(funds, stock_price):
  shares = 1
  while True:
    if shares*stock_price > 2000:
      shares -= 1
      break
    shares += 1  
  
  funds -= stock_price*shares
  #print(f'RF {funds}')
  return shares, funds

  #def momentum():

stock = pdr.get_data_yahoo(t_list[0],start = datetime.datetime(2010,10,1),end=datetime.datetime(2020,1,1))
df = pd.DataFrame(stock)

df.head()
#print(df.iloc[1,3])

#I feel like this is only good in a bull market
#t_list = ['BHF']
returns = []
for ticker in t_list:
  if ticker == 'BHF':
    continue
  risk = 1  
  try:
    stock = pdr.get_data_yahoo(ticker,start = datetime.datetime(2010,10,1),end=datetime.datetime(2020,1,1))
  except:
    continue
  df = pd.DataFrame(stock)
  df['One Year SMA'] = df[['Close']].dropna().rolling(200).mean()
  df['Half Year SMA'] = df[['Close']].dropna().rolling(100).mean()
  window = 5
  df['5 Day EMA'] = pd.Series.ewm(df['Close'], span=window).mean()
  df['10 Day Rolling STD'] = df[['Close']].rolling(10).std()
  i = 0 
  buy = True
  sell = False
  bought_price = 0
  sold_price = 0
  funds = 2000
  profit = 0
  #date_b = []
  #date_s = []
  shares = 1
  while i < len(df):
    while buy == True and i < len(df):
      if df.iloc[i,8]/df.iloc[i,3] > 1.05*risk and df.iloc[i,9]/df.iloc[i,3] > .025:
        bought_price = df.iloc[i,3]
        risk += .02
        shares, funds = share_finder(funds,df.iloc[i,3])
        db = df.index.date[i]
        #print(f'Bought {shares} shares for: {bought_price} on {db}')
        buy = False
        sell = True
        investment =  bought_price * shares
        
      i += 1 
    while sell == True and i < len(df):
      if bought_price/df.iloc[i,3] < .95*risk and df.iloc[i,3] > bought_price and df.iloc[i,9]/df.iloc[i,3]>.1:
        sold_price = df.iloc[i,3]
        funds += sold_price*shares
        buy = True
        sell = False
        ds = df.index.date[i]
        #print(f'Sold {shares} shares for: {sold_price} on {ds}')
        #print(f'Profit so far: {funds - 2000}')
      elif df.iloc[i,3]/bought_price <= .75*(1.1-risk):
        sold_price = df.iloc[i,3]
        funds += sold_price*shares
        risk -= .03
        buy = True
        sell = False
        ds = df.index.date[i]
        #print(f'Sold {shares} shares for: {sold_price} on {ds}')
      i += 1

  #cash out    
  if sell == True:
    #print(f'{shares} at {df.iloc[-1,3]} that were bought at {bought_price} on {db}')
    print(f'{ticker} Profit: {funds-investment+df.iloc[-1,3]*shares-2000}')
    returns.append(funds-investment+df.iloc[-1,3]*shares)

    
  else:
    print(f'{ticker} Profit: {funds-2000}')
    returns.append(funds)
    
print(f'Mean return is {np.mean(returns)-2000}')

print(returns)

for i, r in enumerate(returns):
  if r > 2000000:
    print(i)

"""The section below is testing grounds for theories"""

stock = pdr.get_data_yahoo('TSLA',start = datetime.datetime(2010,10,1),end=datetime.datetime(2020,3,13))



#I feel like this is only good in a bull market
#t_list = ['BHF']
returns = []
for ticker in t_list:
  if ticker == 'BHF':
    continue
  risk = 1  
  try:
    stock = pdr.get_data_yahoo(ticker,start = datetime.datetime(2010,10,1),end=datetime.datetime(2020,1,1))
  except:
    continue
  df = pd.DataFrame(stock)
  df['One Year SMA'] = df[['Close']].dropna().rolling(200).mean()
  df['Half Year SMA'] = df[['Close']].dropna().rolling(5).mean()
  window = 5
  df['5 Day EMA'] = pd.Series.ewm(df['Close'], span=window).mean()
  df['10 Day Rolling STD'] = df[['Close']].rolling(10).std()
  i = 0 
  buy = True
  sell = False
  bought_price = 0
  sold_price = 0
  funds = 2000
  profit = 0
  transactions = 0
  #date_b = []
  #date_s = []
  past50 = []
  shares = 1
  while i < len(df):
    past50.append(df.iloc[i,2])
    if len(past50) > 30:
      past50 = past50[1:]
    while buy == True and i < len(df):
      if df.iloc[i,3] == max(past50):
        bought_price = df.iloc[i,3]
        risk += .02
        shares, funds = share_finder(funds,df.iloc[i,3])
        db = df.index.date[i]
        #print(f'Bought {shares} shares for: {bought_price} on {db}')
        buy = False
        sell = True
        investment =  bought_price * shares
        transactions += 1
        
      i += 1 
    while sell == True and i < len(df):
      #if df.iloc[i,3] > bought_price and df.iloc[i,7] < df.iloc[i,3]:
        #sold_price = df.iloc[i,3]
        #funds += sold_price*shares
        #buy = True
        #sell = False
        #ds = df.index.date[i]
        #print(f'Sold {shares} shares for: {sold_price} on {ds}')
        #print(f'Profit so far: {funds - 2000}')
      if df.iloc[i,3] == min(past50[-20:]):
        sold_price = df.iloc[i,3]
        funds += sold_price*shares
        risk -= .03
        buy = True
        sell = False
        ds = df.index.date[i]
        transactions += 1
        #print(f'Sold {shares} shares for: {sold_price} on {ds}')
      i += 1

  #cash out    
  if sell == True and transactions != 0:
    #print(f'{shares} at {df.iloc[-1,3]} that were bought at {bought_price} on {db}')
    print(f'{ticker} Final Funds: {funds+df.iloc[-1,3]*shares}')
    returns.append(funds+df.iloc[-1,3]*shares)

    
  elif transactions != 0:
    print(f'{ticker} Final Funds: {funds}')
    returns.append(funds)
    
print(f'Mean return is {np.mean(returns)}')

adj_ret = []
for ret in returns:
  if ret != 2000:
    adj_ret.append(ret)

print(np.mean(adj_ret))