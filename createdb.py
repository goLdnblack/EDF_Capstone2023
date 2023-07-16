import sqlite3
from sqlite3 import Error

import AppLogger

# Initialize the database for the first time before use

# TODO - Look up myphp admin to set up a database

# Logger
logDir = (AppLogger.os.getcwd() + '\\log')
logger = AppLogger.logging.setLoggerClass(AppLogger.LogApp)
logger = AppLogger.setupLogger('sql-database', logDir)

# TODO - Use seed file to generate a new database

def createDB(db):
    connection = None
    try:
        connection = sqlite3.connect(db)
        # TODO - Create a log of the db being created
        logger.info(sqlite3.version)
    except Error as e:
        logger.critical(e)
    finally:
        if connection:
            connection.close()

# TODO - encrypt user passwords entered into
# user database

# Enter data into the DB to test
def init_data():
    db = sqlite3.connect("Database_EDF.db", check_same_thread=False)
    sql = db.cursor()

    sql.execute('''
                CREATE SCHEMA IF NOT EXISTS VDB
                ''')
    sql.execute('''
                CREATE TABLE IF NOT EXISTS VDB.USERS (
                vid text NOT NULL, name text, password text, salt text
                )
                ''')
    # TODO - store signatures as BLOB or different data type instead of text.
    sql.execute('''
                CREATE TABLE IF NOT EXISTS VDB.EDF (
                name text, vid text, department text, position text, edf_start date, budget_index text,
                account_id text, course_name text, course_number text, credit_hours int,
                degree_title text, college text, course_start date, course_end date, degree_program text,
                out_of_pocket varchar(1), workshop_title text, host text, location text,
                workshop_start date, workshop_end date, registration_cost text,
                registration_pay_method text, purpose text, benefit_college text,
                employee_signature text, admin_signature text
                )
                ''')
    
    sql.execute()
    return

# TODO - Function to handle manual
# data entry into the db
def enterData():
    return


#if __name__ == '__main__':
    # Uncomment to create a new
    # empty database.
    # createDB("Database_EDF.db")