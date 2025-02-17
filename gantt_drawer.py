import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib as matplotlib
import datetime as dt

#main source:
#https://www.datacamp.com/tutorial/how-to-make-gantt-chart-in-python-matplotlib

Projecttitle="Example project"
freq_days=90
colour="orange"

df = pd.DataFrame({'task': ['Time', 'B', 'C'],
                  'start': pd.to_datetime(['2024-03-25', '2024-03-25', '2025-03-25']),
                  'end': pd.to_datetime(['2028-03-25', '2026-05-27', '2027-09-25']),
                  'completion_frac': [0, 0.1, 1]})

df=pd.read_csv("./example.txt",header=0,names=["task","start","end","completion_frac"])
df["start"]=pd.to_datetime(df["start"])
df["end"]=pd.to_datetime(df["end"])




df["completion_frac"][0]=(dt.datetime.now()-df['start'].min()).days/((df['end'].max() - df['start'].min()).days)

df['days_to_start'] = (df['start'] - df['start'].min()).dt.days
df['days_to_end'] = (df['end'] - df['start'].min()).dt.days
df['task_duration'] = df['days_to_end'] - df['days_to_start'] + 1  # to include the end date too
df['completion_days'] = df['completion_frac'] * df['task_duration']



xticks = np.arange(0, df['days_to_end'].max() + 2,freq_days)
xticklabels = pd.date_range(start=df['start'].min() + dt.timedelta(days=5), end=df['end'].max(),freq=dt.timedelta(days=freq_days)).strftime("%m-%d")
print(xticklabels)

fig, ax = plt.subplots()
for index, row in df.iterrows():
    plt.barh(y=row['task'], width=row['task_duration'], left=row['days_to_start'] + 1, alpha=0.4,color=colour)
    plt.barh(y=row['task'], width=row['completion_days'], left=row['days_to_start'] + 1,color=colour)

plt.title(Projecttitle, fontsize=15)
plt.gca().invert_yaxis()
ax.set_xticks(xticks)
ax.set_xticklabels(xticklabels)
ax.xaxis.grid(True, alpha=0.5)

# Marking the current date on the chart
ax.axvline(x=(dt.datetime.now()-df['start'].min()).days, color='r', linestyle='dashed')
#ax.text(x=29.5,y=11.5, s=str(dt.datetime.now())[:10], color='r')

plt.show()