import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import functions
import matplotlib.pyplot as plt

#Time period
period_end = datetime.datetime.now()
period_start = period_end - datetime.timedelta(days=40)

#Start BTC ticker (Download, Prepare, and create 3 SMAs)
BTC = functions.YFDownloadTicker("BTC-USD",start=period_start, end=period_end, interval="5m")
BTC = functions.PrepareTicker(BTC)
BTC = functions.SMA(BTC, 5, column="Close")
BTC = functions.SMA(BTC, 60, column="Close")
BTC = functions.SMA(BTC, 200, column="Close")

#Calculate the signals for the 3 MA strategy
#If the 3 are pointing up == BUY
#If the 3 are pointing down == SELL
BTC["Signals"] = np.where((
    functions.signal_SMA_direction("5_Close_SMA", BTC)==1) &
    (functions.signal_SMA_direction("60_Close_SMA", BTC)==1) &
    (functions.signal_SMA_direction("200_Close_SMA", BTC)==1),
    1,
    0)
BTC["Signals"] = np.where(
    (functions.signal_SMA_direction("5_Close_SMA", BTC)==-1) &
    (functions.signal_SMA_direction("60_Close_SMA", BTC)==-1) &
    (functions.signal_SMA_direction("200_Close_SMA", BTC)==-1),
    -1,
    BTC["Signals"])

#Signal calculation 
# BUY position if Signal == 1; else end order
# SELL position if Signal == -1; else end order
BTC["Signals_Return"] = BTC["Signals"]*BTC["Return"]


print(BTC[["Line","Return","Signals","Signals_Return","Close"]][0:200])

print("\n\n"+"~"*16+"Results:"+"~"*16)
print(f"Buy and Hold Return: {np.exp(BTC["Return"]).cumprod().iloc[-1]-1}")
print(f"SMA strategy Return: {np.exp(BTC["Signals_Return"]).cumprod().iloc[-1]-1}")

#Plot the graph
plt.plot(np.exp(BTC["Return"]).cumprod(), label="Buy/Hold")
plt.plot(np.exp(BTC["Signals_Return"]).cumprod(), label="MMA Strategy")
#plt.plot(BTC["Close"], label="Close Price")
plt.legend(loc=2)
plt.grid(visible=True, alpha=.3)
plt.show()
