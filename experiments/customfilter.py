from pyalgotrade import dataseries
from pyalgotrade import technical
from scipy import signal
import numpy as np

# An EventWindow is responsible for making calculations using a window of
# values.


class EMA(technical.EventWindow):

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

# Build a sequence based DataSeries.
seqDS = dataseries.SequenceDataSeries()
# Wrap it with a filter that will get fed as new values get added to the
# underlying DataSeries.
accum = technical.EventBasedFilter(seqDS, EMA(16))

# Put in some values.
for i in range(0, 50):
    seqDS.append(i)

# Get some values.
for i in xrange(50):
    print accum[i]
