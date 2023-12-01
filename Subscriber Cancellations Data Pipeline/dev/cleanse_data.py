#!/usr/bin/env python
# coding: utf-8

""" Subscriber Cancellations Data Pipeline """

# Project aim: Create a data ingestion pipeline in Python to automatically clean and update a customer information databse. 
# In addition to cleaning and updating the data, we’ll automate the updatong process using error logging and bash scripting.

# This script cleanse the data, uploads it to the new dataframe and runs some unit tests


## Import libraries 
import sqlite3
import pandas as pd
import ast
import numpy as np
import logging


## Configure logger
logging.basicConfig(filename="./dev/cleanse_db.log",
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    filemode='w',
                    level=logging.DEBUG,
                    force=True)
logger = logging.getLogger(__name__)


""" Data Cleaning """
## Student table cleaning
def cleanse_student_table(df):
    """
    Parameters:
        df (DataFrame): `students` table from `cademycode.db`

    Returns:
        df (DataFrame): cleaned version of the input table
        missing_data (DataFrame): incomplete data that was removed for later inspection
    """
    
    # Calculate Age (more usefule than date of birth)
    today_date = pd.to_datetime('now',utc=True)
    df['age'] = (today_date - pd.to_datetime(df['dob'],utc=True)).astype('<m8[Y]')
    df['age_group'] = df['age'].apply(lambda x: np.floor(x / 10) * 10)

    # Sort Contact Info formatting
    df['contact_info'] = df["contact_info"].apply(lambda x: ast.literal_eval(str(x)))
    explode_contact = pd.json_normalize(df['contact_info'])
    df = pd.concat([df, explode_contact], axis=1)
    df = df.drop('contact_info', axis=1).reset_index(drop=True)

    # Split the Address line
    split_address = df['mailing_address'].str.split(',', expand=True)
    split_address.columns = ['street', 'city', 'state', 'zipcode']
    df = pd.concat([df,split_address], axis=1)
    df = df.drop('mailing_address', axis=1).reset_index(drop=True)

    # Ensure data types are appropriate
    df[['job_id', 'num_course_taken','current_career_path_id', 'time_spent_hrs']] = \
        df[['job_id', 'num_course_taken','current_career_path_id', 'time_spent_hrs']].astype(float)

    # Missing data
    missing_data = pd.DataFrame()

    # Job ID
    missing_job_id = df[df['job_id'].isna()] 
    missing_data = pd.concat([missing_data,missing_job_id])
    df = df.dropna(subset='job_id')

    # Number of Course Taken 
    missing_course_taken = df[df['num_course_taken'].isna()]
    missing_data = pd.concat([missing_data, missing_course_taken])
    df = df.dropna(subset=['num_course_taken'])

    # Current Career Path ID and Hours Spent
    missing_path_id = df[df['current_career_path_id'].isna()] 
    df['current_career_path_id'] = np.where(df['current_career_path_id'].isna(), 0, df['current_career_path_id'])
    df['time_spent_hrs'] = np.where(df['time_spent_hrs'].isna(), 0, df['time_spent_hrs'])

    # Convert uuid to int
    df['uuid'] = df['uuid'].astype(int)

    return(df, missing_data)


## Career Path table cleaning
def cleanse_career_path_table(df):
    """
    Parameters:
        df (DataFrame): `cademycode_courses` table from `cademycode.db`

    Returns:
        df (DataFrame): cleaned version of the input table

    """

    # Adding the "0" career path we've added in student into this dataframe
    no_career_path = {'career_path_id': 0,
                    'career_path_name': 'not applicable',
                    'hours_to_complete' : 0}

    df.loc[len(df)] = no_career_path

    return(df)


## Student Jobs table cleaning
def cleanse_student_jobs_table(df):
    """
    Parameters:
        df (DataFrame): `cademycode_student_jobs` table from `cademycode.db`

    Returns:
        df (DataFrame): cleaned version of the input table

    """

    return(df.drop_duplicates())


""" Unit Testing """
## Unit Test: Ensure that all `current_career_path_id` in the *students* df are referenced in the *career_paths* df
def test_for_path_id(students, career_paths):
    """
    Parameters:
        students (DataFrame): `cademycode_students` table from `cademycode.db`
        career_paths (DataFrame): `cademycode_courses` table from `cademycode.db`

    Returns:
        None
    """

    student_table = students.current_career_path_id.unique()
    is_subset = np.isin(student_table, career_paths.career_path_id.unique())
    missing_id = student_table[~is_subset]
    try:
        assert len(missing_id) == 0, "Missing career_path_id(s): " + str(list(missing_id)) + " in `career_paths` table"
     # Raise and log error if the *career_path* table is missing a key present in *students*
    except AssertionError as ae:
        logger.exception(ae)
        raise ae
    else:
        print('All career_path_ids are present.')


## Unit Test: Ensure that all `job_id` in the *students* df are referenced in the *student_jobs* df
def test_for_job_id(students, student_jobs):
    """
    Parameters:
        students (DataFrame): `cademycode_students` table from `cademycode.db`
        student_jobs (DataFrame): `cademycode_student_jobs` table from `cademycode.db`

    Returns:
        None
    """

    student_table = students.job_id.unique()
    is_subset = np.isin(student_table, student_jobs.job_id.unique())
    missing_id = student_table[~is_subset]
    try:
        assert len(missing_id) == 0, "Missing job_id(s): " + str(list(missing_id)) + " in `student_jobs` table"
    # Raise and log error if the *student_jobs* table is missing a key present in *students*
    except AssertionError as ae:
        logger.exception(ae)
        raise ae
    else:
        print('All job_ids are present.')


## Unit Test: Ensure that no rows in the cleaned table are NaN
def test_nans(df):
    """
    Parameters:
        df (DataFrame): DataFrame of the cleansed table

    Returns:
        None
    """

    cnt_missing = df.isna().sum().sum()

    try:
        assert cnt_missing == 0, "There are " + str(cnt_missing) + " nulls in the table."
    # Raise and log error if NaNs are found in the cleansed df
    except AssertionError as ae:
        logger.exception(ae)
        raise ae
    else:
        print('No null rows found.')


## Unit Test: Ensure that the number of columns in the cleaned DataFrame match the number of columns in the SQLite3 database table.
def test_num_cols(local_df, db_df):
    """
    Parameters:
        local_df (DataFrame): DataFrame of the cleansed table
        db_df (DataFrame): `cademycode_aggregated` table from `cademycode_cleansed.db`

    Returns:
        None
    """
    try: 
        assert len(local_df.columns) == len(db_df.columns), "Number of columns in cleaned table does not match production database." 
    # Raise and log error if number of columns not the same  
    except AssertionError as ae:
        logger.exception(ae)
        raise ae
    else:
        print("Number of columns are the same.")


## Unit Test: Ensure that the column dtypes in the cleaned DataFrame match the column dtypes in the SQLite3 database table.
def test_schema(local_df, db_df):
    """
    Parameters:
        local_df (DataFrame): DataFrame of the cleansed table
        db_df (DataFrame): `cademycode_aggregated` table from `cademycode_cleansed.db`

    Returns:
        None
    """
    errors = 0
    for col in db_df:
        try:
            if local_df[col].dtypes != db_df[col].dtypes:
                errors += 1
        # Raise and log error if a column doesn't exist
        except NameError as ne:
            logger.exception(ne)
            raise ne

        # Log if dtypes don't match

    if errors > 0:
        assert_err_msg = str(errors) + " columns have different dtypes."
        logger.exception(assert_err_msg)
        assert errors == 0, assert_err_msg
    else:
        print("dtypes columns are the same")


""" Main Method (driver to execute all the functions defined above) """
def main():

    ## Initialize log
    logger.info("Start Log")
    # Check for current version and calculate next version for changelog
    with open('./dev/changelog.md') as f:
        lines = f.readlines()
    next_ver = int(lines[0].split('.')[2][0])+1


    ## Connect to the dev database and read in the three tables
    con = sqlite3.connect('./dev/cademycode.db')
    #con = sqlite3.connect('./dev/cademycode_updated.db')
    students = pd.read_sql_query("SELECT * FROM cademycode_students", con)
    career_paths = pd.read_sql_query("SELECT * FROM cademycode_courses", con)
    student_jobs = pd.read_sql_query("SELECT * FROM cademycode_student_jobs", con)
    con.close()


    ## Try to connect to prod databse (i.e., the cleased database) to check if they're any new students to add
    try: 
        con = sqlite3.connect('./prod/cademycode_cleansed.db')
        students_prod_db = pd.read_sql_query("SELECT * FROM students_clean", con)
        career_paths_prod_db = pd.read_sql_query("SELECT * FROM career_paths_clean", con)
        student_jobs_prod_db = pd.read_sql_query("SELECT * FROM student_jobs_clean", con)
        missing_prod_db = pd.read_sql_query("SELECT * FROM missing_data", con)
        con.close()

        # Filter for students that don't exist in the cleansed database
        #new_students = students.loc[~students['uuid'].isin(students_prod_db['uuid'].unique())].copy()
        new_students = students

    # If cleansed database doesn't exist
    except:
        new_students = students


    ## Clean `new_students` data 
    new_students_clean, missing_data = cleanse_student_table(new_students)


    ## Check for any new missing data not already in the cleansed database. Only add in that case
    try:
        # Filter for incomplete rows that don't exist in the missing data table
        #new_missing_data = missing_data[~np.isin(missing_data.uuid.unique(), missing_prod_db.uuid.unique())]
        new_missing_data = missing_data.loc[~missing_data['uuid'].isin(missing_prod_db['uuid'].unique())].copy()
    except:
        new_missing_data = missing_data

    if len(new_missing_data) > 0:
        con = sqlite3.connect('./dev/cademycode_cleansed.db')   # to dev folder, as the whole db will be transfer to prod at end of process
        missing_data.to_sql('missing_data', con, if_exists='append', index=False)
        con.close()


    ## Only if there are new students, clean the *career_path* and *student_jobs* df
    if len(new_students_clean) > 0:
        career_paths_clean = cleanse_career_path_table(career_paths)
        student_jobs_clean = cleanse_student_jobs_table(student_jobs)


        ## UNIT TESTING
        # Ensure that all path_id and job_id in *students* respetively exist in the *career_paths* and *student_jobs* tables
        test_for_path_id(new_students_clean, career_paths_clean)
        test_for_job_id(new_students_clean, student_jobs_clean)

        # Compare schema of cleaned data with prod databse (if it already exists)
        # Ensure correct schema and complete data before upserting to database
        
        local_dfs = [new_students_clean, career_paths_clean, student_jobs_clean]
        db_dfs = [students_prod_db, career_paths_prod_db, student_jobs_prod_db] 
        table_names = ["Students:", "Career paths:", "Student jobs:"]

        for t in range(len(local_dfs)):
            # For user readability
            print(table_names[t])
            # Run unit tests to check the schema of the local dfs match the destination (i.e., the database schema)
            test_num_cols(local_dfs[t], db_dfs[t])
            test_schema(local_dfs[t], db_dfs[t])
            # Check there's no NaNs before upserting to database
            test_nans(local_dfs[t])
    
        #print("Schema unit tests couldn't be run because there isn't any production databse yet")
        

        ## Connect to the dev database to upsert the three tables
        con = sqlite3.connect('./dev/cademycode_cleansed.db')
        new_students_clean.to_sql('students_clean', con, if_exists='append', index=False)
        career_paths_clean.to_sql('career_paths_clean', con, if_exists='append', index=False)
        student_jobs_clean.to_sql('student_jobs_clean', con, if_exists='append', index=False)
        con.close()

        ## Merge the 3 local dfs and write to .csv file
        new_students_clean['job_id'] = new_students_clean['job_id'].astype(int)
        new_students_clean['current_career_path_id'] = new_students_clean['current_career_path_id'].astype(int)
        
        df_clean = new_students_clean.merge(career_paths_clean, left_on='current_career_path_id', right_on='career_path_id', how='left')
        df_clean = df_clean.merge(student_jobs_clean, on='job_id', how='left')
        
        df_clean.to_csv('./dev/cademycode_cleansed.csv')


        ## Create new automatic changelog entry
        new_lines = [
            '## 0.0.' + str(next_ver) + '\n' +
            '### Added\n' +
            '- ' + str(len(new_students_clean)) + ' more data to database of raw data\n' +
            '- ' + str(len(new_missing_data)) + ' new missing data to incomplete_data table\n' +
            '\n'
        ]
        w_lines = ''.join(new_lines + lines)

        # Update the changelog
        with open('./dev/changelog.md', 'w') as f:
            for line in w_lines:
                f.write(line)


    ## But if there is not any new students
    else:
        print("No new data")
        logger.info("No new data")
    logger.info("End Log")


## Run the main function in the driver
if __name__ == "__main__":
    main()