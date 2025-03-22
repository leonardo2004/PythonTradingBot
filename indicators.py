import pandas as pd
import numpy as np

def VWAP(ticker: pd.DataFrame):
    """
        THIS FUNCTION GENERATES THE VWAP, CREATING A COLUMN IN THE TICKER DATAFRAME
    """
    try:
        ticker["VWAP"] = (((ticker["High"] + ticker["Low"] + ticker["Close"]) * 
                       (ticker["Volume"]).cumsum()) / 
                      (3 * ticker["Volume"].cumsum()))
    except:
        print("Error: Could not generate VWAP")
    return ticker

def SMA(ticker: pd.DataFrame, SMA_window: int, column: str):
    """
        THIS FUNCTION CREATES A SIMPLE MOVING AVERAGE BASED ON A COLUMN
        ** THIS WILL REMOVE ANY DATA BEFORE THE SMA STARTS **

        PARAMNS:
            ticker: pd.DataFrame -> ticker DATAFRAME
            SMA_window: INT -> WINDOW OF THE SMA, EX: 20

    """

    #Create the SMA
    try:
        ticker[f"{SMA_window}_{column}_SMA"] = ticker[column].rolling(window=SMA_window).mean().shift()
    except:
        print(f"Error: Could not generate SMA ({SMA_window}_{column}_SMA)")
    
    #Update return column values
    try:
        ticker.loc[ticker["Line"] == 1,"Return"] = 0
    except:
        print(f"Error: Could not update Return column when creating SMA ({SMA_window}_{column}_SMA)")

    return ticker