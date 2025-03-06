import vectorbt as vbt
import datetime
import pandas as pd
import numpy as np

end = datetime.datetime.now()
start = end - datetime.timedelta(days=7)

btc_price = vbt.YFData.download(
    "BTC-USD",
    missing_index="drop",
    start=start,
    end=end,
    interval='1m'
).get("Close")

def MMA(close,windowA=5,windowB=20,windowC=60, windowD=200) :
    #ma_A = vbt.MA.run(close, windowA)
    ma_B = vbt.MA.run(close, windowB)
    ma_C = vbt.MA.run(close, windowC)
    ma_D = vbt.MA.run(close, windowD)

    #ma_A_above_signals = ma_A.close_above(ma_A.ma).to_numpy()
    ma_B_above_signals = ma_B.close_above(ma_B.ma).to_numpy()
    ma_C_above_signals = ma_C.close_above(ma_C.ma).to_numpy()
    ma_D_above_signals = ma_D.close_above(ma_D.ma).to_numpy()
    trend = np.where(ma_B_above_signals & ma_C_above_signals & ma_D_above_signals, 1, 0)

    #ma_A_below_signals = ma_A.close_below(ma_A.ma).to_numpy()
    ma_B_below_signals = ma_B.close_below(ma_B.ma).to_numpy()
    ma_C_below_signals = ma_C.close_below(ma_C.ma).to_numpy()
    ma_D_below_signals = ma_D.close_below(ma_D.ma).to_numpy()
    trend = np.where(ma_B_below_signals & ma_C_below_signals, -1, trend)

    return trend

ind = vbt.IndicatorFactory(
    class_name='3_signal_ma',
    short_name='3ma',
    input_names= ['close'],
    param_names= ['windowA', 'windowB', 'windowC', 'windowD'],
    output_names= ['value']
).from_apply_func(
    MMA,
    windowA=5,
    windowB=20,
    windowC=60,
    windowD=200
)

teste = ind.run(
    btc_price
)

#print(teste.value.to_string())

entries = teste.value == 1
exits = teste.value == -1

pf = vbt.Portfolio.from_signals(btc_price, entries, exits)
print(pf.stats())

pf.plot().show()