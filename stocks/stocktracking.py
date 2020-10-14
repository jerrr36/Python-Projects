#tracks vxx and spy and alerts you if certain conditions are met
#emails you that certain condition is met
#actually kinda good at alerting you to potential red days for option purposes

import statistics
import datetime
import smtplib, ssl
import iexfinance
from iexfinance.stocks import Stock, get_historical_data



#iex token
t = ''

#email function
def email(msg):
  #initial information
  port = 465  # For SSL
  smtp_server = "smtp.gmail.com"
  sender_email = ""  # Enter your address
  receiver_email = ""  # Enter receiver address
  password = input("Type your password and press enter: ")
  message = msg
  context = ssl.create_default_context()

  #sending email
  with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)

#Stock information function
def get_stock(ticker):
  #getting stock information
  stock = Stock(ticker,token = t)
  s = stock.get_quote()
  prev = s['previousClose']
  price = s['latestPrice']
  
  #calculating percent change from previous close
  change = round((price / prev - 1) * 100, 2)

  #getting dates for historical data
  today = datetime.date.today()
  yesterday = today - datetime.timedelta(days =  1)
  week = today - datetime.timedelta(days =  7)

  #Getting last week closing prices
  hist = get_historical_data(ticker, week, yesterday, close_only=True, token = t)

  prices = []
  for date in hist:
    prices.append(hist[date]['close'])

  #calculating average from historical data
  weeklyAverage = statistics.mean(prices)

  #calculating percent change of current price vs weeklyAverage
  weeklyChange = round((price / weeklyAverage - 1) * 100, 2)
  return change, weeklyChange

def main():
  #main variables
  spy = "SPY"
  vxx = "VXX"

  tickers =["MSFT","AAPL","AMZN","GOOGL"]

  vxxChange, vxxweeklyChange = get_stock(vxx)
  spyChange, spyweeklyChange = get_stock(spy)


  if vxxweeklyChange > 0 and spyweeklyChange > 0 or vxxChange > 0 and spyChange > 0:
    msg = """\
    Subject: Hi there


    VXX and SPY above either their previous close or weekly average."""
    email(msg)
  
  else:
    msg = """\
    Subject: Hi there
    

    Nothing to report"""
    email(msg)


main()