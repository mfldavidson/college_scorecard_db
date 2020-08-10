
def create_db_and_tables(cnx, cursor, tables_sql, db_name):
    '''
    Use database or create it if not exist; create tables

    :param cnx: pymysql connection object
    :param cursor: pymysql cursor object
    :param tables_sql: dict of SQL to create tables
    :return: None
    '''
    try:
        cursor.execute(f"USE {db_name}")
        cnx.database = db_name
    except:
        print(f"Database {db_name} does not exist, creating now.")
        try:
            cursor.execute(f"CREATE DATABASE {db_name}")
            cursor.execute(f"USE {db_name}")
        except:
            print("Failed creating database")
        cnx.database = db_name

    # Create tables
    for k, v in tables_sql.items():
        cursor.execute(v)