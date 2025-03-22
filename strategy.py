#Base:
import pandas as pd
import numpy as np
import datetime

#Custom:
import brain
import indicators
import signals
import plotting

"""
TO-DO:
    * Volume strategy
    * Fee calculation

Rules:
    snake_case for variables, functions and methods
    PascalCase for classes
    SCREAMING_SNAKE_CASE for constants
"""

#Time period
PERIOD_END = datetime.datetime.now()
PERIOD_START = PERIOD_END - datetime.timedelta(days=8)


#Start BTC ticker (Download, Prepare, and create 3 SMAs)
BTC = brain.YFTicker("BTC-USD",start=PERIOD_START, end=PERIOD_END, interval="1m")


#Create SMAs
#Close
BTC = indicators.SMA(ticker=BTC, 
                    SMA_window=20, 
                    column="Close")
BTC = indicators.SMA(ticker=BTC, 
                    SMA_window=60, 
                    column="Close")
BTC = indicators.SMA(ticker=BTC, 
                    SMA_window=200,
                    column="Close")


#Calculate the signals for the 3 MA strategy
#If the 3 are pointing up == BUY
#If the 3 are pointing down == SELL
BTC["Signals"] = np.where((signals.SMA_above("20_Close_SMA","60_Close_SMA", BTC)==1) &
                          (signals.SMA_direction("60_Close_SMA", BTC)==1),
                          1,
                          0)
BTC["Signals"] = np.where((signals.SMA_direction("20_Close_SMA", BTC)==-1) &
                          (signals.SMA_direction("60_Close_SMA", BTC)==-1),
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
Strategy_percentual_return = Strategy_total_return*100/(BTC["Close"].iat[0])

#Buy and Hold return:
BnH_total_return = BTC["Close"].iat[-1] - BTC["Close"].iat[0]
BnH_percentual_return = (BnH_total_return*100)/(BTC["Close"].iat[0])

brain.run_strategy(BTC)
print(f"Buy and Hold Return: {BnH_percentual_return:.2f}%")
print(f"SMA strategy Return: {Strategy_percentual_return:.2f}%")

plotting.plot_results(BTC)
