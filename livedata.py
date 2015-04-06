# livedata.py
import pandas.io.data as web
import arrow
import datetime


start = datetime.datetime(2010, 1, 1)
end = datetime.datetime(2013, 1, 27)

f=web.DataReader("F", 'yahoo', start, end)
print f
