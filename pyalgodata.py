from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.tools import yahoofinance
from pyalgotrade.technical import ma
from pyalgotrade.technical import rsi
from pyalgotrade import dataseries
from pyalgotrade import technical

import technicalfilters as tf


feed = yahoofinance.build_feed(
    ['GE', 'JCI', 'AAPL', 'ADI'], 2000, 2015, './data/historical/daily-atrader', frequency=86400, skipErrors=False)


class MyStrategy(strategy.BacktestingStrategy):

    def __init__(self, feed, instrument, cash):
        strategy.BacktestingStrategy.__init__(self, feed, cash)
        self.__rsi = rsi.RSI(feed[instrument].getCloseDataSeries(), 14)
        self.__sma = ma.SMA(self.__rsi, 15)
        self.__instrument = instrument
        self.__EMA = tf.EMA(feed[instrument].getCloseDataSeries(), 16, .3)
        self.__DT = tf.Derivative(feed[instrument])

    def onBars(self, bars):

        bar = bars[self.__instrument]
        self.info("%s %s %s %s" %
                  (bar.getClose(), self.__rsi[-1], self.__sma[-1], self.__EMA[-1]))

# Load the yahoo feed from the CSV file
# feed = yahoofeed.Feed()
# feed.addBarsFromCSV("orcl", "orcl-2000.csv")

# Evaluate the strategy with the feed's bars.
myStrategy = MyStrategy(feed, 'GE', 200)
myStrategy.run()
