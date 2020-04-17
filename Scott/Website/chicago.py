#importing dependencies and setting app token
import pandas as pd
from datetime import date, datetime
from sodapy import Socrata
import csv
import sqlite3

MyAppToken = 'GuILMuJLLhVOQ8u9cyXPc56p3'

#checking the day of the month and printing the result, this is used to filter the dataframe later
today = date.today()
daynum = today.strftime("%d")
month = today.strftime("%m")
day = int(daynum) - 7
print(f"Day: {day} \nMonth: {month}")

def getData():
    crime_data = "ijzp-q8t2"
    client = Socrata("data.cityofchicago.org", MyAppToken)
    df = pd.DataFrame(
        client.get(
            crime_data, 
            where=f"Date BETWEEN '2020-01-01' AND '2020-{month}-{day}'",
            limit=100000,
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
    df2019.shape

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



