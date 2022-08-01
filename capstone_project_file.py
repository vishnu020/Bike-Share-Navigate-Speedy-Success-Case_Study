#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import numpy as np
import seaborn as sns

import plotly.express as px
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)

import cufflinks as cf


# In[2]:


Oct_2020 = pd.read_csv('202010-divvy-tripdata.csv')
Nov_2020 = pd.read_csv('202011-divvy-tripdata.csv')
Dec_2020 = pd.read_csv('202012-divvy-tripdata.csv')
Jan_2021 = pd.read_csv('202101-divvy-tripdata.csv')
Feb_2021 = pd.read_csv('202102-divvy-tripdata.csv')
Mar_2021 = pd.read_csv('202103-divvy-tripdata.csv')
Apl_2021 = pd.read_csv('202104-divvy-tripdata.csv')
May_2021 = pd.read_csv('202105-divvy-tripdata.csv')
Jun_2021 = pd.read_csv('202106-divvy-tripdata.csv')
Jul_2021 = pd.read_csv('202107-divvy-tripdata.csv')
Aug_2021 = pd.read_csv('202108-divvy-tripdata.csv')
Sep_2021 = pd.read_csv('202109-divvy-tripdata.csv')


# In[3]:


df = pd.concat([Oct_2020,Nov_2020,Dec_2020,Jan_2021,Feb_2021,Mar_2021,Apl_2021,May_2021,Jun_2021,Jul_2021,Aug_2021,Sep_2021], ignore_index = True)


# In[4]:


df


# In[5]:


df = df.drop(columns=['start_station_name', 'start_station_id', 'end_station_name', 'end_station_id', 'start_lat', 'start_lng', 'end_lat', 'end_lng'])

df.tail()

#remove irrelevent columns 


# In[6]:


df['started_at'] = df['started_at'].astype('datetime64')
df['ended_at'] = df['ended_at'].astype('datetime64')
# Coverting datatype of "started_at" & "ended_at" columns to "datetime64" type.


# In[7]:


df['ride_length'] = (df['ended_at'] - df['started_at'])/pd.Timedelta(minutes=1)
df['ride_length'] = df['ride_length'].astype('int32')

# Creating New Column "ride_length" and changing its datatype to "int32"
# In this column, each row contains the difference between "starting time" and "ending time" columns in minutes.

df.head()


# In[8]:


df.sort_values(by = 'ride_length')


# In[9]:


# Its seen that many rows in some months contained negative values. 
# Such errors happened because the "ending time" is earlier than the "starting time" in their respective rows.

df[df['ride_length'] < 0].count()

# Number of rows containing Negative Values.


# In[10]:


df[df['ride_length'] < 1].count()

# Number of rows containing "ride length" less than "1" minute.


# In[11]:


df = df[df['ride_length'] >= 1]
df = df.reset_index()
df = df.drop(columns=['index'])

# Removing 80845 rows containing negative values & ride length less than 1 minute. 
# Any trips that were below 60 seconds in length are potentially false starts or users trying to re-dock a bike to ensure it was secure.

df


# In[12]:


sns.boxplot(data=df,x='member_casual',y='ride_length',order=['member','causal'])

it is clearly visible causal memeber use cycles for more duration
# In[13]:


df = df.astype({'ride_id':'string', 'rideable_type':'category', 'member_casual':'category'})

df.info()

# Coverting datatypes of each columns.


# In[14]:


df.shape


# In[15]:


df.isna().sum()


# In[16]:


df['ride_id']=df['ride_id'].str.strip()

#removing leading and trailing whitespaces from the dataset


# In[17]:


df[df['ride_id'].duplicated()]


# In[18]:


from pandas.api.types import CategoricalDtype


# # ANALYSE AND SHARE 

# In[19]:


df['year'] = df['started_at'].dt.year

cats1 = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
df['month'] = df['started_at'].dt.month_name()
df['month'] = df['month'].astype(CategoricalDtype(categories=cats1, ordered=False))

cats2 = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
df['day_of_week'] = df['started_at'].dt.day_name()
df['day_of_week'] = df['day_of_week'].astype(CategoricalDtype(categories=cats2, ordered=False))

df['hour'] = df['started_at'].dt.hour

df = df.astype({'year':'int16', 'hour':'int8'})

# Creating new columns "year", "month", "day_of_week", "hour" and Converting datatypes.

df.head()


# In[20]:


df.info()


# # Analyzing the Difference in Number of Rides Between Casual riders and Members.

# #total number of rides in one year 

# In[21]:


pd.pivot_table(df,
              index = 'member_casual',
              values = 'ride_id',
              aggfunc = ['count'],
              margins = True,
              margins_name = 'Total Count')


# In[22]:


fig_1=df.groupby('member_casual',as_index=False).count()
fig_1


# In[23]:


px.bar(fig_1,y='member_casual',x='ride_id',range_x=[0,3000000],
      color='member_casual',
      height=300,
       text='ride_id',
      labels={'ride_id':'No Of rides','member_casual':'member/Casual'},
      hover_name = 'member_casual', hover_data = {'member_casual': False, 'month': False, 'ride_id': True}, 
        color_discrete_map = {'casual': '#FF934F', 'member': '#058ED9'})


# # number of rides in one month

# In[24]:


df_pv1=pd.pivot_table(df,
                     index=['year','month','member_casual'],
                     values='ride_id',
                     aggfunc=['count'],
                     margins=True,
                     margins_name='Total count')
df_pv1 = df_pv1.loc[(df_pv1 != 0).any(axis=1)]
df_pv1


# In[25]:


fig_2=df.groupby(['year','month','member_casual'],as_index=False).count()
fig_2=fig_2[fig_2['ride_id']!=0]


px.line(fig_2,x='month',y='ride_id',range_y=[0,450000],
       color='member_casual',
       line_shape='spline',
       markers=True,
       labels = {'ride_id': 'No. of Rides', 'month': 'Months (Oct 2020 - Sep 2021)', 'member_casual': 'Member/Casual'},
        hover_name = 'member_casual', hover_data = {'member_casual': False, 'month': True, 'ride_id': True}, 
        color_discrete_map = {'casual': '#FF934F', 'member': '#058ED9'})


# 1.It shows that the total number of rides fall during winter season and rise during summer season.
# 
# 2.The behaviour of casual riders and members tend to be the same as the season changes.
# 
# 3.Maximum riders are using bikes in summer season.
# 
# 4.Casual riders overtake members during summer.

# # Average Number of Rides in Each Weekday

# In[26]:


pd.pivot_table(df,
              index = ['day_of_week', 'member_casual'],
              values = 'ride_id',
              aggfunc = ['count'],
              margins = True,
              margins_name = 'Total Count')


# In[27]:


fig_3 = df.groupby(['day_of_week', 'member_casual'], as_index=False).count()
  
px.line(fig_3, x = 'day_of_week', y = 'ride_id', range_y = [0,550000],
        color = 'member_casual',  
        line_shape = 'spline',
        markers=True,
        labels = {'ride_id': 'No. of Rides', 'day_of_week': 'Weekdays', 'member_casual': 'Member/Casual'},
        hover_name = 'member_casual', hover_data = {'member_casual': False, 'month': False, 'ride_id': True}, 
        color_discrete_map = {'casual': '#FF934F', 'member': '#058ED9'})
          
    


# 1.Here it shows more casual riders are using bike share on WEEKENDS (ie., Saturdays and Sundays).
# 
# 2.But there are a fixed number of casual riders using on WEEKDAYS, might be commuting.
# 
# 3.While the number of members riding tend to be same almost daily.

# # Average Number of Rides in Each Hour

# In[28]:


pd.pivot_table(df,
               index=['hour','member_casual'],
              values='ride_id',
              aggfunc=['count'],
              margins=True,
              margins_name='total_count')


# In[29]:


fig_4=df.groupby(['hour','member_casual'],as_index=False).count()
fig_4a = px.line(fig_4, x = 'hour', y = 'ride_id', range_x = [0,23], range_y = [0,300000],
                 color = 'member_casual',
                 line_shape = 'spline',
                 markers=True,
                 labels = {'ride_id': 'No. of Rides', 'hour': '24 Hours', 'member_casual': 'Member/Casual'},
                 hover_name = 'member_casual', hover_data = {'member_casual': False, 'month': False, 'ride_id': True},
                 color_discrete_map = {'casual': '#FF934F', 'member': '#058ED9'})
fig_4a.update_xaxes(dtick=1)
fig_4a.show()


# 1.In a day, casual riders and members use bike share more during AFTERNOON, peak use during EVENING .
# 
# 2.While in the MORNING time, the number of CASUAL MEMBER are way less than the MEMBERS.

# # Analyzing Difference in Average Ride Length Between Casual riders and Members.

# # #Average Ride Length in 1 Year

# In[30]:


pd.pivot_table(df,
              index='member_casual',
              values='ride_length',
              aggfunc=['mean'],
              margins=True,
              margins_name='Total Ride Average')


# In[31]:


fig_4 = round(df.groupby('member_casual', as_index=False).mean(),2)

px.bar(fig_4, y = 'member_casual', x = 'ride_length', range_x = [0,35],
        color = 'member_casual', 
        height = 300,
        text = 'ride_length', 
        labels = {'ride_length': 'Average Ride Length (minutes)', 'member_casual': 'Member/Casual'},
        hover_name = 'member_casual', hover_data = {'member_casual': False, 'ride_length': True}, 
        color_discrete_map = {'casual': '#FF934F', 'member': '#058ED9'})


# 1.The average ride length of casual riders are more than twice of members.

# # Average Ride Length in Each Month

# In[32]:


pd.pivot_table(df,
              index=['year','month','member_casual'],
              values=['ride_length'],
              aggfunc=['mean'],
              margins=True,
              margins_name='Total ride average')


# In[33]:


fig_5=round(df.groupby(['year','month','member_casual'],as_index=False,).mean(),2).dropna()

px.bar(fig_5,x='month',y='ride_length',
      color='member_casual',
      barmode='group',
      text='ride_length',
      labels={'ride_length':'average ride length(min)','member_casual':'member/casual','month':'months(oct2020-sep2021)'},
      hover_name='member_casual',hover_data={'member_casual':False,'ride_length':True},
      color_discrete_map = {'casual': '#FF934F', 'member': '#058ED9'})



# 1.Average ride length of casual riders are more than twice than members in all months.
# 
# 2.Its seen that Average ride length of February 2021 is unusually higher than the adjacent months.
# 
# As reported in News earlier, (You can read news here) Chicago had 9th Snowiest February on Record and snowstorm in 2021.
# 
# 3.So my conclusion is that riders were not able to return bikes as usual and bikes were stuck with them in February. 
# 
# This increased the ride length. In the graph of Number of Rides Each Month  we can see that February
# 
# has the lowest number of rides in all months.

# # Average Ride Length in each WeekDay

# In[34]:


pd.pivot_table(df,
              index=['day_of_week','member_casual'],
              values=['ride_length'],
              aggfunc=['mean'],
              margins=True,
              margins_name='Total Ride Average'      
                     
                     )


# In[35]:


fig_6=round(df.groupby(['day_of_week','member_casual'],as_index=False).mean(),2)
px.bar(fig_6, x = 'day_of_week', y = 'ride_length',
        color = 'member_casual',
        barmode='group',
        text = 'ride_length', 
        labels = {'ride_length': 'Average Ride Length (minutes)', 'member_casual': 'Member/Casual', 'day_of_week': 'Weekdays'},
        hover_name = 'member_casual', hover_data = {'member_casual': False, 'ride_length': True}, 
        color_discrete_map = {'casual': '#FF934F', 'member': '#058ED9'})


# 1.In Weekends casual riders' ride length is maximum when compared to Weekdays.
# 
# 2.Members' ride length tend to be almost same in all Weekdays and marginally higher in Weekends.
# 
# 3.Both Casual riders and Members use bikes for long rides during Weekends.

# # Analyzing Difference in Rideable Type Usage Between Casual riders and Members.

# In[36]:


pd.pivot_table(df,
               index = ['rideable_type', 'member_casual'],
               values = ['ride_id'],
               aggfunc = ['count'],
               margins = True,
               margins_name = 'Total Rides')


# In[37]:


fig_7 = df.groupby(['rideable_type', 'member_casual'], as_index=False).count()

px.bar(fig_7, x = 'rideable_type', y = 'ride_id',
        color = 'member_casual',
        barmode='group',
        text = 'ride_id', 
        labels = {'ride_id': 'No. of Rides', 'member_casual': 'Member/Casual', 'rideable_type' : 'Rideable Type'},
        hover_name = 'member_casual', hover_data = {'member_casual': False, 'ride_length': False}, 
        color_discrete_map = {'casual': '#FF934F', 'member': '#058ED9'})


# # Conclusion

# 1.Annual members and Casual riders use Cyclistic bike share differently.
# 
# 2.The average ride length of causual riders are more than twice as of members.
# 
# 3.From the average ride length difference, we can conclude that Annual members usually use bike share for daily commuting,
#  while casual riders mostly use bike share for leisure rides mostly during Weekends.
# 
# 4.But there are a fixed number of casual riders who use bike share for commuting.

# # Recommendations

# 1.A new Annual Membership package for Weekend usage only will attract current Weekend casual riders.
# 
# 2.Promotions aiming at current Weekday casual riders must be implemented as soon as possible. 
# Those promtions must include the financial savings of taking membership when compared to single passes and full day passes for a year long period.
# 
# 3.A Loyalty Program for casual riders can be implemented, where occasional membership fees discounts must be given to casual riders with high loyalty points.

# In[ ]:




