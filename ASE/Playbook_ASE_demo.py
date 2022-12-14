# data downloaded manually from https://factfinder.census.gov/bkmk/table/1.0/en/ASE/2016/00CSA01

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
df = pd.read_csv('/Users/hmurray/Desktop/data/ASE/ASE_demo/ASE_2016_00CSA01_with_ann.csv')

# keep vars
df = df[['GEO.display-label', 'NAICS.display-label', 'SEX.display-label', 'ETH_GROUP.display-label', 'RACE_GROUP.display-label','VET_GROUP.display-label', 'FIRMPDEMP']]


# Rename columns
df.rename(columns={"GEO.display-label": "region", "NAICS.display-label": "industry", "SEX.display-label": "sex"\
    ,"ETH_GROUP.display-label": "ethnicity", "RACE_GROUP.display-label": "race", "VET_GROUP.display-label": "vet",\
                   "FIRMPDEMP": "emp_firms",},inplace=True)

# filters
df = df[df['region'] == 'United States']
df = df[df['industry'] == 'Total for all sectors']
df = df[(df.sex == 'All firms') | (df.sex == 'Male-owned')]
df = df[df['ethnicity'] == 'All firms']
df = df[df['vet'] == 'All firms']
df = df[(df.race == 'All firms') | (df.race == 'Minority') | (df.race == 'Nonminority') | (df.race == 'White')]

# reset index
df.reset_index(inplace=True, drop=True)
print(df)

# total firms
total_firms = df.iloc[0,6]
total_firms = int(total_firms)
print(total_firms)

# white firms
white_firms = df.iloc[1,6]
white_firms = int(white_firms)
print(white_firms)

# minority firms
min_firms = df.iloc[2,6]
min_firms = int(min_firms)
print(min_firms)

# nonminority firms
nonmin_firms = df.iloc[3,6]
nonmin_firms = int(nonmin_firms)
print(nonmin_firms)

# male firms
male_firms = df.iloc[4,6]
male_firms = int(male_firms)
print(male_firms)

# percent minority firms
min_firms_per = (min_firms/total_firms)*100
print(min_firms_per)

# percent Nonminority firms
nonmin_firms_per = (nonmin_firms/total_firms)*100
print(nonmin_firms_per)

# percent White firms
white_firms_per = (white_firms/total_firms)*100
print(white_firms_per)

# percent Male firms
male_firms_per = (male_firms/total_firms)*100
print(male_firms_per)