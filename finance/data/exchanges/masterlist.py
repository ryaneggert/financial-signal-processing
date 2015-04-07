import pandas as pd


def importmasterlist():
    return pd.read_csv('./data/companies/master.csv')


def importnyse():
    return pd.read_csv('./data/companies/nyse.csv')


def importnasdaq():
    return pd.read_csv('./data/companies/nasdaq.csv')


def importamex():
    return pd.read_csv('./data/companies/amex.csv')


def generatemasterlist():
    """Data from http://www.nasdaq.com/screening/company-list.aspx.
    Imports the modified data (added exchange column, replaced 'n/a' with "nan")"""

    exchanges = ['nyse', 'nasdaq', 'amex']
    for i, exchange in enumerate(exchanges):
        if i == 0:
            combine = pd.read_csv('./data/companies/%s.csv' % exchange)
        else:
            combine = combine.merge(
                pd.read_csv('./data/companies/%s.csv' % exchange), how='outer')
    # Save as CSV
    combine.to_csv('./data/companies/master.csv')

if __name__ == '__main__':
    importmasterlist()
