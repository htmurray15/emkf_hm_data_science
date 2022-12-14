# data downloaded manually from https://factfinder.census.gov/bkmk/table/1.0/en/ASE/2016/00CSA03

import os
import sys
import time
import zipfile
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option('max_columns', 1000)
pd.set_option('max_info_columns', 1000)
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 30000)
pd.set_option('max_colwidth', 4000)
pd.set_option('display.float_format', lambda x: '%.3f' % x)


# load PEP data
df = pd.read_csv('/Users/hmurray/Desktop/data/ASE/ASE_receipts/ASE_2016_00CSA03_with_ann.csv')

# keep vars
df = df[['GEO.display-label', 'NAICS.display-label', 'SEX.display-label', 'ETH_GROUP.display-label',\
         'RACE_GROUP.display-label','VET_GROUP.display-label', 'RCPSZFI.display-label', 'FIRMPDEMP']]

# Rename columns
df.rename(columns={"GEO.display-label": "region", "NAICS.display-label": "industry", "SEX.display-label": "sex"\
    ,"ETH_GROUP.display-label": "ethnicity", "RACE_GROUP.display-label": "race", "VET_GROUP.display-label": "vet",\
                   "RCPSZFI.display-label": "receipts", "FIRMPDEMP": "count"},inplace=True)

# filters
df = df[df['region'] == 'United States']
df = df[df['industry'] == 'Total for all sectors']
df = df[df['sex'] == 'All firms']
df = df[df['ethnicity'] == 'All firms']
df = df[df['vet'] == 'All firms']
df = df[(df.race == 'All firms') |  (df.race == 'Minority') | (df.race == 'Nonminority')]
df = df[(df.receipts == 'Firms with sales/receipts of $1,000,000 or more')]

# reset index
df.reset_index(inplace=True, drop=True)
print(df)

# Total firms with receipts exceeding $1 million:
total_firms = df.iloc[0,7]
total_firms = int(total_firms)
print(total_firms)

#Minority firms exceeding $1 million:
min_firms = df.iloc[1,7]
min_firms = int(min_firms)
print(min_firms)

#Nonminority firms exceeding $1 million:
nonmin_firms = df.iloc[2,7]
nonmin_firms = int(nonmin_firms)
print(nonmin_firms)

# percent minority firms
min_firms_per = (min_firms/total_firms)*100
print(min_firms_per)

# percent Nonminority firms
nonmin_firms_per = (nonmin_firms/total_firms)*100
print(nonmin_firms_per)
