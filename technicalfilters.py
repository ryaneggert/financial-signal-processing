import numpy as np
from pyalgotrade import technical
from pyalgotrade import dataseries

from scipy import signal


class EMAEventWindow(technical.EventWindow):

    def __init__(self, flen):
        technical.EventWindow.__init__(self, flen)

    def EMAfilter(self, data, flen, alpha):
        bcoeffs = []
        for i in xrange(flen):
            bcoeffs.append((1 - alpha) ** i)
        b = np.asarray(bcoeffs).astype(np.float64)
        a = np.asarray([sum(bcoeffs)]).astype(np.float64)
        out = signal.lfilter(b, a, data)
        return out

    def getValue(self):
        ret = None
        if self.windowFull():
            these_vals = self.getValues()
            filt = self.EMAfilter(these_vals, self.getWindowSize(), .5)
            ret = filt[-1]
        return ret


class EMA(technical.EventBasedFilter):

    """Exponential Moving Average filter.
    """

    def __init__(self, dataSeries, flen, maxLen=dataseries.DEFAULT_MAX_LEN):
        technical.EventBasedFilter.__init__(
            self, dataSeries, EMAEventWindow(flen), maxLen)
