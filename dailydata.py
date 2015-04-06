# dailydata.py
import pandas.io.data as web
import arrow
import datetime

import matplotlib.pyplot as plt

start = datetime.datetime(1995, 1, 1)
end = datetime.datetime(2013, 1, 27)

f=web.DataReader("F", 'yahoo', start, end)
f.plot()
plt.show()
