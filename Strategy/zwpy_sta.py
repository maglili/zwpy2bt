import backtrader as bt
from Strategy.BaseStrategyFrame import BaseStrategyFrame
from Strategy.utils import VolumeWeightedAveragePrice


class SmaStrategy(BaseStrategyFrame):
    """
    Implementing SMA strategy in zwPython.

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

        # Add a MovingAverageSimple indicator
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod
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
    Implementing CMA strategy in zwPython.

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

        # Add a MovingAverageSimple indicator
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod
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
    Implementing VWAP strategy in zwPython.

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

        # Add a MovingAverageSimple indicator
        self.vwap = VolumeWeightedAveragePrice(
            self.datas[0], period=self.params.maperiod
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
    Implementing BBands strategy in zwPython.

    Rule:

    Args:
        BBandsperiod (int): ma period

    """

    params = (('BBandsperiod', 20),)

    def __init__(self):

        # multiple inheritance
        super(BBandsStrategy, self).__init__()

        print("printlog:", self.params.printlog)
        print("BBandsperiod:", self.params.BBandsperiod)

        # Add a MovingAverageSimple indicator
        self.bband = bt.indicators.BBands(
            self.datas[0], period=self.params.BBandsperiod)

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
