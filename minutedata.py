import requests
import pandas as pd
from io import StringIO
import numpy as np
import arrow


def minutestockdata(ticker, days):
    """Given a ticker symbol and a number of days, returns a pandas
    DataFrame of minute-by-minute data indexed by timestamps

    Args:
        ticker (str): Ticker symbol (e.g. 'JCI')
        days (int): Days of data to fetch. Maximum value: 14.

    Returns:
        DataFrame: Pandas DataFrame with columns of
            'DATE', 'CLOSE', 'HIGH', 'LOW', 'OPEN', 'VOLUME'

    """
    link = 'http://www.google.com/finance/getprices?i=60&p=%dd&f=d,o,h,l,c,v&df=cpct&q=%s' % (days, ticker)
    res = requests.get(link)
    stin = res.text
    colheaders = stin[stin.index('COLUMNS')+8:stin.index('\nDATA')+1]
    csvstart = stin.index('\na') + 1
    csv = stin[csvstart:]
    in_data = StringIO()
    in_data.write(colheaders)
    in_data.write(csv)
    in_data.seek(0)
    # print in_data.getvalue()
    df = pd.read_csv(in_data, encoding='utf8')
    in_data.close()
    datetms = []
    daysc = 0
    for i in xrange(len(df)):
        this_date = df.iloc[i].DATE
        if this_date[0] == 'a':
            startdt = arrow.get(this_date[1:]).to('US/Eastern')
            datetms.append(startdt.timestamp)
            daysc += 1
        elif int(this_date) <= 390:
            intthisdate = int(this_date)
            hours = intthisdate / 60
            minutes = intthisdate % 60
            # addtime = arrow.get('%d:%d' % (hours, minutes), 'h:m')
            newdt = startdt.replace(hours=+ hours, minutes=+minutes)
            datetms.append(newdt.to('US/Eastern').timestamp)
        else:
            print 'ERROR'
    print daysc
    df.drop('DATE', axis=1)
    pdts =  pd.to_datetime(datetms, unit='s').tz_localize('UTC').tz_convert('US/Eastern')  # pandas timestamps
    df['DATE'] = pd.Series(pdts)
    dft = df.set_index('DATE')
    # dft.index.tz_localize('UTC').tz_convert('US/Eastern')
    return dft

def main(companies):
    companieslist = companies.Symbol.tolist()
    for company in companieslist:
        print company
        try:
            df = minutestockdata(company, 14)
        except:
            print 'ERROR'
        else:
            df.to_csv('./data/historical/minute/%s.csv' % company)

if __name__ == '__main__':
    from finance.data.exchanges import master
    companies = master()
    main(companies)
