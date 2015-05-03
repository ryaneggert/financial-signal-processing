import itertools
import arrow
from numpy import arange
from pyalgotrade.optimizer import local
import strategies
import data_handling as daq


def time_estimator(parameters):
    time_per_run = 10
    no_of_runs = len(list(parameters))
    print list(parameters)
    est_dur = time_per_run * no_of_runs
    nowtime = arrow.utcnow().to('US/Eastern')
    est_end = nowtime.replace(seconds=+est_dur)
    print 'We estimate that the optimization will be complete %s. [%s]' % (
        est_end.humanize(), est_end.format('h:mm A, MMM D, YYYY'))


def EMACrossoverParams(instruments):
    instruments = [instruments]
    cash = [100000]
    ema_len = range(1, 90, 5)
    ema_alpha = arange(0, 1, .1).tolist()
    commission_scheme = [('TradePercentage', .01), ('FixedPerTrade', 10)]
    outparams = itertools.product(
        instruments, cash, ema_len, ema_alpha, commission_scheme)
    time_estimator(outparams)
    return itertools.product(
        instruments, cash, ema_len, ema_alpha, commission_scheme)


def parameters_generator():
    instrument = ["dia"]
    entrySMA = range(150, 251)
    exitSMA = range(5, 16)
    rsiPeriod = range(2, 11)
    overBoughtThreshold = range(75, 96)
    overSoldThreshold = range(5, 26)
    return itertools.product(instrument, entrySMA, exitSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold)


# The if __name__ == '__main__' part is necessary if running on Windows.
if __name__ == '__main__':
    instruments = ['JCI', 'AAPL', 'YUM', 'ABC']
    # Load the feed from the CSV files.
    feed = daq.build_stock_feed(instruments, (2010, 2015))

    local.run(strategies.EMACrossover, feed,
              EMACrossoverParams(instruments), workerCount=4)
