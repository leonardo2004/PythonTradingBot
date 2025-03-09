import vectorbt as vbt
import datetime
import pandas as pd
import custom_indicators_vectorbt

# Analysis period
end = datetime.datetime.now()
start = end - datetime.timedelta(days=7)

#Setting the theme for vectorbt
vbt.settings.set_theme("dark")

# Data download (Using YFinance ; Package must be installed)
btc_price = vbt.YFData.download(
    "BTC-USD",
    missing_index="drop",
    start=start,
    end=end,
    interval="1m"
).get("Close")



MMA = custom_indicators_vectorbt.MMA_ind.run(
    btc_price
)

#Defining entry/exit points
entries = MMA.value == 1
exits = MMA.value == -1

pf = vbt.Portfolio.from_signals(btc_price, entries, exits)
print(pf.stats())

pf.plot().show()