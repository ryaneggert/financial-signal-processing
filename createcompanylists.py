from finance.data.exchanges.masterlist import generatemasterlist, addminbool
from finance.data.exchanges import master

import pandas as pd
# Data from http://www.nasdaq.com/screening/company-list.aspx
# # Imports the modified data (added exchange column, replaced 'n/a' with "nan")
# generatemasterlist()
# addminbool()

mast = master()

# g1 = mast.groupby('Exchange')
# print g1['LastSale'].mean()

print len(mast[mast['minutedata'] == True] )
