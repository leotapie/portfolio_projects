This projects looks at NYC's city bike rental trip data for the year 2016 and the correlation with the weather forecast. Aim is to clean, combine and import the data in to a PostgreSQL databse before analysing it in Tableau

## 1 - Cleaning & Exploration
The data was explored and cleaned in hte `Citi_bike_cleaning_and_exploration` notebook. This was to:
- get familiar with the data's format
- understand the steps required to clean the data
- explain the steps taken
- and preapre/load the tables into the databse

## 2 - Loading data into a Postgre dataframe
The code was then packaged into `load_data_into_db.py` for clarity and usage, as the notebook is pretty crowded. 

A Postgre database was created in the **Postbird** client. And the tables (and their dependancies) were created using the queries saved in `create_tables.sql`. The data was then load into these tables by running the python script, and some views were created using `create views.sql`

## 3 - Visualisation
The views were imported into Tableau for analysis and visualisation of the data [link]()
