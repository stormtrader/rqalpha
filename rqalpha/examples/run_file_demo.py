# -*- coding: utf-8 -*-

from rqalpha import run_file

config = {
  "base": {
    "start_date": "2017-08-14",
    "end_date": "2018-01-05",
    "benchmark": "000300.XSHG",
    "accounts": {
      "stock": 100000
    }
  },
  "extra": {
    "log_level": "verbose",
  },
  "mod": {
    "sys_analyser": {
      "enabled": True,
      "plot": True
    }
  }
}

#strategy_file_path = "./golden_cross.py"
strategy_file_path = "./sma_triger.py"
run_file(strategy_file_path, config)
