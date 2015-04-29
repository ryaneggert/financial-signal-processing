# companyyears.py


while inbusiness:
    try:
        yahoofinance.build_feed(
            ['GE'], 1962, 2015, './data/historical/daily-atrader', frequency=86400, skipErrors=False)
    except Exception, e:
        raise e
    else:
        pass

