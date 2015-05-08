import itertools
import arrow
from numpy import arange
from pyalgotrade.optimizer import local
import strategies
import data_handling as daq


def time_estimator(parameters):
    time_per_run = 9.7
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
    ema_len = range(25, 35, 1)
    ema_alpha = arange(.8, 1, .01).tolist()
    commission_scheme = [('FixedPerTrade', 10)]
    outparams = itertools.product(
        instruments, cash, ema_len, ema_alpha, commission_scheme)
    time_estimator(outparams)
    return itertools.product(
        instruments, cash, ema_len, ema_alpha, commission_scheme)



def SLTRIXCrossoverParams(instruments):
    instruments = [instruments]
    cash = [100000]
    shortlen = range(3, 7, 1)
    longlen = range(9, 15, 1)
    a1 = arange(.1,.3, .02 )
    a3 = arange(.3,.5, .02 )
    outparams = itertools.product(
        instruments, cash, shortlen, longlen, a1, a3)
    time_estimator(outparams)
    return itertools.product(
       instruments, cash, shortlen, longlen, a1, a3)

# feed, instruments, cash, shortlen, longlen, sha1, sha2, sha3, la1, la2, la3)

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
    instruments = ['JCI']
    # Load the feed from the CSV files.
    feed = daq.build_stock_feed(instruments, (2006, 2011))

    # local.run(strategies.EMACrossover, feed,
    #           EMACrossoverParams(instruments), workerCount=None)

    local.run(strategies.SLTRIXCrossover, feed,
              SLTRIXCrossoverParams(instruments), workerCount=None)