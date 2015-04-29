from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.utils import stats
from pyalgotrade.broker import backtesting

from pyalgotrade.tools import yahoofinance

yahoofinance.download_daily_bars('aeti', 2009, 'aeti-2009-yahoofinance.csv')
yahoofinance.download_daily_bars('egan', 2009, 'egan-2009-yahoofinance.csv')
yahoofinance.download_daily_bars('glng', 2009, 'glng-2009-yahoofinance.csv')
yahoofinance.download_daily_bars('simo', 2009, 'simo-2009-yahoofinance.csv')


class MyStrategy(strategy.BacktestingStrategy):

    def __init__(self, feed):
        strategy.BacktestingStrategy.__init__(self, feed, 100000)

        # We wan't to use adjusted close prices instead of close.
        self.setUseAdjustedValues(True)

        # Place the orders to get them processed on the first bar.
        orders = {
            "egan": 1000,
        }
        for instrument, quantity in orders.items():
            self.marketOrder(
                instrument, quantity, onClose=True, allOrNone=True)

    def onBars(self, bars):
        for instrument, bar in bars.items():
            print instrument, bar.getVolume()

# Load the yahoo feed from CSV files.
feed = yahoofeed.Feed()
feed.addBarsFromCSV("aeti", "aeti-2009-yahoofinance.csv")
feed.addBarsFromCSV("egan", "egan-2009-yahoofinance.csv")
feed.addBarsFromCSV("glng", "glng-2009-yahoofinance.csv")
feed.addBarsFromCSV("simo", "simo-2009-yahoofinance.csv")

# Evaluate the strategy with the feed's bars.
myStrategy = MyStrategy(feed)

# Set commission
# https://github.com/gbeced/pyalgotrade/blob/master/testcases/sharpe_analyzer_test.py
myStrategy.getBroker().setCommission(backtesting.FixedPerTrade(10))  # $10 commission per trade
myStrategy.getBroker().setCommission(backtesting.TradePercentage(.10))  # 10.% commission per trade

# Attach returns and sharpe ratio analyzers.
retAnalyzer = returns.Returns()
myStrategy.attachAnalyzer(retAnalyzer)
sharpeRatioAnalyzer = sharpe.SharpeRatio()
myStrategy.attachAnalyzer(sharpeRatioAnalyzer)


# Run the strategy
myStrategy.run()

# Print the results.
print "Final portfolio value: $%.2f" % myStrategy.getResult()
print "Anual return: %.2f %%" % (retAnalyzer.getCumulativeReturns()[-1] * 100)
print "Average daily return: %.2f %%" % (stats.mean(retAnalyzer.getReturns()) * 100)
print "Std. dev. daily return: %.4f" % (stats.stddev(retAnalyzer.getReturns()))
print "Sharpe ratio: %.2f" % (sharpeRatioAnalyzer.getSharpeRatio(0))
