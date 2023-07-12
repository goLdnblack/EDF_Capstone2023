import sqlite3
from sqlite3 import Error

import AppLogger

# Initialize the database for the first time before use

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
    return

# TODO - Function to handle manual
# data entry into the db
def enterData():
    return


#if __name__ == '__main__':
    # Uncomment to create a new
    # empty database.
    # createDB("Database_EDF.db")