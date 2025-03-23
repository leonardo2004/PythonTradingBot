import pandas as pd
import numpy as np
import yfinance as yf
import datetime

def YFTicker(ticker: str, start: datetime.datetime, end: datetime.datetime, interval: str, balance: float):
    """
        DOWNLOAD ticker FUNCTION
        THIS WILL DOWNLOAD ANY TICKER FROM YFINANCE AND PREPARE IT FOR FUTURE USE

        PARAMS:
            ticker: STR -> ticker NAME, EX: "ticker-USD"
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
        newticker["Return"] = newticker["Close"].diff()
        newticker["Return"] = (balance*newticker["Return"] / newticker["Close"].iat[0])
        newticker["Return"].fillna(0)
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

def run_strategy(ticker: pd.DataFrame, fee: float, initial_balance: float):
    val = line = total_operations = win_operations = total_fee = profit = 0

    balance = initial_balance
    ticker["Strategy_Return"] = pd.Series(0)

    #Run strategy:
    for i in ticker.Entry:
        if (i > 0):
            if (val == -1 or i == 2):
                #SELL END
                delta = start - ticker["Close"].iat[line]
                if delta > 0:
                    win_operations += 1
                print(f"SHORT {balance:.2f} {(delta*balance)/start:.2f} {ticker["Entry"].iat[line]} LINE {line}")

                profit = (delta*balance)/start
                balance += profit
                ticker["Strategy_Return"].iat[line] = profit

                val = 0
            if (val == 0):
                #BUY START
                total_fee += balance * (fee / 100)
                total_operations += 1
                start = ticker["Close"].iat[line]
                val = 1

        elif (i < 0):
            if (val == 1 or i == -2):
                #BUY END
                delta = ticker["Close"].iat[line] - start
                if delta > 0:
                    win_operations += 1
                print(f"LONG {balance:.2f} {(delta*balance)/start:.2f} {ticker["Entry"].iat[line]} LINE {line}")

                profit = (delta*balance)/start
                balance += profit
                ticker["Strategy_Return"].iat[line] = profit

                total_fee += balance * (fee / 100)
                val = 0
            if (val == 0):
                #SELL START
                total_fee += balance * (fee /100)
                total_operations += 1
                start = ticker["Close"].iat[line]
                val = -1

        line += 1


    #Strategy return calculation:
    ticker["Strategy_Return"] = ticker["Strategy_Return"].fillna(0)

    #Buy and Hold return:
    bnh_total_return = ticker["Close"].iat[-1] - ticker["Close"].iat[0]
    bnh_percentual_return = (bnh_total_return*100)/(ticker["Close"].iat[0])

    #Printing results:    
    print("\n\n"+"~"*16+"Results:"+"~"*16)
    print(f"Total operations: {total_operations}")
    print(f"Win operations: {win_operations}")
    if total_operations > 0:
        print(f"Win percentage: {win_operations / total_operations *100:.2f}%")
    else:
        print("Win percentage: 0.00%")
    print(f"Total fees: {total_fee:.2f}")
    print(f"Buy Hold return: {bnh_percentual_return:.2f}%")
    print(f"Strategy return: {((balance-initial_balance)*100/initial_balance):.2f}%")
    print(f"Balance: {((balance)-total_fee):.2f}")
    print(f"Profit: {((balance - initial_balance)-total_fee):.2f}")
    return
