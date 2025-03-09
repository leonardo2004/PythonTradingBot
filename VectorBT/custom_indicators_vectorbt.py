import vectorbt as vbt
import numpy as np

""" 
Creating indicator: Comparing moving averages
        The indicator compares 3 moving averages
        it returns a buy signal when the 3 averages are going 
        up and a sell signal when the 3 averages are going down
"""

def MMA(close,windowA=20,windowB=60,windowC=200) :
    ma_A = vbt.MA.run(close, windowA)
    ma_B = vbt.MA.run(close, windowB)
    ma_C = vbt.MA.run(close, windowC)

    ma_A_above_signals = ma_A.close_above(ma_A.ma).to_numpy()
    ma_B_above_signals = ma_B.close_above(ma_B.ma).to_numpy()
    ma_C_above_signals = ma_C.close_above(ma_C.ma).to_numpy()
    trend = np.where(ma_A_above_signals & ma_B_above_signals & ma_C_above_signals, 1, 0)

    ma_A_below_signals = ma_A.close_below(ma_A.ma).to_numpy()
    ma_B_below_signals = ma_B.close_below(ma_B.ma).to_numpy()
    ma_C_below_signals = ma_C.close_below(ma_C.ma).to_numpy()
    trend = np.where(ma_A_below_signals & ma_B_below_signals & ma_C_below_signals, -1, trend)

    return trend

# Creating indicator: Defining the factory for the indicator
MMA_ind = vbt.IndicatorFactory(
    class_name="3_signal_ma",
    short_name="3ma",
    input_names= ["close"],
    param_names= ["windowA", "windowB", "windowC"],
    output_names= ["value"]
).from_apply_func(
    MMA,
    windowA=20,
    windowB=60,
    windowC=200,
)