from scipy import signal
import numpy as np
from matplotlib import pyplot as plt
from pandas import read_csv

exclude_transients = True


def movingaveragefilter(data, flen):
    b = np.asarray([1] * flen).astype(np.float64)
    a = np.asarray([flen]).astype(np.float64)
    out = signal.lfilter(b, a, data)
    return out


def WMAfilter(data, flen, weight):
    bcoeffs = []
    for i in xrange(flen):
        bcoeffs.append(weight - i)
    b = np.asarray(bcoeffs).astype(np.float64)
    a = np.asarray([sum(bcoeffs)]).astype(np.float64)
    out = signal.lfilter(b, a, data)
    return out


def EMAfilter(data, flen, alpha):
    bcoeffs = []
    for i in xrange(flen):
        bcoeffs.append((1 - alpha) ** i)
    b = np.asarray(bcoeffs).astype(np.float64)
    a = np.asarray([sum(bcoeffs)]).astype(np.float64)
    out = signal.lfilter(b, a, data)
    return out


def TRIXfilter(data, flen, alpha):
    out1 = EMAfilter(data, flen, alpha)
    out2 = EMAfilter(out1, flen, alpha)
    out3 = EMAfilter(out2, flen, alpha)
    return out3


def MMAfilter(data, flen):
    # MMA(16) = WMA(8) + [ WMA(8) - WMA(16) ] = 2 WMA(8) - WMA(16).
    wmah = WMAfilter(data, flen / 2, flen / 2)
    wmaf = WMAfilter(data, flen, flen)
    mma = 2 * wmah - wmaf
    return mma

def HMAfilter(data, flen):
    """ Hull Moving Average
    http://www.financialwisdomforum.org/gummy-stuff/MA-stuff.htm
    """
    mma = MMAfilter(data, flen**2)
    hull = WMAfilter(data, flen, flen)
    return hull

df = read_csv('../data/historical/minute/AAPL.csv')

x = df['CLOSE'].tolist()[4000:5300]
length = len(x)
n = range(length)
# x = [randint(0, 10) for size in n]
filtlen = 30
maout = movingaveragefilter(x, filtlen)
wmaout = WMAfilter(x, filtlen, filtlen + 1)
emaout = EMAfilter(x, filtlen, .25)
trixout = TRIXfilter(x, filtlen, .5)
mmaout = MMAfilter(x, 16)
hmaout = HMAfilter(x, 15)

if exclude_transients:
    plt.plot(n[filtlen:], x[filtlen:], '-', label="Stock Data")
    plt.plot(n[filtlen:], maout[filtlen:], label="Moving Average")
    plt.plot(n[filtlen:], wmaout[filtlen:], label="Weighted Moving Average")
    plt.plot(n[filtlen:], emaout[filtlen:], label="Exponential Moving Average")
    plt.plot(n[filtlen:], trixout[filtlen:], label="Triple EMA")
    plt.plot(n[filtlen:], mmaout[filtlen:], label="MMA")
    plt.plot(n[filtlen:], hmaout[filtlen:], label="Hull")
else:
    plt.plot(n, x, '-', label="Stock Data")
    plt.plot(n, maout, label="Moving Average")
    plt.plot(n, wmaout, label="Weighted Moving Average")
    plt.plot(n, emaout, label="Exponential Moving Average")
    plt.plot(n, trixout, label="Triple EMA")
    plt.plot(n, mmaout, label="MMA")
    plt.plot(n, hmaout, label="Hull")
plt.legend()
plt.show()
