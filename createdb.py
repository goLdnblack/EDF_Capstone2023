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

# Enter data into the DB to test
def init_data():
    db = sqlite3.connect("Database_EDF.db", check_same_thread=False)
    sql = db.cursor()

    
    #sql.execute('''CREATE SCHEMA IF NOT EXISTS VDB''')
    #logger.info('Created schema VDB')
    sql.execute('''
                CREATE TABLE IF NOT EXISTS USERS (
                vid text NOT NULL,
                name text,
                password text,
                salt text
                )
                ''')
    logger.info(f'Created table USERS')
    # TODO - store signatures as BLOB or different data type instead of text.
    # TODO - instead of storing all the information in one big table, make
    # foreign keys to other tables to join the data together

    # TODO - should degree title be another radio button on the
    # webpage?
    sql.execute('''
                CREATE TABLE IF NOT EXISTS EDF (
                name text,
                vid text,
                department text,
                position text,
                edf_start date,
                budget_index text,
                account_id text,
                course_name text,
                course_number text,
                credit_hours int,
                degree_title text,
                college text,
                course_start date,
                course_end date,
                degree_program text,
                out_of_pocket varchar(1),
                workshop_title text,
                host text,
                location text,
                workshop_start date,
                workshop_end date,
                registration_cost text,
                registration_pay_method text,
                purpose text,
                benefit_college text,
                employee_signature text,
                admin_signature text,
                edf_submitted varchar(1),
                edf_id text NOT NULL
                )
                ''')
    logger.info(f'Created table EDF')

    db.commit()
    
    if db:
        db.close()

    logger.info(f'Connection to DB closed.')
    return

# TODO - Function to handle manual
# data entry into the db
def enterData():
    db = sqlite3.connect("Database_EDF.db", check_same_thread=False)
    sql = db.cursor()

    # password is testpass
    #sql.execute('''
    #            INSERT INTO USERS VALUES (
    #            'V1000',
    #            'John Doe',
    #            'c5e4de6117d55b498ff0cc7a0db1f4570e289e7701440e4e893b09bfd6b5c18b',
    #            '48055c7ac5684edd'
    #            )
    #            ''')

    sql.execute('''
                ALTER TABLE EDF
                ADD edf_id text
                ''')
    db.commit()
    return


if __name__ == '__main__':
    # Uncomment to create a new
    # empty database.
    enterData()
    # createDB("Database_EDF.db")