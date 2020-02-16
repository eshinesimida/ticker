# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 23:03:39 2020

@author: a4546
"""

import tushare
import pandas
import datetime
import os
import time

def stockPriceIntrady(ticker, folder):
    #step 1, get intrady data online
    intraday = tushare.get_hist_data(ticker, ktype= '5')
    #print(intraday)
    
    #step 2, if the history exists, append
    file = folder + '/' + ticker + '.csv'
    
    if os.path.exists(file):
        history = pandas.read_csv(file, index_col = 0)
        intraday.append(history)
    #step 3, inverse based on index
    intraday.sort_index(inplace = True)
    intraday.index.name = 'timestamp'
    
    #step 4, save
    intraday.to_csv(file)
    print('Intraday for ['+ ticker+'] got.')
#step 1 : get tickers online
tickerRawData = tushare.get_stock_basics()
tickers = tickerRawData.index.tolist()
print(tickerRawData)

#step 2: save the ticker list to a local file

dateToday = datetime.datetime.today().strftime('%Y-%m-%d')
file = 'TickerList_' + dateToday + '.csv'
tickerRawData.to_csv(file)

for i, ticker in enumerate(tickers):
    try:
        print('Intraday', i ,'/', len(tickers))
        stockPriceIntrady(ticker,folder = 'IntradayCN/')
    except:
        pass
    if i > 20:
        break
print('Intraday for all stocks got.')
#step 3.get stock price for all
stockPriceIntrady('600031',folder = 'IntradayCN/')



###k line picture
import pandas
import matplotlib
import mpl_finance as mpf
import matplotlib.pyplot as plt

matplotlib.style.use('ggplot')

def stockPricePlot(ticker):
    #step 1. load data
    history = pandas.read_csv('IntradayCN/'+ ticker+'.csv', 
                              parse_dates = True,index_col = 0)
    
    
    #step 2. data manipulation
    close = history['close']
    close = close.reset_index()
    close['timestamp'] = close['timestamp'].map(matplotlib.dates.date2num)
    
    onlc = history[['open','high','low','close']].resample('1H').ohlc()
    onlc = onlc.reset_index()
    onlc['timestamp'] = onlc['timestamp'].map(matplotlib.dates.date2num)
    
    #step 3. plot figure,  subplot 1: scatter plot, 2 ,candle
    #3.1 subplot 1: scatter plot
    plt.figure(figsize=(20,20))
    subplot1 = plt.subplot2grid((2,1),(0,0), rowspan = 1, colspan = 1)
    subplot1.xaxis_date()
    subplot1.plot(close['timestamp'], close['close'],'b.')
    plt.title(ticker)
    
    
    #3.2 subplot 2: candle stick plot
    plt.figure(figsize=(20,20))
    subplot2 = plt.subplot2grid((2,1),(1,0), rowspan = 1, colspan = 1,
                                sharex = subplot1)
    mpf.candlestick_ochl(ax=subplot2, quotes = onlc.values, width = 0.01,
                         colorup = 'g', colordown = 'r')
    plt.show()

stockPricePlot('600031')
