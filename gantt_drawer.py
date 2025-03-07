import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib as matplotlib
import datetime as dt

#main source:
#https://www.datacamp.com/tutorial/how-to-make-gantt-chart-in-python-matplotlib

Projecttitle="Title of Project"
freq_days=90
colour="purple"
first_colour="orange"


df=pd.read_csv("../timeline.txt",header=0,names=["task","start","end","completion_frac","desc"])
df["start"]=pd.to_datetime(df["start"])
df["end"]=pd.to_datetime(df["end"])

print(df)


df.loc[0,"completion_frac"]=(dt.datetime.now()-df['start'].min()).days/((df['end'].max() - df['start'].min()).days)

df['days_to_start'] = (df['start'] - df['start'].min()).dt.days
df['days_to_end'] = (df['end'] - df['start'].min()).dt.days
df['task_duration'] = df['days_to_end'] - df['days_to_start'] + 1  # to include the end date too
df['completion_days'] = df['completion_frac'] * df['task_duration']



xticks = np.arange(0, df['days_to_end'].max() + 2,freq_days)
xticklabels = pd.date_range(start=df['start'].min() + dt.timedelta(days=5), end=df['end'].max(),freq=dt.timedelta(days=freq_days)).strftime("%m-%d")

fig, ax = plt.subplots(figsize=(12,4))
for index, row in df.iterrows():
    c=colour
    if(row.name==0):
        c=first_colour
    plt.barh(y=row['task'], width=row['task_duration'], left=row['days_to_start'] + 1, alpha=0.1,color=c)
    plt.barh(y=row['task'], width=row['completion_days'], left=row['days_to_start'] + 1,color=c)

plt.title(Projecttitle, fontsize=15)
plt.gca().invert_yaxis()
ax.set_xticks(xticks)
ax.set_xticklabels(xticklabels)
ax.xaxis.grid(True, alpha=0.5)

# Marking the current date on the chart
ax.axvline(x=(dt.datetime.now()-df['start'].min()).days, color='r', linestyle='dashed')
plt.subplots_adjust(left=0.2,right=0.99) 
#plt.show()
plt.savefig("../timeline.pdf")