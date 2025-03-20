import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import functions
import matplotlib.pyplot as plt

#TO-DO:
#* Estratégia com OBV


#Rules:
#snake_case for variables, functions and methods;
#PascalCase for classes;
#SCREAMING_SNAKE_CASE for constants.


#Time period
period_end = datetime.datetime.now()
period_start = period_end - datetime.timedelta(days=8)


#Start BTC ticker (Download, Prepare, and create 3 SMAs)
BTC = functions.YFDownloadTicker("BTC-USD",start=period_start, end=period_end, interval="1m")
BTC = functions.PrepareTicker(BTC)

#Create 3 SMAs
BTC = functions.SMA(ticker=BTC, 
                    SMA_window=20, 
                    column="Close")
BTC = functions.SMA(ticker=BTC, 
                    SMA_window=60, 
                    column="Close")
BTC = functions.SMA(ticker=BTC, 
                    SMA_window=200,
                    column="Close")


#Calculate the signals for the 3 MA strategy
#If the 3 are pointing up == BUY
#If the 3 are pointing down == SELL
BTC["Signals"] = np.where((functions.signal_SMA_direction("20_Close_SMA", BTC)==1) &
                          (functions.signal_SMA_direction("60_Close_SMA", BTC)==1) &
                          (functions.signal_SMA_direction("200_Close_SMA", BTC)==1),
                          1,
                          0)
BTC["Signals"] = np.where((functions.signal_SMA_direction("20_Close_SMA", BTC)==-1) &
                          (functions.signal_SMA_direction("60_Close_SMA", BTC)==-1) &
                          (functions.signal_SMA_direction("200_Close_SMA", BTC)==-1),
                          -1,
                          BTC["Signals"])


#Entry calculation 
# BUY position if Signal == 1; else end order
# SELL position if Signal == -1; else end order
BTC["Signals_Return"] = BTC["Signals"]*BTC["Return"]
BTC["Entry"] = BTC.Signals.diff()


#Return calculation
#Strategy return calculation
Strategy_total_return = BTC["Signals_Return"].sum()
Strategy_percentual_return = Strategy_total_return*100/(BTC["Close"].iat[0,0])

#Buy and Hold return:
BnH_total_return = BTC["Close"].iat[-1,0] - BTC["Close"].iat[0,0]
BnH_percentual_return = (BnH_total_return*100)/(BTC["Close"].iat[0,0])

functions.run_strategy(BTC)
print(f"Buy and Hold Return: {BnH_percentual_return:.2f}%")
print(f"SMA strategy Return: {Strategy_percentual_return:.2f}%")


#Plots:
fig, ax = plt.subplots(nrows=3,
                       ncols=1,
                       sharex=True)

#Plots profits
ax[2].plot(BTC["Return"].cumsum(), 
           label="Buy/Hold")
ax[2].plot(BTC["Signals_Return"].cumsum(), 
           label="MMA Strategy")

#Plots the SMAs
ax[0].plot(BTC["20_Close_SMA"], 
           label="SMA 20", 
           color="xkcd:lavender")
ax[0].plot(BTC["60_Close_SMA"], 
           label="SMA 60", 
           color="xkcd:light purple")
ax[0].plot(BTC["200_Close_SMA"], 
           label="SMA 200", 
           color="xkcd:violet")

#Plots Close and Volume
ax[1].plot(BTC["Close"], 
           label="Price")
ax_volume = ax[1].twinx()
ax_volume.bar(BTC.index.values,
              BTC["Volume"].values.reshape(len(BTC)), 
              ec="k", label="Volume", 
              color="xkcd:black", 
              align='edge', 
              width=np.timedelta64(1, "m"))

#Make the entry points
ax[1].plot(BTC.loc[BTC["Entry"]>0].index.values, 
           BTC["Close"].loc[BTC.Entry>0], 
           '^',
           color = 'xkcd:sea green', 
           markersize = 12)
ax[1].plot(BTC.loc[BTC["Entry"]<0].index.values, 
           BTC["Close"].loc[BTC.Entry<0], 
           'v',
            color = 'xkcd:light red',
            markersize = 12)

#Makes the grid visible
ax[0].grid(visible=True, alpha=.3)
ax[1].grid(visible=True, alpha=.3)
ax[2].grid(visible=True, alpha=.3)
fig.legend()
plt.show()
