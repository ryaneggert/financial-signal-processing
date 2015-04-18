import pandas as pd
from os import listdir
from os.path import isfile, join


def importmasterlist():
    return pd.read_csv('./data/companies/master.csv', index_col="indx")


def importnyse():
    return pd.read_csv('./data/companies/nyse`.csv', index_col="indx")


def importnasdaq():
    return pd.read_csv('./data/companies/nasdaq`.csv', index_col="indx")


def importamex():
    return pd.read_csv('./data/companies/amex`.csv', index_col="indx")


def addindxlabel():
    exchanges = ['nyse', 'nasdaq', 'amex']
    for exchange in exchanges:
        df = pd.read_csv('./data/companies/%s.csv' % exchange)
        df.index.name = 'indx'
        df.to_csv('./data/companies/%s.csv' % exchange)


def generatemasterlist():
    """Data from http://www.nasdaq.com/screening/company-list.aspx.
    Imports the modified data (added exchange column, replaced 'n/a' with "nan")"""

    exchanges = ['nyse', 'nasdaq', 'amex']
    for i, exchange in enumerate(exchanges):
        if i == 0:
            combine = pd.read_csv(
                './data/companies/%s.csv' % exchange, index_col="indx")
        else:
            combine = combine.merge(
                pd.read_csv('./data/companies/%s.csv' % exchange, index_col="indx"), how='outer')
    # Save as CSV
    combine.index.name = 'indx'
    combine.to_csv('./data/companies/master.csv')


def addminbool():
    mypath = './data/historical/minute/'
    minutedata = [f[:-4] for f in listdir(mypath) if isfile(join(mypath, f))]

    exchanges = ['nyse', 'nasdaq', 'amex', 'master']
    for exchange in exchanges:
        if exchange == 'master':
            df = pd.read_csv('./data/companies/master.csv', index_col="indx")
            writename = 'master'
        else:
            df = pd.read_csv('./data/companies/%s.csv' %
                             exchange, index_col="indx")
            writename = exchange + '`'

        df['minutedata'] = df['Symbol'].isin(minutedata)
        df.to_csv('./data/companies/%s.csv' % writename)


if __name__ == '__main__':
    pass
