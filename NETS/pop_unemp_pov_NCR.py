# pop data downloaded manually from: https://data.ers.usda.gov/reports.aspx?ID=17827
# unemp data downloaded manually from: https://data.ers.usda.gov/reports.aspx?ID=17828
# pov data downloaded manually from: https://data.ers.usda.gov/reports.aspx?ID=17826

import os
import sys
import shutil
import xlrd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import xlsxwriter
from textwrap import wrap

pd.set_option('max_columns', 1000)
pd.set_option('max_info_columns', 1000)
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 30000)
pd.set_option('max_colwidth', 4000)
pd.set_option('display.float_format', lambda x: '%.2f' % x)
pd.options.mode.chained_assignment = None

#########################################################################################################################
############################################## IRS SELF-EMPLOYMENT ANALYSIS #############################################
#########################################################################################################################

# pull county level self-employment
self = pd.read_csv('/Users/hmurray/Desktop/Data_Briefs/NETS/Danny_Smith_briefs/Four_Brief_Assignments/DC_Abnormality/python_edits/pop_unemp_pov_NCR/IRSSelfEmployment.csv',header=0,encoding = 'unicode_escape', dtype={'user_id': int}, low_memory=False)


# slice df for total returns and returns with self-employment
self = self[['county', 'State', 'Returns', 'Returns_with_Self_Tax', 'percent_returns_self_emp']]

# rename columns
self.rename(columns={"N1": "Returns", "N03300": "Returns_with_Self_employment", "A03300": "Self_employment",\
                     "DP03_HC01_VC69": "estimate_uninc_se", "DP03_HC03_VC69": "percent_uninc_se"},inplace=True)

df = self.groupby(['county'])['Returns', 'Returns_with_Self_Tax'].agg('sum').reset_index()
df['percent_returns_self_emp'] = (df['Returns_with_Self_Tax']/df['Returns'])*100


# filter, reset index, take a look
df = df.loc[(df.county == 11001) | (df.county == 24031) | (df.county == 24033) |\
            (df.county == 51013) | (df.county == 51059) | (df.county == 51107) | (df.county == 51153)]
df.reset_index(inplace=True)
print(df)

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('/Users/hmurray/Desktop/Data_Briefs/NETS/Danny_Smith_briefs/Four_Brief_Assignments/DC_Abnormality/python_edits/pop_unemp_pov_NCR/percent_returns_self_emp.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='percent_returns_self_emp', index=False)

# Get the xlsxwriter workbook and worksheet objects.
workbook  = writer.book
worksheet = writer.sheets['percent_returns_self_emp']

# Apply a conditional format to the cell range.
# worksheet.conditional_format('A1:E8', {'type': '3_color_scale'})

# Close the Pandas Excel writer and output the Excel file.



#########################################################################################################################
################################################ POP, UNEMP, POV ANALYSIS ###############################################
#########################################################################################################################

# pull sjc  and NEB
pop = pd.read_excel('/Users/hmurray/Desktop/Data_Briefs/NETS/Danny_Smith_briefs/Four_Brief_Assignments/DC_Abnormality/python_edits/pop_unemp_pov_NCR/pop_unemp_pov_NCR.xlsx', sheet_name='Population')
unemp = pd.read_excel('/Users/hmurray/Desktop/Data_Briefs/NETS/Danny_Smith_briefs/Four_Brief_Assignments/DC_Abnormality/python_edits/pop_unemp_pov_NCR/pop_unemp_pov_NCR.xlsx', sheet_name='Unemployment')
pov = pd.read_excel('/Users/hmurray/Desktop/Data_Briefs/NETS/Danny_Smith_briefs/Four_Brief_Assignments/DC_Abnormality/python_edits/pop_unemp_pov_NCR/pop_unemp_pov_NCR.xlsx', sheet_name='Poverty')

def _filter(df):
    df = df[(df.County == 'District of Columbia') | (df.County == 'Montgomery County')| (df.County == 'Prince George\'s County') | (df.County == 'Arlington County') |\
            (df.County == 'Fairfax County') | (df.County == 'Loudoun County') | (df.County == 'Prince William County')]
    df.reset_index(drop=True, inplace=True)
    return df

pop = _filter(pop)
unemp = _filter(unemp)
pov = _filter(pov)

# rename unemp columns
unemp.rename(columns={"2010": "Unemployment 2010", "2018": "Unemployment 2018"},inplace=True)
pov.rename(columns={"Percent": "Percent in Poverty"},inplace=True)

print(pop.head())
print(unemp.head())
print(pov.head())


df = pd.concat([pop,unemp,pov],sort=True, axis=1)
df = df[['County', 'FIPS*', 'Pop. 2010',  'Pop. 2018' , 'Change 2010-18', 'Unemployment 2010', 'Unemployment 2018', 'Median Household Income (2018)', '% of State Median HH Income', 'Percent in Poverty']]
data = df.iloc[:, np.r_[2, 4:13]]
print(data)


data.to_excel(writer, sheet_name='pop_unemp_pov', index=False)
workbook.close()
writer.save()

sys.exit()