import numpy as np
from pyalgotrade import technical
from pyalgotrade import dataseries

from scipy import signal


class EMAEventWindow(technical.EventWindow):

    def __init__(self, flen, alpha):
        technical.EventWindow.__init__(self, flen)
        self.__alpha = alpha

    def EMAfilter(self, data, flen):
        bcoeffs = []
        for i in xrange(flen):
            bcoeffs.append((1 - self.__alpha) ** i)
        b = np.asarray(bcoeffs).astype(np.float64)
        a = np.asarray([sum(bcoeffs)]).astype(np.float64)
        out = signal.lfilter(b, a, data)
        return out

    def getValue(self):
        ret = None
        if self.windowFull():
            these_vals = self.getValues()
            filt = self.EMAfilter(these_vals, self.getWindowSize())
            ret = filt[-1]
        return ret


class EMA(technical.EventBasedFilter):

    """Exponential Moving Average filter.
    """

    def __init__(self, dataSeries, flen, alpha, maxLen=dataseries.DEFAULT_MAX_LEN):
        technical.EventBasedFilter.__init__(
            self, dataSeries, EMAEventWindow(flen, alpha), maxLen)


class DerivativeEventWindow(technical.EventWindow):

    def __init__(self):
        technical.EventWindow.__init__(self, 2)

    def Derivativefilter(self, data):
        bcoeffs = [1, -1]
        b = np.asarray(bcoeffs).astype(np.float64)
        a = np.asarray([1]).astype(np.float64)
        out = signal.lfilter(b, a, data)
        return out

    def getValue(self):
        ret = None
        if self.windowFull():
            these_vals = self.getValues()
            filt = self.Derivativefilter(these_vals)
            ret = filt[-1]
        return ret


class Derivative(technical.EventBasedFilter):

    """Exponential Moving Average filter.
    """

    def __init__(self, dataSeries, maxLen=dataseries.DEFAULT_MAX_LEN):
        technical.EventBasedFilter.__init__(
            self, dataSeries, DerivativeEventWindow(), maxLen)
