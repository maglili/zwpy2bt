"""
This file contains carious strategies from zwpython.
All strategies are class objects that inherits BaseStrategyFrame class,
so user only need to writing 1) __init__ method and 2) next method.
"""

import backtrader as bt
from Strategy.BaseStrategyFrame import BaseStrategyFrame
from Strategy.utils import VolumeWeightedAveragePrice


class Tim0Strategy(BaseStrategyFrame):
    """
    Implementing the tim0Trad strategy from zwPython.

    Rule:
        buy stock at first day then do nothing.

    Args:
        None.
    """

    def __init__(self):

        # multiple inheritance
        super(Tim0Strategy, self).__init__()

        print("printlog:", self.params.printlog)

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log("Close, %.2f" % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # BUY, BUY, BUY!!! (with all possible default parameters)
            self.log("BUY CREATE, %.2f" % self.dataclose[0])

            # Keep track of the created order to avoid a 2nd order
            self.order = self.buy()


class SmaStrategy(BaseStrategyFrame):
    """
    Implementing the SMA_sta strategy from zwPython.

    Rule:
        If close price > SMA: buy
        If close price < SMA: sell

    Args:
        maperiod (int): The time period for moving average.
    """

    params = (("maperiod", 15),)

    def __init__(self):

        # multiple inheritance
        super(SmaStrategy, self).__init__()

        print("printlog:", self.params.printlog)
        print("maperiod:", self.params.maperiod)

        # Add indicators
        self.sma = bt.indicators.SimpleMovingAverage(
            self.dataclose, period=self.params.maperiod
        )

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log("Close, %.2f" % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] > self.sma[0]:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log("BUY CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            if self.dataclose[0] < self.sma[0]:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log("SELL CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()


class CmaStrategy(BaseStrategyFrame):
    """
    Implementing the CMA_sta strategy from zwPython.

    Rule:
        While close and MA crossover:
            If MA trend is go up: buy.
            If MA trend is go down: sell.

    Args:
        maperiod (int): The time period for moving average.
    """

    params = (("maperiod", 15),)

    def __init__(self):

        # multiple inheritance
        super(CmaStrategy, self).__init__()

        print("printlog:", self.params.printlog)
        print("maperiod:", self.params.maperiod)

        # Add indicators
        self.sma = bt.indicators.SimpleMovingAverage(
            self.dataclose, period=self.params.maperiod
        )

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log("Close, %.2f" % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check stock Trend
        trend = None
        ma, ma_lag2 = self.sma[0], self.sma[-2]
        close, close_lag2 = self.dataclose[0], self.dataclose[-2]
        if (close > ma) and (close_lag2 < ma_lag2) and (close > close_lag2):
            trend = 1
        elif (close < ma) and (close_lag2 > ma_lag2) and (close < close_lag2):
            trend = -1

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if trend == 1:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log("BUY CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            if trend == -1:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log("SELL CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()


class VwapStrategy(BaseStrategyFrame):
    """
    Implementing the VWAP_sta strategy from zwPython.

    Rule:
        No description in the book.

    Args:
        maperiod (int): The time period for sliding window in VWAP.
        kvwap (float): threshold.
    """

    params = (("maperiod", 15), ("kvwap", 0.01))

    def __init__(self):

        # multiple inheritance
        super(VwapStrategy, self).__init__()

        print("printlog:", self.params.printlog)
        print("maperiod:", self.params.maperiod)
        print("kvwap:", self.params.kvwap)

        # Add indicators
        self.vwap = VolumeWeightedAveragePrice(
            self.dataclose, period=self.params.maperiod
        )

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log("Close, %.2f" % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check stock Trend
        vwap = self.vwap[0]
        if vwap > 0:
            close = self.dataclose[0]
            kvwap = self.params.kvwap
            stock_num = self.broker.getposition(self.datas[0]).size
            cash = self.broker.get_cash()
            stock_value = stock_num * close

            if not self.position:

                if (close > vwap * (1 + kvwap)) and (stock_value < (cash * 0.9)):

                    # BUY, BUY, BUY!!! (with all possible default parameters)
                    self.log("BUY CREATE, %.2f" % self.dataclose[0])

                    # Keep track of the created order to avoid a 2nd order
                    self.order = self.buy()

            else:

                if (close < vwap * (1 - kvwap)) and (stock_value > 0):

                    # SELL, SELL, SELL!!! (with all possible default parameters)
                    self.log("SELL CREATE, %.2f" % self.dataclose[0])

                    # Keep track of the created order to avoid a 2nd order
                    self.order = self.sell()


class BBandsStrategy(BaseStrategyFrame):
    """
    Implementing the BBANDS_sta strategy from zwPython.

    Rule:
        If close price < bottom bband: sell.
        If close price > top bband: buy.

    Args:
        BBandsperiod (int): ma period

    """

    params = (("BBandsperiod", 20),)

    def __init__(self):

        # multiple inheritance
        super(BBandsStrategy, self).__init__()

        print("printlog:", self.params.printlog)
        print("BBandsperiod:", self.params.BBandsperiod)

        # Add indicators
        self.bband = bt.indicators.BBands(
            self.dataclose, period=self.params.BBandsperiod
        )

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log("Close, %.2f" % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            if self.dataclose[0] < self.bband.lines.bot[0]:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log("BUY CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:
            if self.dataclose[0] > self.bband.lines.top[0]:

                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log("SELL CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()


class TurStrategy(BaseStrategyFrame):
    """
    Implementing the tur10 strategy from zwPython.

    Rule:
        If close price > max( high price of pass n days): buy.
        After buy action, if close price < min( low proce of pass n day): sell

    Args:
        n_high(int): highest high price of pass n day.
        n_low(int): lowest low price of pass n day.

    """

    params = (("n_high", 30), ("n_low", 15))

    def __init__(self):

        # multiple inheritance
        super(TurStrategy, self).__init__()

        print("printlog:", self.params.printlog)
        print("n_high:", self.params.n_high)
        print("n_low:", self.params.n_low)

        # Add indicators
        self.pass_highest = bt.indicators.Highest(
            self.datahigh, period=self.params.n_high
        )

        self.pass_lowest = bt.indicators.Lowest(self.datalow, period=self.params.n_low)

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log("Close, %.2f" % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] > self.pass_highest[-1]:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log("BUY CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            if self.dataclose[0] < self.pass_lowest[-1]:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log("SELL CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()


class MacdV1Strategy(BaseStrategyFrame):
    """
    Implementing the macd10 strategy from zwPython.

    Rule:
        If MACD > 0: buy.
        If MACD < 0: sell.

    Args:.
        fast_period (int): fast ema period.
        slow_period (int): slow ema period.
        signal_period (int): macd signal period.

    """

    params = (("fast_period", 12), ("slow_period", 26), ("signal_period", 9))

    def __init__(self):

        # multiple inheritance
        super(MacdV1Strategy, self).__init__()

        print("printlog:", self.params.printlog)
        print("period_me1:", self.params.fast_period)
        print("period_me2:", self.params.slow_period)
        print("period_signal:", self.params.signal_period)

        # Add indicators
        self.macd = bt.indicators.MACD(
            self.dataclose,
            period_me1=self.params.fast_period,
            period_me2=self.params.slow_period,
            period_signal=self.params.signal_period,
        )

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log("Close, %.2f" % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.macd.macd[0] > 0:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log("BUY CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            # self.mcross[0] == -1:
            if self.macd.macd[0] < 0:

                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log("SELL CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()


class MacdV2Strategy(BaseStrategyFrame):
    """
    Implementing the macd20 strategy from zwPython.

    Rule:
        If MACD - MACD_signal > 0: buy.
        If MACD - MACD_signal < 0: sell.

    Args:
        fast_period (int): fast ema period.
        slow_period (int): slow ema period.
        signal_period (int): macd signal period.
    """

    params = (("fast_period", 12), ("slow_period", 26), ("signal_period", 9))

    def __init__(self):

        # multiple inheritance
        super(MacdV2Strategy, self).__init__()

        print("printlog:", self.params.printlog)
        print("period_me1:", self.params.fast_period)
        print("period_me2:", self.params.slow_period)
        print("period_signal:", self.params.signal_period)

        # Add indicators
        self.macd = bt.indicators.MACD(
            self.dataclose,
            period_me1=self.params.fast_period,
            period_me2=self.params.slow_period,
            period_signal=self.params.signal_period,
        )

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log("Close, %.2f" % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.macd.macd[0] > self.macd.signal[0]:  # self.mcross[0] == 1:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log("BUY CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            # self.mcross[0] == -1:
            if self.macd.macd[0] < self.macd.signal[0]:

                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log("SELL CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()


class KdjV1Strategy(BaseStrategyFrame):
    """
    Implementing the kdj10 strategy from zwPython.

    Rule:
        If K value > 90: buy.
        If K value < 10: sell.

    Args:
        period_dfast (int): EMA period in D value.

    """

    params = (("period_dfast", 3),)

    def __init__(self):

        # multiple inheritance
        super(KdjV1Strategy, self).__init__()

        print("printlog:", self.params.printlog)
        print("period_dfast:", self.params.period_dfast)

        # Add indicators
        self.kd = bt.indicators.StochasticFast(
            self.datas[0],
            period=1,
            period_dfast=self.params.period_dfast,
            movav=bt.indicators.EMA,
            safediv=True,
        )

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log("Close, %.2f" % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.kd.percK[0] > 90:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log("BUY CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            if self.kd.percK[0] < 10:

                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log("SELL CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()


class KdjV2Strategy(BaseStrategyFrame):
    """
    Implementing the kdj10 strategy from zwPython.

    Rule:
        If K value > d value, and k value is upward: buy.
        If K value < d value, and k value is downward: sell.

    Args:
        period_dfast (int): EMA period in D value.

    """

    params = (("period_dfast", 3),)

    def __init__(self):

        # multiple inheritance
        super(KdjV2Strategy, self).__init__()

        print("printlog:", self.params.printlog)
        print("period_dfast:", self.params.period_dfast)

        # Add indicators
        self.kd = bt.indicators.StochasticFast(
            self.datas[0],
            period=1,
            period_dfast=self.params.period_dfast,
            movav=bt.indicators.EMA,
            safediv=True,
        )

        self.crossover = bt.indicators.CrossOver(self.kd.percK, self.kd.percD)

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log("Close, %.2f" % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.crossover[0] == 1:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log("BUY CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            if self.crossover[0] == -1:

                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log("SELL CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()


class RsiStrategy(BaseStrategyFrame):
    """
    Implementing the rsi10 strategy from zwPython.

    Rule:
        If rsi > kbuy: buy.
        If rsi < ksell: sell.

    Args:
        period (int): period for calucate rsi.
        kbuy (int): buy threshold for rsi value.
        ksell (int): sell threshold for rsi value.

    """

    params = (("period", 14), ("kbuy", 80), ("ksell", 20))

    def __init__(self):

        # multiple inheritance
        super(RsiStrategy, self).__init__()

        print("printlog:", self.params.printlog)
        print("period:", self.params.period)
        print("kbuy:", self.params.kbuy)
        print("ksell:", self.params.ksell)

        # Add indicators
        self.rsi = bt.indicators.RelativeStrengthIndex(
            self.dataclose,
            period=self.params.period,
            movav=bt.indicators.EMA,
            safediv=False,
        )

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log("Close, %.2f" % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.rsi[0] > self.params.kbuy:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log("BUY CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            if self.rsi[0] < self.params.ksell:

                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log("SELL CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
