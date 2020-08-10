import pymysql
import os
from create_db import create_db_and_tables
from load_db import load_all_data
from vars import DB_NAME, TABLES

if __name__ == "__main__":
    # Set up connection and cursor
    CNX = pymysql.connect(user=os.environ.get('username'),
                          password=os.environ.get('password'),
                          cursorclass=pymysql.cursors.DictCursor)
    CURSOR = CNX.cursor()

    create_db_and_tables(CNX, CURSOR, TABLES, DB_NAME) # Create database and tables
    load_all_data(CNX, CURSOR) # Load all data into the tables

    # Close cursor and connection
    CURSOR.close()
    CNX.close()