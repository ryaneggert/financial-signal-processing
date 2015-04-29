# strategies.py

from pyalgotrade import strategy
import technicalfilters as tf


class EMACrossover(strategy.BacktestingStrategy):

    def __init__(self, feed, instruments, cash):
        strategy.BacktestingStrategy.__init__(self, feed, cash)

        # We wan't to use adjusted close prices instead of close.
        self.setUseAdjustedValues(True)

        # Place the orders to get them processed on the first bar.
        # orders = {
        #     "egan": 1000,
        # }
        # for instrument, quantity in orders.items():
        #     self.marketOrder(
        #         instrument, quantity, onClose=True, allOrNone=True)

        # Initialize indicators for each instrument.
        self.__ema = {}
        self.__dt = {}
        for instrument in instruments:
            priceDS = feed[instrument].getPriceDataSeries()
            self.__ema[instrument] = tf.EMA(priceDS, 15, .5)
            self.__dt[instrument] = tf.Derivative(self.__ema[instrument])

    def onBars(self, bars):
        for instrument, bar in bars.items():
            self.info("%s %s %s" %
                      (bar.getClose(), self.__ema[instrument][-1], self.__dt[instrument][-1]))
