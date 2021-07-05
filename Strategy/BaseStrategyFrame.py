import backtrader as bt


class BaseStrategyFrame(bt.Strategy):
    """
    Define base Strategy class (main structure),
    so the class structure could remain consistent.

    All Strategy inherit this class.

    Args:
        doprint (int): Whather to print message.
    """

    params = (("printlog", False),)

    def log(self, txt, dt=None, doprint=False):
        """Logging function fot this strategy"""
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print("%s, %s" % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataopen = self.datas[0].open
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    "BUY EXECUTED, Price: %.2f, Size: %.2f, Cost: %.2f, Comm %.2f, Cash %.2f"
                    % (
                        order.executed.price,
                        order.executed.size,
                        order.executed.value,
                        order.executed.comm,
                        self.broker.getcash(),
                    )
                )

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log(
                    "SELL EXECUTED, Price: %.2f, Size: %.2f, Cost: %.2f, Comm %.2f, Cash %.2f"
                    % (
                        order.executed.price,
                        order.executed.size,
                        order.executed.value,
                        order.executed.comm,
                        self.broker.getcash(),
                    )
                )

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled/Margin/Rejected")

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log("OPERATION PROFIT, GROSS %.2f, NET %.2f" % (trade.pnl, trade.pnlcomm))

    def start(self):
        # self.log('Ending Value %.2f' % self.broker.getvalue(), doprint=True)
        print("=== Backtesting Start! ===")

    def stop(self):
        # self.log('Ending Value %.2f' % self.broker.getvalue(), doprint=True)
        print("=== Backtesting Finished! ===")
