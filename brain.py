import pandas as pd
import numpy as np
import yfinance as yf
import datetime

def YFTicker(ticker: str, start: datetime.datetime, end: datetime.datetime, interval: str):
    """
        DOWNLOAD ticker FUNCTION
        THIS WILL DOWNLOAD ANY TICKER FROM YFINANCE AND PREPARE IT FOR FUTURE USE

        PARAMS:
            ticker: STR -> ticker NAME, EX: "BTC-USD"
            start: DATETIME.DATETIME -> START DATE
            end: DATETIME.DATETIME -> END DATE
            interval: STR -> TRADE INTERVALS
    """
    try:
        newticker = yf.download(
        ticker,
        start=start,
        end=end,
        interval=interval,
        auto_adjust=True,
        multi_level_index=False
)
    except:
        print("Download error")  
    
    """
    THIS NEXT PART:
        * ADDS THE LINE COLUMN -> IT COUNTS THE NUMBER OF 
        LINES IN THE DATABASE, SO EACH INTERVAL IS REPRESENTED 
        AS A LINE

        * REORGANIZES THE DATAFRAME IN THE FOLLOWING
        ORDER: "Line","Open","High","Low","Close","Volume"

        * SQUEEZE THE TICKER (FOR OPTIMIZATION)
    """

    #Add a column that contains the line number
    #try:
    newticker["Line"] = np.arange(1, len(newticker)+1)
    #except:
    #    print("Error: Could not add lines to ticker Dataframe")

    #Format the ticker (Line, Open, High, Low, Close, Volume)
    try:
        newticker = newticker.loc[:,["Line","Open","High","Low","Close","Volume"]]
    except:
        print("Error: Could not reorganize ticker values")
    
    #Add a return column based on previous and current day values
    try:
        newticker.loc[:,"Return"] = newticker.loc[:,"Close"].diff()
        newticker.loc[newticker["Line"] == 1,"Return"] = 0
    except:
        print("Error: Could not create Return column")

    #Repeats previous values when volume is missing data (This will probably change)
    try:
        newticker["Volume"] = newticker["Volume"].replace(0, np.nan).ffill()
    except:
        print("Error: Could not remove empty values from volume")

    #Squeeze the ticker for use
    try:
        newticker = newticker.squeeze()
    except:
        print("Error: Could not squeeze ticker")
    
    return newticker

def run_strategy(ticker: pd.DataFrame):
    val = 0
    line = 0
    total_operations = 0
    win_operations = 0
    for i in ticker.Entry:
        if (i == 1):
            if (val == 0):
                #BUY START
                total_operations += 1
                delta = ticker["Close"].iat[line]
                val = 1
            elif (val == -1):
                #SELL END
                delta = delta - ticker["Close"].iat[line]
                if delta > 0:
                    win_operations += 1
                print(f"SELL {delta} LINE {line}")
                val = 0
        elif (i == -1):
            if (val == 0):
                #SELL START
                total_operations += 1
                delta = ticker["Close"].iat[line]
                val = -1
            elif (val == 1):
                #BUY END
                delta = ticker["Close"].iat[line] - delta
                if delta > 0:
                    win_operations += 1
                print(f"BUY {delta} LINE {line}")
                val = 0
        line += 1
    
    print("\n\n"+"~"*16+"Results:"+"~"*16)
    print(f"Total operations: {total_operations}")
    print(f"Win operations: {win_operations}")
    if total_operations > 0:
        print(f"Win percentage: {win_operations / total_operations *100:.2f}%")

    return True
