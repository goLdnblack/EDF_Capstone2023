# SQL code
import sqlite3

import os,sys

# Handle HTML swithing
from flask import Flask, flash
from flask import url_for
from flask import render_template, request, redirect

import datetime

# Log application
import AppLogger

# Hash user passwords
from HashGenerator import HashGenerator

# AppLogger functions: (increasing severity)

# msg is string containing description

# log(msg)
# log_debug(msg)
# log_warning(msg)
# log_error(msg)
# log_critical(msg)


# Executable
base_dir = '.'


# Logger
logDir = (AppLogger.os.getcwd() + '\\log')
logger = AppLogger.logging.setLoggerClass(AppLogger.LogApp)
logger = AppLogger.setupLogger('edf_logger', logDir)

# Password Hash generator
hw = HashGenerator()

# Initialize app and connect to database
app = Flask(__name__)
database = sqlite3.connect("Database_EDF.db", check_same_thread=False)


def connectDB():
    sql = database.cursor()
    return sql

# TODO - hash value generator for password encryption
def generateHashVal():
    return

# TODO - salt is a cryptography term for a random value that's
# associated to a password to further increase its encryption
def generateSalt():
    return

# TODO - When user signs in with their VID, auto fill form
# document sections based on their information from the
# database
def autoComplete():
    return

# TODO - When clicking on confirm to make changes to database
# call this function to verify and quality check the information
# entered
def qualityCheck():
    return

# TODO - When someone else is looking for an existing EDF
# to approve, this method searches for it. Could find either
# by EDF ID or professor
def getEDF():
    return

# TODO - Update current EDF
def updateEDF():
    return

# TODO - Verify login credentials are correct
def verifyUser(username, password):
    sql = connectDB()
    sql.execute('''
                SELECT vid, password, salt FROM USERS
                WHERE vid=?
                ''', (username,))
    #sql.execute('''SELECT * FROM USERS''')
    result = sql.fetchall()

    if (len(result) == 0):
        logger.info(f'No user found.')
        return False
    
    # Generate the same hash value based on the user's
    # salt value and password entered
    hashPassValue = hw.generatePasswordSalt(password, result[0][2])

    if (hashPassValue == result[0][1]):
        logger.info(f'User {str(username)} verified')
        return True
    
    return False

# TODO - HTML section below
###########################



# TODO - Set log in page as initial page
@app.route("/", methods=["POST", "GET"])
def login():
    logger.info(f'User attempting to log in')

    
    if request.method == "POST":
        # Verify user credentials match database information
        username = request.form["vidlogin"]
        password = request.form["password"]

        if(verifyUser(username, password)):
            return redirect(url_for("homePage"))
        else:
            return redirect(url_for("login"))
        
        

    return render_template("Login.html")

# TODO - Instead of going straight to the EDF page
# the first page could show a list of current EDF's
# in the database that are assigned to the specific
# user. The user could select to edit an already
# opened EDF, an admin could select an EDF
# that is waiting for their approval or create
# a brand new EDF which would go to the createEDF
# page.

# First page to enter information into EDF
@app.route("/Form_Index", methods=["POST", "GET"])
def homePage():
    logger.info(f'Loaded blank EDF form')

    return render_template("index.html")

# Information page on how to navigate site
@app.route("/Instructions", methods=["POST", "GET"])
def instructPage():
    logger.info(f'Switched to instruct page')
    
    return render_template("Instructions.html")

# More information required to complete an EDF form
@app.route("/Form_Continued", methods=["POST", "GET"])
def formPartTwo():

    return render_template("Form2Page.html")

###########################

if __name__ == "__main__":
    # Initialize logging
    # init()
    print('Program start')

    if hasattr(sys, '_MEIPASS'):
        base_dir = os.path.join(sys._MEIPASS)

    # Initialize HTML page
    app.secret_key = '2023edf'
    app.config['SESSION_TYPE'] = 'filesystem'
    # app.run(host="0.0.0.0", port=5000, debug=True)
    app.run(debug=True)
    database.close()
