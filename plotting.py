import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_results(ticker: pd.DataFrame):
    fig, ax = plt.subplots(nrows=3,
                       ncols=1,
                       sharex=True)

    #Plots profits
    ax[2].plot(ticker["Return"].cumsum(), 
            label="Buy/Hold")
    ax[2].plot(ticker["Signals_Return"].cumsum(), 
            label="Strategy")

    #Plots the SMAs
    #Close
    ax[0].plot(ticker["20_Close_SMA"], 
            label="SMA 20", 
            color="xkcd:lavender")
    ax[0].plot(ticker["60_Close_SMA"], 
            label="SMA 60", 
            color="xkcd:light purple")
    ax[0].plot(ticker["200_Close_SMA"], 
            label="SMA 200", 
            color="xkcd:violet")

    #Plots Close and Volume values
    ax[1].plot(ticker["Close"], 
            label="Price")
    ax_volume = ax[1].twinx()
    ax_volume.bar(ticker.index.values,
                ticker["Volume"].values.reshape(len(ticker)), 
                ec="k", label="Volume", 
                color="xkcd:black", 
                align='edge', 
                width=np.timedelta64(1, "m"))

    #Make the entry points
    ax[1].plot(ticker.loc[ticker["Entry"]>0].index.values, 
            ticker["Close"].loc[ticker.Entry>0], 
            '^',
            color = 'xkcd:sea green', 
            markersize = 12)
    ax[1].plot(ticker.loc[ticker["Entry"]<0].index.values, 
            ticker["Close"].loc[ticker.Entry<0], 
            'v',
                color = 'xkcd:light red',
                markersize = 12)

    #Makes the grid visible
    ax[0].grid(visible=True, alpha=.3)
    ax[1].grid(visible=True, alpha=.3)
    ax[2].grid(visible=True, alpha=.3)
    fig.legend()
    plt.show()
    return True