# zwpy2bt

## Overview

Porting strategies from zwpython to Backtrader.
Original strategies are located in `zwStrategy.py` in zwpython.

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

## Strategy

The **Strategy** package consists of 3 modules.

- BaseStrategyFrame
- utils
- zwpy_sta

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
