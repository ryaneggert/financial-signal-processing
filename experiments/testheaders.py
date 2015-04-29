import requests
import string

days = 1
ticker = 'AAPL'

for letter in string.ascii_lowercase:
    link = 'http://www.google.com/finance/getprices?i=60&p=%dd&f=d,%s&df=cpct&q=%s' % (
        days, letter, ticker)
    res = requests.get(link)
    stin = res.text
    colheaders = stin[stin.index('COLUMNS') + 8:stin.index('\nDATA') + 1]
    print letter, colheaders[:-1]