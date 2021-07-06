# zwpy2bt

## Overview

Porting strategies from zwpython to Backtrader.
Original strategies are located in `zwStrategy.py` in zwpython.

**Strategy list:**

1. Tim0Strategy (tim0Trad)
2. SmaStrategy (SMA_sta)
3. CmaStrategy (CMA_sta)
4. VwapStrategy (VWAP_sta)
5. BBandsStrategy (BBANDS_sta)
6. TurStrategy (tur10)
7. MacdV1Strategy (macd10)
8. MacdV2Strategy (macd20)
9. KdjV1Strategy (kdj10)
10. KdjV2Strategy (kdj20)
11. RsiStrategy (rsi10)

## Prerequisites

- Python 2.7
- Python 3.2 / 3.3/ 3.4 / 3.5

Errors could occur in newer version python.

## Installation

**clone repo:**

```bash
git clone https://github.com/maglili/zwpy2bt.git
```

**install requirements:**

```bash
pip install backtrader[plotting]
```

## Run

```bash
python main.py
```

If you use 600401_yahoo.csv as sample data, then reverse parameter
in datafeed should be "True",
because 600401_yahoo.csv is decreased order.

```python
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2015, 1, 1),
        todate=datetime.datetime(2015, 12, 31),
        reverse=True,
    )
```

## Strategy Package

The **Strategy** package consists of 3 modules.

- BaseStrategyFrame
- utils
- zwpy_sta

```text
./stock-zwpython/
├── main.py
├── readme.md
├── result.png
├── sample_data
│   ├── 600401_yahoo.csv
│   ├── orcl-1995-2014.txt
│   └── readme.md
└── Strategy
    ├── BaseStrategyFrame.py
    ├── __init__.py
    ├── utils.py
    └── zwpy_sta.py

2 directories, 10 files
```

### Module Description

**BaseStrategyFrame:** Define the base structure of Strategy class,
BaseStrategyFrame is inheriting the `bt.Strategy` class,
and all strategies in `zwpy_sta.py` are
inheriting the `BaseStrategyFrame` class.

**utils:** Define class / function tools.

**zwpy_sta:** Define various strategies from zwpython.
Here, strategies are sub-class inherit from `BaseStrategyFrame`.
This can help user reduce code works because strategies
are now only need fewer code.

## Result Comparison

A Comparison experiment is conducted and the result (stocks value + balances) as shown on following table.

**Experiment setting:**

```text
Initial cash: 10000
Data: 600401_yahoo.csv
Backtest period: 2015, 1, 1 ~
Sizer: PercentSizerInt, percents=90
```

**Original result:**

|    Strategy    |   zwpython   |  backtrader  |
| :------------: | :----------: | :----------: |
|  Tim0Strategy  |   11158.60   |   11158.60   |
|  SmaStrategy   | **10892.66** | **11055.51** |
|  CmaStrategy   | **12860.46** | **13404.05** |
|  VwapStrategy  | **17102.59** | **16823.13** |
| BBandsStrategy |   9966.22    |   9966.22    |
|  TurStrategy   |   15193.05   |   15193.05   |
| MacdV1Strategy | **14405.99** | **15758.85** |
| MacdV2Strategy | **10557.62** | **11860.55** |
| KdjV1Strategy  | **18550.29** | **20098.48** |
| KdjV2Strategy  | **14807.79** | **16429.68** |
|  RsiStrategy   | **7808.42**  | **8995.14**  |

**After handing decimal place problem:**

Remove round process in backtest.

|    Strategy    |   zwpython   |  backtrader  |
| :------------: | :----------: | :----------: |
|  Tim0Strategy  |   11158.60   |   11158.60   |
|  SmaStrategy   |   10892.66   |   10892.66   |
|  CmaStrategy   |   12860.46   |   12860.46   |
|  VwapStrategy  | **17102.59** | **16823.13** |
| BBandsStrategy |   9966.22    |   9966.22    |
|  TurStrategy   |   15193.05   |   15193.05   |
| MacdV1Strategy | **14405.99** | **14301.22** |
| MacdV2Strategy |   10557.62   |   10557.62   |
| KdjV1Strategy  | **18550.29** | **20098.48** |
| KdjV2Strategy  | **14807.79** | **16429.68** |
|  RsiStrategy   | **7808.42**  | **8995.14**  |

**After handing formula problem:**

To correct the VWAP formula in zwpython.

|   Strategy   | zwpython | backtrader |
| :----------: | :------: | :--------: |
| VwapStrategy | 17102.59 |  17102.59  |

>There are some bugs in zwpython
>and I already fixed some of them,
>so you might not have a same result as the table above.

### Why still a difference b/t bt and zwpy?

The difference comes from decimal place problem
in technical index calculation (e.g. VWAP, MACD, KDJ,...),
say RSI = 93.700 vs RSI = 96.849, will have different decision in strategy.
That merely a order difference b/t a day can cause a big different result,
the problem cannot solve by merely remove rounding  process
that in backtest in zwpython.

### Which one is more accurate?

The result of backtrader might more accurate since it still maintaining
by github community (6.6k star).
Technical index in Backtrader are calculated by bt.indicator or TA-lib package,
which offer a reliable result,
while in zwpython, Technical index are calculated by functions
that created by creator of zwpython, there might exist some bugs
(and there are indeed some bugs in some scripts in zwpython).
