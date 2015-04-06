import pandas as pd

# Data from http://www.nasdaq.com/screening/company-list.aspx
# Imports the modified data (added exchange column, replaced 'n/a' with "nan")

exchanges = ['nyse', 'nasdaq', 'amex']
for i, exchange in enumerate(exchanges):
    if i == 0:
        combine = pd.read_csv('./data/companies/%s.csv' % exchange)
    else:
        combine = combine.merge(pd.read_csv('./data/companies/%s.csv' % exchange), how='outer')
print combine.Exchange
# Save as CSV
combine.to_csv('./data/companies/master.csv')
