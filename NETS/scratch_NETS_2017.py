# NETS2017_Misc.txt - use 'firstyear' as business age
# NETS2017_Emp.txt - emp90 and empc90 tells you

import pandas as pd
import time
import sys

pd.set_option('max_columns', 1000)
pd.set_option('max_info_columns', 1000)
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 30000)
pd.set_option('max_colwidth', 4000)
pd.set_option('display.float_format', lambda x: '%.2f' % x)
pd.options.mode.chained_assignment = None

# time
start = time.time()

# pull from S3
df = pd.read_csv('s3://emkf.data.research/other_data/nets/NETS_2017/NETS2017_Misc/NETS2017_Misc.txt',\
                 sep='\t', na_values=' ', lineterminator='\r', error_bad_lines=False, encoding='latin1')

# subset
df = df[['DunsNumber', 'FipsCounty', 'FirstYear']]
df['FipsCounty'] = df['FipsCounty'].astype(float)

# create state_fip
df['hm_county_fips'] = df['FipsCounty'].astype(str).str.zfill(5)
df['state_fips'] = df['hm_county_fips'].astype(str).str[:2]
df.sort_values(by='state_fips', inplace=True)
df.reset_index(drop=True, inplace=True)

# state_codes dict, reverse dict, and recode fips to strings
state_codes = {
    'WA': '53', 'DE': '10', 'DC': '11', 'WI': '55', 'WV': '54', 'HI': '15',
    'FL': '12', 'WY': '56', 'PR': '72', 'NJ': '34', 'NM': '35', 'TX': '48',
    'LA': '22', 'NC': '37', 'ND': '38', 'NE': '31', 'TN': '47', 'NY': '36',
    'PA': '42', 'AK': '02', 'NV': '32', 'NH': '33', 'VA': '51', 'CO': '08',
    'CA': '06', 'AL': '01', 'AR': '05', 'VT': '50', 'IL': '17', 'GA': '13',
    'IN': '18', 'IA': '19', 'MA': '25', 'AZ': '04', 'ID': '16', 'CT': '09',
    'ME': '23', 'MD': '24', 'OK': '40', 'OH': '39', 'UT': '49', 'MO': '29',
    'MN': '27', 'MI': '26', 'RI': '44', 'KS': '20', 'MT': '30', 'MS': '28',
    'SC': '45', 'KY': '21', 'OR': '41', 'SD': '46'
}
inv_state_codes = {v: k for k, v in state_codes.items()}
df["state_fips"].replace(inv_state_codes, inplace=True)

# value_counts
print(df['state_fips'].value_counts())
counts = (df.groupby(["state_fips", "FirstYear"]).size())
counts = counts.reset_index()
counts.rename(columns = {0:'est_count'}, inplace = True)
print(counts)
counts.to_excel('/Users/hmurray/Desktop/data/NETS/st_est_counts.xlsx', index=False)
end = time.time()
print((end/60) - (start/60))

sys.exit()

# # state codes for int
# state_codes = {
#     'WA': 53, 'DE': 10, 'DC': 11, 'WI': 55, 'WV': 54, 'HI': 15,
#     'FL': 12, 'WY': 56, 'PR': 72, 'NJ': 34, 'NM': 35, 'TX': 48,
#     'LA': 22, 'NC': 37, 'ND': 38, 'NE': 31, 'TN': 47, 'NY': 36,
#     'PA': 42, 'AK': 2, 'NV': 32, 'NH': 33, 'VA': 51, 'CO': 8,
#     'CA': 6, 'AL': 1, 'AR': 5, 'VT': 50, 'IL': 17, 'GA': 13,
#     'IN': 18, 'IA': 19, 'MA': 25, 'AZ': 4, 'ID': 16, 'CT': 9,
#     'ME': 23, 'MD': 24, 'OK': 40, 'OH': 39, 'UT': 49, 'MO': 29,
#     'MN': 27, 'MI': 26, 'RI': 44, 'KS': 20, 'MT': 30, 'MS': 28,
#     'SC': 45, 'KY': 21, 'OR': 41, 'SD': 46
# }

#########################################################################################################################
################################################# Danny's Files #########################################################
#########################################################################################################################

# pull in data
df = pd.read_excel('/Users/hmurray/Desktop/data/NETS/Danny_Smith_briefs/Four_Brief_Assignments/Brief_1/qc/db_1_raw.xlsx',\
                   sheet_name='KESE_NEB_merge (1)', usecols=['state', 'year', 'ba', 'nets_new_establishments'])
print(df.head())

# figure_1
figure_1 = df.groupby(df['year'])[['ba', 'nets_new_establishments']].median().reset_index()
print(figure_1)
# plot figure_1
figure_1.plot(x='year', y=['ba', 'nets_new_establishments'])
plt.xticks(rotation=45)
plt.title("\n".join(wrap('Figure 1: BA and NETS Medians Over Time, 2005-2016', 50)))
plt.tight_layout()
plt.grid()
plt.savefig('/Users/hmurray/Desktop/data/NETS/Danny_Smith_briefs/Four_Brief_Assignments/Brief_1/qc/figure_1.png')
plt.show()

# figure_2
figure_2 = df.groupby(df['year'])[['ba', 'nets_new_establishments']].min().reset_index()
print(figure_2)
# plot figure_2
figure_2.plot(x='year', y=['ba', 'nets_new_establishments'])
plt.xticks(rotation=45)
plt.title("\n".join(wrap('Figure 2. BFS and NETS Minimums Over Time, 2005-2016', 50)))
plt.tight_layout()
plt.grid()
plt.savefig('/Users/hmurray/Desktop/data/NETS/Danny_Smith_briefs/Four_Brief_Assignments/Brief_1/qc/figure_2.png')
plt.show()

# figure_3
figure_3 = df.groupby(df['year'])[['ba', 'nets_new_establishments']].max().reset_index()
print(figure_3)
# plot figure_3
figure_3.plot(x='year', y=['ba', 'nets_new_establishments'])
plt.xticks(rotation=45)
plt.title("\n".join(wrap('Figure 3. BFS and NETS Maximums Over Time, 2005-2016', 50)))
plt.tight_layout()
plt.grid()
plt.savefig('/Users/hmurray/Desktop/data/NETS/Danny_Smith_briefs/Four_Brief_Assignments/Brief_1/qc/figure_3.png')
plt.show()

# figure_4
figure_4 = df[df['year'] == 2016]
print(figure_4)
# plot figure_4
figure_4.sort_values("ba", ascending=False).plot(x="state", y=["ba", "nets_new_establishments"], kind="bar")
plt.title("\n".join(wrap('Figure 4. BFS and NETS Counts of New Establishments by State, 2016', 50)))
plt.tight_layout()
plt.grid()
plt.savefig('/Users/hmurray/Desktop/data/NETS/Danny_Smith_briefs/Four_Brief_Assignments/Brief_1/qc/figure_4.png')
plt.show()

# figure_5
figure_5 = df.groupby(df['state'])[['ba', 'nets_new_establishments']].sum().reset_index()
print(figure_5)
# plot figure_5
figure_5.sort_values("ba", ascending=False).plot(x='state', y=['ba', 'nets_new_establishments'], kind="bar")
plt.title("\n".join(wrap('Figure 5. Summed BFS and NETS Counts of New Establishments by State, 2005-2016', 50)))
plt.tight_layout()
plt.grid()
plt.savefig('/Users/hmurray/Desktop/data/NETS/Danny_Smith_briefs/Four_Brief_Assignments/Brief_1/qc/figure_5.png')
plt.show()

sys.exit()

import pandas as pd
import numpy as np
import sys

pd.set_option('max_columns', 1000)
pd.set_option('max_info_columns', 1000)
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 30000)
pd.set_option('max_colwidth', 4000)
pd.set_option('display.float_format', lambda x: '%.2f' % x)
pd.options.mode.chained_assignment = None

# pull from S3
move = pd.read_csv('s3://emkf.data.research/other_data/nets/NETS_2017/NETS2017_Move/NETS2017_Move.txt',\
                 sep='\t', na_values=' ', nrows=5000, lineterminator='\r', error_bad_lines=False, encoding='latin1')
print(move.head())

misc = pd.read_csv('s3://emkf.data.research/other_data/nets/NETS_2017/NETS2017_Misc/NETS2017_Misc.txt',\
                 sep='\t', na_values=' ', lineterminator='\r', nrows=5000, error_bad_lines=False, encoding='latin1', low_memory=False)
print(misc.head(500))
print(misc['PubPriv'].value_counts())
print(misc['LegalStat'].value_counts())
print(pd.crosstab(misc['PubPriv'], misc['LegalStat'], margins=True, margins_name="Total"))
df = move.merge(misc, on='DunsNumber')
print(df.head())



sys.exit()

# # # pull from S3
# df = pd.read_csv('s3://emkf.data.research/other_data/nets/NETS_2017/NETS2017_Misc/NETS2017_Misc.txt',\
#                  sep='\t', na_values=' ', lineterminator='\r', error_bad_lines=False, encoding='latin1')
# pull from S3
df = pd.read_csv('s3://emkf.data.research/other_data/nets/NETS_2017/NETS2017_Move/NETS2017_Move.txt',\
                 sep='\t', na_values=' ', nrows=500, lineterminator='\r', error_bad_lines=False, encoding='latin1')
print(df)
df.to_excel('/Users/hmurray/Desktop/2017_nets_move_sample.xlsx')

# logic check
df['left'] = np.where(df['OriginState'] == df['DestState'], 'stayed', 'left')

# subset by move-outs
df = df[df['left'] == 'left'].reset_index(drop=True)

# value_counts
move_in = df.groupby(['DestState', 'MoveYear']).size().reset_index()
move_in.rename(columns={"DestState": "region", 0: "move_in"}, inplace=True)
move_out = df.groupby(['OriginState', 'MoveYear']).size().reset_index()
move_out.rename(columns={"OriginState": "region", 0: "move_out"}, inplace=True)

# merge value_counts and rename columns
in_out = move_in.merge(move_out, on=['region', 'MoveYear'])

# calculate ratio
in_out['ratio'] = in_out['move_in'] / in_out['move_out']
print(in_out)
sys.exit()

# df = pd.read_csv('s3://emkf.data.research/other_data/nets/NETS_2017/NETS2017_Misc/NETS2017_Misc.txt',\
#                  sep='\t', na_values=' ', lineterminator='\r', nrows=500, error_bad_lines=False, encoding='latin1', low_memory=False)
print(df.head(500))

# subset
df = df[['DunsNumber', 'FipsCounty', 'FirstYear']]

# create state_fips
df['hm_county_fips'] = df['FipsCounty'].astype(str).str.zfill(5)
df['state_fips'] = df['hm_county_fips'].astype(str).str[:2].astype(int)

# state_codes dict, reverse dict, and recode fips to strings
state_codes = {
    'WA': 53, 'DE': 10, 'DC': 11, 'WI': 55, 'WV': 54, 'HI': 15,
    'FL': 12, 'WY': 56, 'PR': 72, 'NJ': 34, 'NM': 35, 'TX': 48,
    'LA': 22, 'NC': 37, 'ND': 38, 'NE': 31, 'TN': 47, 'NY': 36,
    'PA': 42, 'AK': 2, 'NV': 32, 'NH': 33, 'VA': 51, 'CO': 8,
    'CA': 6, 'AL': 1, 'AR': 5, 'VT': 50, 'IL': 17, 'GA': 13,
    'IN': 18, 'IA': 19, 'MA': 25, 'AZ': 4, 'ID': 16, 'CT': 9,
    'ME': 23, 'MD': 24, 'OK': 40, 'OH': 39, 'UT': 49, 'MO': 29,
    'MN': 27, 'MI': 26, 'RI': 44, 'KS': 20, 'MT': 30, 'MS': 28,
    'SC': 45, 'KY': 21, 'OR': 41, 'SD': 46
}
inv_state_codes = {v: k for k, v in state_codes.items()}
df["state_fips"].replace(inv_state_codes, inplace=True)

# value_counts
print(df['state_fips'].value_counts())
counts = (df.groupby(["state_fips", "FirstYear"]).size())
counts = counts.reset_index()
counts.rename(columns = {0:'est_count'}, inplace = True)
print(counts)
counts.to_excel('/Users/hmurray/Desktop/data/NETS/st_est_counts.xlsx', index=False)
sys.exit()



