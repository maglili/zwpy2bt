import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt
from Strategy.zwpy_sta import *
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = (30, 18)


if __name__ == "__main__":
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    # cerebro.addstrategy(Tim0Strategy, printlog=True)
    # cerebro.addstrategy(SmaStrategy, maperiod=15, printlog=True)
    # cerebro.addstrategy(CmaStrategy, maperiod=20, printlog=True)
    # cerebro.addstrategy(VwapStrategy, maperiod=5, kvwap=0.01, printlog=True)
    # cerebro.addstrategy(BBandsStrategy, BBandsperiod=40, printlog=True)
    # cerebro.addstrategy(TurStrategy, n_high=5, n_low=5, printlog=True)
    # cerebro.addstrategy(MacdV1Strategy, fast_period=12,
    #                     slow_period=26, signal_period=9, printlog=True)
    # cerebro.addstrategy(MacdV2Strategy, fast_period=12,
    #                     slow_period=26, signal_period=9, printlog=True)
    # cerebro.addstrategy(KdjV1Strategy, period_dfast=9, printlog=True)
    # cerebro.addstrategy(KdjV2Strategy, period_dfast=9, printlog=True)
    cerebro.addstrategy(RsiStrategy, period=14, kbuy=70, ksell=30, printlog=True)

    # path to data
    # datapath = "./sample_data/orcl-1995-2014.txt"
    datapath = "./sample_data/600401_yahoo.csv"

    # =====for 600401_yahoo.csv=====
    # Create a Data Feed
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        # Do not pass values before this date
        # fromdate=datetime.datetime(2000, 1, 1),
        fromdate=datetime.datetime(2015, 1, 1),
        # Do not pass values before this date
        # todate=datetime.datetime(2000, 12, 31),
        # Do not pass values after this date
        reverse=True,
    )

    # =====for orcl-1995-2014.txt=====
    # data2 = bt.feeds.YahooFinanceCSVData(
    #     dataname=datapath,
    #     # Do not pass values before this date
    #     fromdate=datetime.datetime(2000, 1, 1),
    #     # Do not pass values before this date
    #     todate=datetime.datetime(2000, 12, 31),
    #     # Do not pass values after this date
    #     reverse=False,
    # )

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)
    # cerebro.adddata(data2)

    # Set our desired cash start
    cerebro.broker.setcash(10000)

    # Add a FixedSize sizer according to the stake
    # cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.addsizer(bt.sizers.PercentSizerInt, percents=90)
    # cerebro.addsizer(bt.sizers.AllInSizerInt)

    # Set the commission
    cerebro.broker.setcommission(commission=0)  # .1425 / 100)

    # Print out the starting conditions
    print("Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())

    # Plot the result
    cerebro.plot()

    # save the plot
    plt.savefig("./result.png", bbox_inches="tight")
