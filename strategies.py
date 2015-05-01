# strategies.py

from pyalgotrade import strategy
from pyalgotrade import dataseries
from pyalgotrade.technical import ma
import technicalfilters as tf
from pyalgotrade.technical import cross


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

        # Create dataseries of zeroes

        self.zeroseq = dataseries.SequenceDataSeries()

        # Initialize indicators for each instrument.
        self.__closes = {}
        self.__ema = {}
        self.__dt = {}
        self.__zeroseries = {}
        self.__zeroema = {}

        for instrument in instruments:
            self.__closes[instrument] = feed[instrument].getPriceDataSeries()
            self.__ema[instrument] = tf.EMA(
                self.__closes[instrument], 10, .005)
            self.__dt[instrument] = tf.Derivative(self.__ema[instrument])
            self.__zeroseries[instrument] = tf.ZeroSeries(
                self.__closes[instrument])
            self.__zeroema[instrument] = ma.EMA(
                self.__zeroseries[instrument], 3)

    def inventory(self, instrument):
        broker = self.getBroker()
        return (broker.getCash(), broker.getShares(instrument))

    def buyamount(self, instrument, price, volume, cash, cashpct):
        full = cash / price
        buyqty = full * cashpct
        if buyqty < 1:
            self.warning('Insufficient cash to buy %s.' % instrument)
        if buyqty > volume:
            self.warning('Coercing volume of %s.' % instrument)
            buyqty = max(volume - 1, 0)
        return buyqty

    def getEMA(self, instrument):
        return self.__ema[instrument]

    def onBars(self, bars):
        for instrument, bar in bars.items():
            if cross.cross_above(self.__dt[instrument], self.__zeroema[instrument]) > 0:
                # If the derivative crosses above zero (deriv - -> +),
                # buy the instrument.
                now_cash, now_shares = self.inventory(instrument)
                buyqty = self.buyamount(
                    instrument, bar.getClose(), bar.getVolume(), now_cash, .2)
                self.marketOrder(instrument, buyqty)
                self.info('Order %d shares of %s @$%.2f. COH $%.2f' %
                          (buyqty, instrument, bar.getClose(), now_cash))

            elif cross.cross_below(self.__dt[instrument], self.__zeroema[instrument]) > 0:
                # If the derivative crosses below zero (deriv + -> -),
                # sell the instrument.
                now_cash, now_shares = self.inventory(instrument)
                if now_shares > 0:
                    # Sell all shares
                    self.marketOrder(instrument, -now_shares)
                    self.info('Sell %d shares of %s @$%.2f. COH $%.2f' %
                              (now_shares, instrument, bar.getClose(), now_cash))
            # self.info("%s %s %s %s" %
            #           (
            #               bar.getClose(),
            #               self.__dt[instrument][-2:],
            #               self.__zeroema[instrument][-2:],
            #               cross.cross_above(self.__dt[instrument], self.__zeroema[instrument]))
            #           )
