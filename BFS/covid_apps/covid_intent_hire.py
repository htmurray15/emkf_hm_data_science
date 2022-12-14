# data downloaded from csv link at the bottom of this webpage: https://www.census.gov/econ/bfs/data.html
# csv link: https://www.census.gov/econ/bfs/csv/bfs_quarterly.csv
# pulling from Kauffman library

import sys
import pandas as pd
from kauffman.data import bfs
import matplotlib.pyplot as plt
import datetime
import numpy as np
from textwrap import wrap
from matplotlib.dates import date2num

pd.set_option('max_columns', 1000)
pd.set_option('max_info_columns', 1000)
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 30000)
pd.set_option('max_colwidth', 4000)
# pd.set_option('display.float_format', lambda x: '%.2f' % x)
pd.options.mode.chained_assignment = None

# read in ba and wba
def data_create():
    return pd.read_excel('/Users/hmurray/Desktop/data/BFS/ba_wba_4bf_8bf/2021/updated_data/covid_intent_hire.xlsx')
    # pull from kauffman library
    df = bfs(['BA_BA', 'BA_CBA', 'BA_WBA', 'BF_SBF8Q'],\
             obs_level='us', industry='all', annualize=False)

def filterer(df):
    # calculate percent BA_WBA and percent BA_CBA
    df['percent_wba'] = df['BA_WBA'] / df['BA_BA']
    df['percent_cba'] = df['BA_CBA'] / df['BA_BA']
    df['percent_SBF8Q'] = df['BF_SBF8Q'] / df['BA_BA']
    # filter for all industry
    df = df[df['naics'] == '00']
    # save this filtered df
    location = '/Users/hmurray/Desktop/data/BFS/ba_wba_4bf_8bf/2021/updated_data/calcs_covid_intent_hire.xlsx'
    writer = pd.ExcelWriter(location, engine='xlsxwriter')
    # export each df to separate sheet
    df.to_excel(writer, sheet_name='covid_bfs', index=False)
    # save to excel
    writer.save()
    return df

def plotter_1(df):
    df2 = df[(df['time'] > '2020-01-01') & (df['time'] < '2021-11-01')]
    # df2 = df.query('20200101 <= time < 20212101')
    df2.plot(x='time', y=['BA_BA', 'BA_CBA', 'BA_WBA'])
    plt.xlabel('time')
    plt.xticks(rotation=45)
    # plt.xlim(2005, 2019)
    plt.ylabel('Count')
    # plt.yticks(np.arange(0, 1150, step=100), rotation=45)
    leg_1_labels = ['Business Applications', 'Corporate Business Applications', 'Employer Business Applications']
    plt.legend(labels=leg_1_labels)
    title = ('Figure 1: Monthly Business Applications since Jan 2020')
    plt.title("\n".join(wrap(title, 50)))
    plt.tight_layout()
    plt.grid()
    plt.savefig('/Users/hmurray/Desktop/data/BFS/ba_wba_4bf_8bf/2021/updated_data/plots/2020_counts_covid_intent_hire.png')
    plt.show()
    return df

def plotter_2(df):
    # New Business Applications and New Employer Businesses
    df.plot(x='time', y=['BA_BA', 'BA_CBA', 'BA_WBA'])
    plt.xlabel('time')
    plt.xticks(rotation=45)
    # plt.xlim(2005, 2019)
    plt.ylabel('Count')
    # plt.yticks(np.arange(0, 1150, step=100), rotation=45)
    leg_1_labels = ['Business Applications', 'Corporate Business Applications', 'Employer Business Applications']
    plt.legend(labels=leg_1_labels)
    title = ('Figure 2: Monthly Business Applications 2004-2021')
    plt.title("\n".join(wrap(title, 50)))
    plt.tight_layout()
    plt.grid()
    # plt.axvspan(date2num(datetime(2020,1,1)), date2num(datetime(2020,2,1)),label="March", color="crimson", alpha=0.3)
    plt.savefig('/Users/hmurray/Desktop/data/BFS/ba_wba_4bf_8bf/2021/updated_data/plots/all_counts_covid_intent_hire.png')
    plt.show()
    return df

def plotter_3(df):
    df3 = df[(df['time'] > '2020-01-01') & (df['time'] < '2021-11-01')]
    # df3 = df.query('20200101 <= time < 20212101')
    df3.plot(x='time', y=['percent_wba', 'percent_SBF8Q'])
    plt.xlabel('time')
    plt.xticks(rotation=45)
    # plt.xlim(2005, 2019)
    plt.ylabel('Share of all business applications')
    # plt.yticks(np.arange(0, 1150, step=100), rotation=45)
    leg_1_labels = ['Intent to Hire', 'Hiring']
    plt.legend(labels=leg_1_labels)
    title = ('Figure 3: 2020 Monthly Intent to Hire vs Actual Hiring')
    plt.title("\n".join(wrap(title, 50)))
    plt.tight_layout()
    plt.grid()
    plt.savefig('/Users/hmurray/Desktop/data/BFS/ba_wba_4bf_8bf/2021/updated_data/plots/2020_intent_vs_actual.png')
    plt.show()
    return df

def plotter_4(df):
    # New Business Applications and New Employer Businesses
    df.plot(x='time', y=['percent_wba', 'percent_SBF8Q'])
    plt.xlabel('time')
    plt.xticks(rotation=45)
    # plt.xlim(2005, 2019)
    plt.ylabel('Share of all business applications')
    # plt.yticks(np.arange(0, 1150, step=100), rotation=45)
    leg_1_labels = ['Intent to Hire', 'Hiring']
    plt.legend(labels=leg_1_labels)
    title = ('Figure 4: Monthly Intent to Hire vs Actual Hiring 2004-2021')
    plt.title("\n".join(wrap(title, 50)))
    plt.tight_layout()
    plt.grid()
    # plt.axvspan(date2num(datetime(2020,1,1)), date2num(datetime(2020,2,1)),label="March", color="crimson", alpha=0.3)
    plt.savefig('/Users/hmurray/Desktop/data/BFS/ba_wba_4bf_8bf/2021/updated_data/plots/all_intent_vs_actual.png')
    plt.show()
    return df

if __name__ == '__main__':
    df = data_create()
    df = filterer(df)
    df = plotter_1(df)
    df = plotter_2(df)
    df = plotter_3(df)
    df = plotter_4(df)

sys.exit()