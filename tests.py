import matplotlib.pyplot as plot
import pandas as pd
import numpy as np

def run_strategy(ticker: pd.DataFrame, entry: pd.Series):
    val = 0
    line = 0
    total_operations = 0
    win_operations = 0
    for i in entry:
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
                print(f"SELL {delta}")
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
                print(f"BUY {delta}")
                val = 0
        line += 1
    print(f"total operations: {total_operations}")
    print(f"win operations: {win_operations}")
    if total_operations > 0:
        print(f"win %: {win_operations / total_operations}")
    
    return True

data = {
    "teste" : [0,-1,0,1,-1,0,0,1],
    "Close" : [10,9,8,7,8,10,11,9]
}
data = pd.DataFrame(data)

fig, ax = plot.subplots(2,1)
ax[0].plot(data["teste"],data["teste"])
ax[1].hist(data["teste"],bins=3,ec="k")
plot.show()

run_strategy(data,data["teste"])


int_interval = 1
char_interval = "m"
interval = f"{int_interval}{char_interval}"
print(interval)

# .loc localiza os valores desejados, nesse caso, teste == 1
#Retorna os valores de índice que satisfaçam teste == 1 ; retorna uma lista
#print(data.loc[data.teste==1].index.values)