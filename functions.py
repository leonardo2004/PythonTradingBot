import pandas as pd
import numpy as np
import yfinance as yf
import datetime

def YFDownloadTicker(ticker: str, start: datetime.datetime, end: datetime.datetime, interval: str):
    """
        DOWNLOAD ticker FUNCTION
        NOTE: THIS FUNCTION IS PURELY FOR ASTHETICS, IT IS THE SAME AS "yfinance.download()"

        THIS WILL DOWNLOAD ANY ticker FROM YFINANCE

        PARAMS:
            ticker: STR -> ticker NAME, EX: "BTC-USD"
            start: DATETIME.DATETIME -> START DATE
            end: DATETIME.DATETIME -> END DATE
            interval: STR -> TRADE INTERVALS
    """
    try:
        Newticker = yf.download(
        ticker,
        start=start,
        end=end,
        interval=interval,
        auto_adjust=True
)
    except:
        print("Download error")
    
    return Newticker

def PrepareTicker(ticker: pd.DataFrame):
    """
        PREPARE THE ticker FOR USAGE FOR BACKTESTING

        * ADDS THE LINE COLUMN -> IT COUNTS THE NUMBER OF 
        LINES IN THE DATABASE, SO EACH INTERVAL IS REPRESENTED 
        AS A LINE

        * REORGANIZES THE DATAFRAME IN THE FOLLOWING
        ORDER: "Line","Open","High","Low","Close","Volume"

        PARAMNS:
            ticker: pd.DataFrame -> ticker DATAFRAME
    """

    #Add a column that contains the line number
    try:
        ticker["Line"] = np.arange(1, len(ticker)+1)
    except:
        print("Error: Could not add lines to ticker Dataframe")

    #Format the ticker (Line, Open, High, Low, Close, Volume)
    try:
        ticker = ticker.loc[:,["Line","Open","High","Low","Close","Volume"]]
    except:
        print("Error: Could not reorganize ticker values")
    #Add a return column for benchmarking against Buy n Hold strategies
    try:
        ticker.loc[:,"Return"] = np.log(ticker.loc[:,"Close"]).diff()
        ticker.loc[ticker["Line"] == 1,"Return"] = 0
    except:
        print("Error: Could not create Return column")

    return ticker

def SMA(ticker: pd.DataFrame, SMA_window: int, column: str):
    """
        THIS FUNCTION CREATES A SIMPLE MOVING AVERAGE BASED ON A COLUMN
        ** THIS WILL REMOVE ANY DATA BEFORE THE SMA STARTS **

        PARAMNS:
            ticker: pd.DataFrame -> ticker DATAFRAME
            SMA_window: INT -> WINDOW OF THE SMA, EX: 20

    """

    #Checks if the column type is numeric
    if pd.api.types.is_numeric_dtype(ticker[column]):
        print("Error: Column type is not a number")
        return ticker
    
    #Create the SMA
    try:
        ticker[f"{SMA_window}_{column}_SMA"] = ticker[column].rolling(window=SMA_window).mean().shift()
    except:
        print("Error: Could not create SMA")
    
    #Update return column values
    try:
        ticker.loc[ticker["Line"] == 1,"Return"] = 0
    except:
        print("Error: Could not update Return column when creating SMA")

    return ticker

def signal_SMA_direction(column: str, ticker: pd.DataFrame):
    """
        THIS FUNCTIONS CHECKS IF THE SMA IS GOING UP OR DOWN BASED ON THE PREVIOUS VALUE
        IT RETURNS A SIGNAL NUMPY LIST: 1 == BUY, 0 == WAIT, -1 == SELL

        PARAMNS:
            column: str -> THE SMA COLUMN NAME IN THE PANDAS DATAFRAME
            ticker: pd.DataFrame -> ticker DATAFRAME
    """
    #.shift(1) -> GETS THE VALUE OF THE PREVIOUS LINE
    signal = np.where((ticker[column]>ticker[column].shift(1)),1,0)
    signal = np.where((ticker[column]<ticker[column].shift(1)),-1,signal)
    return signal
