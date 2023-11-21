'''  CITI BIKE RENTAL '''


## Import libraries
import pandas  as pd
import os
import datetime


## Import all (monthly) data and concatenate it in a single dataframe, in order
df_bike_trips = pd.DataFrame()

for file in sorted(os.listdir('data')):
    if file.startswith('JC'):
        df_temp = pd.read_csv('data/' + file)
        df_bike_trips = pd.concat([df_bike_trips, df_temp], axis=0)

# Reset the index after concatenation
df_bike_trips.reset_index(drop=True, inplace=True)

# Add an ID column -- this will be useful for counts and eventually a primary key
df_bike_trips['id'] = df_bike_trips.index

# Change Start/Stop times to datatime format
df_bike_trips['Start Time'] = pd.to_datetime(df_bike_trips['Start Time'],infer_datetime_format=True)
df_bike_trips['Stop Time'] = pd.to_datetime(df_bike_trips['Stop Time'],infer_datetime_format=True)
df_bike_trips.dtypes

# Reformat column names
df_bike_trips.columns = [x.replace(' ','_').lower() for x in df_bike_trips.columns]
df_bike_trips.head(1)

# Add `age` column and remove outlier
df_bike_trips['age'] = 2016 - df_bike_trips['birth_year'].values
idx_to_drop = df_bike_trips['age'].sort_values(ascending=False).index[0]
df_bike_trips.drop([idx_to_drop], inplace=True)

# We'll replace replace the NaN by "unknown" in `user_type` category
df_bike_trips.fillna({'user_type':'Unknown'},inplace=True)

# Add min & hrs duration columns to the df for ease of interpretation 
df_bike_trips["trip_duration_min"] = round(df_bike_trips.trip_duration.apply(lambda x: x/60),1)
df_bike_trips["trip_duration_hrs"] = round(df_bike_trips.trip_duration.apply(lambda x: x/(60*60)),1)

# Add `valid_duration`` flag
df_bike_trips["valid_duration"] = df_bike_trips.trip_duration_hrs .apply(lambda x: 0 if x > 24 else 1).astype(bool)

# Since we've dropped some data, let's reset the index and set `id` column
df_bike_trips.reset_index(drop=True,inplace=True)
df_bike_trips['id'] = df_bike_trips.index


## Import weather data 
df_weather = pd.read_csv('data/newark_airport_2016.csv')

# Delete columns we don't need
df_weather.drop(["STATION","NAME","PGTM","TSUN","WDF2","WDF5","WSF2","WSF5"], axis=1, inplace=True)

# Change DATE to datatime format
df_weather['DATE'] = pd.to_datetime(df_weather['DATE'],yearfirst=True)

# Rename and add useful columns:
df_weather.columns = ['rec_date','avg_wind','prcp','snowfall','snow_depth','t_avg','t_max','t_min']

df_weather['rain'] = df_weather.prcp.apply(lambda x: 1 if x > 0 else 0).astype(bool)
df_weather['snow'] = df_weather.snowfall.apply(lambda x: 1 if x > 0 else 0).astype(bool)


## Definie Postgre tables 

# -- Date Dimension Table --
# Create the first column
date_col = [datetime.datetime(2016,1,1) + datetime.timedelta(x) for x in range(366)]   # 2016 leap year

df_date = pd.DataFrame(date_col, dtype='datetime64[ns]')
df_date.columns = ['full_date']

# Create month and day columns
df_date['month'] = df_date['full_date'].apply(lambda x: x.month)
df_date['day'] = df_date['full_date'].apply(lambda x: x.day)
df_date['month_name'] = df_date['full_date'].apply(lambda x: x.strftime('%B'))
df_date['day_name'] = df_date['full_date'].apply(lambda x: x.strftime('%A'))
df_date['weekend'] = df_date['day_name'].apply(lambda x: 1 if (x == 'Saturday' or x=='Sunday') else 0).astype(bool)

# Let's add a date key to each of our tables.
df_date['date_key'] = df_date['full_date'].apply(lambda x: int(x.strftime('%Y%m%d').strip('-')))

# Do the same for the `df_bike_trips` and `df_weather dataframes` :
df_weather['date_key'] = df_weather['rec_date'].apply(lambda x: int(x.strftime('%Y%m%d').strip('-')))
df_bike_trips['date_key'] = df_bike_trips['start_time'].apply(lambda x: int(x.strftime('%Y%m%d').strip('-')))


# -- Demographic Table --
# Create a table with the relevant columns taken from `df_bike_trips`:
df_demographic = df_bike_trips[['user_type','birth_year','gender','age']]
df_demographic = df_demographic.drop_duplicates(subset=['user_type','birth_year','gender']).reset_index(drop=True)
df_demographic['trip_demo'] = df_demographic.index

# Create `df_rides` dataframe from `df_bike_trips`.
# Add the demographic key to the table.
# Then drop the demographic columns from `df_rides` to avoid redendancies.
df_rides = df_bike_trips.merge(df_demographic, \
        on=['user_type','birth_year','gender','age']) \
        .sort_values(by='id') \
        .reset_index(drop=True)

# Drop the demographic info from rides
df_rides = df_rides.drop(['user_type','birth_year','gender','age'],axis=1)

# Now we can change the name of the df_demographic id column for the database
df_demographic.rename(columns={'trip_demo':'id'}, inplace=True)

# -- Station Table --
# Let's create a table of stations
starts = df_rides[['start_station_id','start_station_name','start_station_latitude','start_station_longitude']]
ends = df_rides[['end_station_id','end_station_name','end_station_latitude','end_station_longitude']]

# Rename columns so both start and end dataframes have the same column names
starts.columns = ['id','station_name','latitude','longitude']
ends.columns = ['id','station_name','latitude','longitude']

# Combine the 2 dataframe and drop duplicates 
df_stations = pd.concat([starts,ends]).drop_duplicates().reset_index(drop=True)

# -- Rides Table --
# Drop the station columns from df_rides (but we've kept the station_id for key)
df_rides = df_rides.drop(['start_station_name','start_station_latitude','start_station_longitude', \
    'end_station_name','end_station_latitude','end_station_longitude'],axis=1)

df_rides.rename(columns={'demogrphic_key':'demographic_key'}, inplace=True)

# -- Weather Table --
# Nothing to change from `df_weather`, we'll just use the dataframe directly


## Sqlalchemy and Database Code
# Import library
import sqlalchemy

# Establish connection with previously created "Citi Bike Rental" database
# format: url = 'postgresql+psycopg2://user_name@host_name:port_number/database_name' 
engine = sqlalchemy.create_engine( \
    'postgresql+psycopg2://Leo:password@localhost:5432/Citi Bike Rental')
con = engine.connect()

# Load data from the cleaned up dfs into the predefinied tables in the databse
df_date.to_sql('date_dim', con, if_exists='append',index=False,chunksize=10000)
df_stations.to_sql('stations', con, if_exists='append',index=False,chunksize=10000)
df_demographic.to_sql('trip_demo', con, if_exists='append',index=False,chunksize=10000)
df_weather.to_sql('weather', con, if_exists='append',index=False,chunksize=10000)
df_rides.to_sql('rides', con, if_exists='append',index=False,chunksize=10000)

con.close()