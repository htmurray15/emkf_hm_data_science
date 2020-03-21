# data downloaded manually from: https://www.federalreserve.gov/consumerscommunities/shed_data.htm

import os
import sys
import shutil
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import xlsxwriter

pd.set_option('max_columns', 1000)
pd.set_option('max_info_columns', 1000)
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 30000)
pd.set_option('max_colwidth', 4000)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.options.mode.chained_assignment = None


# pull,
data = pd.read_csv('/Users/hmurray/Desktop/data/SHED/2018_SHED_data.csv',header=0,encoding = 'unicode_escape', dtype={'user_id': int}, low_memory=False)

# replace "Refused" with NaN
data.replace('Refused', np.nan, inplace=True)
data.replace('Other (Please specify):', np.nan, inplace=True)

# shorten strings
data['D3A'] = data['D3A'].str.replace("For a single company or employer", "Employed", case = True)
data['D3A'] = data['D3A'].str.replace("For yourself or your family business", "Family- or Self-Employed", case = True)

# subset using startswith()
df = data[data.columns[pd.Series(data.columns).str.startswith(('D3A', 'E1', 'E2', 'E4'))]]
print(df.head())

# crosstabs
new = pd.DataFrame()
def crosser(var, save=None):
    print(var.value_counts(normalize=True))
    new = (pd.crosstab([var], df['D3A'], normalize='columns')).round(4) * 100
    print(new)
    if save:
        new.to_excel(save, index=True)

names = list(df.columns.values)
for x in names:
    crosser(df[x], '/Users/hmurray/Desktop/data/SHED/health_coverage/D3A' + str(x) + '.xlsx')


