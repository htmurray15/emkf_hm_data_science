import os
import sys
import shutil
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


pd.set_option('max_columns', 1000)
pd.set_option('max_info_columns', 1000)
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 30000)
pd.set_option('max_colwidth', 4000)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

# pull BEA employment data
df1 = pd.read_csv('/Users/hmurray/Desktop/data/BEA/BEA_Data/locally_saved/BEA_employment.csv')
df_emp = df1[['GeoName','Description','2018']]

# pull BEA income data
df2 = pd.read_csv('/Users/hmurray/Desktop/data/BEA/BEA_Data/locally_saved/BEA_income.csv')
df_inc = df2[['GeoName','Description','2018:Q1','2018:Q2','2018:Q3','2018:Q4']]

# drop rows with missing values (NaN)
df_emp = df_emp.dropna()
df_inc = df_inc.dropna()

# drop rows with non numeric values
df_emp = df_emp[df_emp['2018'] != '(D)']
df_inc = df_inc[df_inc['2018:Q1'] != '(D)']

df_inc.reset_index(inplace=True, drop=True)
df_emp.reset_index(inplace=True, drop=True)

# convert income data to integer
df_inc['2018:Q1'] = pd.to_numeric(df_inc['2018:Q1'])
df_inc['2018:Q2'] = pd.to_numeric(df_inc['2018:Q2'])
df_inc['2018:Q3'] = pd.to_numeric(df_inc['2018:Q3'])
df_inc['2018:Q4'] = pd.to_numeric(df_inc['2018:Q4'])

# sum BEA quarterly income data
df_inc['2018'] = df_inc['2018:Q1'] + df_inc['2018:Q2'] + df_inc['2018:Q3'] + df_inc['2018:Q4']

# sort description alphabetically
df_emp.sort_values(by=['Description'],ascending = True, inplace = True)
df_inc.sort_values(by=['Description'],ascending = True, inplace = True)

# reset index
df_inc.reset_index(inplace=True, drop=True)
df_emp.reset_index(inplace=True, drop=True)

# subset proprietor emp and inc
df_emp = df_emp[6532:6592]
df_inc = df_inc[2392:2452]

# sort GeoName alphabetically
df_emp.sort_values(by=['GeoName'],ascending = True, inplace = True)
df_inc.sort_values(by=['GeoName'],ascending = True, inplace = True)

# reset index
df_inc.reset_index(inplace=True, drop=True)
df_emp.reset_index(inplace=True, drop=True)

# convert type to integer
df_inc['2018'] = pd.to_numeric(df_inc['2018'])
df_emp['2018'] = pd.to_numeric(df_emp['2018'])

# merge dataframes
df_merge = pd.merge(df_emp, df_inc, on='GeoName')

# create new dataframe
data = (df_inc['2018'] / df_emp['2018']) * 1000
df_merge['avg_prop_emp_inc'] = (df_merge['2018_y'] / df_merge['2018_x']) * 1000
df_merge.sort_values(by=['avg_prop_emp_inc'],ascending = True, inplace = True)
print(df_merge)

