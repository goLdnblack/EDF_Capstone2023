# SQL code
import sqlite3

# Handle HTML swithing
from flask import Flask, flash
from flask import url_for
from flask import render_template, request, redirect

# Log application
from AppLogger import *
# AppLogger functions: (increasing severity)

# msg is string containing description

# log(msg)
# log_debug(msg)
# log_warning(msg)
# log_error(msg)
# log_critical(msg)


# Initialize app and connect to database
app = Flask(__name__)
database = sqlite3.connect("Database_EDF.db", check_same_thread=False)
sql = database.cursor()

# TODO - When user signs in with their VID, auto fill form
# document sections based on their information from the
# database
def autoComplete():

# TODO - When clicking on confirm to make changes to database
# call this function to verify and quality check the information
# entered
def qualityCheck():

# TODO - When someone else is looking for an existing EDF
# to approve, this method searches for it. Could find either
# by EDF ID or professor
def getEDF():

# TODO - Update current EDF
def updateEDF():

# TODO - Verify login credentials are correct
def verifyUser():


# TODO - HTML section below
###########################


###########################

if __name__ == "__main__":
    # Initialize logging
    init()

    # Initialize HTML page
    # app.secret_key = '2023edf'
    # app.config['SESSION_TYPE'] = 'filesystem'
    # app.run(host="0.0.0.0", port=5000, debug=True)
    # app.run()
    # db.close()
