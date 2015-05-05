# trading.py
from pyalgotrade import plotter
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.utils import stats
from pyalgotrade.broker import backtesting
from random import sample, choice

import strategies as sgs
import data_handling as daq


def main(printinfo=True):
    firstyear = 2010
    lastyear = 2015
    num_instr = 20
    posinstruments = daq.find_instruments_by_year(firstyear)
    instruments = sample(posinstruments, num_instr)
    print instruments
    feed = daq.build_stock_feed(instruments, [firstyear, lastyear])
    this_Strategy = sgs.SLTRIXCrossover(
        feed, instruments, 100000, 12, 27, .53, .4, printinfo=printinfo)
    retAnalyzer = returns.Returns()
    this_Strategy.attachAnalyzer(retAnalyzer)
    # this_Strategy.getBroker().setCommission(
    # backtesting.TradePercentage(.01))  # 1.% commission per trade
    this_Strategy.getBroker().setCommission(
        backtesting.FixedPerTrade(10))  # $10 commission per trade

    # Attach plotters
    # Attach the plotter to the strategy.
    plt = plotter.StrategyPlotter(this_Strategy)
    # Include the SMA in the instrument's subplot to get it displayed along
    # with the closing prices.
    for pltinstr in instruments:
        plt.getInstrumentSubplot(pltinstr).addDataSeries(
            "Short TRIX", this_Strategy.getshorttrix(pltinstr))
        plt.getInstrumentSubplot(pltinstr).addDataSeries(
            "Long TRIX", this_Strategy.getlongtrix(pltinstr))
    # Plot the simple returns on each bar.
    plt.getOrCreateSubplot("returns").addDataSeries(
        "Simple returns", retAnalyzer.getReturns())
    # Run the strategy
    this_Strategy.run()

    # Print the results.
    print "Final portfolio value: $%.2f" % this_Strategy.getResult()
    print "Annual return: %.2f %%" % ((retAnalyzer.getCumulativeReturns()[-1] * 100)/float(lastyear - firstyear))
    print "Average daily return: %.2f %%" % (stats.mean(retAnalyzer.getReturns()) * 100)
    print "Std. dev. daily return: %.4f" % (stats.stddev(retAnalyzer.getReturns()))

    return this_Strategy.getResult()
    # plt.plot()

if __name__ == '__main__':
    resultsout = []
    for i in xrange(50):
        print i
        resultsout.append(main(printinfo=False))
    print resultsout
    # build_complete_dataset(['AAPL', 'FMTW', 'ALK', 'FMTW', 'AMG', 'FMTW', 'AMZN', 'FMTW', 'BWLD', 'FMTW', 'CLDN', 'FMTW', 'CMG',
    # 'FMTW', 'CMI', 'FMTW', 'GLW', 'FMTW', 'JCI', 'FMTW', 'OLN', 'FMTW', 'ROK', 'FMTW', 'TSLA', 'FMTW', 'UJPSX', 'VFINX'])
