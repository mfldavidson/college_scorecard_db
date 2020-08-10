import requests, zipfile, io
import pandas as pd
import numpy as np
from pymysql.err import IntegrityError
from vars import COLS, DTYPES

def import_data():
    '''
    Load the institution dataset and the data dictionary into data frames
    :return: inst_df (data frame of institutions from institution dataset),
             datadict_df (data frame from data dict)
    '''
    # Get College Scorecard data by year from Zip
    r = requests.get('https://ed-public-download.app.cloud.gov/downloads/CollegeScorecard_Raw_Data.zip', stream=True)
    if r.ok:
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extract('CollegeScorecard_Raw_Data/MERGED2014_15_PP.csv', path='data/')
    else:
        print(f'Failed to get files: {r.status_code} {r.reason}')
    # Get Data Dictionary
    r = requests.get('https://collegescorecard.ed.gov/assets/CollegeScorecardDataDictionary.xlsx')
    if r.ok:
        with open('data/CollegeScorecardDataDictionary.xlsx','wb') as dd:
            dd.write(r.content)
    else:
        print(f'Failed to get file: {r.status_code} {r.reason}')
    # Load data into pandas data frames
    inst_df = pd.read_csv('data/CollegeScorecard_Raw_Data/MERGED2014_15_PP.csv',
                          low_memory=False, usecols=COLS, dtype=DTYPES, na_values=['PrivacySuppressed', 'NULL'])
    datadict_df = pd.read_excel('data/CollegeScorecardDataDictionary.xlsx',
                             sheet_name='institution_data_dictionary',
                             usecols=['VARIABLE NAME','VALUE','LABEL'])
    datadict_df.rename({'VARIABLE NAME': 'VARIABLE_NAME'}, axis=1, inplace=True)
    return inst_df, datadict_df

def get_var_df(var, df):
    '''
    Get the enumerated variable data from the data dictionary given the variable to retrieve
    :param var: string representing the variable to get enumerated data for from the data dict
    :param df: data dictionary data frame
    :return: cleaned data frame
    '''
    # Get the index where the values start
    start = int(df.index[df.VARIABLE_NAME == var][0])
    step = start + 1
    # Get the index where the values end
    while True:
        val = df.VARIABLE_NAME.iloc[step]
        if val is np.nan:
            step += 1
        else:
            break
    # Create the data frame
    new = df[['VALUE', 'LABEL']].iloc[start:step]
    new['VALUE'] = new.VALUE.astype(np.int64)
    return new

def load_control_level_df(cnx, cursor, datadict_df):
    '''
    Load the control and level data into existing tables in an existing database
    :param cnx: pymysql connection object
    :param cursor: pymysql cursor object
    :param datadict_df: data dictionary data frame
    :return: None
    '''

    vars = {
        'levels': 'ICLEVEL',
        'controls': 'CONTROL'
    }
    for k,v in vars.items():
        # Get a data frame of the data for this var from the data dict
        df = get_var_df(v, datadict_df)

        sql = (f"INSERT INTO {k} ("
               f"{k[:-1]}_id, "
               f"{k[:-1]}) "
                "VALUES (%s, %s);")

        vals = df.to_dict('split')

        for v in vals['data']:
            try:
                cursor.execute(sql, (v[0], v[1]))
            except IntegrityError as err:
                print(f'Could not insert data: {err}')

    cnx.commit()
    return None

def load_states_df(cnx, cursor, inst_df, datadict_df):
    '''
    Load, clean, and insert data from 2 data frames about states into existing database and states table
    :param cnx: pymysql connection object
    :param cursor: pymysql cursor object
    :param inst_df: data frame of institutions
    :param datadict_df: data dictionary data frame
    :return: None
    '''
    # Load and clean the states data
    states = inst_df[['STABBR', 'ST_FIPS', 'REGION']]
    states_no_dups = states.drop_duplicates()
    states_dropped_region = states_no_dups[states_no_dups.REGION > 0]
    # Load the long state name data
    long_state = get_var_df('ST_FIPS', datadict_df)
    # Merge the long state and states data
    states_state = states_dropped_region.merge(long_state, left_on='ST_FIPS', right_on='VALUE', how='left')
    states_state.drop(['VALUE'], axis=1, inplace=True)
    # Load and clean the region data
    region = get_var_df('REGION', datadict_df)
    region['region_clean'] = region.LABEL.apply(lambda x: x.split('(')[0].strip())
    region.drop('LABEL', axis=1, inplace=True)
    # Merge the states and region data
    states_region = states_state.merge(region, left_on='REGION', right_on='VALUE', how='left')
    states_region.drop(['VALUE', 'REGION'], axis=1, inplace=True)
    # Load the states data
    vals = states_region.to_dict('split')
    for v in vals['data']:
        try:
            sql = ("INSERT INTO states ("
                   "state_id, long_state, abbr_state, region) "
                   f"VALUES ({v[1]}, '{v[2]}', '{v[0]}', '{v[3]}');")
            cursor.execute(sql)
        except IntegrityError as err:
            print(f'Could not insert data: {err}')
    cnx.commit()
    return None

def load_inst_df(cnx, cursor, inst_df):
    '''
    Load the institutions data frame into existing database and institutions table
    :param cnx: pymysql connection object
    :param cursor: pymysql cursor object
    :param inst_df: data frame of institutions
    :return: None
    '''
    # Create a column with all the net cost data
    inst_df['NPT4_ALL'] = inst_df[['NPT4_PUB','NPT4_PRIV']].sum(axis=1)
    no_nan = inst_df.astype(object).where(pd.notnull(inst_df), None)
    vals = no_nan.to_dict('split')
    for v in vals['data']:
        try:
            sql = ("INSERT INTO institutions ("
                   "inst_id, name, city, state_id, control_id, level_id, "
                   "mean_earn, family_inc, mean_cost, first_gen) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")
            cursor.execute(sql,  (v[0], v[1], v[2], v[5], v[4], v[12], v[11], v[10], v[13], v[9]))
        except IntegrityError as err:
            print(f'Could not insert data: {err}')
    cnx.commit()
    return None

def load_all_data(CNX, CURSOR):
    '''
    Import the data to load and load it into the existing tables
    :return: None
    '''
    inst_df, datadict_df = import_data()
    load_control_level_df(CNX, CURSOR, datadict_df)
    load_states_df(CNX, CURSOR, inst_df, datadict_df)
    load_inst_df(CNX, CURSOR, inst_df)
    return None