import os
import sys
import shutil
import pandas as pd
import matplotlib.pyplot as plt


pd.set_option('max_columns', 1000)
pd.set_option('max_info_columns', 1000)
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 30000)
pd.set_option('max_colwidth', 4000)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

# add options to the end of location to avoid using too much memory
df_tot = pd.read_csv('/Users/hmurray/Downloads/public2018.csv',header=0,encoding = 'unicode_escape', dtype={'user_id': int}, low_memory=False)

# look at df
print(df_tot.head())

# print frequencies
print(df_tot['D3A'].value_counts())
print(df_tot['D3B'].value_counts())
print(df_tot['ppreg4'].value_counts())
print(df_tot['ppstaten'].value_counts())
print(df_tot['SL3'].value_counts())
print(df_tot['SL4'].value_counts())
print(df_tot['FS20_b'].value_counts())

# group types of work by ...
state_pop = df_tot['D3B'].groupby([df_tot['ppreg4'], df_tot['D3B']]).count()
print(state_pop)

# crosstab business ownership by region
print(pd.crosstab(df_tot['ppreg4'], df_tot['D3A']))

# crosstab work status by region
print(pd.crosstab(df_tot['ppreg4'], df_tot['D3B']))

# crosstab work status by state
print(pd.crosstab(df_tot['ppstaten'], df_tot['D3B']))

# crosstab work status by state
print(pd.crosstab(df_tot['ppstaten'], df_tot['D3B']))

#crosstab business ownership by work status
print(pd.crosstab(df_tot['D3A'], df_tot['D3B']))
