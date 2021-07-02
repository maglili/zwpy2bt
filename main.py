import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt
from Strategy.zwpy_sta import *
import matplotlib.pyplot as plt


if __name__ == "__main__":
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    # cerebro.addstrategy(SmaStrategy, maperiod=20, printlog=True)
    # cerebro.addstrategy(CmaStrategy, maperiod=20, printlog=True)
    #cerebro.addstrategy(VwapStrategy, maperiod=20, kvwap=0.01, printlog=True)
    cerebro.addstrategy(BBandsStrategy, BBandsperiod=20, printlog=True)

    # path to data
    datapath = "./sample_data/orcl-1995-2014.txt"

    # Create a Data Feed
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        # Do not pass values before this date
        fromdate=datetime.datetime(2000, 1, 1),
        # Do not pass values before this date
        todate=datetime.datetime(2000, 12, 31),
        # Do not pass values after this date
        reverse=False,
    )

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(1000)

    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    # Set the commission
    cerebro.broker.setcommission(commission=0.1425 / 100)

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
