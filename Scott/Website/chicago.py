#importing dependencies and setting app token
import pandas as pd
from datetime import date, datetime
from sodapy import Socrata
import csv
import sqlite3
from api_keys import MyAppToken; # for sodapy

from datetime import datetime, date, timedelta
import time

# checking the day of the month and printing the result, this is used to filter the dataframe later
today = date.today()
daynum = today.strftime("%d")
month = today.strftime("%m")
day = int(daynum) - 7
print(f"Day: {day} \nMonth: {month}")

###################################
# Script-level Variables
###################################
# https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-present/ijzp-q8t2
crime_data = "ijzp-q8t2" # Socrata unique id to the Chicago Crime dataset



###################################
# App flow:
#       Step 1. Call getRawData 3x (1x per yr) and store results in df2018, df2019, df2020
#       Step 2. Create one data set from all (dfAll)
#       Step 3. Pass this new dataframe to aggregateTheData_by_date() and create dfAggs
#       Step 4. Store dfAll and dfAggs into SqlLite using importIntoDb()
###################################


def getRawData(start_date, end_date, city='Chicago', max_rows_to_return=20):
    ###################################
    # "Get the data into Pandas" 
    ###################################
    client = Socrata("data.cityofchicago.org", MyAppToken)
    
    df = pd.DataFrame(
        client.get(
            crime_data, 
            where=f"Date BETWEEN '{start_date}' AND '{end_date}'",
            limit=max_rows_to_return,
            exclude_system_fields=True
        )
    )
    client.close()

    df["city"] = city

    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    df['day'] = pd.DatetimeIndex(df['date']).day
    df['month'] = pd.DatetimeIndex(df['date']).month
    df['year'] = pd.DatetimeIndex(df['date']).year
    df['month_day'] = df['date'].dt.strftime('%m-%d')

    # Data is all upper-case; let's make it capital case:
    df["primary_type"] = df["primary_type"].str.lower().str.title()
    df["description"] = df["description"].str.lower().str.title()
    df["location"] = df["location_description"].str.lower().str.title() 
    
    # Organize: 
    dfReturn = df[[
        "city"
        , "primary_type"
        , "description"
        , "date"
        , "month_day"
        , "day"
        , "month"
        , "year"
        , "location"
        , "latitude"
        , "longitude"
        , "domestic"
    ]]
    
    return dfReturn

def aggregateTheData_by_date(df):    
    ###################################
    # "Agg the data" 
    ###################################
    aggs_overall = df.groupby(["date", "month_day"]).agg({
            'day': [
                np.count_nonzero
            ]
    }).reset_index() # Gets rid of auto aggregation/hierarchy
    aggs_overall.columns = ["date", "month_day", "crimes_committed"]
    aggs_overall.sort_values(["date"])

    ###################################
    # Rolling mean + Bollinger bands
    ###################################
    # set number of days and standard deviations to use for rolling 
    # lookback period for Bollinger band calculation
    window = 3
    no_of_std = 1.5

    # calculate rolling mean and standard deviation
    rolling_mean = aggs_overall['crimes_committed'].rolling(window).mean()
    rolling_std = aggs_overall['crimes_committed'].rolling(window).std()

    # create two new DataFrame columns to hold values of upper and lower Bollinger bands
    aggs_overall['Rolling Mean'] = rolling_mean
    aggs_overall['Bollinger High'] = rolling_mean + (rolling_std * no_of_std)
    aggs_overall['Bollinger Low'] = rolling_mean - (rolling_std * no_of_std)
    
    return aggs_overall
    
def importIntoDb(df):
    ###################################
    # "Write to SQL Lite" 
    ###################################
    db = sqlite3.connect('chicago_data.sqlite3')

    # 'replace' = "replace: Drop the table before inserting new values"
    df.to_sql('chicago_data', db, if_exists = 'replace')

    db.close()

    

###################################
# Let's go!
###################################
# Step 1: Get the data
####    2018
year = 2018
start = "{year}-01-01"
end = today.replace(year=year) # Get the latest

df2018 = getRawData(start, end)

####    2019:
year = year + 1
start = "{year}-01-01"
end = today.replace(year=year) 
df2019 = getRawData(start, end)

####    2020:
year = year + 1
start = "{year}-01-01"
end = today.replace(year=year) 
df201920 = getRawData(start, end)

# Step 2: Combine into 1 dataframe
dfAll = df2018.copy();
dfAll = dfAll.append(df2019);
dfAll = dfAll.append(df2020);
dfAll = dfAll.sort_values(["date"])

# Step 3: Create aggregates
dfAggs = aggregateTheData_by_date(dfAll)

# Step 4: Import into database
importIntoDb(dfAll)
importIntoDb(dfAggs)
















def getData():
    client = Socrata("data.cityofchicago.org", MyAppToken)
    df = pd.DataFrame(
        client.get(
            crime_data, 
            where=f"Date BETWEEN '2018-01-01' AND '2020-{month}-{day}'",
            limit=2000000,
            exclude_system_fields=True
        )
    )
    client.close()

    #reformatting the data from the api call and organizing the results
    df['month'] = pd.DatetimeIndex(df['date']).month
    df['year'] = pd.DatetimeIndex(df['date']).year
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%m.%d.%Y')

    #converting strings from all caps to an easier to read format
    df["primary_type"] = df["primary_type"].str.lower().str.title()
    df["description"] = df["description"].str.lower().str.title()
    df["location"] = df["location_description"].str.lower().str.title()

    # Organize columns: 
    df2020 = df[["date","month", "year","primary_type", "description","latitude", "longitude", "domestic"]]
    df2020.shape

    df1 = pd.DataFrame(
        client.get(
            crime_data, 
            where=f"Date BETWEEN '2019-01-01' AND '2019-{month}-{day}'",
            limit=100000,
            exclude_system_fields=True
        )
    )
    client.close()

    #reformatting the data from the api call and organizing the results
    df1['month'] = pd.DatetimeIndex(df1['date']).month
    df1['year'] = pd.DatetimeIndex(df1['date']).year
    df1['date'] = pd.to_datetime(df1['date']).dt.strftime('%m.%d.%Y')

    #converting strings from all caps to an easier to read format
    df1["primary_type"] = df1["primary_type"].str.lower().str.title()
    df1["description"] = df1["description"].str.lower().str.title()
    df1["location"] = df1["location_description"].str.lower().str.title()

    # Organize columns: 
    df2019 = df1[["date","month","year","primary_type","description","latitude","longitude","domestic"]]
    console.log(df2019.shape);

    #second api call to recieve the data from 2019
    df2 = pd.DataFrame(
        client.get(
            crime_data, 
            where=f"Date BETWEEN '2018-01-01' AND '2018-{month}-{day}'",
            limit=100000,
            exclude_system_fields=True
        )
    )
    client.close()

    #reformatting the data from the api call and organizing the results
    df2['month'] = pd.DatetimeIndex(df2['date']).month
    df2['year'] = pd.DatetimeIndex(df2['date']).year
    df2['date'] = pd.to_datetime(df2['date']).dt.strftime('%m.%d.%Y')

    #converting strings from all caps to an easier to read format
    df2["primary_type"] = df2["primary_type"].str.lower().str.title()
    df2["description"] = df2["description"].str.lower().str.title()
    df2["location"] = df2["location_description"].str.lower().str.title()

    # Organize columns: 
    df2018 = df2[["date","month","year","primary_type","description","latitude","longitude","domestic"]]
    df2018.shape

    #combining the 2019 and 2020 dataframes into one, also resetting the index
    dataframes = [df2018, df2019, df2020]
    final_df = pd.concat(dataframes)
    final_df.reset_index(inplace=True)
    print(final_df.shape)
    final_df.head()


    # dom_df = final_df.filter(like = 'True')
    # dom_df

    groupby_df = final_df.groupby(['month', 'domestic', 'year']).count()
    groupby_df.reset_index(inplace=True)

    
    db = sqlite3.connect('chicago_data.sqlite3')

    #inserts only new values from api call into sqlite file
    final_df.to_sql('chicago_data', db, if_exists = 'replace')

    db.close()

if __name__ == '__main__':
    getData()



