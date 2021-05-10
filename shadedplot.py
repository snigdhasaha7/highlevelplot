"""
This script reads reaction data from multiple .csvs, 
generates a shaded timeseries plot, and saves
the average readings for every second of the video
in a .csv in the same directory.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from os import listdir, path

# video length in seconds
upperbound = 1255

# organize the data by folder - all the files for one plot
# should be in one folder
# only extracts .csv files
folder = 'data_exp_42502-v4'
dfs = []
for file in listdir(folder):
    if not file.endswith('.csv'):
        continue
    df = pd.read_csv(path.join(folder, file))
    dfs.append(df)
    
def clean(df):
    """
    Takes original dataframes, extracts relevant columns and rows,
    and reindexes the data.
    
    Input: df (Pandas Dataframe)
    Output: df (Pandas Dataframe)
    """
    df1 = df[['Trial Number', 'Zone Name', 'Reaction Time', 'Response']]
    for i in range(1, len(df1['Response'])):
        if pd.isnull(df1['Response'][i]):
            df1['Response'][i] = 0
        
    # getting rid of non-slider rows 
    dropped = []
    for i in range(len(df1)):
        if df1['Zone Name'][i] != 'slider' or pd.isnull(df1['Reaction Time'][i]):
            #print(f'{i} row')
            dropped.append(i)
            df1 = df1.drop(labels=i)
    
    adder = 0
    for i in range(len(df)):
        if i in dropped:
            continue
        #print(adder)
        df1['Reaction Time'][i] += adder
        j = i + 1
        while j != len(df) - 1 and j in dropped:
            j += 1

        if j not in dropped and df1['Trial Number'][i] != df1['Trial Number'][j]:
            adder = df1['Reaction Time'][i]
    
    for i in range(len(df)):
        if i in dropped:
            continue
        df1['Reaction Time'][i] /= 1000
    
    # reindexing
    reaction_times = []
    responses = []
    for i in range(len(df)):
        if i in dropped:
            continue
        reaction_times.append(df1['Reaction Time'][i])
        responses.append(df1['Response'][i])
    
    data = {'Reaction Time': reaction_times,
           'Response': responses}
    df1 = pd.DataFrame(data)
    
    return df1

# applying cleaning function to all dfs
clean_dfs = []
for df in dfs:
    df1 = clean(df)
    clean_dfs.append(df1)

# creating dfs for every second of the video
# done to be able to compare dfs
modified_dfs = []
for k in range(len(clean_dfs)):
    list_of_zeros = [0] * (int(upperbound))
    data = {'Reaction Time': range(0, int(upperbound)),
           'Response':  list_of_zeros}
    df2 = pd.DataFrame(data)
    
    j = 0
    for i in range(len(clean_dfs[k]) - 1):
        while j < upperbound and df2['Reaction Time'][j] <= clean_dfs[k]['Reaction Time'][i + 1]:
            df2['Response'][j] = clean_dfs[k]['Response'][i]
            j += 1
    modified_dfs.append(df2)

# mass df created with all data across dfs
all_reaction_times = []
all_responses = []
for df in modified_dfs:
    for i in range(len(df)):
        all_reaction_times.append(df['Reaction Time'][i])
        all_responses.append(df['Response'][i])
data = {'Reaction Time': all_reaction_times,
       'Response': all_responses}
final_df = pd.DataFrame(data)

# average df prepared to save
list_of_zeros = [0] * (int(upperbound))
data = {'Reaction Time': range(0, int(upperbound)),
           'Response':  list_of_zeros}
avg_df = pd.DataFrame(data)

for i in range(upperbound):
    response_sum = 0
    for df in modified_dfs:
        response_sum += df['Response'][i]
    avg_df['Response'][i] = response_sum * 1.0 / len(modified_dfs)

avg_df.to_csv(r'average_responses.csv')


# plotted using seaborn to view shading
sns.lineplot(data=final_df, x='Reaction Time',
    y='Response')