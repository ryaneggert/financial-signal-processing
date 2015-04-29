# trading.py

from pyalgotrade.tools import yahoofinance
from pyalgotrade.stratanalyzer import returns


from datetime import date
import pandas as pd

import strategies as sgs


def log_business_years(instrument, years):
    df = pd.read_csv(
        './data/historical/daily_company_years.csv', index_col='instrument')
    df.loc[instrument] = years
    df = df.sort(['first-year'], ascending=False)
    df.to_csv(
        './data/historical/daily_company_years.csv', index_label='instrument')


def acquire_daily_data(instrument, year):
    if year == 'all':
        this_year = date.today().year  # Get current year
        final_year = this_year
        in_business = True
        while in_business:
            try:
                yahoofinance.build_feed(
                    [instrument], this_year, this_year,
                    './data/historical/daily-atrader',
                    frequency=86400, skipErrors=False)
            except:
                in_business = False
                log_business_years(instrument, [this_year + 1, final_year])
            else:
                this_year -= 1
    else:
        yahoofinance.build_feed([instrument], year[0], year[1],
                                './data/historical/daily-atrader',
                                frequency=86400, skipErrors=False)


def build_complete_dataset(instruments):
    for instrument in instruments:
        acquire_daily_data(instrument, 'all')


def build_stock_feed(instruments, years):
    return yahoofinance.build_feed(instruments, years[0], years[1],
                                   './data/historical/daily-atrader',
                                   frequency=86400, skipErrors=False)


def find_instruments_by_year(start_year):
    df = pd.read_csv(
        './data/historical/daily_company_years.csv', index_col='instrument')
    existing_companies = df[df['first-year'] < start_year]
    return existing_companies.index.values.tolist()


def main():
    firstyear = 2012
    instruments = find_instruments_by_year(firstyear)
    feed = build_stock_feed(instruments, [firstyear, 2015])
    EMA_Crossover = sgs.EMACrossover(feed, instruments, 100000)

    retAnalyzer = returns.Returns()
    EMA_Crossover.attachAnalyzer(retAnalyzer)

    # Run the strategy
    EMA_Crossover.run()





if __name__ == '__main__':
    main()
    # build_complete_dataset(['AAPL', 'FMTW', 'ALK', 'FMTW', 'AMG', 'FMTW', 'AMZN', 'FMTW', 'BWLD', 'FMTW', 'CLDN', 'FMTW', 'CMG',
    # 'FMTW', 'CMI', 'FMTW', 'GLW', 'FMTW', 'JCI', 'FMTW', 'OLN', 'FMTW', 'ROK', 'FMTW', 'TSLA', 'FMTW', 'UJPSX', 'VFINX'])
