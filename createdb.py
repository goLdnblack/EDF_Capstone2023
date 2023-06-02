import sqlite3
from sqlite3 import Error

# Initialize the database for the first time before use

def createDB(db):
    connection = None
    try:
        connection = sqlite3.connect(db)
        # TODO - Create a log of the db being created
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    createDB("Database_EDF.db")