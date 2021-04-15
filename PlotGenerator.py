# written by snigdha saha

import pandas as pd

import bokeh.io
import bokeh.plotting

# Enable viewing Bokeh plots in the notebook
bokeh.io.output_notebook()

# read csv into dataframe
# replace with each .csv
df = pd.read_csv('data_exp_42502-v4/data_exp_42502-v4_task-15i8.csv')

# extracting the only three relevant columns
#getting rid of as many unnnecessary rows from top and bottom as possible
df2 = df[['Trial Number', 'Zone Name', 'Reaction Time', 'Response']]

# replacing all NaN values with 0
for i in range(1, len(df2['Response'])):
    if pd.isnull(df2['Response'][i]):
        df2['Response'][i] = 0
        
# getting rid of non-slider rows 
dropped = []
for i in range(len(df2)):
    if df2['Zone Name'][i] != 'slider' or pd.isnull(df2['Reaction Time'][i]):
        #print(f'{i} row')
        dropped.append(i)
        df2 = df2.drop(labels=i)

# adjusting all time periods to make a continuous chart    
adder = 0
for i in range(len(df)):
    if i in dropped:
        continue
    #print(adder)
    df2['Reaction Time'][i] += adder
    j = i + 1
    while j != len(df) - 1 and j in dropped:
        j += 1    
    if j not in dropped and df2['Trial Number'][i] != df2['Trial Number'][j]:
        adder = df2['Reaction Time'][i]

# code for generating plot:

p = bokeh.plotting.figure(
    frame_width=500,
    frame_height=300,
    x_axis_label='Reaction Time',
    y_axis_label='Response'
)

p.line(
    source=df2,
    x='Reaction Time',
    y='Response'
);

bokeh.io.show(p)